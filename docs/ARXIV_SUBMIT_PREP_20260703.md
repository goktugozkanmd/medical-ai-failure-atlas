# ArXiv Preprint Submission Prep
# Tarih: 2026-07-03
# Durum: HAZIRLIK — Zenodo DOI sonrası submit edilecek

---

## Metadata

| Alan | Değer |
|------|-------|
| Title | MedFailBench: A Clinician-Built Open-Source Benchmark for Medical AI Safety Boundary Inspection |
| Authors | Goktug Ozkan, MD |
| Categories | cs.AI, cs.CL, cs.LG |
| License | CC-BY-4.0 (text), Apache-2.0 (code) |
| DOI | (v0.2.1 release sonrası Zenodo'dan alınacak — issue #184) |

## ArXiv Format Gereksinimleri

1. **LaTeX kaynağı:** main.tex (310 satır, arXiv uyumlu)
   - `hyperref`, `authblk`, `booktabs`, `amsmath`, `enumitem`, `graphicx` — standart paketler
   - Tek dosya + `references.bib` (110 satır, 13 referans)
   - `.bbl` ön-derleme kabul edilir; ayrı yükleme de mümkün

2. **Resimler/figures:** mevcut — `preprint/figures/severity_distribution.pdf` (Figure 1).
   `main.tex`'te `\includegraphics` ile referans verilmiş.

3. **Referanslar:** 13 referans, tüm arXiv ID'leri doğrulandı (22:00 audit).
   - `pal2024medhelm` arXiv ID'siz — "Preprint; arXiv ID not verified" notu var.
   - DOI'siz journal referansları (`levkovich2024dosing`) crossref doğrulaması gerektirir.

4. **Abstract:** 74 kelime, arXiv sınırı (1920 karakter) içinde.

5. **AI disclosure:** eklendi (AI-Assisted Writing Disclosure section, main.tex'te).

## Submit Öncesi Checklist

- [ ] Zenodo DOI eklensin (issue #184)
- [ ] main.tex'e DOI referansı ekle
- [ ] ArXiv PDF preview render dene (`make` çalışıyorsa Makefile ile)
- [ ] Anahtar kelimeler listesi hazırla
- [ ] Yazar ORCID ekle (varsa)
- [ ] AI-assisted writing disclosure: eklendi (main.tex'te AI-Assisted Writing Disclosure section)
- [ ] Figure 1 (severity distribution) mevcut
- [ ] LaTeX derleme testi: `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
- [ ] .bbl dosyasını da arXiv'e yükle (bibliography ayrı dosya kalırsa)

## Timeline
- Zenodo DOI → v0.2.1 release'ine bağlanacak
- DOI sonrası arXiv submit
- Submit sonrası: HF Space'e arXiv badge ekle, README güncelle