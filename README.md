# Thesis: Surveying the Energy Landscapes of Multistable Elastic Structures

LaTeX source for Sam Avis's PhD thesis (Durham University), available at
<https://etheses.durham.ac.uk/id/eprint/15229/>.

## Building the thesis

Requires a LaTeX distribution (e.g. TeX Live) with `pdflatex` and `bibtex`.

```
make
```

This runs `bibtex` followed by `./runtex thesis.tex`, a helper script that
runs `pdflatex` the necessary number of times (with `bibtex` in between if
citations are present) until cross-references resolve.

Output: `thesis.pdf`.

## Supplementary material

The supplementary material (the ELLib software library, the structural
optimisation script, and supplementary videos) is not part of this
repository. It is available for download at
<https://doi.org/10.15128/r1n870zq87j>.

## Repository layout

| Path | Contents |
|---|---|
| `thesis.tex` | Master file (document class, preamble, `\include`s) |
| `titlepage.tex`, `front.tex` | Title page and front matter |
| `introduction.tex`, `appendix.tex` | Introduction and appendix |
| `<chapter>/chapter.tex` | One directory per chapter |
| `<chapter>/fig/` | Figures used by each chapter, plus the scripts and data that generate them |
| `library.bib` | Bibliography (all chapters) |
| `dur.png` | University logo used on the title page |
| `Makefile` | Build entry point |

## Figures

Each chapter's `fig/` directory contains the figure PDFs included by
LaTeX, together with the source material that produced them: Python
scripts (`plot.py`, `make_*.py`), data files, SVGs, and in some cases
C++ programs with their own `Makefile` (see
`energy_landscapes/fig/features/`).

Figure PDFs are committed rather than rebuilt by `make`, so the thesis
builds without needing to re-run the figure pipelines.

## Cleaning

Remove LaTeX artifacts with:

```
git clean -dxf
```

or manually: `rm *.aux *.log *.bbl *.blg *.out *.toc` (these are all
gitignored).
