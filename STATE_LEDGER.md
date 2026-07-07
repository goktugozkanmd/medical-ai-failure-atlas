# STATE LEDGER — MedFailBench İnşa Döngüsü
## AKTİF FAZ: Faz 1 — Metodolojiyi Yayınlanabilir Yap | İlerleme: 4/5 kapı ölçütü hazır
## SON GÜNCELLEME: 2026-07-07 10:12 TRT (C0R3)

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
- Tarih/saat: 2026-07-07 10:12 TRT — C0R3
- Yapılanlar:
  - G onayıyla LinkedIn haftalık postu paylaşıldı; profil activity sayfasında metin doğrulandı.
  - G onayıyla X kısa postu paylaşıldı; canlı URL doğrulandı: `https://x.com/goktugozkanmd/status/2074389474453209459`.
  - G onayıyla MedHELM Discussion #27 follow-up yorumu gönderildi; canlı URL doğrulandı: `https://github.com/PacificAI/medhelm/discussions/27#discussioncomment-17556891`.
  - G onayıyla Inspect Evals typo-fix draft PR açıldı: `https://github.com/UKGovernmentBEIS/inspect_evals/pull/1897`.
  - X posting script account guard düzeltildi: side account-switcher text boşsa profile link fallback kullanıyor.
- Doğrulama:
  - LinkedIn dry-run: hesap `Göktuğ Özkan`, post editor ve `Gönderi` butonu hazır; canlı paylaşım sonrası profil read-back `found=true`.
  - X dry-run: aktif hesap `@goktugozkanmd`, metin 273 karakter; canlı paylaşım sonrası profile read-back `found=true`.
  - MedHELM: Discussion #27 canlı okundu, yorum sayısı 2'ye çıktı, son yorum `goktugozkanmd`, body içinde `live bilingual example` ve `GLM-5.2` doğrulandı.
  - Inspect Evals: branch `goktug/docs-typo-cleanup` fork'a pushlandı; draft PR #1897 açık, author `goktugozkanmd`, base `main`, head `goktugozkanmd:goktug/docs-typo-cleanup`.
- Dış gönderim:
  - LinkedIn, X, MedHELM comment ve Inspect Evals draft PR tamamlandı.
  - Model-team outreach yapılmadı; ayrı onay/ayrı hazırlık gerektirir.
- Commit:
  - MedFailBench repo içinde bu güncelleme henüz commitlenmedi.

### SIRADAKİ EN İYİ ADAYLAR (öncelik sırası)
1. [P1] 300-500 vaka / 10-20 model cevap hedefi için sıradaki veri/model batch planını başlat.
2. [P1] Model-team outreach için tek hedefli, kaynak-destekli kısa approval packet hazırla; G onayı olmadan mail/comment yok.
3. [P1] arXiv endorsement blocker'ı için pratik çözüm ara; submit mümkün olmadan “submit edildi” deme.
4. [P1] Inspect Evals PR #1897 durumunu takip et; maintainer yorumuna göre cevap taslağı hazırla.

### ESKALASYON / BLOCKER
- Dış gönderim/onay: mail, sosyal post, GitHub dış issue/comment, model ekibi outreach → G onayı olmadan yapılmaz.
- arXiv: endorsement bekliyor; tanıdık yoksa DOI/GitHub release zaten cite edilebilir.
- Model-team outreach: bugün gönderilmedi; önce hedef, kanal ve exact metin seçilmeli.
