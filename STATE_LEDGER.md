# STATE LEDGER — MedFailBench İnşa Döngüsü
## AKTİF FAZ: Faz 0 — Temel Sağlamlaştırma | İlerleme: 1/5 kapı ölçütü karşılandı
## SON GÜNCELLEME: 2026-07-04 14:25 TRT (C0R3)

> Bu dosya Codex'in her iterasyonda güncellediği canlı durum defteridir.
> Ana şartname: CODEX_3YEAR_BUILD_LOOP.md (değişmez, önce o okunur).

---

### FAZ KAPISI DURUMU (Faz 0)
- [x] Kanonik SPEC_TAXONOMY_SEVERITY.md (taksonomi + severity rubriği, versiyonlu) → docs/SPEC_TAXONOMY_SEVERITY.md v0.3.0
- [ ] Zenodo DOI kurulumu hazır (GitHub-Zenodo login blocker → ONAY BEKLEYEN)
- [x] CI yeşil: pytest + validate-public + secret-scan + YAML, otomatik → 63 passed, 2026-07-04
- [x] STATE_LEDGER.md canlı ve protokole bağlı ← bu dosya
- [ ] Panel davet paketi hazır (davet metni + değerlendirici kılavuzu + kappa şablonu) → ONAY BEKLEYEN

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
