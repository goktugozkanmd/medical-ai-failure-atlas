# AI Eval Trends — Secondary Lens (2026-07-08 18:00 UTC)

> Deep dive into AI evaluation ecosystem trends, model safety benchmarks, regulatory developments.
> 21 DDGS queries → 84 hits → 6 key findings → 3 side project ideas.

---

## Key Findings

### F1: LM Eval Harness Issue #3866 — Açık ve Bekliyor

C0R3'ün lm-evaluation-harness reposuna açtığı **Turkish Clinical Source Support** task proposal
(`#3866`) hala **açık, labelsiz ve atanmamış**.

- **State:** open, no labels, no assignee
- **İçerik:** 10 soruluk Türkçe tıbbi kaynak destek değerlendirme task'ı (multiple choice)
- **Konumlandırma:** `clinical_safety` grubu altında yeni task
- **Link:** https://github.com/EleutherAI/lm-evaluation-harness/issues/3866
- **Aksiyon:** Issue'a `new-task` label ekle + task YAML'ını hazırla + sonra PR'a dönüştür

### F2: Diagens DoctorBench — Yeni Çin Tıbbi AI Eval Platformu

Mayıs 2026'da lansmanı yapılan **DoctorBench**, Çin merkezli tıbbi AI değerlendirme platformu.

- **Firma:** Diagens (Çin biyoteknoloji/IVD şirketi)
- **Pozisyon:** "AI teknolojisinin sınırlarını ve klinik pratiğin taleplerini anlamak"
- **Tehdit:** MedFailBench ile benzer konumlandırma, Çin pazarında güçlü olabilir
- **Fırsat:** Farklılaşma alanımız: açık kaynak, batı modelleri kapsamı, worst-case safety odaklı
- **Link:** https://www.bio-equip.cn/ensrc.asp?id=10602

### F3: International AI Safety Report 2026 (Bengio)

Yoshua Bengio liderliğinde Şubat 2026'da yayınlanan 2. Uluslararası AI Güvenlik Raporu.

- **Kapsam:** Model değerlendirme, dangerous capability thresholds, if-then güvenlik yaklaşımları
- **Önem:** MedFailBench'in referans alınabileceği en prestijli uluslararası rapor
- **Link:** https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026
- **Aksiyon:** Rapor içeriğini tara — MedFailBench benzeri çalışmalar var mı, citation fırsatı var mı?

### F4: LLM Eval Framework Ecosystem 2026 — Olgunlaşma

2026'da LLM değerlendirme framework'leri olgunlaştı. AIML.QA benchmark'ı 8 framework'ü karşılaştırıyor:

| Framework | Güçlü olduğu alan |
|-----------|-------------------|
| DeepEval | CI entegrasyonu, en geniş kütüphane |
| RAGAS | RAG değerlendirme (kanonik) |
| Promptfoo | CLI red-teaming, cross-model matrix |
| Arize Phoenix | Production monitoring |
| W&B Weave | Experiment tracking + eval |

**Ecosystem trendi:** Olgun ekipler 2 framework'ü paralel çalıştırıyor: biri development eval (DeepEval/Promptfoo), biri production monitoring (Arize/W&B).

**MedFailBench fırsatı:** Hiçbiri klinik güvenlik değerlendirmesine odaklı değil. MedFailBench clinical safety layer olarak konumlanabilir.

### F5: Inspect Evals — Upstream PR Fırsatı

Inspect Evals reposu hala aktif. Eval template'i mevcut:

```
https://inspect.aisi.org.uk/reference/inspect_eval.html
https://github.com/UKGovernmentBEIS/inspect_evals
```

MedFailBench Inspect Evals task PR taslağı (`leaderboard/medfailbench_inspect_task.py`) mevcut ama **draft durumda**. PR #1897 typo fix hala review bekliyor.

- **Aksiyon:** PR #1897'ye yorum yap (ping reviewer). Sonra asıl MedFailBench task PR'ını hazırla.

### F6: AI Model Evaluation Guide (aisecurityandsafety.org)

AI Safety Directory'de 2026 güncel rehber. Safety benchmarks, red teaming, bias testing kapsıyor.

- **Fırsat:** MedFailBench bu rehberde listelenmemiş. Outreach/dizin ekleme fırsatı.
- **Link:** https://aisecurityandsafety.org/en/guides/ai-model-evaluation/

---

## Yan Proje Fikirleri

### P1 (HOT): LM Eval Harness — Turkish Clinical Safety Task PR

Issue #3866 açık ve bekliyor. Yapılacaklar:
1. Issue'a `new-task` label ekle (GitHub API ile)
2. Task YAML dosyasını hazırla: `lm_eval/tasks/clinical_safety/turkish_clinical_source_support/`
3. 10 soruluk veri setini YAML + JSON formatında oluştur
4. PR aç

**Değer:** lm-eval-harness'e merge edilirse MedFailBench'in adı EleutherAI ekosistemine girer. 
**Risk:** Düşük — YAML task formatı basit, 10 MC question.
**Efor:** ~2 saat.

### P2: MedFailBench + DeepEval/Promptfoo Entegrasyonu

Hiçbir eval framework'ü klinik güvenlik değerlendirmesi sunmuyor. MedFailBench'i bir plugin/veri seti olarak DeepEval veya Promptfoo'ya entegre etmek:

- DeepEval: Custom metric olarak `ClinicalSafetyMetric`
- Promptfoo: Prompt set + scoring rubric olarak

**Değer:** Binlerce geliştirici MedFailBench'i kendi pipeline'ında kullanır.
**Risk:** Orta — entegrasyon eforu, bakım yükü.

### P3: International AI Safety Report 2026 — Citation Outreach

Raporun ekibine MedFailBench'i tanıtmak. Raporun model değerlendirme bölümünde klinik güvenlik benchmark'ı boşluğu var.

**Değer:** Citation = prestij + görünürlük.
**Risk:** Düşük — outreach maili + evidence packet.
**Aksiyon:** Rapor içeriğini tara, uygun bölümü belirle, G onayı ile outreach.

---

## Sıradaki En İyi Aksiyon

**P1 — LM Eval Harness Issue #3866 canlandırma:**
1. Issue'a `new-task` label ekle
2. Task YAML ve dataset hazırla
3. G onayı al
4. PR aç

---

*Kaynak: C0R3 deep growth dual-loop — secondary lens 'ai_eval_trends'*
*21 DDGS queries, 84 hits, 6 key findings, 3 side project ideas.*