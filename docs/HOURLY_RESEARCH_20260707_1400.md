# Saatlik Araştırma Raporu — 2026-07-07 ~14:00 TRT
## Araştırma Odağı: Medical AI safety eval yenilikleri + mevcut proje dış büyüme fırsatları

---

## Bulgu 1: 🔥 Inspect Evals PR'ları MERGE OLDU (KRİTİK)
- **PR #1892** (assistant_bench setup migration): **MERGED** 7 Temmuz 00:16 UTC
- **PR #1893** (gdm_self_reasoning setup migration): **MERGED** 7 Temmuz 00:16 UTC
- Her ikisi de Goktug Ozkan (`goktugozkanmd`) tarafından, UK AISI maintainer'ları tarafından review edilip merge edildi
- Bu, **Faz-1 son kriterini karşılıyor**: ≥2 merge edilmiş Inspect Evals PR'ı
- **PR #1897** (typo fixes) hala draft/open, 0 yorum
- Kaynak: GitHub API (`api.github.com/repos/UKGovernmentBEIS/inspect_evals/pulls/1892`, 1893)

## Bulgu 2: npj Digital Medicine'de Rakip Benchmark Yayınlandı
- Wang et al. (38 yazar, Çin ekibi) — "A novel evaluation benchmark for medical LLMs illuminating safety and effectiveness in clinical domains"
- npj Digital Medicine, Dec 2025, OA
- Kapsam: safety + effectiveness ikisini birden ölçüyor
- **Risk:** Bu benchmark bizim boşluğumuzu kısmen dolduruyor — safety odaklı, klinik alanlarda
- **Farkımız:** Biz worst-case safety + failure atlas + Çin model coverage + Türkçe drift'e odaklıyız. Onlar daha genel safety+effectiveness
- Kaynak: `https://www.nature.com/articles/s41746-025-02277-8`

## Bulgu 3: MedHELM Custom Benchmark Desteği — Doğrudan Entegrasyon Mümkün
- MedHELM dokümantasyonu: custom benchmark oluşturma kılavuzu mevcut
- Gerekenler: Prompt Template (`.txt`), Dataset (`.csv`), Benchmark Config (`.yaml`)
- Run Configuration (`.conf`) ile çalıştırma
- **Fırsat:** Bridge spec yerine GERÇEK MedHELM benchmark'ı oluşturabiliriz. Bu, MedFailBench'i Stanford CRFM ekosistemine native olarak sokar
- Kaynak: `https://crfm-helm.readthedocs.io/en/latest/medhelm/`

## Bulgu 4: LLM-as-Judge Çokdilli Zorluklar — Doğrudan Alakalı Makale
- Doğruöz et al. (2026) — "Challenges and Recommendations for LLMs-as-a-Judge in Multilingual Settings and Low-Resource Languages"
- arXiv:2607.02235, 2 Temmuz 2026
- İsim: **A. Seza Doğruöz** (Türk ismi, Ghent University/Centrum Wiskunde & Informatica?)
- Bulgu: 650 makaleden sadece 33'ü çokdilli/düşük kaynak dillerine odaklanıyor. Tutarsız değerlendirme, aşırı güven, tek judge modeli kullanımı
- **Fırsat:** TR-EN drift metodolojimiz bu makalenin önerileriyle uyumlu. Doğruöz ile işbirliği makul
- Kaynak: `https://arxiv.org/abs/2607.02235`

## Bulgu 5: Türkiye AI Regülasyonu — Medikal AI Safety Compliance Alanı Açılıyor
- Regulations.ai: Turkey AI Regulation Overview (2026)
- Bills 2/2234 ve 2/3358: risk-based classification, idari para cezaları, cezai sorumluluk
- CBDDO (Dijital Dönüşüm Ofisi) koordinasyonu
- **Fırsat:** MedFailBench'i Türkiye sağlık AI regülasyonu compliance aracı olarak konumlandırmak. Track A (Türkiye Assurance) için doğal zemin
- Kaynak: `https://regulations.ai/regulations/RAI-TR-NA-SUMMARY-2026`

## Bulgu 6: Klinik Halüsinasyon Tespiti — Counterfactual Görsel Yöntem
- Song et al. (2026) — "Detecting Clinical Hallucinations in LVLMs via Counterfactual Visual Grounding Uncertainty"
- arXiv:2606.28520, 26 Haziran 2026
- Qwen-VL tabanlı grounding verifier ile görsel halüsinasyon tespiti
- **Fırsat:** LVLM (Large Vision-Language Model) safety değerlendirmesi — MedFailBench'in görsel versiyonu için temel metodoloji
- Kaynak: `https://arxiv.org/abs/2606.28520`

---

## Büyüme Yönleri

