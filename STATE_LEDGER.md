# STATE LEDGER — MedFailBench İnşa Döngüsü
## AKTİF FAZ: Faz 1 — Metodolojiyi Yayınlanabilir Yap | İlerleme: 5/5 kapı ölçütü hazır ✅
||| SON GUNCELLEME: 2026-07-11 13:45 TRT (C0R3 — prompt-linked rescoring corrected; external corrections prepared)

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
- Tarih/saat: 2026-07-11 13:45 TRT — C0R3 (prompt-linked scorer audit correction)
- Yapilanlar:
  - Geç gelen bağımsız denetim, legacy hard30 ham dosyalarında `prompt_text` bulunmadığını ve ilk düzeltilmiş yeniden puanlamada prompt-bağımlı kapıların çalışmadığını ortaya çıkardı.
  - Qwen ve DeepSeek ham dosyalarına kanonik 30 prompt bağlandı; skor dosyaları yeniden üretildi. Qwen: 4 lexical alarm, ortalama safety 4.0/5. DeepSeek: 6 lexical alarm, ortalama safety 3.8/5.
  - Teknik inceleme, alarmların çoğunda açık klinik yönetim dili bulunduğunu; DeepSeek H001 ve H009'da ise self-referential/truncated çıktı kusuru olduğunu gösterdi. Klinik adjudication hâlâ bekliyor.
  - Prompt metni olmayan girdiler artık scorer tarafından reddediliyor. CLI etiket özeti eski `risk_label` yerine gerçek `final_label` alanını okuyor.
  - Qwen ve DeepSeek dış kayıtları için şeffaf düzeltme metinleri hazırlandı; eski 0-trigger iddiası repo belgelerinden kaldırıldı.
- Dogrulama:
  - Local test: 126 passed.
  - Qwen prompt-linked rescore: 30 rows, 4 `missed_urgent_escalation` alarmı.
  - DeepSeek prompt-linked rescore: 30 rows, 5 `missed_urgent_escalation` + 1 `unsafe_remote_dosing` alarmı.
- Dis gonderim: Şeffaf follow-up düzeltmeleri commit bağlantısı hazırlandıktan sonra aynı GitHub kayıtlarına eklenecek.

### ÖNCEKİ ITERASYON
- Tarih/saat: 2026-07-09 12:12 TRT — C0R3 (UTSAK 2026 oral abstract submitted)
- Yapilanlar:
  - UTSAK/Symplify hesabi olusturuldu, Gmail Spam'e dusen dogrulama mailinden hesap aktive edildi.
  - Credential vault'a `utsak_symplify` ve `utsak_symplify_username` olarak kaydedildi.
  - Türkçe/İngilizce oral abstract paketi hazirlandi; de-AI/humanizasyon, referans halusinasyon kontrolu ve claim-support kontrolu yapildi.
  - Sözlü Bildiri olarak portala gonderildi.
- Dogrulama:
  - Portal bildiri no: `2C81DB04`.
  - Portal durumu: `Başvuru gönderildi`.
  - Portal detayinda Türkçe ve İngilizce özet readback yapildi.
  - Yazar readback: `Uzm. Dr. Göktuğ Özkan`, sorumlu yazar; kurum `Kütahya Emet Dr. Fazıl Doğan State Hospital`.
  - Dosya yukleme zorunlulugu gorunmedi; portal `Bu bildiriye ait yüklü dosya bulunamadı` yazdi.
  - Ödeme ekrani cikmadi; ödeme yapilmadi.
  - Paket kaydi: `.../utsak_2026_goktug_ai_drug_safety_20260709/UTSAK2026_GOKTUG_AI_ILAC_GUVENLIGI_PORTAL_KAYIT_20260709.md`.
- Dis gonderim: UTSAK oral abstract formal portal submit tamamlandi.

### ÖNCEKİ ITERASYON
- Tarih/saat: 2026-07-09 11:43 TRT — C0R3 (JBI Editorial Manager submission completed)
- Yapilanlar:
  - JBI submission package Editorial Manager uzerinden tamamlandi ve final onay verildi.
  - Article type etik engel nedeniyle Special Communication yerine Original Research yapildi; EIC daveti/on yazisma bulunmadigi icin Special Communication onayi verilmedi.
  - Final DOCX/PDF paketi temizlendi: structured abstract, statement-of-significance table, CRediT roles, data/code availability, subscription publishing route.
  - Elsevier Publishing Options: Subscription secildi; ekranda `Nothing to pay` goruldu.
- Dogrulama:
  - EM confirmation: `Thank you for approving "A Clinical Informatics Evidence Layer for Health AI Safety Governance: Mapping Synthetic Failure-Mode Benchmarks to Oversight Workflows"`.
  - Gmail confirmation: `JBI-26-2501 - Confirming your submission to Journal of Biomedical Informatics`.
  - Final main menu readback: Incomplete 0, Waiting for Author Approval 0, Submissions Being Processed 1.
  - Built EM PDF kaydi: `JBI_EM_BUILT_SUBMISSION_PDF_20260709.pdf`, 13 sayfa, 1,510,196 bytes.
  - Pre-submit reference/claim audit kaydi mevcut: `JBI_V0_5_DELTA_REFERENCE_CLAIM_AUDIT_20260709_0047.md/json`.
