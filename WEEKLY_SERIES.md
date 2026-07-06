# MedFailBench — 8 Week Content Series

> **Prensip:** Self-promotion değil, self-evident artefact. Her hafta bir bulgu öne çıkar. Veri konuşur.
> **Tonalite:** Klinisyen sükuneti. Suçlayıcı değil, sorgulayıcı. "Bunu kim yaptı?" dedirten içerik.
> **Başlangıç:** ROADMAP_30DAYS Hafta 1 ile senkron
> **Sahibi:** G · Hazırlayan: Mercury

---

## Serinin Genel Arc'ı

| Hafta | Tema | Duygu |
|-------|------|-------|
| 1 | Problem tanımı: Exam benchmark'ları neyi kaçırıyor? | Merak |
| 2 | "Ortalama yalan söyler": Worst-case safety | Şok |
| 3 | Çin frontier modelleri: Aile bazlı desenler | Analiz |
| 4 | Kaynaksız iddia: Source support sessiz failure mode | Endişe |
| 5 | Daha büyük ≠ daha güvenli: Scale ve safety | Paradoks |
| 6 | Ekosistem katkısı: MedHELM köprüsü | İşbirliği |
| 7 | Bilingual drift: Türkçe tıbbi AI güvenliği | Küresel |
| 8 | Yol önü: Klinik panel, preprint, açık çağrı | Vizyon |

> Seri bir hikaye gibi akar: **Sorun → Kanıt → Desen → Kök neden → Paradoks → Çözüm önerisi → Küresel bağ → Vizyon.**

---

## Hafta 1 — "Sınav Doğru Cevap Veriyor, Ama Hasta Güvende mi?"

### Ana Konu
Exam-style medical AI benchmark'ları klinik failure mode'ları kaçırıyor. Bir model doğru teşhis koyabilir ama güvenlik sınırında fail edebilir — ve bu, hasta için daha tehlikelidir.

### Alt Başlıklar
- Exam benchmark paradigması: "Doğru cevap = güvenli" varsayımı neden kırık?
- 5 safety gate taxonomy: urgent escalation, remote dosing, discharge reassurance, evidence overclaim, unsafe protocol detail
- Spesifik senaryo: Normal ilk troponin ile gelen göğüs ağrısı — model acil riski görünür tutuyor mu?
- Spesifik senaryo: Şiddetli ani baş ağrısı, normal muayene — model yanlış güvence veriyor mu?
- MedFailBench'in farkı: accuracy değil, failure mode sınıflandırması

### Platformlar
- **X:** 7 tweet'lik mega-thread (her safety gate için 1 tweet + intro/outro)
- **LinkedIn:** Long-form post (600–800 kelime)
- **Blog:** "Why Exam-Style Medical Benchmarks Miss Clinical Failure Modes" (ilk blog post, serinin temel taşı)

### Hedef Kitle
AI/ML araştırmacıları, medical AI startup kurucuları, benchmark builders, health-tech investors

### İçerik Formatı
- X: Educational mega-thread (7 tweets, her biri bir safety gate örneği)
- LinkedIn: Long-form narrative post
- Blog: Foundational long-form essay (2,000+ kelime, alıntılanabilir)

### CTA
> "Pick one case, one safety gate, or one wording choice from the repo and tell me what's missing. Narrow objections only."

### Anahtar Kelimeler / Hashtag'ler
`#MedicalAI` `#AISafety` `#LLMBenchmark` `#PatientSafety` `#MedFailBench` `#HealthAI` `ClinicalSafety` `#HealthTech`

---

## Hafta 2 — "Ortalama Yalan Söyler: Worst-Case Safety Gerçeği"

### Ana Konu
Bir model ortalama 45–52 safety score alabilir ve yine de her 3 prompt'tan 1'inde "unsafe tier"a düşebilir. Ortalama, hasta zararını gizler. Worst-case konuş.

### Alt Başlıklar
- Veri: Qwen 3.7 Max — 30 promptun 14'ünde (%46.7) safety score 1–2/5
- Veri: GLM-5.2 — 28 promptun 11'inde (%39.3) unsafe tier
- Veri: Qwen 3.6 Plus — 30 promptun 11'inde (%36.7) unsafe tier
- Llama 3.1-8B: Unsafe tier'dan kaçınan tek model — ama yine de her prompt'ta "missed urgent escalation"
- "Tek bir unsafe yanıtın klinik sonucu vardır" — ortalama neden yetersiz bir metrik

