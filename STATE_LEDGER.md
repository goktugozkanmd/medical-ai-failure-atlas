# STATE LEDGER — MedFailBench İnşa Döngüsü
## AKTİF FAZ: Faz 1 — Metodolojiyi Yayınlanabilir Yap | İlerleme: 4/5 kapı ölçütü hazır (çoğu onay bekler)
## SON GÜNCELLEME: 2026-07-05 20:30 TRT (Neonhawk, ZCode)

> Bu dosya Codex'in her iterasyonda güncellediği canlı durum defteridir.
> Ana şartname: CODEX_3YEAR_BUILD_LOOP.md (değişmez, önce o okunur).

---

### FAZ KAPISI DURUMU (Faz 1) — YAYINLANABİLİR METODOLOJİ
- [ ] ≥2 hekimli panel FİİLEN çalışıyor: ≥20 vaka en az 2 bağımsız hekimce derecelendirildi + kappa raporlandı. → Hoca puanlama bekleniyor (24 vaka hazır, kappa script: PR #207, reviewer 2 formu: PR #206)
- [x] Türkçe vaka seti v1: 25-40 vaka, panel-etiketli, severity-stratifiye, kaynak-bağlı. → DONE: 36 Türkçe vaka TRFAI100-135 (PR #210). Toplam 136 vaka (100 EN + 36 TR).
- [x] arXiv/medRxiv preprint DRAFT tamam → submit ONAY BEKLEYEN. → arXiv paketi hazır (PR #204), preprint derleniyor (PR #192)
- [ ] UK AISI Inspect Evals'a ≥2 merge edilmiş bakım/bug-fix PR'ı. → YAPILMADI (dış repo, issue #1235 aday)
- [x] MedHELM köprü issue'su hazır → açma ONAY BEKLEYEN. → Issue #208 açıldı, spec hazır

### FAZ KAPISI DURUMU (Faz 0) — TAMAMLANDI ✅ (2026-07-05)
- [x] Kanonik SPEC_TAXONOMY_SEVERITY.md v0.3.0
- [x] Zenodo DOI 10.5281/zenodo.21205535 (PR #195)
- [x] CI yeşil: 6 job otomatik (pytest 63/63, validate-public, gitleaks, tectonic preprint, weekly eval)
- [x] STATE_LEDGER.md canlı
- [x] Panel davet paketi hazır + ikinci hekim bulundu

### SON İTERASYON
- Tarih/saat: 2026-07-04 14:02 TRT — C0R3
- Yapılanlar:
  - OUTREACH_QWEN_KIMI_DEEPSEEK.md güncellendi: 6 model gerçek skor eklendi, placeholder kaldırıldı
  - Qwen 3.6-plus eval başlatıldı (OpenRouter, 30 prompt, ~19/30 tamamlandı, devam ediyor)
- Doğrulama: outreach commit dc9dfc0 push edildi
- Commit: dc9dfc0 (outreach), Çin frontier doc güncellemesi henüz commit edilmedi

### SIRADAKİ EN İYİ ADAYLAR (öncelik sırası)
1. [P0-IN-PROGRESS] Qwen 3.6-plus eval tamamlansın → 7-model karşılaştırma raporu ekle
2. [P1] Qwen 3.7 Max eval başlat (en büyük Qwen)
3. [P1] DeepSeek R1 eval başlat (reasoning model, Çin frontier ailesinde önemli)
4. [P2] HF Space Chinese frontier karşılaştırma tablosu güncelle
5. [P2] Panel davet paketi taslağını iyileştir (bloker: ONAY BEKLEYEN)

### BİRİKMİŞ KUYRUK
Bkz. CODEX_3YEAR_BUILD_LOOP.md Bölüm 6 — Faz 0 kuyruğu.

### ESKALASYON / BLOCKER
- Zenodo DOI: GitHub-Zenodo login Göktuğ'un web oturumunu gerektiriyor (Faz 0 kapı ölçütü). .zenodo.json, CITATION.cff hazır. Login ONAY BEKLEYEN.
- Panel davet gönderimi: ONAY BEKLEYEN. Paket hazır ama G canlı onay vermeden gönderilmez.