- Dis gonderim: JBI Editorial Manager submit tamamlandi. Odeme yok; OA secilmedi.

### ÖNCEKİ ITERASYON
- Tarih/saat: 2026-07-08 11:35 TRT — Codex (workflow scope fixed + GitHub eval dry-run verified)
- Yapilanlar:
  - GitHub CLI token'a `workflow` scope eklendi.
  - Local eval automation commit'i `5d5a49a` remote `main` dalina push edildi.
  - Eval Pipeline workflow'u GitHub'da aktif hale geldi.
  - Workflow dispatch ile masrafsiz dry-run calistirildi.
- Dogrulama:
  - GitHub auth scope readback: `workflow` scope mevcut.
  - Push: `65e0899..5d5a49a main -> main`.
  - Normal CI run `28929069347`: success.
  - Eval Pipeline dry-run `28929095888`: success. Dry-run oldugu icin `leaderboard/results` artifact uyarisi beklenen davranis; API cagrisi ve provider harcamasi yapilmadi.
- Dis gonderim: Yok. Bu iterasyonda email, sosyal post veya model-team outreach gonderilmedi.

### ÖNCEKİ ITERASYON
- Tarih/saat: 2026-07-08 11:18 TRT — Codex (G-approved eval automation implementation)
- Yapilanlar:
  - Eval CI Pipeline Phase 1 uygulandi: `.github/workflows/eval-pipeline.yml`, `scripts/ci_eval_runner.py`, `scripts/ci_score_runner.py`.
  - Workflow `config/models.yaml` model registry'sini okuyacak, dry-run varsayilanıyla masraf çıkarmadan doğrulayacak, manuel gerçek run'da ham JSON üretip skorlayacak ve isteğe bağlı sonuç commit'i yapacak şekilde kuruldu.
  - Runner `leaderboard/medfailbench_prompts_v0_2.jsonl` prompt setini doğrudan okuyacak şekilde yazıldı; skor runner mevcut `failure_atlas/scorer.py` ile uyumlu JSON kullanıyor.
  - `leaderboard/EVAL_PIPELINE_PHASE_1.md` plan durumundan implementation record durumuna güncellendi.
- Dogrulama:
  - Workflow YAML parse check: PASS.
  - `.venv/bin/python -m pytest tests/test_ci_eval_pipeline.py`: 2 passed.
  - `scripts/ci_eval_runner.py --dry-run` real API çağrısı yapmadan 2 prompt planını doğruladı.
  - `scripts/ci_score_runner.py` mevcut Qwen raw run üstünde `/tmp/medfailbench_ci_scored_demo.json` üretti: 5 scored item.
- Dis gonderim: Yok. GitHub Actions gerçek run ve provider secret kontrolü henüz canlı GitHub üstünden yapılmadı.

### ÖNCEKİ ITERASYON
- Tarih/saat: 2026-07-08 11:01 TRT — Codex (user-approved cleanup: items 1, 2, 5, 6, 7)
- Yapilanlar:
  - Inspect Evals PR #1897 `ready for review` yapildi. Canli durum: OPEN, not draft, MERGEABLE, review required. Tania'nin onceki approval'i draft oldugu icin dismissed kaldi; yeni review bekleniyor.
  - Future-date kaymasi yeni dosyalarda 2026-07-08'e cekildi; `docs/CORE_TRACK_AUTOMATION_DATA_PIPELINE_20260708.md`, `docs/SECONDARY_LENS_AUTOMATION_DATA_20260708.md`, `docs/SECONDARY_LENS_DISTRIBUTION_VISIBILITY_20260708.md`.
  - Model team outreach queue guncellendi: `docs/MODEL_TEAM_FEEDBACK_OUTREACH.md`. Qwen, GLM, DeepSeek, Kimi icin hedef sirasi, evidence anchor, subject line ve pre-send gate netlestirildi. Dis gonderim yapilmadi.
  - Hard30 raw output'lari yeni API cagrisi olmadan local rule scorer ile skorlandi. Yeni dosyalar: `model_runs/batch_expansion_20260707/deepseek_deepseek_v4_pro_hard30_rule_scores.json` ve `model_runs/batch_expansion_20260707/qwen_qwen3_max_hard30_rule_scores.json`.
  - Hard30 kapanis notu eklendi: `docs/HARD30_RULE_SCORING_20260708.md`. DeepSeek V4 Pro hard30: 30/30 rows, 1 unsafe local label (H027). Qwen 3.7 Max hard30: 30/30 rows, 3 unsafe local labels (H018, H019, H027). Public claim update yok.
  - Distribution visibility packet eklendi: `docs/DISTRIBUTION_VISIBILITY_SPRINT_20260708.md`; checklist statuslari packet-ready olarak guncellendi. Dis form/PR/email/comment gonderilmedi.
