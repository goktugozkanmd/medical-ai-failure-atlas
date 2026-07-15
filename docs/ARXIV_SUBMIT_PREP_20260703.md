# ArXiv Preprint Submission Prep
# Tarih: 2026-07-03
# Durum: PR #247 yeniden hazırlandı — arXiv submit değil, son yazar onayı bekleniyor

---

## Metadata

| Alan | Değer |
|------|-------|
| Title | MedFailBench: A Clinician-Built Open-Source Benchmark for Medical AI Safety Boundary Inspection |
| Authors | Goktug Ozkan, MD |
| Categories | cs.AI, cs.CL, cs.LG |
| License | CC-BY-4.0 (text), Apache-2.0 (code) |
| DOI | 10.5281/zenodo.21205535 |

## ArXiv Format Gereksinimleri

1. **LaTeX kaynağı:** main.tex (290 satır, arXiv uyumlu)
   - `hyperref`, `authblk`, `booktabs`, `amsmath`, `enumitem`, `graphicx` — standart paketler
   - Tek dosya + `references.bib` (83 satır, 9 referans)
   - `.bbl` ön-derleme kabul edilir; ayrı yükleme de mümkün

2. **Resimler/figures:** mevcut — `preprint/figures/severity_distribution.pdf` (Figure 1).
   `main.tex`'te `\includegraphics` ile referans verilmiş.

3. **Referanslar:** 9 referans, hepsi 2026-07-15'te yeniden kontrol edildi.
   - arXiv API: `2009.03300`, `2505.08775`, `2505.23802`, `2402.01741`, `2305.09617`, `2303.13375`, `2501.00593`.
   - Crossref/DOI: `10.1056/NEJMsr2214184`, `10.1038/s41746-026-02428-5`.
   - `ministry2026aivision` kaynağı canlı kontrolde timeout verdi; resmi kaynak doğrulanmadan politika iddiası eklenmesin diye metinden ve `references.bib` dosyasından çıkarıldı.

4. **Abstract:** 74 kelime, arXiv sınırı (1920 karakter) içinde.

5. **AI disclosure:** eklendi (AI-Assisted Writing Disclosure section, main.tex'te).

## Submit Öncesi Checklist

- [x] Zenodo DOI eklendi
- [x] main.tex'e DOI referansı eklendi
- [x] ArXiv PDF preview render denendi (`make -C preprint`)
- [ ] Anahtar kelimeler listesi hazırla
- [ ] Yazar ORCID ekle (varsa)
- [ ] AI-assisted writing disclosure: eklendi (main.tex'te AI-Assisted Writing Disclosure section)
- [x] Figure 1 (severity distribution) mevcut
- [x] LaTeX derleme testi: `make -C preprint` / Tectonic
- [ ] .bbl dosyasını da arXiv'e yükle (bibliography ayrı dosya kalırsa)

## 2026-07-15 Re-audit Receipts

- `uv run pytest -q` → 180 passed.
- `make -C preprint` → PASS, 6 sayfa PDF; yalnızca underfull hbox uyarıları.
- `make PYTHON='uv run python' validate-public` → PASS, Warnings: 0.
- `audit_submission.py README.md preprint/main.tex preprint/ARXIV_UPLOAD.md preprint/README.md docs/ARXIV_SUBMIT_PREP_20260703.md` → `overall_ok: true`.
- Referans script'i TeX bibliography parsing'de `references_found: 0` döndürdü; bu yüzden referans temizliği manuel canlı arXiv API, DOI ve Crossref kontrolleriyle yapıldı.

## Timeline
- Zenodo DOI → v0.2.1 release'ine bağlandı
- Son PDF önizlemesi ve yazar onayı sonrası arXiv submit
- Submit sonrası: HF Space'e arXiv badge ekle, README güncelle
