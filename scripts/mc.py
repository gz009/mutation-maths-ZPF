import numpy as np
def mc_run(N, beta, J=1.0, sweeps=30000, burn=6000, seed=1):
    r = np.random.default_rng(seed)
    s = r.choice([-1,1], size=N).astype(np.int8)
    E = -J*np.sum(s*np.roll(s,-1)); Es=[]; Ms=[]
    for t in range(sweeps):
        for _ in range(N):
            i = r.integers(N)
            dE = 2*J*s[i]*(s[(i-1)%N]+s[(i+1)%N])
            if dE<=0 or r.random()<np.exp(-beta*dE):
                s[i]=-s[i]; E+=dE
        if t>=burn: Es.append(E); Ms.append(s.sum())
    return np.array(Es,float), np.array(Ms,float)

def autocorr_time(x, maxlag=2000):
    x = x - x.mean(); n=len(x); v=(x*x).mean()
    if v==0: return 1.0
    tau=0.5
    for k in range(1,min(maxlag,n//2)):
        c=(x[:-k]*x[k:]).mean()/v
        if c<0.05: break
        tau+=c
    return 2*tau

N=64
print("="*88)
print(f"Metropolis vs exact, N={N}, 30,000 sweeps each (24,000 after burn-in)")
print("="*88)
print(f"{'beta':>5} {'xi':>8} {'u exact':>10} {'u MC':>10} {'err':>9} {'|M|/N MC':>10} {'tau_int':>9} {'verdict':>10}")
rows=[]
for beta in (0.2,0.5,1.0,1.5,2.0,2.5,3.0):
    T=np.array([[np.exp(beta),np.exp(-beta)],[np.exp(-beta),np.exp(beta)]])
    lam=np.sort(np.linalg.eigvalsh(T))[::-1]; xi=1/np.log(lam[0]/lam[1])
    u_ex=-np.tanh(beta)
    Es,Ms=mc_run(N,beta,sweeps=30000,burn=6000,seed=7)
    u_mc=Es.mean()/N; err=abs(u_mc-u_ex)
    tau=autocorr_time(Ms)
    verdict = "ok" if err<0.01 else ("drifting" if err<0.05 else "FAILS")
    rows.append((beta,xi,u_ex,u_mc,err,abs(Ms).mean()/N,tau,verdict))
    print(f"{beta:>5.1f} {xi:>8.2f} {u_ex:>10.5f} {u_mc:>10.5f} {err:>9.5f} {abs(Ms).mean()/N:>10.4f} {tau:>9.1f} {verdict:>10}")
print("\nNote: xi is the correlation length in lattice units; N=64.")
print("When xi approaches N the chain can no longer decorrelate within the run.")
import json; json.dump([list(map(float,r[:7]))+[r[7]] for r in rows], open("mc_rows.json","w"), indent=1)
