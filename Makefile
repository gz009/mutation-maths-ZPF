# Build every dossier from source.  Requires a TeX Live with tikz, pgfplots,
# tcolorbox, newtx.  Each part is a separate document; 00-preamble.tex is shared
# and found via TEXINPUTS.
TEX     := pdflatex -interaction=nonstopmode -halt-on-error
SRC     := src
OUT     := build
TEXIN   := TEXINPUTS=..//:

PARTS := part06_idea_analysis/main \
         part07_nano_quantum_biology/partvii \
         part08_amr_ngs_measurement/partviii \
         part09_measure_not_the_point/partix \
         part10_learning_Z_v1.0/partx \
         part10_learning_Z_v2.0/partx2 \
         tutorial_proof_techniques/tutorial

.PHONY: all clean check-no-books check-guidelines check
all:
	@for p in $(PARTS); do \
	  d=$(SRC)/$${p%/*}; f=$${p##*/}; \
	  echo "==> $$d/$$f.tex"; \
	  ( cd $$d && $(TEXIN) $(TEX) $$f.tex >/dev/null && $(TEXIN) $(TEX) $$f.tex >/dev/null ) \
	    || { echo "FAILED: $$d/$$f"; exit 1; }; \
	done
	@echo "All parts built. PDFs are beside their sources; copy to docs/ to publish."

clean:
	@find $(SRC) -name '*.aux' -o -name '*.log' -o -name '*.out' -o -name '*.toc' | xargs rm -f
	@echo "aux files removed"

# Refuse to be surprised: fail loudly if a book ever lands in the working tree.
check-no-books:
	@n=$$(git ls-files | grep -v '^docs/' | grep -ci '\.pdf$$' || true); \
	 if [ "$$n" != "0" ]; then echo "FAIL: $$n tracked PDF(s) outside docs/"; exit 1; fi
	@echo "OK: no PDFs tracked outside docs/"

# The reading manifests live inside the book folders, which are gitignored.
# guidelines/ holds the tracked copies. This target keeps the two honest.
check-guidelines:
	@ok=1; \
	 for p in "Z_Ref_Books:Z_Ref_Books__MANIFEST.md" "Maths_Proof_Skill:Maths_Proof_Skill__MANIFEST.md"; do \
	   d=$${p%%:*}; g=$${p##*:}; live="Partition_Function_Study/$$d/00_README_MANIFEST.md"; \
	   if [ ! -f "$$live" ]; then echo "skip: $$live not present (books not on this machine)"; continue; fi; \
	   if cmp -s "$$live" "guidelines/$$g"; then echo "in sync: $$d"; \
	   else echo "DIVERGED: $$live vs guidelines/$$g  -> run 'make sync-guidelines'"; ok=0; fi; \
	 done; [ $$ok = 1 ]

sync-guidelines:
	@for p in "Z_Ref_Books:Z_Ref_Books__MANIFEST.md" "Maths_Proof_Skill:Maths_Proof_Skill__MANIFEST.md"; do \
	   d=$${p%%:*}; g=$${p##*:}; live="Partition_Function_Study/$$d/00_README_MANIFEST.md"; \
	   [ -f "$$live" ] && cp "$$live" "guidelines/$$g" && echo "copied $$live -> guidelines/$$g"; \
	 done

check: check-no-books check-guidelines