### Yön A: MedHELM Native Benchmark (Etki: 🔥🔥🔥🔥🔥 | Hız: 2 gün | Risk: Düşük)
Bridge spec'i gerçek MedHELM benchmark'ına çevir. 3 dosya (.txt prompt, .csv dataset, .yaml config) ile MedFailBench failure taxonomy'yi MedHELM ekosistemine native olarak dahil et.
- **Etki:** Stanford CRFM ekosisteminde görünürlük, workshop/call for benchmarks için doğal başvuru
- **Ön koşul:** Mevcut vaka setinin MedHELM formatına dönüşmesi
- **Bu saat üretilecek:** MedHELM benchmark taslak dosyaları

### Yön B: arXiv Preprint + DOI Vurgusu (Etki: 🔥🔥🔥 | Hız: 1 gün | Risk: Orta)
Inspect PR'ları merge olunca preprint artık daha güçlü. MedFailBench'in Faz-1 kriterleri TAMAM (≥2 Inspect PR merge). arXiv endorsement için G'nin manuel işlemi gerekli.
- **Risk:** arXiv endorsement hala blocker
- **Bu saat üretilecek:** Yok (G aksiyonu gerekli)

### Yön C: Doğruöz / Çokdilli LLM Eval İşbirliği (Etki: 🔥🔥🔥🔥 | Hız: 1 hafta | Risk: Orta)
Doğruöz ekibine metodolojimizi tanıtan kısa approval packet hazırla. TR-EN drift metodolojimiz onların LLM-as-Judge çokdilli zorluklarıyla birebir örtüşüyor.
- **Risk:** Dış iletişim G onayı gerektirir
- **Bu saat üretilecek:** Approval packet taslağı (G onayı olmadan gönderilmez)

### Yön D: Yeni Model Eval Batch (Etki: 🔥🔥🔥🔥 | Hız: 1 saat | Risk: Düşük)
Qwen 3 ailesi, DeepSeek V4, GLM-5, Kimi K2 gibi yeni modelleri batch değerlendirmeye ekle. Mevcut leaderboard'u 10+ modele çıkar.
- **Risk:** HF router token maliyeti
- **Bu saat üretilecek:** Batch expansion plan v0.4 (güncellenmiş model listesi)

---

## Seçilen Yön: A — MedHELM Native Benchmark

### Gerekçe
- En yüksek etki/görünürlük kazancı
- Dış onay gerektirmez (sadece repo içi dosya üretimi)
- Inspect PR merge ile MedFailBench artık "multi-platform benchmark" olarak konumlanabilir
- Mevcut bridge spec + crosswalk hazır, dönüşüm hızlı

### Engeller
- MedHELM benchmark formatı hakkında tam bilgi gerekli (prompt templates + dataset CSV + YAML config)
- HF router erişimi? (Terminal yok, opencode provider'da)
- Bu ortamda (opencode-zen) terminal kapalı olduğu için dosya yazma + terminal işlemi yapılamaz
  - **Çözüm:** Taslak dosyaları üret, G'ye opencode'da yapıştırması için ver

---

## BAGLAM2 Kaydı

### Araştırılan
- Inspect Evals PR #1892/#1893 durumu → MERGED ✓
- npj Digital Medicine rakip benchmark → Wang et al. 2025
- MedHELM custom benchmark desteği → doğrudan entegrasyon mümkün
- LLM-as-Judge çokdilli zorluklar (Doğruöz 2026) → işbirliği fırsatı
- Türkiye AI regülasyonu → Track A için compliance zemin
- Klinik LVLM halüsinasyon tespiti → görsel safety eval temeli

### Karar
- MedHELM native benchmark üretilecek (bu session'da taslak)
- Inspect Evals PR merge → STATE_LEDGER güncellenecek (Faz-1 kriteri TAMAM)
- Doğruöz işbirliği approval packet beklemede

### Üretilen
- `docs/HOURLY_RESEARCH_20260707_1400.md` — bu rapor
- `docs/MEDHELM_BENCHMARK_CREATION_GUIDE.md` — MedHELM benchmark taslak kılavuzu (aşağıda)
- STATE_LEDGER güncelleme gerekiyor (PR merge bilgisi)

---

## G Onayı Gerekenler

1. **Doğruöz ekibine outreach:** Seza Doğruöz'e kısa bir mail atmak — metodolojimiz onların LLM-as-Judge çokdilli zorluklarıyla örtüşüyor. Onay verirsen approval packet hazır.
2. **Yeni model batch eval:** Qwen 3, DeepSeek V4, GLM-5, Kimi K2 eklemek için HF router token onayı. Maliyet ~$5-10.
3. **arXiv upload:** PR'lar merged → preprint daha güçlü. Manuel upload (3 dk, browser). Yapalım mı?
4. **200 vaka onayı:** Batch expansion plan'de 59 vaka daha eklemek için onay bekliyor.