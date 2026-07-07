# STATE LEDGER — MedFailBench İnşa Döngüsü
## AKTİF FAZ: Faz 1 — Metodolojiyi Yayınlanabilir Yap | İlerleme: 4/5 kapı ölçütü hazır
## SON GUNCELLEME: 2026-07-08 11:00 TRT (C0R3 — daily growth loop)

> Bu dosya Codex/C0R3 iterasyonlarında güncel durum defteridir.
> Ana şartname: CODEX_3YEAR_BUILD_LOOP.md.

---

### FAZ KAPISI DURUMU (Faz 1) — YAYINLANABİLİR METODOLOJİ
- [ ] ≥2 hekimli panel fiilen çalışıyor: ≥20 vaka en az 2 bağımsız hekimce derecelendirildi + kappa raporlandı. → Şu an single-physician / clinician-authored metodoloji; dış klinisyen panel validasyonu bekliyor.
- [x] Türkçe vaka seti v1 / TR-EN safety drift preview materyali hazır. → Public core, intake, Turkish ve drift katmanları ayrı validation tier olarak tutulacak; tek toplam vaka claim'i yapılmayacak.
- [x] arXiv/medRxiv preprint draft hazır. → arXiv endorsement bekliyor; DOI/GitHub release mevcut.
- [ ] UK AISI Inspect Evals'a ≥2 merge edilmiş bakım/bug-fix PR'ı. → PR/issue hattı upstream review bekliyor.
- [x] MedHELM köprü hattı hazır. → Discussion/adapter demo/spec var; dış takipte canlı kaynak kontrolü şart.

### FAZ KAPISI DURUMU (Faz 0) — TAMAMLANDI ✅
- [x] Kanonik taksonomi/rubrik
- [x] Zenodo DOI 10.5281/zenodo.21205535
- [x] CI yeşil
- [x] STATE_LEDGER.md canlı
- [x] Panel/kappa araçları hazır, dış panel validasyonu bekliyor

### SON ITERASYON
- Tarih/saat: 2026-07-08 11:00 TRT — C0R3 (daily growth loop)
- Yapilanlar:
  - HF Space Worst-case Safety tabina model family filter eklendi: dropdown ile All / Chinese Frontier / Western / Other secimi yapilabiliyor.
  - `detect_model_family()` heuristic: qwen/deepseek/glm/kimi -> Chinese Frontier, llama -> Western.
  - `update_worst_case()` callback ile filtre degisiminde canli guncelleme.
  - Inspect Evals PR #1897 kontrol edildi: OPEN, yorum/review yok.
  - Tum 69 test gecti, commit/push: 464fa96.
- Dogrulama:
  - `python3 -m pytest -v` -> 69 passed.
  - Model family filter manual test: All=2, Chinese Frontier=1, Western=1, Other=0.
  - Inspect Evals PR #1897: state=OPEN, no comments, no reviews, last updated 2026-07-07.
- Dis gonderim:
  - Yeni dis gonderim yok (G onayi bekler).
- Commit:
  - 464fa96: feat: add model family filter to worst-case safety tab
  - Pushlandi: origin/main.

### SIRADAKİ EN İYİ ADAYLAR (öncelik sırası)
1. [P1] 300-500 vaka / 10-20 model cevap hedefi için sıradaki veri/model batch planını başlat.
2. [P1] Model-team outreach için tek hedefli, kaynak-destekli kısa approval packet hazırla; G onayı olmadan mail/comment yok.
3. [P1] arXiv endorsement blocker'ı için pratik çözüm ara; submit mümkün olmadan “submit edildi” deme.
4. [P1] Inspect Evals PR #1897 durumunu takip et; maintainer yorumuna göre cevap taslağı hazırla.

### ESKALASYON / BLOCKER
- Dış gönderim/onay: mail, sosyal post, GitHub dış issue/comment, model ekibi outreach → G onayı olmadan yapılmaz.
- arXiv: endorsement bekliyor; tanıdık yoksa DOI/GitHub release zaten cite edilebilir.
- Model-team outreach: bugün gönderilmedi; önce hedef, kanal ve exact metin seçilmeli.
