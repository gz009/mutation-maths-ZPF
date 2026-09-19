# Z_Ref_Books — reference shelf for the partition function

Assembled 19 September 2026 from four libraries on this machine. **23 books, 256 MB, all
MD5-verified byte-identical to their originals.** Nothing was moved or deleted; these are copies.

> **The point of this folder is not the books — it is the section numbers.** Almost every book here
> is needed for 20–40 pages, not cover to cover. The "READ" column is the whole value.

---

## Folder 01 — Operators, spectral theorem, trace  ✅ FULL

| Book | READ | Why |
|---|---|---|
| `Axler_Linear_Algebra_Done_Right_2015.pdf` | **§7.B** (p. 217 complex / 219 real), **§7.C** (p. 225), **§10.A** (p. 296–299) | 7.B lets you *define* `e^{-βH}` at all; 7.C makes it a positive operator so `Z>0`; 10.A makes `Tr` basis-independent |

**~30 pages. Start here.** With these three sections you can construct the quantum partition
function, and then do the calculation in the companion notebook.

## Folder 02 — Measure and the Lebesgue integral  ✅ FULL

| Book | READ | Why |
|---|---|---|
| `Axler_Measure_Integration_Real_Analysis_2022.pdf` | ch. 1–3 | same author as folder 01 — the continuation |
| `Kuttler_Linear_Algebra_and_Analysis_2020.pdf` | **ch. 20–24** | filed as linear algebra; the last five chapters are a full measure course. **ch. 22** = Riesz representation: *a positive operator determines a measure* — folders 01 and 02 meeting |

## Folder 03 — Probability and stochastic processes  ✅ FULL

| Book | READ | Why |
|---|---|---|
| `LeGall_Measure_Probability_Stochastic_Processes_2022.pdf` | measure → probability → processes | the bridge from folder 02 |
| `Lauritzen_Fundamentals_of_Mathematical_Statistics_2023.pdf` | reference | inference side |
| `Bressloff_..._Cell_Biology_Vol1_2022.pdf` | Vol. 1 first | **stochastic processes in actual cells** — the Cox-process gap from Part IX |
| `Bressloff_..._Cell_Biology_Vol2_2022.pdf` | later | spatial and network extensions |

## Folder 04 — Complex analysis, saddle point  ✅ FULL

| Book | READ | Why |
|---|---|---|
| `Radozycki_..._Part_III_2020.pdf` | contour integrals, Laurent series, **residue theorem** | how `Z` is *evaluated* asymptotically. Steepest descent is contour deformation |

## Folder 05 — Classical statistical mechanics  ✅ FULL

| Book | READ | Why |
|---|---|---|
| `Feynman_Statistical_Mechanics_Lectures.pdf` | **§1.1 The Partition Function**; **ch. 5 Order–Disorder** (§5.2 1-D, §5.3 2-D, **§5.4 The Onsager Problem** p. 136) | ch. 5 is the 1D Ising model and then why 2D was a landmark |
| `Phillips_Physical_Biology_of_the_Cell_2ed_2012.pdf` | **ch. 6 "Entropy Rules!"** | Boltzmann distribution, free-energy minimisation, **statistical mechanics of gene expression**. The bridge to biology |
| `Shankar_Principles_of_Quantum_Mechanics_2ed_1994.pdf` | **§21.2** (ch. 21, p. 627) | eq. 21.2.59 is the 1D Ising partition function; then the quantum↔classical path-integral map. *"The role of ħ is played by T."* |

**Folders 05 and the notebook are the same calculation three ways.** Read Shankar §21.2 and
Feynman ch. 5 against each other — one arrives from quantum mechanics, one from statistical
mechanics, and they meet at the Ising chain.

## Folder 06 — Quantum mechanics  ✅ FULL

| Book | Use |
|---|---|
| `Sakurai_Napolitano_Modern_Quantum_Mechanics_3ed_2021.pdf` | the graduate standard |
| `Griffiths_Introduction_to_Quantum_Mechanics_2018.pdf` | gentlest entry |
| `Binney_Skinner_The_Physics_of_Quantum_Mechanics_2013.pdf` | Oxford course; strong on the operator picture |

*(Shankar also belongs here — kept in folder 05 because §21.2 is why it is on this shelf.)*

## Folder 07 — Density operators, von Neumann entropy  ✅ FULL

