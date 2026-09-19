import numpy as np, json
def chain_M(N,beta,sweeps,burn,seed,J=1.0):
    r=np.random.default_rng(seed); s=r.choice([-1,1],size=N).astype(np.int8); Ms=[]
    for t in range(sweeps):
        for _ in range(N):
            i=r.integers(N); dE=2*J*s[i]*(s[(i-1)%N]+s[(i+1)%N])
            if dE<=0 or r.random()<np.exp(-beta*dE): s[i]=-s[i]
        if t>=burn: Ms.append(s.sum()/N)
    return float(np.mean(Ms))
N=64; SW=30000; BURN=6000; SEEDS=range(8)
print("="*92)
print(f"The honest failure test: TRUE <M> = 0 exactly (h=0 symmetry), for every beta.")
print(f"8 independent chains, N={N}, {SW:,} sweeps each. If MCMC works they all return ~0.")
print("="*92)
print(f"{'beta':>5} {'xi':>8} |  per-chain <M>/N from 8 independent chains {'':>24} | {'spread':>8} {'verdict':>9}")
rows=[]
for beta in (0.2,0.5,1.0,1.5,2.0,2.5,3.0):
    T=np.array([[np.exp(beta),np.exp(-beta)],[np.exp(-beta),np.exp(beta)]])
    lam=np.sort(np.linalg.eigvalsh(T))[::-1]; xi=1/np.log(lam[0]/lam[1])
    vals=[chain_M(N,beta,SW,BURN,1000+s) for s in SEEDS]
    spread=max(vals)-min(vals)
    verdict = "ok" if spread<0.15 else ("poor" if spread<0.8 else "BROKEN")
    txt=" ".join(f"{v:+5.2f}" for v in vals)
    print(f"{beta:>5.1f} {xi:>8.2f} | {txt} | {spread:>8.3f} {verdict:>9}")
    rows.append({"beta":beta,"xi":xi,"vals":vals,"spread":spread,"verdict":verdict})
json.dump(rows,open("mc_ergodicity.json","w"),indent=1)
print("\nEvery chain is running the correct algorithm. None of them is buggy.")
print("They disagree because none of them has mixed -- the barrier between +M and -M")
print("grows with beta, and the time to cross it grows exponentially.")
