# arXiv upload package — MedFailBench v0.2.1

This package contains the arXiv-ready preprint source for MedFailBench v0.2.1.

## Files

- `main.tex` — manuscript source (arXiv-compatible, compiles with tectonic or pdflatex+bibtex)
- `references.bib` — bibliography (10 entries, all cited)
- `figures/severity_distribution.pdf` — figure (note: removed from text in v0.2.1 stats update; safe to delete or replace)

## How to build locally

```bash
cd preprint
make            # uses tectonic
# or
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

## How to upload to arXiv

1. Zip the contents of `preprint/` (main.tex, references.bib, figures/):
   ```bash
   cd preprint && zip -r ../dist/release/medfailbench-v0.2.1-arxiv.zip main.tex references.bib figures/
   ```
2. Go to https://arxiv.org/submit
3. License: choose arXiv's default or CC-BY-4.0 (matches the data license)
4. Upload the zip as the source
5. Category suggestion: `cs.CL` (Computation and Language) or `cs.AI` (Artificial Intelligence), cross-list `q-bio.QM` if relevant
6. DOI: enter `10.5281/zenodo.21205535` in the "DOI" field so arXiv links back to the Zenodo record
7. Submit

## Notes

- The preprint builds automatically on every PR via the `preprint` CI job (tectonic).
- Citation integrity is checked automatically: every `\cite{}` key must exist in references.bib.
- The abstract claims 100 cases and a real weekly pipeline — verified at submission time.