| Book | READ | Why |
|---|---|---|
| `Nielsen_Chuang_..._2011.pdf` | **§2.1.8** operator functions · **§2.4** density operator · **§11.3** von Neumann entropy · **ch. 8** quantum noise | §2.1.8 is Axler §7.B in physicists' notation — read them back to back. **ch. 8** is the entry to open systems (Kraus/operator-sum) |
| `Schumacher_Westmoreland_..._2010.pdf` | ch. 8 density operators · **§19.5 Entropy and thermodynamics** | the thermodynamic link, stated cleanly |

## Folder 08 — Quantum statistical mechanics  ✅ FULL

| Book | Use |
|---|---|
| `Attard_Quantum_Statistical_Mechanics_from_First_Principles_2016.pdf` | exactly the title |
| `Bru_deSiqueiraPedra_Cstar_Algebras_Foundations_of_QSM_2020.pdf` | **the rigorous destination** — operator-algebraic. Go here only after folders 01, 02, 07 |

*(Feynman ch. 2–3 — density matrices, and the path-integral form of the density matrix — is in
folder 05.)*

## Folder 09 — Electronic structure, computing U(x)  ✅ FULL

| Book | Use |
|---|---|
| `Harvard_Practical_Guide_to_DFT.pdf` | **start here** — 36 pp, practical |
| `Harbola_DFT_Fundamentals_and_Applications.pdf` | 53 pp, fuller treatment |
| `Nomura_Akashi_..._arXiv_2210.07647.pdf` | 11 pp modern review |
| `Fiolhais_A_Primer_in_DFT_contents.pdf` | contents only — the full primer is not on the machine |

**This is the quantum layer that matters for docking:** DFT supplies `U(x)`; classical statistical
mechanics does everything above it.

## Folder 10 — Open quantum systems  🟡 PARTIAL

| Book | Status |
|---|---|
| `CONTESTED__Khrennikov_..._2023.pdf` | **Take the open-systems formalism; leave the interpretation.** Khrennikov's programme of applying quantum formalism to cognition and social science is idiosyncratic and not accepted |

**Also needed here:** Nielsen & Chuang **ch. 8** (folder 07) for Kraus/operator-sum.
**Still missing on this machine:** HEOM and master equations proper — Breuer & Petruccione,
*The Theory of Open Quantum Systems*, would fill it. This is the Part IX Tier 3 gap.

---

## Still to acquire — two books, neither on this machine

| Book | Why |
|---|---|
| **Levin & Peres, *Markov Chains and Mixing Times*** (free PDF from the authors) | the only thing that explains the notebook's §7 failure *quantitatively*. Le Gall and Bressloff cover stochastic processes but not mixing time |
| **Frenkel & Smit, *Understanding Molecular Simulation*** | you have GROMACS 2023.3 compiled and no text for the mathematics it implements — umbrella sampling, thermodynamic integration, FEP |

---

## Reading order

```
01 (Axler §7.B/7.C/10.A)  ->  the notebook  ->  05 (Shankar §21.2)
   ->  05 (Feynman ch.1, 5)  ->  05 (PBoC2 ch.6)
   ->  07 (N&C §2.4, §11.3, ch.8)  ->  02/03 (measure, then Le Gall)
   ->  08 (Attard, then Bru & Pedra)
```

Folder 04 whenever you need to *evaluate* rather than *define*.
Folder 06 as reference throughout. Folder 09 only when you turn to docking.

---

## Provenance

| Source library | Books taken |
|---|---|
| `~/Pure_Maths_TC_SelfStudy` | 8 (Axler ×2, Kuttler, Le Gall, Lauritzen, Feynman, Radozycki) |
| `~/TensoQi101` | 9 (Shankar, Sakurai, Griffiths, Binney & Skinner, N&C, Schumacher, 4 DFT) |
| `~/QBIT-HIS` | 6 (PBoC2, Bressloff ×2, Attard, Bru & Pedra, Khrennikov) |
| `~/qm-qi-qml` | 0 — nothing there that is not better covered above |

All 23 copies verified MD5-identical to source. Originals untouched.
Companion dossier: `../Learning_Z__PartX_v2.0__Four_Library_Audit__Study_Dossier.pdf`
Companion notebook: `../Partition_Function_01_Ising_Transfer_Matrix.ipynb`
