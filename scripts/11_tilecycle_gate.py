"""Tile-cycle failure gate: find (tile, cycle) cells whose REAL error rate is far above
their neighbours, regardless of what quality score the instrument reported.

Why this exists
---------------
On our own run, 4 tile-cycles out of 28 x 251 produced 38% of all substitution errors,
and a large share of those wrong bases were reported at Q37-Q39. FastQC cannot see this,
because FastQC reads the machine's own quality claim and the claim is the thing that is
wrong. The only way to see it is to align reads back and count real mismatches.

Majority-vote consensus has a breakdown point of 50%. Inside these cells the local error
rate is 68-99%, so MORE COVERAGE MAKES THE ANSWER WORSE. The only fix is to remove them.

usage:
    python 11_tilecycle_gate.py READS_vs_CONTIGS.bam CONTIGS.fasta OUT_PREFIX
                                [--min-excess 20] [--min-mismatches 50] [--mapq 30]

writes:
    OUT_PREFIX.json     full per-cell table + the flagged list
    OUT_PREFIX.mask.tsv two columns, tile<TAB>cycle  -- feed this to your filter step
    prints a short human-readable report

Pure standard library apart from `samtools` on PATH. Deterministic: same BAM, same answer.
"""
import sys, re, json, math, subprocess, collections

# ---------------------------------------------------------------- arguments
args = [a for a in sys.argv[1:] if not a.startswith("--")]
opts = dict(zip([a.lstrip("-") for a in sys.argv[1:] if a.startswith("--")],
                [sys.argv[i + 1] for i, a in enumerate(sys.argv[1:], 1) if a.startswith("--")]))
if len(args) < 3:
    sys.exit(__doc__)
bam, fasta, prefix = args[0], args[1], args[2]
MIN_EXCESS = float(opts.get("min-excess", 20))      # cell rate / cycle background
MIN_MIS    = int(opts.get("min-mismatches", 50))    # ignore tiny counts
MAPQ       = int(opts.get("mapq", 30))

# ---------------------------------------------------------------- reference
ref, name, buf = {}, None, []
for line in open(fasta):
    if line.startswith(">"):
        if name: ref[name] = "".join(buf)
        name, buf = line[1:].split()[0], []
    else:
        buf.append(line.strip().upper())
if name: ref[name] = "".join(buf)

# ---------------------------------------------------------------- scan the BAM
bases = collections.Counter()    # (cycle, tile) -> aligned bases
mis   = collections.Counter()    # (cycle, tile) -> mismatches
subs  = collections.defaultdict(collections.Counter)   # (cycle,tile) -> A>T etc
qrep  = collections.defaultdict(collections.Counter)   # (cycle,tile) -> reported Q of wrong bases
COMP  = str.maketrans("ACGTN", "TGCAN")
cig   = re.compile(r"(\d+)([MIDNSHP=X])")

proc = subprocess.Popen(["samtools", "view", bam], stdout=subprocess.PIPE, text=True)
for line in proc.stdout:
    f = line.split("\t")
    flag, mapq = int(f[1]), int(f[4])
    if flag & (4 | 256 | 2048) or mapq < MAPQ:
        continue
    parts = f[0].split(":")
    if len(parts) < 5:
        continue                                  # not an Illumina-style read name
    tile = int(parts[4])
    rev, seq, qual = bool(flag & 16), f[9], f[10]
    L, r = len(seq), ref.get(f[2])
    if r is None:
        continue
    i, j = 0, int(f[3]) - 1
    for n, op in cig.findall(f[5]):
        n = int(n)
        if op in "M=X":
            for k in range(n):
                rb, cb = r[j + k], seq[i + k]
                if rb == "N" or cb == "N":
                    continue
                c = (L - 1 - (i + k) if rev else i + k) + 1     # 1-based sequencing cycle
                key = (c, tile)
                bases[key] += 1
                if rb != cb:
                    mis[key] += 1
                    a, b = (rb.translate(COMP), cb.translate(COMP)) if rev else (rb, cb)
                    subs[key][f"{a}>{b}"] += 1
                    qrep[key][ord(qual[i + k]) - 33] += 1
            i += n; j += n
        elif op in "IS":
            i += n
        elif op == "D":
            j += n
proc.stdout.close(); proc.wait()

if not bases:
    sys.exit("no aligned bases counted -- check the BAM, the MAPQ filter, and that read "
             "names are Illumina-style (instrument:run:flowcell:lane:tile:x:y)")

