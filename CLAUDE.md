# Working in this repository

Run Claude Code from this directory (`~/mutation-maths-ZPF`). Everything the
project needs is under this root: the dossiers, their LaTeX, the notebooks, and
the two reference libraries.

## The one hard rule

**No third-party book ever gets committed.** `Z_Ref_Books/` and
`Maths_Proof_Skill/` are on local disk for reading; they are not this
repository's to distribute. Three guards enforce it, and none of them should be
weakened:

1. `.gitignore` excludes both directory names, at any depth.
2. `.gitignore` excludes `*.pdf` everywhere, with one exception: `!docs/*.pdf`.
3. `make check-no-books` fails if any PDF outside `docs/` is ever tracked.

If a produced PDF needs publishing, it goes in `docs/` — nowhere else is tracked.

## Layout

```
docs/                        the 7 published PDFs (CC BY 4.0)
src/                         LaTeX, one directory per part, shared 00-preamble.tex
guidelines/                  reading manifests + bookshelf inventory
scripts/                     Python (MIT)
Partition_Function_Study/    the live study folder — JupyterLab opens this
    *.ipynb                  tracked
    Z_Ref_Books/             23 books, 256 MB   NOT tracked
    Maths_Proof_Skill/        8 books,  22 MB   NOT tracked
    archive_v1.0/            superseded PDFs    NOT tracked
```

## Commands

```sh
make all               # rebuild all 7 PDFs from src/ (verified page counts)
make clean             # remove aux files
make check             # no stray PDFs tracked + guidelines still in sync
make sync-guidelines   # re-copy the live manifests into guidelines/
```

`make all` needs TeX Live with `tikz`, `pgfplots`, `tcolorbox`, `newtx`.

## Jupyter / SageMath

Kernel `sagemath-10.9`, registered at
`~/Library/Jupyter/kernels/sagemath-10.9/kernel.json`, pointing at

```
/Applications/SageMath-10-9.app/Contents/Frameworks/Sage.framework/Versions/Current/venv/bin/sage
```

Point it at a **stable** path. Sage's launcher scripts under `/var/tmp` get
purged by macOS and the kernel then dies with no useful error. `~/bin/sage` is a
wrapper script, not a symlink — a symlink breaks Sage (`sage-eval: not found`).

Three Sage facts these notebooks were built around:

* `A.eigenmatrix_right()` returns **`(D, P)`** — diagonal matrix **first**.
* `.simplify_full()` will not close hyperbolic identities; `.exponentialize()` will.
* Never name a variable `N` — `N()` is Sage's numerical evaluation function.

A CAS returning `False` is a failure to simplify, **not** a disproof.

## How work is done here

> Think step by step and deeper. Be precise. Show evidence. Be realistic. Be pragmatic.

In practice:

* **Check before printing.** Quotations come from the PDFs on disk, not memory.
  Page and section numbers get verified against the actual file.
* **Build, render, look.** Every dossier is compiled, rasterised to PNG and
  visually inspected before it is deployed. Overlaps and overflows are fixed, not
  shipped.
* **Corrections stay visible.** When something published turns out wrong, the
  correction goes into the document itself — Part X §1 records that v1.0 told the
  reader to buy books already on the shelf; the proof tutorial §10 records a
  mis-cited cell number. Superseded versions are kept, labelled.
* **A computation is never a proof.** Verifying 20 cases is 20 facts. The
  distinction is the argument of the whole project.
