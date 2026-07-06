# STATE LEDGER — MedFailBench İnşa Döngüsü
## AKTİF FAZ: Faz 1 — Metodolojiyi Yayınlanabilir Yap | İlerleme: 4/5 kapı ölçütü hazır
## SON GÜNCELLEME: 2026-07-06 18:29 TRT (C0R3)

> Bu dosya Codex/C0R3 iterasyonlarında güncel durum defteridir.
> Ana şartname: CODEX_3YEAR_BUILD_LOOP.md.

---

### FAZ KAPISI DURUMU (Faz 1) — YAYINLANABİLİR METODOLOJİ
- [ ] ≥2 hekimli panel fiilen çalışıyor: ≥20 vaka en az 2 bağımsız hekimce derecelendirildi + kappa raporlandı. → Şu an single-physician / clinician-authored metodoloji; dış klinisyen panel validasyonu bekliyor.
- [x] Türkçe vaka seti v1 / TR-EN safety drift preview materyali hazır. → Aktif dashboard: 241 tracked rows; validation tier ayrımı korunacak.
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
- Tarih/saat: 2026-07-06 18:29 TRT — C0R3
- Yapılanlar:
  - GLM/Mercury'nin ürettiği draftlar silinmeden temizlendi ve public-risk hataları düzeltildi.
  - `clinician-reviewed` gibi riskli ifadeler current public dosyalarda `clinician-authored` / reviewer-pending çizgisine çekildi.
  - 10-model public leaderboard ile 11-row historical worst-case JSON ayrımı README'de netleştirildi.
  - `docs/HARD_FINDINGS_V0_2_1.md` oluşturuldu.
  - `docs/CHINESE_FRONTIER_SAFETY_REPORT.md` oluşturuldu.
  - `docs/MODEL_TEAM_FEEDBACK_OUTREACH.md` oluşturuldu.
  - Model failure cards ve model-team feedback draftları tutuldu, ama dış gönderim onay bekler.
- Doğrulama:
  - `python3 -m pytest -q` → 63 passed.
  - `make validate-public` → PASS, warnings 0.
  - `git diff --cached --check` → temiz.
  - staged secret/dangerous-code scan → temiz.
- Commit: bu değişiklik seti final review sonrası commit/push edilecek.

### SIRADAKİ EN İYİ ADAYLAR (öncelik sırası)
1. [P0] Final independent review sonucu PASS ise commit + push.
2. [P0] GitHub'da README linkleri ve yeni docs dosyaları canlı doğrula.
3. [P0] Dış post/outreach yok: Qwen/DeepSeek/GLM/Kimi taslakları G onayı bekler.
4. [P1] MedHELM postuna gerçek paired TR/EN model output örneği eklemeden dışarı atma.
5. [P1] TR/EN paired drift promptlarını gerçek model çıktısıyla koştur, preprint'e güvenli subsection ekle.
6. [P1] Inspect Evals upstream review durumunu canlı kontrol et.

### ESKALASYON / BLOCKER
- Dış gönderim/onay: mail, sosyal post, GitHub dış issue/comment, model ekibi outreach → G onayı olmadan yapılmaz.
- arXiv: endorsement bekliyor; tanıdık yoksa DOI/GitHub release zaten cite edilebilir.
- MedHELM draft: gerçek paired model-output örneği eklenmeden public discussion'a taşınmaz.