### Platformlar
- **X:** 5 tweet'lik data thread (her tweet bir modelin worst-case'i)
- **LinkedIn:** Carousel / infographic (10 model worst-case unsafe rate bar chart)
- **Blog:** Yok (veri thread yeterli)

### Hedef Kitle
Model safety ekipleri, AI alignment araştırmacıları, regulatory/HTA profesyonelleri, clinical informatics community

### İçerik Formatı
- X: Data-driven thread (hard numbers, no opinion)
- LinkedIn: Visual carousel (shareable infographic — failure rate bar chart)

### CTA
> "Full worst-case breakdown with prompt IDs and raw outputs: [link to docs/HARD_FINDINGS_V0_2_1.md]. Verify it yourself."

### Anahtar Kelimeler / Hashtag'ler
`#ModelSafety` `#WorstCase` `#AIBenchmark` `#PatientSafety` `#LLMEval` `#MedFailBench` `#AIFailure` `UnsafeAI`

---

## Hafta 3 — "Çin Frontier Modelleri: Aile Bazlı Safety Desenleri"

### Ana Konu
10 modelden 8'i Çin kökenli. Family bazında (Qwen, DeepSeek, GLM, Kimi) safety desenleri belirgin. "Çin modelleri kötü" değil — "bu modellerin bu benchmark'da bu pattern'leri var."

### Alt Başlıklar
- Qwen ailesi: 2.5-7B (en güvenli, 52.0) → 3.7 Max (en az güvenli, 45.3) — scale arttıkça safety düşüyor
- DeepSeek ailesi: Üç model de source support'ta 48.0 — "bilmiyor" değil "desteksiz iddia ediyor"
- GLM-5.2: %39.3 unsafe rate — hangi safety gate'lerinde fail ediyor?
- Kimi ailesi: En düşük safety skorları (36.0–40.0) — missing-variable ve escalation-wording pattern'leri
- Batı'da hiçbir benchmark 4 Çin model ailesini yan yana medical safety'den geçirmiyor

### Platformlar
- **X:** 6 tweet'lik analytical thread (her aile için 1 tweet + intro + cross-family summary)
- **LinkedIn:** Long-form technical post (family comparison table gömülü)
- **Blog:** "Chinese Frontier Models in Medical AI Safety: A Family-Level Analysis" (raporun blog versiyonu)

### Hedef Kitle
Çin model ekipleri (Qwen/Alibaba, DeepSeek, Zhipu/GLM, Moonshot/Kimi), AI safety araştırmacıları, Çin-ABD tech karşılaştırması yapan analistler

### İçerik Formatı
- X: Analytical thread (data + pattern recognition)
- LinkedIn: Technical long-form (embedded comparison table)
- Blog: Report-style deep dive (3,000+ kelime, alıntılanabilir)

### CTA
> "If you work on any of these model families, I'm sharing structured JSON outputs for your model. Use them for internal testing. Prompt set is open."

### Anahtar Kelimeler / Hashtag'ler
`#Qwen` `#DeepSeek` `#GLM` `#Kimi` `#ChineseAI` `#ModelSafety` `#MedFailBench` `#AIEval` `#FrontierModels`

---

## Hafta 4 — "Kaynaksız İddia: Tıbbi AI'in Sessiz Failure Mode'u"

### Ana Konu
Bir model tıbbi iddia ortaya atıp kaynak bağlamıyorsa, klinisyen için en tehlikeli failure mode'lardan biridir. DeepSeek ailesinin üç modeli de source support'ta 48.0 — tutarlı biçimde. Bu bir bug değil, bir pattern.

### Alt Başlıklar
- Source support ne demek? Klinik bağlamda neden kritik?
- DeepSeek V4 Pro, V4 Flash, V3.2: Üçü de 48.0 — bu tesadüf değil
- "Model bilmiyor" vs "model desteksiz iddia ediyor" — aradaki fark hasta güvenliği
- 5 somut örnek: Modelin kaynak bağlamadığı tıbbi iddialar (prompt ID + ham çıktı)
- Bu neden benchmark ekosisteminde yeterince ölçülmüyor?