# ---------------------------------------------------------------- background per cycle
# robust: median rate across tiles, so a few broken tiles cannot inflate their own baseline
cycles = sorted({c for c, _ in bases})
tiles  = sorted({t for _, t in bases})
background = {}
for c in cycles:
    rates = [mis[(c, t)] / bases[(c, t)] for t in tiles if bases[(c, t)] >= 200]
    rates.sort()
    if not rates:
        continue
    m = len(rates)
    background[c] = rates[m // 2] if m % 2 else 0.5 * (rates[m // 2 - 1] + rates[m // 2])

# ---------------------------------------------------------------- flag the outliers
def log10_binom_tail(k, n, p):
    """crude but sufficient: log10 P(X >= k) via a normal approximation with continuity."""
    if p <= 0: return -999.0
    mu, sd = n * p, math.sqrt(n * p * (1 - p))
    if sd == 0: return -999.0
    z = (k - 0.5 - mu) / sd
    if z <= 0: return 0.0
    # log10 of the upper tail of a standard normal, Mills-ratio approximation
    return (-z * z / 2 - math.log(z * math.sqrt(2 * math.pi))) / math.log(10)

flagged, table = [], []
for (c, t), b in sorted(bases.items()):
    if b < 200:
        continue
    m = mis[(c, t)]
    bg = background.get(c, 0.0)
    rate = m / b
    excess = (rate / bg) if bg > 0 else float("inf")
    row = {"cycle": c, "tile": t, "bases": b, "mismatches": m,
           "rate": rate, "background_rate": bg,
           "excess": None if excess == float("inf") else round(excess, 1),
           "logP": round(log10_binom_tail(m, b, max(bg, 1e-9)), 1)}
    table.append(row)
    if m >= MIN_MIS and (excess >= MIN_EXCESS) and row["logP"] < -10:
        row["top_substitutions"] = subs[(c, t)].most_common(4)
        row["reported_Q_of_wrong_bases"] = qrep[(c, t)].most_common(4)
        flagged.append(row)

flagged.sort(key=lambda r: -r["mismatches"])
tot_bases = sum(bases.values()); tot_mis = sum(mis.values())
lost_bases = sum(r["bases"] for r in flagged); lost_mis = sum(r["mismatches"] for r in flagged)

out = {"parameters": {"min_excess": MIN_EXCESS, "min_mismatches": MIN_MIS, "mapq": MAPQ},
       "totals": {"aligned_bases": tot_bases, "mismatches": tot_mis,
                  "substitution_rate": tot_mis / tot_bases,
                  "tiles": len(tiles), "cycles": len(cycles),
                  "tile_cycles_examined": len(table)},
       "flagged": flagged,
       "impact": {"tile_cycles_flagged": len(flagged),
                  "fraction_of_tile_cycles": len(flagged) / max(len(table), 1),
                  "bases_removed": lost_bases,
                  "fraction_of_bases_removed": lost_bases / tot_bases,
                  "mismatches_removed": lost_mis,
                  "fraction_of_mismatches_removed": lost_mis / max(tot_mis, 1),
                  "substitution_rate_after": (tot_mis - lost_mis) / max(tot_bases - lost_bases, 1)},
       "per_tile_cycle": table}

json.dump(out, open(prefix + ".json", "w"), indent=1)
with open(prefix + ".mask.tsv", "w") as fh:
    fh.write("tile\tcycle\n")
    for r in flagged:
        fh.write(f"{r['tile']}\t{r['cycle']}\n")

# ---------------------------------------------------------------- report
def q(p): return 99.0 if p <= 0 else -10 * math.log10(p)
print(f"tile-cycles examined      {len(table):,}  ({len(tiles)} tiles x {len(cycles)} cycles)")
print(f"aligned bases             {tot_bases:,}")
print(f"substitution rate  before {out['totals']['substitution_rate']:.6f}   (Q{q(out['totals']['substitution_rate']):.2f})")
print(f"substitution rate  after  {out['impact']['substitution_rate_after']:.6f}   (Q{q(out['impact']['substitution_rate_after']):.2f})")
print(f"\nFLAGGED {len(flagged)} tile-cycle(s) "
      f"= {out['impact']['fraction_of_tile_cycles']:.4%} of the run")
print(f"  bases discarded      {lost_bases:,} ({out['impact']['fraction_of_bases_removed']:.4%})")
print(f"  mismatches removed   {lost_mis:,} ({out['impact']['fraction_of_mismatches_removed']:.1%} of all errors)")
if flagged:
    print(f"\n  {'tile':>6} {'cycle':>6} {'rate':>9} {'background':>11} {'excess':>8}   reported Q of the wrong bases")
    for r in flagged:
        ex = "inf" if r["excess"] is None else f"{r['excess']:.0f}x"
        qs = ", ".join(f"{n} at Q{qq}" for qq, n in r.get("reported_Q_of_wrong_bases", [])[:2])
        print(f"  {r['tile']:>6} {r['cycle']:>6} {r['rate']:>9.4f} {r['background_rate']:>11.6f} {ex:>8}   {qs}")
    print(f"\n  -> {prefix}.mask.tsv written. Exclude these (tile, cycle) pairs before "
          f"assembly or variant calling.")
else:
    print("\n  no tile-cycle failures detected at these settings.")
