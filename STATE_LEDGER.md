# STATE LEDGER — MedFailBench İnşa Döngüsü
## AKTİF FAZ: Faz 1 — Metodolojiyi Yayınlanabilir Yap | İlerleme: 5/5 kapı ölçütü hazır ✅
| SON GUNCELLEME: 2026-07-07 16:47 TRT (C0R3 — EU AI Act whitepaper + README compliance link)

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
- Tarih/saat: 2026-07-07 16:47 TRT — C0R3 (EU AI Act whitepaper + README compliance link)
- Yapilanlar:
  - `docs/BENCHMARKING_CLINICAL_AI_SAFETY_FOR_EU_AI_ACT_CONFORMITY.md` public whitepaper v0.1 olarak hazirlandi.
  - `docs/BENCHMARKING_CLINICAL_AI_SAFETY_FOR_EU_AI_ACT_CONFORMITY_AUDIT_20260707.md` referans ve claim-support audit olarak eklendi.
  - `README.md` icine COMPLIANCE.md, whitepaper ve audit linkleri eklendi.
  - `COMPLIANCE.md` resmi EU AI Act kaynaklariyla guclendirildi; high-risk wording daha konservatif hale getirildi.
- Dogrulama:
  - Internal link + row-count check: PASS; scenario 150, prompt 70, leaderboard 10, worst-case row 11.
  - Reference/source audit: PASS after scope limits; legal/regulatory/journal submit icin legal/target review gerekir.
  - `git diff --check` -> PASS.
  - `python3 -m pytest -q` -> 72 passed.
  - `make validate-public` -> PASS, warnings 0.
- GitHub push: docs commit `2f96e99`; raw README/COMPLIANCE/whitepaper/audit read-back 200 OK; CI run `28871313498` success.
- Dis gonderim: Yok; repo ici public dokuman guncellendi.

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
1. [P0] MedHELM native benchmark'i gerçek dosyalara çevir (prompt template + CSV dataset + YAML config). Mevcut bridge spec'i çalıştırılabilir benchmark'a dönüştür.
2. [P1] Faz-1 TAMAM — arXiv preprint gönderimi için endorsement sorununu çöz (G manuel işlem).
3. [P1] Model-team outreach için hedefli approval packet hazırla; G onayı olmadan mail yok.
4. [P1] Batch expansion: 10-20 modele çıkmak için yeni eval batch planını uygulamaya koy.
5. [P2] Doğruöz (LLM-as-Judge multilingual) ekibine işbirliği approval packet.

### ESKALASYON / BLOCKER
- Dış gönderim/onay: mail, sosyal post, GitHub dış issue/comment, model ekibi outreach → G onayı olmadan yapılmaz.
- arXiv: endorsement bekliyor; tanıdık yoksa DOI/GitHub release zaten cite edilebilir.
- Model-team outreach: bugün gönderilmedi; önce hedef, kanal ve exact metin seçilmeli.