- Dogrulama:
  - PR #1897 GitHub readback: `isDraft=false`, `mergeable=MERGEABLE`, `reviewDecision=REVIEW_REQUIRED`.
  - Hard30 raw row check: DeepSeek 30/30 empty 0; Qwen 30/30 empty 0.
- Dis gonderim: Yok. PR #1897 draft state degistirildi; model-team outreach, aggregator/list submissions ve awesome-list PR'lari gonderilmedi.

### ÖNCEKİ ITERASYON
- Tarih/saat: 2026-07-08 19:00 TRT — C0R3 (deep growth: distribution/visibility lens)
- Yapilanlar:
  - **Model Registry:** `config/models.yaml` oluşturuldu — 10 model tanımı, scheduled cadence, provider/active/tier alanları. Batı modelleri (GPT-4o, Claude, Gemini) P1 olarak yorum satırında bekliyor.
  - **Eval CI Pipeline Phase 1 Plan:** `leaderboard/EVAL_PIPELINE_PHASE_1.md` yazıldı — 3-job workflow tasarımı (resolve-models → eval → commit). Script iskeletleri (`ci_eval_runner.py`, `ci_score_runner.py`) belirtildi. G onayı bekliyor.
  - **Distribution Visibility Checklist:** `docs/DISTRIBUTION_VISIBILITY_CHECKLIST.md` — 9 benchmark aggregator/directory hedef belirlendi. Mevcut durum: 0/9 listed. En yüksek öncelik: AISafetyBenchExplorer, PapersWithCode.
  - **Secondary Lens Report:** `docs/SECONDARY_LENS_DISTRIBUTION_VISIBILITY_20260708.md` — 5 bulgu, 1 yeni proje fikri (MedAI Safety Benchmark Index).
- Dogrulama:
  - `config/models.yaml` YAML valid
  - Dosyalar fiziksel olarak klasörlerde mevcut
- Dis gonderim: Yok (G onayı bekler — eval pipeline implementasyonu, aggregator submission'ları)

### DAHA ÖNCEKİ ITERASYON
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
2. [PUBLIC-GITHUB / Pypi BLOCKED] **SafetyGuard publish:** GitHub Release `safetyguard-v0.1.0` public; wheel/sdist doğrulandı; PyPI API token/account yok.
3. [DONE] **LM Eval Harness Turkish Clinical PR:** PR #3903 açık, mergeable, Issue #3866 kapanış referanslı.
4. [DONE] **International AI Safety Report 2026 citation outreach:** mail gönderildi ve Sent doğrulandı.
5. [P0-YENI] **Distribution & Visibility:** **PACKET HAZIR** (`docs/DISTRIBUTION_VISIBILITY_SPRINT_20260708.md`, `docs/DISTRIBUTION_VISIBILITY_CHECKLIST.md`). Dis submit/PR/form icin final metin onayi gerekir.
6. [DONE] **Eval CI Pipeline Phase 1:** workflow YAML + runner scriptleri remote main'de; normal CI yesil; GitHub `workflow_dispatch` dry-run yesil. Gercek provider run icin secret ve harcama onayi gerekir.
7. [P0-YENI] **MedAI Safety Benchmark Index:** Yeni proje fikri — medical AI benchmark karşılaştırma indeksi (`docs/MEDAI_SAFETY_BENCHMARK_INDEX.md`). G onayı ile başlanabilir.
8. [P0-YENI] **Medical AI Safety Monitoring Bot:** **SPEC HAZIR** (`docs/SECONDARY_LENS_AUTOMATION_DATA_20260708.md`). G onayı ile build'e başla.
9. [P0-YENI] **Clinical AI Safety Audit Framework:** **OUTLINE HAZIR** (`docs/CLINICAL_AI_SAFETY_AUDIT_FRAMEWORK_OUTLINE.md`). Go/stop kararı bekliyor.
10. [P1] Batı modelleri batch expansion (GPT-4o, Claude, Gemini) — OpenRouter kredi gerektirir.
11. [DONE-LOCAL] Hard30 local rule scoring tamamlandi — score dosyalari yazildi; public claim update icin manual review gerekir.
12. [PACKET-READY] Model-team outreach approval packet (Qwen, DeepSeek, GLM, Kimi) — gonderim yapilmadi, exact target/channel onayi gerekir.
13. [P2] Doğruöz (LLM-as-Judge multilingual) işbirliği approval packet.
14. [P2] Diagens DoctorBench competitor monitoring — yeni Çin tıbbi AI eval platformu.

NOT: Eski P0 (MedHELM native benchmark) iptal — HELM maintenance modunda. Yerine LM Eval Harness + Inspect Evals dual track.

### ESKALASYON / BLOCKER
- Dış gönderim/onay: mail, sosyal post, GitHub dış issue/comment, model ekibi outreach → G onayı olmadan yapılmaz.
- arXiv: endorsement bekliyor; tanıdık yoksa DOI/GitHub release zaten cite edilebilir.
- Model-team outreach: bugün gönderilmedi; önce hedef, kanal ve exact metin seçilmeli.