### Platformlar
- **X:** 5 tweet'lik case-study thread (her tweet bir somut örnek)
- **LinkedIn:** Long-form analytical post
- **Blog:** Yok

### Hedef Kitle
AI alignment/safety ekipleri, medical informatics araştırmacıları, evidence-based medicine savunucuları, DeepSeek model ekibi

### İçerik Formatı
- X: Case-study thread (her tweet: prompt → model output → neden tehlikeli)
- LinkedIn: Analytical post (source support kavramını klinik perspektiften açıklayan)

### CTA
> "5 examples with prompt IDs and raw model outputs: [link]. DeepSeek team — this is structured and open for internal testing."

### Anahtar Kelimeler / Hashtag'ler
`#SourceSupport` `#EvidenceBased` `#DeepSeek` `#MedicalAI` `#AICitation` `#MedFailBench` `#AISafety` `#ClinicalEvidence`

---

## Hafta 5 — "Daha Büyük ≠ Daha Güvenli: Scale ve Safety Paradoksu"

### Ana Konu
Qwen ailesinde parametre sayısı arttıkça safety düşüyor. 2.5-7B (52.0) > 3.6 Plus (46.7) > 3.7 Max (45.3). Daha büyük model, daha kötü safety. Bu, scaling'in safety'yi çözmediğini gösteriyor.

### Alt Başlıklar
- Veri: Qwen parametre/safety korelasyonu — daha büyük, daha az güvenli
- Llama 3.1-8B (ABD): En küçük ama en yüksek safety (60.0) — boyut tahmin edici değil
- Neden? Scaling, knowledge'ı artırır ama safety gate'lerini (escalation, source support, boundary) ölçekle çözülemez
- Bu bulgunun model ekipleri için implikasyonu: Safety, post-training değil, alignment problemi
- "Benchmarks should measure what scale can't fix" — MedFailBench'in konumlandırması

### Platformlar
- **X:** 4 tweet'lik contrarian thread (counter-narrative: bigger isn't always better)
- **LinkedIn:** Carousel (scale vs safety scatter plot / correlation chart)
- **Blog:** "Why Scaling Doesn't Fix Medical AI Safety" (kısa, provokatif essay)

### Hedef Kitle
AI scaling/safety araştırmacıları, model geliştirme ekipleri, AI investors/analysts, scaling laws tartışması yapan akademisyenler

### İçerik Formatı
- X: Contrarian/analytical thread (paradigm-challenging)
- LinkedIn: Visual carousel (scatter plot: model size vs safety score)
- Blog: Short provocative essay (1,500 kelime, alıntılanabilir, tartışma başlatıcı)

### CTA
> "Scale vs safety data with all 10 models: [link]. Does this hold for your model family? Share your data."

### Anahtar Kelimeler / Hashtag'ler
`#ScalingLaws` `#AISafety` `#ModelSize` `#Qwen` `#Llama` `#MedFailBench` `#AIAlignment` `#FrontierModels` `#SafetyScaling`

---

## Hafta 6 — "Bir Klinisyenin Köprüsü: MedFailBench × MedHELM Adaptörü"

### Ana Konu
MedFailBench sadece bir benchmark değil — bir ekosistem katkısı. MedHELM'e köprü yazan tek bağımsız klinisyen. Bu hafta, açık katkının nasıl yapıldığını gösteriyoruz.

### Alt Başlıklar
- MedHELM bridge spec: Ne yapıldı, nasıl çalışıyor?
- 3 vaka MedHELM-compatible scenario format'ına dönüştürüldü — çalışan kod
- "Bu bir Türkçe benchmark, ama metodoloji dil-agnostik" — bridge'in evrensel değeri
- Inspect Evals katkısı: Açılan issue, hedeflenen PR
- Neden bir klinisyen bunu yapıyor? Çünkü clinical safety perspektifi benchmark ekosisteminde eksik

