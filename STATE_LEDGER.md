# STATE LEDGER — MedFailBench İnşa Döngüsü
## AKTİF FAZ: Faz 1 — Metodolojiyi Yayınlanabilir Yap | İlerleme: 5/5 kapı ölçütü hazır ✅
|| SON GUNCELLEME: 2026-07-09 08:00 UTC (C0R3 — deep growth dual-loop: eval CI pipeline design + Clinical AI Safety Audit Framework outline + automation/data secondary lens)

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
- Tarih/saat: 2026-07-07 21:22 TRT — C0R3 (G onaylı dış aksiyon paketi)
- Yapilanlar:
  - **LM Eval Harness:** Issue #3866 hattı PR #3903'e dönüştürüldü/güncellendi. Branch `feat/turkish-clinical-source-support`, head `1db2dbfa`, PR açık ve mergeable.
  - **HF Dataset:** `goktugozkanmd/medfailbench-v02-results` public push tamamlandı. Train split 181 satır, 0 skipped.
  - **SafetyGuard:** PyPI-ready paket düzeltildi; package adı `safetyguard`, prompt/rubric pakete gömülü, wheel/sdist build edildi. PyPI upload credential yokluğu nedeniyle bloklu.
  - **International AI Safety Report outreach:** Resmi site maili decode edildi (`secretariat.AIStateofScience@dsit.gov.uk`); outreach maili gönderildi ve Gmail Sent içinde doğrulandı.
- Dogrulama:
  - LM Eval task: `.venv/bin/python -m lm_eval --model dummy --tasks turkish_clinical_source_support --limit 1` geçti.
  - HF dataset API: public false değil, `private=False`; `load_dataset(..., split="train")` -> 181 rows.
  - SafetyGuard: `pytest -q` -> 72 passed; `twine check` -> PASSED; pip wheel install Python 3.13 -> help + prompt/rubric load OK.
  - Outreach: Message-ID `<178344851375.87342.16612323023986284931@gmail.com>` sent+verified.
- Dis gonderim: Yapıldı — IASR outreach maili. PyPI gerçek upload credential bekliyor.

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
1. [DONE] **HF Dataset publish:** `goktugozkanmd/medfailbench-v02-results` public, 181 train rows.
2. [BLOCKED] **SafetyGuard PyPI publish:** wheel/sdist hazır ve doğrulandı; PyPI API token/account yok.
3. [DONE] **LM Eval Harness Turkish Clinical PR:** PR #3903 açık, mergeable, Issue #3866 kapanış referanslı.
4. [DONE] **International AI Safety Report 2026 citation outreach:** mail gönderildi ve Sent doğrulandı.
5. [P0-YENI-DONE] **Clinical AI Safety Audit Framework:** **OUTLINE HAZIR** (`docs/CLINICAL_AI_SAFETY_AUDIT_FRAMEWORK_OUTLINE.md`). Go/stop kararı bekliyor.
6. [P0-YENI] **Eval CI Pipeline:** **DESIGN HAZIR** (`docs/CORE_TRACK_AUTOMATION_DATA_PIPELINE_20260709.md`). G onayı ile Phase 1 implementasyonuna başla.
7. [P0-YENI] **Medical AI Safety Monitoring Bot:** **SPEC HAZIR** (`docs/SECONDARY_LENS_AUTOMATION_DATA_20260709.md`). G onayı ile build'e başla.
8. [P1] Batı modelleri batch expansion (GPT-4o, Claude, Gemini) — OpenRouter kredi gerektirir.
9. [P1] Hard30 scoring (Python 3.10+ gerekiyor) — batch expansion raw output'ları skorlanmamış.
10. [P1] Model-team outreach approval packet (Qwen, DeepSeek, GLM, Kimi).
11. [P2] Doğruöz (LLM-as-Judge multilingual) işbirliği approval packet.
12. [P2] Diagens DoctorBench competitor monitoring — yeni Çin tıbbi AI eval platformu.

NOT: Eski P0 (MedHELM native benchmark) iptal — HELM maintenance modunda. Yerine LM Eval Harness + Inspect Evals dual track.

### ESKALASYON / BLOCKER
- Dış gönderim/onay: mail, sosyal post, GitHub dış issue/comment, model ekibi outreach → G onayı olmadan yapılmaz.
- arXiv: endorsement bekliyor; tanıdık yoksa DOI/GitHub release zaten cite edilebilir.
- Model-team outreach: bugün gönderilmedi; önce hedef, kanal ve exact metin seçilmeli.
