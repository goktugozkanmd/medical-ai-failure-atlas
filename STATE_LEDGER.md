# STATE LEDGER — MedFailBench İnşa Döngüsü
## AKTİF FAZ: Faz 0 — Temel Sağlamlaştırma | İlerleme: 1/5 kapı ölçütü karşılandı
## SON GÜNCELLEME: 2026-07-04 12:04 TRT (C0R3)

> Bu dosya Codex'in her iterasyonda güncellediği canlı durum defteridir.
> Ana şartname: CODEX_3YEAR_BUILD_LOOP.md (değişmez, önce o okunur).

---

### FAZ KAPISI DURUMU (Faz 0)
- [x] Kanonik SPEC_TAXONOMY_SEVERITY.md (taksonomi + severity rubriği, versiyonlu) → docs/SPEC_TAXONOMY_SEVERITY.md v0.3.0
- [ ] Zenodo DOI kurulumu hazır (GitHub-Zenodo login blocker → ONAY BEKLEYEN)
- [x] CI yeşil: pytest + validate-public + secret-scan + YAML, otomatik → 63 passed, 2026-07-04
- [x] STATE_LEDGER.md canlı ve protokole bağlı ← bu dosya kuruldu, işletim Codex'te
- [ ] Panel davet paketi hazır (davet metni + değerlendirici kılavuzu + kappa şablonu) → ONAY BEKLEYEN

### SON İTERASYON
- Tarih/saat: 2026-07-04 12:04 TRT — C0R3
- Yapılanlar:
  - SPEC_TAXONOMY_SEVERITY.md v0.3.0 oluşturuldu (121 satır, WHO-harm hizalı, birleşik taxonomy+severity+gates)
  - rubric/v0.3.0/README.md oluşturuldu
  - DeepSeek-v4-flash GERÇEK API eval tamamlandı: 5/5 prompt, hepsi "clinically usable with caution", mean=2.6-3.2
  - DeepSeek-v4-pro eval background'da başlatıldı
- Doğrulama: CI 63 passed, SPEC dosyası yazıldı, eval report model_runs/weekly_eval_deepseek-v4-flash_20260704_120225.json
- Commit: beklemede (deepseek-v4-pro eval sonucu ile birlikte commit edilecek)
- ONAY BEKLEYEN dış aksiyonlar: yok

### SIRADAKİ EN İYİ ADAYLAR (öncelik sırası)
1. [P0] SPEC_TAXONOMY_SEVERITY.md yaz — mevcut 20-eksen taksonomi + 1-5 severity ölçeği (WHO harm kategorileriyle hizalı) + derecelendirme talimatı. Dedup: repoda mevcut taksonomi/rubrik dosyalarını ÖNCE tara, üstüne kur, tekrarlama.
2. [P0] CI durumunu kontrol et; pytest/validate-public/secret-scan yeşil mi? Değilse düzelt.
3. [P1] Panel davet paketi taslağı (davet e-postası + 1 sayfa değerlendirici kılavuzu + scripts/interrater_kappa.py + CSV/form şablonu). Not: davet gönderimi ONAY BEKLEYEN.

### BİRİKMİŞ KUYRUK
Bkz. CODEX_3YEAR_BUILD_LOOP.md Bölüm 6 — Faz 0 kuyruğu. İlk iterasyonda buraya kopyala ve dedup et.

### ESKALASYON / BLOCKER
- Zenodo DOI: GitHub-Zenodo login Göktuğ'un web oturumunu gerektiriyor (Faz 0 kapı ölçütü). Hazırlığı yap (.zenodo.json, CITATION.cff), login adımını ONAY BEKLEYEN bırak.
