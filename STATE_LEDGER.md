# STATE LEDGER — MedFailBench İnşa Döngüsü
## AKTİF FAZ: Faz 1 — Metodolojiyi Yayınlanabilir Yap | İlerleme: 4/5 kapı ölçütü hazır
## SON GÜNCELLEME: 2026-07-06 19:36 TRT (C0R3)

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
- Tarih/saat: 2026-07-06 19:36 TRT — C0R3
- Yapılanlar:
  - Commit `d17ab17`: HF demo worst-case safety view + Failure Cards tab + MedHELM real GLM-5.2 TR/EN pair + weekly draft.
  - Commit `7b77ab4`: model failure cards 5'ten 10'a çıkarıldı; renderer testi 10 kartı doğruluyor.
  - Yeni canlı GLM drift probe başlatıldı: 5 EN/TR çift, 10 gerçek output.
  - Yeni artifactler: `data/tr_en_drift_glm_probe_v0_1.tsv`, `model_runs/tr_en_drift_glm_5_2_probe_v0_1.json`, `docs/TR_EN_DRIFT_GLM_PROBE_V0_1.md`, `docs/tr_en_drift_glm_probe_v0_1.json`.
  - README yeni GLM TR/EN safety-drift probe bağlantısıyla güncellendi.
- Doğrulama:
  - `d17ab17` CI run `28806034148` success.
  - `7b77ab4` CI run `28806406317` success.
  - Drift probe turu: `python3 -m pytest tests/test_tr_en_drift_probe.py -q` → 2 passed.
  - Drift probe turu: `python3 -m pytest -q` → 69 passed.
  - Drift probe turu: `make validate-public` → PASS, warnings 0.
  - Commit `3d6501e` pushlandı; TSV CRLF/trailing whitespace fark edildi ve düzeltildi.
  - Commit `43c85f1` pushlandı; CI run `28807189978` success.
  - `git diff --check` → temiz.
  - Lokal path/API key scan → gerçek secret yok.
- Dış gönderim:
  - MedHELM comment, LinkedIn/X post, model-team outreach yapılmadı; G onayı bekler.
- Commit:
  - Drift probe artifactleri pushlandı; son CI yeşil.

### SIRADAKİ EN İYİ ADAYLAR (öncelik sırası)
1. [P0] MedHELM discussion comment taslağını G onayına sun; onay olmadan dış comment yok.
2. [P0] LinkedIn/X weekly draftını G onayına sun; onay olmadan post yok.
3. [P1] Inspect Evals upstream review durumunu canlı kontrol et.
4. [P1] 300-500 vaka / 10-20 model cevap hedefi için sıradaki veri/model batch planını başlat.

### ESKALASYON / BLOCKER
- Dış gönderim/onay: mail, sosyal post, GitHub dış issue/comment, model ekibi outreach → G onayı olmadan yapılmaz.
- arXiv: endorsement bekliyor; tanıdık yoksa DOI/GitHub release zaten cite edilebilir.
- MedHELM draft: gerçek paired model-output örneği eklendi; public discussion comment için yine G onayı gerekir.
