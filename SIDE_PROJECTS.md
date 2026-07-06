# MedFailBench — Side Projects

> Ana projeyi besleyen, bağımsız çalışabilen, somut çıktı üreten 4 yan proje planı.
> İlkeler: Pragmatik · Ana projeye ölçülebilir katkı · Düşük bakım yükü
>
> Sahibi: G · Hazırlayan: Mercury · 2026-07-06

---

## İçindekiler

1. [Proje 1: SafetyGuard CLI](#proje-1-safetyguard-cli)
2. [Proje 2: FailViz Dashboard](#proje-2-failviz-dashboard)
3. [Proje 3: Safety Drift Tracker](#proje-3-safety-drift-tracker)
4. [Proje 4: Clinician Review Console](#proje-4-clinician-review-console)
5. [Özet Matrisi](#özet-matrisi)

---

## Proje 1: SafetyGuard CLI

### Açıklama

Komut satırı aracı: Herhangi bir OpenAI-compatible endpoint'e MedFailBench prompt set'ini gönderir, rule-based scorer ile değerlendirir, worst-case safety raporu üretir. Tek komutla bir modelin medical safety'sini test et.

```bash
safetyguard eval --model qwen-3.7-max --endpoint https://api.example.com/v1 --output report.json
```

### Amacı (Ana Projeye Katkı)

- **Düşük sürtünme adaptasyon:** Model ekipleri (Qwen, DeepSeek, GLM, Kimi) repoyu klonlamak yerine `pip install safetyguard` ile kendi modellerini saniyeler içinde test edebilir. Roadmap'teki "model ekiplerine cold outreach" görevi için kritik: mesajda "şu komutu çalıştırın, sonucu görün" denilebilir.
- **Tekrarlanabilirlik:** Benchmark'ı dışarıdan çalıştırılabilir kılan bir paket, alıntılanabilirlik ve güvenilirlik artırır.
- **CI pipeline'ı besler:** Mevcut weekly CI eval, bu CLI'nın bir wrapper'ı haline gelebilir. Kod tekrarı azalır.

### Teknik Gereksinimler

| Bileşen | Detay |
|---------|-------|
| Dil | Python 3.10+ |
| Paketleme | `pyproject.toml`, PyPI publish |
| Bağımlılıklar | `httpx` (API çağrıları), `typer` (CLI), `rich` (terminal output), `pydantic` (veri modelleri) |
| Prompt set | Mevcut `data/` klasöründen paket içine gömülü |
| Scorer | Mevcut rule-based scorer (`scripts/` altından refaktör edilerek çekilir) |
| Çıktı | JSON + human-readable terminal tablosu (`rich` ile) |
| Test | En az 10 unit test, mock API ile |
| Boyut | ~500 satır kod |

### Tahmini Süre

**3–4 gün** (scorer zaten var, sarmalamın çoğu mekanik)

### Öncelik

**Yüksek** — Roadmap'in 4. haftası (model ekiplerine outreach) için en kritik enabler. Outreach mesajında "pip install safetyguard && safetyguard eval" linki verilebilir.

### Başarı Kriterleri

- [ ] PyPI'da `safetyguard` paketi yayınlandı
- [ ] En az 1 model ekibi tool'u indirip çalıştırdı (GitHub star veya issue ile doğrulanır)
- [ ] CLI, mevcut 10 model sonuçlarından en az 8'ini reproduc ediyor (skor uyumu >%95)
- [ ] README'de 60 saniyelik quickstart var
- [ ] CI pipeline'ı bu CLI'ı kullanacak şekilde migrate edildi (opsiyonel, v2)

---

## Proje 2: FailViz Dashboard

### Açıklama

Statik, GitHub Pages'de host edilebilen interaktif görselleştirme sayfası. Model sonuçlarını failure mode bazında filtreleyebilen, worst-case güvenlik görünümünü tek bakışta gösteren, paylaşılabilir link üreten bir dashboard.

```
https://goktugozkanmd.github.io/medfailbench-failviz/
```

### Amacı (Ana Projeye Katkı)

- **Sosyal medda amplifikasyon:** Roadmap'in 4. haftasında planlanan LinkedIn carousel ve X thread'leri için interaktif link. "Ortalama sizi kandırır" mesajını görsel olarak anlatan tek sayfa.
- **HuggingFace Space'i tamamlar:** HF Space canlı bir app, FailViz ise statik, hızlı, herkesin erişebileceği bir özet. Space'a girmeden önce "neden bu önemli?" sorusunu yanıtlar.
- **Alıntılanabilir görsel:** Akademik preprint ve blog post'larda kullanılabilir tek görsel referans.

### Teknik Gereksinimler

| Bileşen | Detay |
|---------|-------|
| Framework | Vanilla HTML/CSS/JS veya SvelteKit (statik build) |
| Görselleştirme | D3.js veya Observable Plot |
| Veri kaynağı | `model_runs/` altındaki JSON'lar (statik olarak gömülür) |
| Hosting | GitHub Pages (sıfır maliyet) |
| Build | `npm run build` → `dist/` klasörü Pages'e push |
| Responsive | Mobil uyumlu (LinkedIn/X'den gelen trafiğin çoğu mobil) |
| Boyut | ~800 satır (HTML + JS + CSS) |

**Özellikler:**
1. **Worst-case heatmap:** Model × Safety gate matrisi, unsafe tier kırmızı
2. **Family filter:** "Çin modelleri sadece" / "ABD modelleri sadece" toggle
3. **Failure mode drill-down:** Bir failure mode'a tıkla → hangi modeller, hangi prompt'larda fail etmiş
4. **Shareable link:** Filtre durumu URL'e encode edilir (`?models=chinese&gate=escalation`)

### Tahmini Süre

**5–6 gün** (veri hazırlama 1 gün, görselleştirme 3 gün, polish + deploy 1–2 gün)

### Öncelik

**Yüksek** — Sosyal medya amplifikasyonu için kritik. Roadmap'in 2. ve 4. haftasında kullanılacak.

### Başarı Kriterleri

- [ ] GitHub Pages'de canlı
- [ ] En az 3 interaktif görselleştirme (heatmap, drill-down, family filter)
- [ ] Mobil ekranda düzgün render
- [ ] README'de ve sosyal medya post'larında link verilmiş
- [ ] HF Space'e "interactive summary" link olarak eklenmiş
- [ ] En az 100 unique visitor (ilk hafta)

---

## Proje 3: Safety Drift Tracker

### Açıklama

Zaman içinde model güvenlik skorlarını takip eden otomatik sistem. Bir model güncellendiğinde (örneğin Qwen 3.7 → 3.8), aynı prompt set'le yeni skor alır, önceki sürümle karşılaştırır, regresyon/iyileşme tespit eder.

```
[2026-07-06] Qwen 3.7 Max  → safety: 45.3, unsafe_rate: 46.7%
[2026-09-15] Qwen 3.8      → safety: 48.1, unsafe_rate: 33.3%  ▲ +2.8  ▼ -13.4%
```

### Amacı (Ana Projeye Katkı)

- **Sürekli değer teklifi:** Tek seferlik bir benchmark değil, "model ekipleri güncelleme yaptıkça biz tekrar ölçüyoruz" = sürekli alıntılanabilir içerik.
- **Model ekipleri için actionable feedback:** "3.7'den 3.8'e geçtiğinizde safety %13.4 iyileşti" — bu, model ekiplerinin MedFailBench'i internal QA sürecine dahil etmesi için en güçlü argüman.
- **Akademik novelty:** "Medical AI safety drift across model versions" — mevcut hiçbir benchmark bunu takip etmiyor. arXiv preprint'inin ikinci versiyonu için yeni bir section.

### Teknik Gereksinimler

| Bileşen | Detay |
|---------|-------|
| Dil | Python 3.10+ |
| Veri saklama | SQLite (tek dosya, basit, versionable) |
| Scheduler | GitHub Actions cron (haftalık) |
| Diff engine | İki sürüm arası skor farkı, anlamlılık testi (McNemar) |
| Çıktı | Markdown tablo + JSON + opsiyonel grafik (matplotlib) |
| Uyarı | Skor belirli bir eşiğin altına düşerse GitHub Issue otomatik aç |
| Bağımlılık | Proje 1 (SafetyGuard CLI) ile entegre çalışır |

**Mimari:**
```
[GitHub Actions cron] → [SafetyGuard CLI eval] → [SQLite snapshot]
                                                    ↓
                                          [Diff engine] → [Markdown report]
                                                    ↓
                                          [GitHub Issue alert (opsiyonel)]
```

### Tahmini Süre

**4–5 gün** (1 gün DB schema + diff engine, 2 gün GitHub Actions + snapshot logic, 1–2 gün raporlama + alert)

### Öncelik

**Orta** — Mevcut 30 günlük roadmap'ten sonra (Ay 2–3) başlanmalı. Model ekipleri yanıtladıktan sonra "sürüm takibi" teklifi daha güçlü olur.

### Başarı Kriterleri

- [ ] En az 3 model için 2'şer snapshot alınmış (6+ hafta veri)
- [ ] Diff raporu otomatik üretiliyor (Markdown + JSON)
- [ ] En az 1 modelde regresyon veya iyileşme tespit edildi ve dokümante edildi
- [ ] GitHub Actions haftalık çalışıyor (son 4 hafta kesintisiz)
- [ ] Skor düştüğünde otomatik Issue açma çalışıyor (test edilmiş)
- [ ] Drift raporu arXiv preprint'inin v2'sine section olarak eklendi

---

## Proje 4: Clinician Review Console

### Açıklama

Klinisyen paneli için hafif web arayüzü. Model çıktılarını görüntüle, 1–5 severity puanla, safety gate işaretle, yorum yaz. Mevcut manuel Markdown form doldurma sürecini dijitalleştirir.

```
[Prompt #047] [Qwen 3.7 Max output]
─────────────────────────────────────
Safety score: [1] [2] [3] [4] [5]
Gates: ☐ Missing variable  ☑ Unsafe escalation  ☐ Weak source
Comment: "Model red flag semptomunu atladı, acil başvuru önermedi."
─────────────────────────────────────
[Next case →]
```

### Amacı (Ana Projeye Katkı)

- **Panel pilot'u hızlandırır:** Roadmap'te "24 vaka hazır, hekim puanlaması bekleniyor" yazıyor. Manuel form doldurma sürtünmesi, panelin gecikmesinin ana nedeni olabilir. Bu tool sürtünmeyi azaltır.
- **Inter-rater agreement:** İki review'ın otomatik karşılaştırması (Cohen's kappa) tool içinde hesaplanır. Bu, akademik preprint için kritik bir metrik.
- **Kalite kontrol:** Rule-based scorer ile klinisyen puanı arasındaki uyumsuzlukları gösterir. Bu, scorer'ın validasyonu için gerekli.

### Teknik Gereksinimler

| Bileşen | Detay |
|---------|-------|
| Backend | Python + FastAPI (tek dosya, ~200 satır) |
| Frontend | HTML + Alpine.js (framework'suz, hafif) |
| Veri saklama | SQLite (review'lar, reviewer'lar, agreement) |
| Auth | Basit token-based (reviewer başına unique link) |
| İstatistik | `scipy.stats` (Cohen's kappa, Fleiss' kappa) |
| Export | JSON + CSV export (preprint için ham veri) |
| Deploy | HuggingFace Space (gradio yerine FastAPI) veya fly.io |
| Boyut | ~600 satır (backend + frontend) |

**Özellikler:**
1. Reviewer'a özel link (`/review/<token>`) — login yok, direkt erişim
2. Her case'de: prompt, model çıktısı, rule-based skor (ön bilgide), rating alanı
3. İkinci reviewer ile karşılaştırma görünümü (kapatılabilir — blind review için)
4. Progress bar: "47/136 case tamamlandı"
5. Export: tek tıkla JSON/CSV (preprint verisi)

### Tahmini Süre

**4–5 gün** (1 gün backend + DB, 2 gün frontend, 1 gün agreement stats + export, 1 gün test + deploy)

### Öncelik

**Orta** — Panel pilot'u hala manuel olarak ilerliyorsa, bu tool onu hızlandırır. Ama panel zaten tamamlandıysa, v0.3.0+ için "scaling panel" aracı olarak kullanılır.

### Başarı Kriterleri

- [ ] 2–4 reviewer için çalışan unique link sistemi
- [ ] En az 10 vaka üzerinden uçtan uca test edildi
- [ ] Cohen's kappa otomatik hesaplanıyor ve gösteriliyor
- [ ] JSON/CSV export çalışıyor
- [ ] Mevcut 24 vakanın en az %70'i bu tool üzerinden puanlandı
- [ ] Rule-based scorer ile klinisyen puanı arasındaki agreement raporu üretildi

---

## Özet Matrisi

| Proje | Süre | Öncelik | Ana Katkı | Bağımlılık |
|-------|------|---------|-----------|------------|
| **SafetyGuard CLI** | 3–4 gün | 🔴 Yüksek | Model ekiplerine outreach enabler'ı | Yok (bağımsız başlar) |
| **FailViz Dashboard** | 5–6 gün | 🔴 Yüksek | Sosyal amplifikasyon + görsel alıntılanabilirlik | Yok (veri zaten mevcut) |
| **Safety Drift Tracker** | 4–5 gün | 🟡 Orta | Sürekli değer + akademik novelty (sürüm takibi) | Proje 1 (CLI) önerilir |
| **Clinician Review Console** | 4–5 gün | 🟡 Orta | Panel pilot hızlandırma + inter-rater stats | Panel pilot aktif olmalı |

### Önerilen Sıra

```
Hafta 1–2:  SafetyGuard CLI          ← Outreach için kritik path
Hafta 2–3:  FailViz Dashboard         ← Sosyal amplifikasyon için paralel yürür
Ay 2:       Safety Drift Tracker      ← Model yanıtları geldikten sonra
Ay 2–3:     Clinician Review Console  ← Panel scaling ihtiyacına göre
```

### Toplam Tahmini Efor

~17–20 gün kişisel çalışma süresi. Paralel yürütülürse (CLI + FailViz aynı anda), calendar süresi ~10–12 güne sıkışabilir.

---

> Bu plan canlı bir dokümandır. Proje ilerledikçe güncellenir.
> Sahibi: G · Hazırlayan: Mercury · 2026-07-06
