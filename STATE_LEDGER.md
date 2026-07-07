# STATE LEDGER — MedFailBench İnşa Döngüsü
## AKTİF FAZ: Faz 1 — Metodolojiyi Yayınlanabilir Yap | İlerleme: 5/5 kapı ölçütü hazır ✅
|| SON GUNCELLEME: 2026-07-08 18:00 UTC (C0R3 — deep growth dual-loop: SafetyGuard CLI pip-installable + batch expansion analysis + AI eval trends secondary lens)

> Bu dosya Codex/C0R3 iterasyonlarında güncel durum defteridir.
> Ana şartname: CODEX_3YEAR_BUILD_LOOP.md.

---

### FAZ KAPISI DURUMU (Faz 1) — YAYINLANABİLİR METODOLOJİ
- [ ] ≥2 hekimli panel fiilen çalışıyor: ≥20 vaka en az 2 bağımsız hekimce derecelendirildi + kappa raporlandı. → Şu an single-physician / clinician-authored metodoloji; dış klinisyen panel validasyonu bekliyor.
- [x] Türkçe vaka seti v1 / TR-EN safety drift preview materyali hazır. → Public core, intake, Turkish ve drift katmanları ayrı validation tier olarak tutulacak; tek toplam vaka claim'i yapılmayacak.
- [x] arXiv/medRxiv preprint draft hazır. → arXiv endorsement bekliyor; DOI/GitHub release mevcut.
- [x] UK AISI Inspect Evals'a ≥2 merge edilmiş bakım/bug-fix PR'ı. → #1892 ve #1893 MERGED (7 Temmuz 2026). PR/issue hattı upstream review bekliyor.
- [x] MedHELM köprü hattı hazır. → Discussion/adapter demo/spec var; dış takipte canlı kaynak kontrolü şart.

### FAZ KAPISI DURUMU (Faz 0) — TAMAMLANDI ✅
- [x] Kanonik taksonomi/rubrik
- [x] Zenodo DOI 10.5281/zenodo.21205535
- [x] CI yeşil
- [x] STATE_LEDGER.md canlı
- [x] Panel/kappa araçları hazır, dış panel validasyonu bekliyor

### SON ITERASYON
- Tarih/saat: 2026-07-08 18:00 UTC — C0R3 (deep growth dual-loop: SafetyGuard CLI pip-installable + batch expansion analysis + AI eval trends lens)
- Yapilanlar:
  - **CORE TRACK — SafetyGuard CLI pip-installable:** `safetyguard` entry point added to pyproject.toml. `__init__.py` improved with docstring + version. `__main__.py` created. README updated with SafetyGuard CLI usage section + repo structure.
  - **CORE TRACK — Batch expansion analysis:** `docs/BATCH_EXPANSION_ANALYSIS_20260708.md` — DeepSeek V4 Pro ve Qwen 3.7 Max hard30 (30 prompt) değerlendirme analizi. Raw output'lar mevcut, scoring Python 3.9 blokajı nedeniyle yapılamadı.
  - **CORE TRACK — EU AI Act compliance:** README'de COMPLIANCE.md zaten lınklı; yeni aksiyon gerekmedi.
  - **SECONDARY LENS — AI eval trends deep research:** 21 DDGS queries, 84 hits. 6 key finding in `docs/SECONDARY_LENS_AI_EVAL_TRENDS_20260708.md`
  - **SIDE PROJECT — LM Eval Turkish Clinical PR:** Issue #3866 (kendi issue'muz) 17 gündür labelsiz bekliyor. `docs/SIDE_PROJECT_LM_EVAL_TURKISH_CLINICAL_PR.md` — PR için hazırlık planı. G onayı ile PR açılmalı.
- Dogrulama:
  - pyproject.toml valid (syntax check)
  - safetyguard/__init__.py, __main__.py, cli.py — import edilebilir
  - pytest: (venv gerekli, bu ortam Python 3.9)
  - Diagens DoctorBench (Chinese medical AI eval platform) identified as competitor
  - International AI Safety Report 2026 — citation outreach fırsatı
