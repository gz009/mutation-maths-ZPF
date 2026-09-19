# mutation-maths-ZPF

**Mutation, docking and folding are three faces of one sentence — and that sentence is the partition function.**

$$Z=\sum_{\text{states}} e^{-\beta E}\qquad\text{classical}\qquad\qquad Z=\operatorname{Tr}\!\left(e^{-\beta\hat H}\right)\qquad\text{quantum}$$

A self-study record: ten study dossiers, four Jupyter notebooks and the LaTeX
that produces them, working from *why our mathematics is shaped the way it is*
(Lakoff & Núñez) towards *what mathematics the nano/quantum scale of biology
actually needs* — and then down into the one object that keeps appearing:
the partition function $Z$.

Everything here was **built from source in this project**. Nothing here is a
scanned book. See [What is deliberately absent](#what-is-deliberately-absent).

---

## The documents

| | dossier | pp | what it argues |
|---|---|---|---|
| **VI** | [Where Mathematics Comes From — Idea Analysis](docs/Where_Mathematics_Comes_From__PartVI_Idea_Analysis__Study_Dossier.pdf) | 33 | Lakoff & Núñez Part VI, Case Studies 1–4, read closely: grounding metaphors, linking metaphors, the Basic Metaphor of Infinity, and what $e^{\pi i}+1=0$ *means* once you unpack the blend |
| **VII** | [Beyond the Reach of the Body — Nano/Quantum Biology](docs/Beyond_the_Reach_of_the_Body__PartVII_Nano_Quantum_Biology__Study_Dossier.pdf) | 21 | If mathematics is embodied, how do we invent mathematics for scales no body ever inhabited? Re-grounding through diagrammatic calculi — Feynman diagrams, ZX-calculus |
| **VIII** | [AMR R&D Maths — NGS Measurement Problems](docs/AMR_RnD_Maths_BioBio1_PartVIII_NGS_Measurement_Problems_v1.0_gZ_18Sep26.pdf) | 19 | Written for biologists. Which sequencing measurement problems are beaten by redundancy and compute, which are not, and where the breakdown point of a majority vote actually lies |
| **IX** | [The Measure, Not the Point](docs/The_Measure_Not_the_Point__PartIX__Molecular_Biology_Maths__Study_Dossier.pdf) | 17 | The answer to "that was computational maths, not *new* maths": apparent random mutation, docking and AlphaFold-3 are all statements about a measure over configurations, not about a point |
| **X v1.0** | [Learning Z (superseded)](docs/Learning_Z__PartX__The_Partition_Function__Study_Dossier_v1.0.pdf) | 14 | Kept because it was **wrong**: it told the reader to buy five books, four of which were already on the shelf. §1 of v2.0 says so |
| **X v2.0** | [Learning Z — Four-Library Audit](docs/Learning_Z__PartX_v2.0__Four_Library_Audit__Study_Dossier.pdf) | 17 | A twelve-week route to $Z$ through books already owned, audited across four libraries, with the gaps named honestly |
| **Tutorial** | [Proof Techniques — Sage 10.9 notebook companion](docs/Proof_Techniques_TUTORIAL__Sage_10.9_Notebook_Companion__22_Cells_8_Books.pdf) | 14 | Assumes no proof background. Six techniques cell by cell, Tao's nine steps, the CAS boundary, and $\operatorname{Tr}(T^N)=\lambda_+^N+\lambda_-^N$ actually proved |

## The working folder

`Partition_Function_Study/` **is** the live study folder — the directory JupyterLab
opens, not a copy of it. Notebooks are edited there and committed from there.

It also holds the two reference libraries, which are **not** in this repo:

| inside the working folder | what it is | in git? |
|---|---|---|
| `Z_Ref_Books/` | 23 books, 10 topic folders, 256 MB | **no** — `.gitignore` |
| `Maths_Proof_Skill/` | 8 books, 2,164 pp, 22 MB | **no** — `.gitignore` |
| `archive_v1.0/` | superseded Part X PDFs | no — published copy is in `docs/` |
| `*.ipynb` | the four notebooks | **yes** |

Clone this repo and you get the notebooks, the sources and the dossiers; the
books you supply yourself, using `guidelines/`. Drop them into
`Partition_Function_Study/Z_Ref_Books/` and `…/Maths_Proof_Skill/` and git will
ignore them exactly as it does here.

## The notebooks

| notebook | kernel | what it does |
|---|---|---|
| [`Partition_Function_01_Ising_Transfer_Matrix.ipynb`](Partition_Function_Study/Partition_Function_01_Ising_Transfer_Matrix.ipynb) | Python 3 | 1D Ising by transfer matrix, numerically. Includes the honest-failure cell: eight independent Metropolis chains that *should* all return $\langle M\rangle=0$ and visibly fail to mix past $\beta\approx1.5$ |
| [`Partition_Function_01_Sage_10.9_Ising_Transfer_Matrix.ipynb`](Partition_Function_Study/Partition_Function_01_Sage_10.9_Ising_Transfer_Matrix.ipynb) | SageMath 10.9 | The same physics done symbolically — eigenvalues, free energy, correlation length $\xi=1/\ln(\lambda_+/\lambda_-)$ derived rather than fitted |
| [`Proof_Techniques_01_Sage_10.9_From_Pure_to_Applied.ipynb`](Partition_Function_Study/Proof_Techniques_01_Sage_10.9_From_Pure_to_Applied.ipynb) | SageMath 10.9 | 22 cells: direct, cases, counterexample, contrapositive, contradiction, induction — every example drawn from the Ising transfer matrix |
| [`SageMath_10.9_Test_and_Symbolic_Ising.ipynb`](Partition_Function_Study/SageMath_10.9_Test_and_Symbolic_Ising.ipynb) | SageMath 10.9 | Kernel smoke test |

### Running them

The Sage notebooks need a **SageMath 10.9** kernel registered with Jupyter:

```jsonc
// ~/Library/Jupyter/kernels/sagemath-10.9/kernel.json   (macOS)
{
  "argv": ["/Applications/SageMath-10-9.app/Contents/Frameworks/Sage.framework/Versions/Current/venv/bin/sage",
           "--python", "-m", "sage.repl.ipython_kernel", "-f", "{connection_file}"],
  "display_name": "SageMath 10.9",
  "language": "sage"
}
```

Point `argv[0]` at a **stable** path. Sage's own launcher scripts under `/var/tmp`
get purged by macOS and the kernel then dies with no useful error.

Two Sage facts these notebooks were built around, both learned the hard way:

* `A.eigenmatrix_right()` returns **`(D, P)`** — the diagonal matrix **first**.
* `.simplify_full()` will not close hyperbolic identities. `.exponentialize()` will.
  A CAS returning `False` is a failure to simplify, **not** a disproof.

## The sources

`src/` holds the LaTeX for all seven documents, one directory per part, sharing
`src/00-preamble.tex`. Rebuild everything with:

```sh
make all          # builds all 7 PDFs beside their sources
make clean        # removes aux files
make check            # no stray PDFs tracked + guidelines still in sync
```

Requires a TeX Live with `tikz`, `pgfplots`, `tcolorbox` and `newtx`.
Each part was verified to rebuild to its published page count.

## Guidelines

`guidelines/` holds the two reading manifests — which book to open, which
section, and in what order. They describe books that are **not** in this repo.

Each manifest also sits inside its own book folder, where git cannot see it
(the folder is ignored). `make check-guidelines` reports if the two copies have
drifted apart; `make sync-guidelines` re-copies the live one into `guidelines/`.

* [`Maths_Proof_Skill__MANIFEST.md`](guidelines/Maths_Proof_Skill__MANIFEST.md) — 8 books, 2,164 pp, but **week 1 is 42 pages**: Devlin §3 and Thurston
* [`Z_Ref_Books__MANIFEST.md`](guidelines/Z_Ref_Books__MANIFEST.md) — 23 books across 10 topic folders, the route to $Z$
* [`BOOKSHELF_INVENTORY.md`](guidelines/BOOKSHELF_INVENTORY.md) — all 31 books with page counts and MD5s, so you can confirm you hold the same editions these dossiers were written against

## Scripts

| script | what it is |
|---|---|
| [`11_tilecycle_gate.py`](scripts/11_tilecycle_gate.py) | Drop-in Illumina tile×cycle failure gate. Standard library only. Finds the failure mode where a tile reports Q37 while 70% of its calls at one cycle are wrong |
| `calc.py`, `mc.py`, `mc2.py` | Transfer-matrix reference values and the Metropolis runs behind the mixing-failure figure |
| `reference_calculation.py`, `build_nb.py` | Independent check values; notebook assembly |

---

## What is deliberately absent

**No book PDFs.** The study folders this project reads from hold 31 reference
books (~278 MB) — Axler, Devlin, Diedrichs & Lovett, Halmos, Tao, Thurston,
Stewart & Tall, Feynman, and the rest. They are copyrighted and they stay on
local disk. `.gitignore` blocks them three ways:

1. the book directory names (`Z_Ref_Books/`, `Maths_Proof_Skill/`, `*_Books_z/`, …)
2. `*.pdf` everywhere, with a single exception for `docs/*.pdf`
3. `make check-no-books`, which fails if a PDF is ever tracked outside `docs/`

The manifests in `guidelines/` tell you which editions to obtain and exactly
which sections to read. That is the part worth sharing.

## Licence

Dual-licensed — see [LICENSE](LICENSE).

| | licence |
|---|---|
| `docs/`, `src/`, `guidelines/`, `README.md`, `CLAUDE.md` | **CC BY 4.0** — share and adapt, including commercially, with attribution |
| `scripts/`, the notebooks, `Makefile` | **MIT** |
| the 31 books in `Z_Ref_Books/` and `Maths_Proof_Skill/` | **not covered, not distributed** — they are third-party, they stay on local disk, and each remains under its publisher's copyright |

## Standing method

> Think step by step and deeper. Be precise. Show evidence. Be realistic. Be pragmatic.

Which in practice means: every factual claim in these dossiers was checked
against the source before it was printed, corrections are recorded in the
documents rather than quietly patched (Part X §1; Tutorial §10), and a
computation is never allowed to stand in for a proof.