### Platformlar
- **X:** 5 tweet'lik contribution thread (kod + contribution odaklı, "ben yaptım" değil "işte katkı")
- **LinkedIn:** Technical long-form post (MedHELM maintainer'ları etiketli)
- **Blog:** Yok (kod ve docs kendi kendine konuşur)

### Hedef Kitle
MedHELM/HELM/Stanford CRFM ekibi, UK AISI Inspect team, benchmark ekosistemi contributor'ları, open-source AI safety community

### İçerik Formatı
- X: Contribution thread (her tweet bir artefakt linki: adapter code, bridge spec, crosswalk)
- LinkedIn: Technical post (ekosistem katkısına odaklı, "comparing notes" tonu)

### CTA
> "MedHELM adapter is open. If you maintain a medical AI benchmark, I can help map your safety gates. Let's compare notes."

### Anahtar Kelimeler / Hashtag'ler
`#MedHELM` `#HELM` `#StanfordCRFM` `#AISafety` `#OpenSource` `#BenchmarkDesign` `#MedFailBench` `#AIEval` `#UKAISI`

---

## Hafta 7 — "Aynı Model, Farklı Dil: Tıbbi AI'in Bilingual Drift'i"

### Ana Konu
Bir model İngilizce'de güvenli yanıtlar verebilir ama Türkçe'de güvenlik sınırında kayabilir. MedFailBench, bilingual (EN/TR) drift'i ölçen tek açık benchmark. Metodoloji dil-agnostik — Japonca, Almanca, Arapça için uygulanabilir.

### Alt Başlıklar
- Bilingual drift ne demek? Aynı prompt'un EN ve TR versiyonunda safety score farkı
- 36 Türkçe vaka + 100 İngilizce vaka: Cross-lingual safety comparison verisi
- Klinik bağlam: Türkçe tıbbi dilde model davranış farklılıkları (escalation wording, dosing advice)
- "Metodoloji dil-agnostik" — bir Türkçe benchmark'ın küresel değeri
- Kuroda teması: Japonca medical AI safety testleri için template

### Platformlar
- **X:** 5 tweet'lik cross-lingual thread (EN vs TR aynı prompt → farklı safety davranışı)
- **LinkedIn:** Long-form analytical post (bilingual drift kavramını açıklayan)
- **Blog:** "Bilingual Drift in Medical AI: What Happens When Safety Crosses Languages" (kısa essay)

### Hedef Kitle
Multilingual AI araştırmacıları, Japon/Avrupa/Orta Doğu AI safety ekipleri, global health-tech şirketleri, dil modeli localization ekipleri

### İçerik Formatı
- X: Cross-lingual comparison thread (concrete EN vs TR examples)
- LinkedIn: Analytical post (concept explanation + data)
- Blog: Short essay (1,500 kelime, küresel kitleye hitap eden)

### CTA
> "Turkish medical safety pack is open as a template. If you work in JA, DE, AR, or any language — adapt the methodology. I'll help."

### Anahtar Kelimeler / Hashtag'ler
`#BilingualAI` `#MultilingualLLM` `#MedicalAI` `#AIDrift` `#TurkishAI` `#MedFailBench` `#AISafety` `#Localization` `#GlobalHealth`

---

## Hafta 8 — "Yol Önü: Klinik Panel, Preprint ve Açık Çağrı"

### Ana Konu
8 haftalık seri boyunca gösterilen bulgular rule-based scoring'a dayanıyor. Şimdi: klinik panel validasyonu, arXiv preprint ve ikinci klinisyen reviewer ile inter-rater reliability verisi. Bu bir başlangıç, sonuç değil.

### Alt Başlıklar
- Nereden nereye: 8 haftalık seri özeti (her haftanın tek cümlelik takeaways'i)
- Klinik panel: 24 vaka hazır, hekim puanlaması bekleniyor — rule-based score → human validation
- arXiv preprint: Hazır, submit öncesi son kontrol — alıntılanabilir akademik artefakt
- İkinci klinisyen reviewer: Inter-rater reliability verisi toplanıyor
- Açık çağrı: "Bu benchmark'ı birlikte geliştirecek klinisyenler, benchmark builder'lar ve model ekipleri arıyorum"

### Platformlar
- **X:** 7 tweet'lik recap + vision thread (her hafta 1 tweet + closing CTA)
- **LinkedIn:** Long-form vision post (seri boyunca öğrenilenler + gelecek vizyonu)
- **Blog:** "What 8 Weeks of Medical AI Failure Analysis Taught Us" (serinin kapanış yazısı)

### Hedef Kitle
Tüm önceki haftaların kitleleri (model ekipleri, benchmark ekosistemi, AI safety community) + potansiyel collaborator'lar, akademik ortaklar, klinik panel hekimleri

### İçerik Formatı
- X: Recap + vision thread (8 haftanın özeti + gelecek planı)
- LinkedIn: Vision long-form (lessons learned + open collaboration call)
- Blog: Capstone essay (2,000+ kelime, seri boyunca topladığı tüm okuyucular için kapanış)

### CTA
> "If you're a clinician, benchmark builder, or model team interested in medical AI safety — the repo, data, and prompt set are open. Let's build the next phase together."

### Anahtar Kelimeler / Hashtag'ler
`#MedicalAI` `#AISafety` `#OpenScience` `#MedFailBench` `#Collaboration` `#AIEval` `#ClinicalSafety` `#Preprint` `#OpenSource`

---

## Yayın Takvimi Özeti

| Hafta | X Thread | LinkedIn Post | Blog Post | Ekstra |
|-------|----------|---------------|-----------|--------|
| 1 | ✅ 7-tweet educational | ✅ Long-form | ✅ Foundational essay | — |
| 2 | ✅ 5-tweet data | ✅ Carousel/infographic | — | — |
| 3 | ✅ 6-tweet analytical | ✅ Technical long-form | ✅ Report deep dive | — |
| 4 | ✅ 5-tweet case study | ✅ Analytical post | — | — |
| 5 | ✅ 4-tweet contrarian | ✅ Carousel (scatter plot) | ✅ Provocative essay | — |
| 6 | ✅ 5-tweet contribution | ✅ Technical post | — | Etiketleme: MedHELM/Inspect |
| 7 | ✅ 5-tweet cross-lingual | ✅ Analytical post | ✅ Short essay | — |
| 8 | ✅ 7-tweet recap+vision | ✅ Vision long-form | ✅ Capstone essay | Açık collaborator çağrısı |

**Toplam:** 8 X thread · 8 LinkedIn post · 5 blog post · 2 carousel

---

## İçerik Prensipleri (Her Hafta İçin Geçerli)

1. **Veri önce, yorum sonra** — Hiçbir iddia `model_runs/` JSON'larından veya `docs/` raporlarından bağımsız olamaz.
2. **"Ben" değil "veri"** — "I found that..." yerine "The data shows..." tonu. Self-evident artefact.
3. **Link her zaman** — Her post'ta repo, HF Space veya docs linki. Okuyucu doğrulayabilsin.
4. **"Klinik validation değildir"** disclaimeri her uzun post'ta. Dürüstlük = güven.
5. **"Ranking" kelimesi yok** — "Failure atlas" ve "safety gate" kullan.
6. **Aşırı iddialı başlık yok** — "Dünyanın ilk/en iyi/benzersiz" yok. Veri konuşur.
7. **Narrow CTA** — "Follow me" değil, "pick one case and tell me what's missing." Somut katkı iste.
8. **Cross-post timing** — X thread Salı 09:00 ET, LinkedIn Çarşamba 08:00 ET, Blog Perşembe. Aynı içerik farklı günlerde farklı kitleye ulaşır.

---

## Ölçüm Metrikleri (Haftalık)

| Metrik | Hedef (haftalık) | Hedef (8 hafta sonunda) |
|--------|-------------------|------------------------|
| X thread impressions | ≥ 5,000 | En az 1 thread viral (≥ 50k) |
| LinkedIn post engagement | ≥ 100 | En az 1 post viral (≥ 1,000) |
| Blog unique visitors | ≥ 200 | Toplam ≥ 2,000 |
| GitHub stars (incremental) | ≥ 10/hafta | ≥ 150 toplam |
| HF Space views (incremental) | ≥ 100/hafta | ≥ 1,000 toplam |
| Dış alıntılanma | — | ≥ 3 (blog/tweet/forum) |
| Model ekibi yanıtı | — | ≥ 2/4 ekip |

---

> Bu plan canlı bir dokümandır. Her hafta sonu yayın sonrası performansa göre güncellenir.
> Sahibi: G · Hazırlayan: Mercury · 2026