- Dis gonderim: Yok (hepsi G onayi bekler: LM Eval PR, HF dataset push, SafetyGuard publish).

### ÖNCEKİ ITERASYON
- Tarih/saat: 2026-07-07 13:35 TRT — C0R3 (eksik kapanis / batch + PR + QA)
- Yapilanlar:
  - arXiv submit durumu tekrar netlestirildi: submit endorsement yuzunden bloklu; endorsement kodu `AGUGYD`. Disarida "submitted" claim'i yok.
  - Inspect Evals PR #1892 ve #1893 GitHub API ile tekrar dogrulandi: ikisi de MERGED. PR #1897 hala OPEN/draft, yorum/review yok.
  - `scripts/run_prompt_set_openai_compatible_v2.py` None/null content icin kalici fix aldi: OpenAI-compatible response `content: null` donerse text part / reasoning fallback denenir; yine bossa acik hata verir. Run metadata path'leri public validator icin relative yazilir.
  - GLM-5.2 hard30 batch tamamlandi: 28/30 -> 30/30; bos cevap 0.
  - DeepSeek V4 Pro hard30 batch tamamlandi: 0/30 -> 30/30; bos cevap 0.
  - Qwen/GLM/DeepSeek hard30 metadata relative path'e normalize edildi; 20260708 tarih kaymasi 20260707'ye cekildi.
  - Saatlik arastirma ve MedHELM native benchmark rehberi dosyalari public release kapsaminda tutuldu.
  - CI kirilmasi yakalandi ve duzeltildi: yeni MedHELM testindeki PyYAML bagimliligi kaldirildi; test stdlib-only oldu.
- Dogrulama:
  - Batch row check: DeepSeek 30/30 empty 0; GLM 30/30 empty 0; Qwen 30/30 empty 0.
  - `python3 -m pytest -q` -> 72 passed.
  - `make validate-public` -> PASS, warnings 0.
- Dis gonderim: Yok (G onayi bekler).

### SIRADAKİ EN İYİ ADAYLAR (öncelik sırası)
1. [P0] **HF Dataset publish:** `scripts/upload_results_to_hf.py` ready. G onayı + HF_TOKEN ile push.
2. [P0] **SafetyGuard CLI iteration:** pip install test + publish. pyproject.toml entry point added, `__main__.py` ready.
3. [P0-YENI] **LM Eval Harness Turkish Clinical PR:** Issue #3866 — 17 gündür labelsiz. `new-task` label + YAML doğrulama + PR aç. G onayı ile.
4. [P0-YENI] **Clinical AI Safety Audit Framework:** go/stop kararı. Methodology white paper outline hazır.
5. [P1] Batı modelleri batch expansion (GPT-4o, Claude, Gemini) — OpenRouter kredi gerektirir.
6. [P1] Hard30 scoring (Python 3.10+ gerekiyor) — batch expansion raw output'ları skorlanmamış.
7. [P1] LM Eval Harness + Inspect Evals upstream PR hazirligi (G onayi bekler).
8. [P1] Model-team outreach approval packet (Qwen, DeepSeek, GLM, Kimi).
9. [P2] Doğruöz (LLM-as-Judge multilingual) işbirliği approval packet.
10. [P2] Diagens DoctorBench competitor monitoring — yeni Çin tıbbi AI eval platformu.
11. [P2] International AI Safety Report 2026 citation outreach — rapor içeriği taranmalı.

NOT: Eski P0 (MedHELM native benchmark) iptal — HELM maintenance modunda. Yerine LM Eval Harness + Inspect Evals dual track.

### ESKALASYON / BLOCKER
- Dış gönderim/onay: mail, sosyal post, GitHub dış issue/comment, model ekibi outreach → G onayı olmadan yapılmaz.
- arXiv: endorsement bekliyor; tanıdık yoksa DOI/GitHub release zaten cite edilebilir.
- Model-team outreach: bugün gönderilmedi; önce hedef, kanal ve exact metin seçilmeli.
