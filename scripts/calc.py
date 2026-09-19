import numpy as np, itertools, json
rng = np.random.default_rng(20260918)

# ---------------- Method A: transfer matrix, exact ----------------
def transfer_matrix(beta, J=1.0, h=0.0):
    return np.array([[np.exp(beta*(J+h)), np.exp(-beta*J)],
                     [np.exp(-beta*J),    np.exp(beta*(J-h))]])

def Z_transfer(N, beta, J=1.0, h=0.0):
    lam = np.linalg.eigvalsh(transfer_matrix(beta, J, h))
    lam = np.sort(lam)[::-1]                 # lam[0] = lambda_+
    return lam[0]**N + lam[1]**N, lam

# ---------------- Method B: brute force, all 2^N states ----------------
def Z_bruteforce(N, beta, J=1.0, h=0.0):
    Z = 0.0; E_sum = 0.0; M_sum = 0.0
    for cfg in itertools.product((-1, 1), repeat=N):
        s = np.array(cfg)
        E = -J*np.sum(s*np.roll(s, -1)) - h*np.sum(s)   # periodic
        w = np.exp(-beta*E)
        Z += w; E_sum += w*E; M_sum += w*np.sum(s)
    return Z, E_sum/Z, M_sum/Z

# ---------------- Method C: Metropolis Monte Carlo ----------------
def mc_energy(N, beta, J=1.0, h=0.0, sweeps=20000, burn=4000, seed=0):
    r = np.random.default_rng(seed)
    s = r.choice([-1, 1], size=N)
    Es = []
    E = -J*np.sum(s*np.roll(s, -1)) - h*np.sum(s)
    for t in range(sweeps):
        for _ in range(N):
            i = r.integers(N)
            dE = 2*s[i]*(J*(s[(i-1) % N] + s[(i+1) % N]) + h)
            if dE <= 0 or r.random() < np.exp(-beta*dE):
                s[i] = -s[i]; E += dE
        if t >= burn: Es.append(E)
    return float(np.mean(Es)), float(np.std(Es)/np.sqrt(len(Es)))

out = {}

# ---- 1. A vs B agreement ----
print("="*74); print("A (transfer matrix) vs B (brute force, 2^N states)"); print("="*74)
print(f"{'N':>3} {'beta':>6} {'Z_transfer':>18} {'Z_brute':>18} {'rel.err':>12}")
agree = []
for N in (4, 8, 12, 16):
    for beta in (0.2, 0.5, 1.0):
        Za, _ = Z_transfer(N, beta); Zb, Eb, Mb = Z_bruteforce(N, beta)
        rel = abs(Za-Zb)/Zb
        agree.append({"N": N, "beta": beta, "Z_transfer": Za, "Z_brute": Zb, "rel_err": rel})
        print(f"{N:>3} {beta:>6.2f} {Za:>18.10e} {Zb:>18.10e} {rel:>12.2e}")
out["agreement"] = agree
print(f"\nmax relative error over all cases: {max(a['rel_err'] for a in agree):.3e}")

# ---- 2. exact thermodynamics at h=0 ----
print("\n"+"="*74); print("Exact free energy per spin, h=0:  f = -kT ln(2 cosh(beta J))"); print("="*74)
betas = np.linspace(0.05, 3.0, 60)
f_exact = [-np.log(2*np.cosh(b))/b for b in betas]
u_exact = [-np.tanh(b) for b in betas]                  # energy per spin
c_exact = [(b*np.cosh(b)**-1)**2 for b in betas]         # heat capacity per spin, C/k
out["curves"] = {"beta": betas.tolist(), "f": f_exact, "u": u_exact, "c": c_exact}
for b in (0.2, 0.5, 1.0, 2.0, 3.0):
    print(f"  beta={b:4.1f}   f={-np.log(2*np.cosh(b))/b:+8.5f}   u={-np.tanh(b):+8.5f}   C/k={(b/np.cosh(b))**2:8.5f}")

# ---- 3. correlation length and the eigenvalue gap ----
print("\n"+"="*74); print("Correlation length from the eigenvalue gap:  xi = 1/ln(lam+/lam-)"); print("="*74)
xi_rows = []
for b in (0.2, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
    _, lam = Z_transfer(10, b)
    xi = 1.0/np.log(lam[0]/lam[1])
    xi_rows.append({"beta": b, "lam_plus": lam[0], "lam_minus": lam[1], "xi": xi})
    print(f"  beta={b:4.1f}   lam+={lam[0]:9.5f}   lam-={lam[1]:9.5f}   ratio={lam[0]/lam[1]:9.4f}   xi={xi:8.4f}")
out["xi"] = xi_rows
