# STATE LEDGER — MedFailBench İnşa Döngüsü
## AKTİF FAZ: Faz 1 — Metodolojiyi Yayınlanabilir Yap | İlerleme: 4/5 kapı ölçütü hazır
## SON GÜNCELLEME: 2026-07-06 19:20 TRT (C0R3)

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

### SON İTERASYON
- Tarih/saat: 2026-07-06 19:20 TRT — C0R3
- Yapılanlar:
  - HF/Gradio demo ana ekranına worst-case safety özeti eklendi ve public leaderboard modelleriyle filtrelendi.
  - HF demoya Failure Cards tabı eklendi; her kartta `Neden Tehlikeli?` ve `Daha Güvenli Cevap` bölümleri görünüyor.
  - MedHELM draftı gerçek GLM-5.2 TR/EN paired output ile güncellendi.
  - İlk weekly visibility taslağı hazırlandı: `docs/weekly_failure_of_the_week/001_average_scores_hide_unsafe_chest_pain.md`.
  - 10 model failure card hedefi tamamlandı: `docs/model_failure_cards/001`-`010`.
- Doğrulama:
  - Batch commit `d17ab17` pushlandı; GitHub CI run `28806034148` success.
  - Son 10 kart turu: `python3 -m pytest tests/test_leaderboard_app.py -q` → 27 passed.
  - Son 10 kart turu: `python3 -m pytest -q` → 67 passed.
  - Son 10 kart turu: `make validate-public` → PASS, warnings 0.
  - `git diff --check` → temiz.
  - Lokal path/API key scan → gerçek secret yok; test fixture içindeki sahte `Bearer abcdef...3456` eşleşmesi false-positive.
- Dış gönderim:
  - MedHELM comment, LinkedIn/X post, model-team outreach yapılmadı; G onayı bekler.
- Commit:
  - 10 kart turu commit/push bekliyor.

### SIRADAKİ EN İYİ ADAYLAR (öncelik sırası)
1. [P0] 10 kart turunu commit + push et; GitHub CI sonucunu canlı doğrula.
2. [P0] MedHELM discussion comment taslağını G onayına sun; onay olmadan dış comment yok.
3. [P0] LinkedIn/X weekly draftını G onayına sun; onay olmadan post yok.
4. [P1] Inspect Evals upstream review durumunu canlı kontrol et.
5. [P1] 300-500 vaka / 10-20 model cevap hedefi için sıradaki veri/model batch planını başlat.

### ESKALASYON / BLOCKER
- Dış gönderim/onay: mail, sosyal post, GitHub dış issue/comment, model ekibi outreach → G onayı olmadan yapılmaz.
- arXiv: endorsement bekliyor; tanıdık yoksa DOI/GitHub release zaten cite edilebilir.
- MedHELM draft: gerçek paired model-output örneği eklendi; public discussion comment için yine G onayı gerekir.
