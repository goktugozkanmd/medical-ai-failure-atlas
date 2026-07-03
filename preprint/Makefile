main.pdf: main.tex references.bib
	tectonic main.tex

clean:
	rm -f *.aux *.bbl *.blg *.log *.out main.pdf
	tectonic -X clean 2>/dev/null || true
