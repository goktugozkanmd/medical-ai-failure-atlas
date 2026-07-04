# Outreach: Qwen / Kimi / DeepSeek

Bu taslaklar Cinli frontier model ekiplerine gonderilecek.
Su an sadece taslak. G canli onay vermeden gonderilmez.

Guncel: 2026-07-04 — 6 model gercek API testi tamamlandi, karsilastirma raporu hazir.

---

## DeepSeek (deepseek-ai)

**Hedef repo:** github.com/deepseek-ai
**Konu:** Medical safety behavior on clinical vignettes

```
Merhaba DeepSeek ekibi,

MedFailBench adinda acik kaynak bir klinik AI guvenlik benchmark'i gelistiriyorum.
DeepSeek v4 Flash, v4 Pro, V3.2 modellerini zorlu klinik guvenlik sorularinda test ettim.

30 klinik vaka uzerinden sonuclar (Qwen 3.7 Max dahil 8 model karsilastirmasi):
- DeepSeek V3.2: genel 2.9/5, guvenlik 3.0/5 (8 model icinde 3. sirada)
- DeepSeek V4 Pro: genel 2.8/5, guvenlik 2.2/5
- DeepSeek V4 Flash: genel 2.8/5, guvenlik 2.0/5

Tum modeller "klinik kullanimda dikkatli olunmali" seviyesinde.
Ana sorun: acil eskalasyon atlaniyor.
Dogru teshis veriliyor ama doktora git demiyor.

Amac modeli kotulemek degil.
Hangi guvenlik sinirlarinda nerede davrandigini anlamak.

Karsilastirma raporu: github.com/goktugozkanmd/medical-ai-failure-atlas
Eval seti acik. Feedback veya isbirligi cok degerli olur.

Goktug Ozkan, MD
```

## Qwen / Alibaba (QwenLM)

**Hedef repo:** github.com/QwenLM
**Konu:** Clinical safety across Qwen model sizes

```
Merhaba Qwen ekibi,

MedFailBench ile Qwen 2.5-7B, 3.6 Plus ve 3.7 Max modellerini klinik guvenlik acisindan test ettim.
Turkce + Ingilizce klinik vaka setleri uzerinde calisiyorum.

30 klinik vaka uzerinden Qwen sonuclari (karsilastirmali):
- Qwen 3.7 Max: genel 2.8/5, guvenlik 2.9/5, dogruluk 3.2/5
- Qwen 3.6 Plus: genel 2.9/5, guvenlik 2.8/5, dogruluk 3.2/5
- Qwen 2.5-7B: genel 2.8/5, guvenlik 2.4/5, dogruluk 3.8/5

8 Cinli model icinde orta siralarda. Guvenlik acisindan acil eskalasyon
atlaniyor — bu tum modellerde ortak sorun.

Bir klinisyen olarak amacim: model boyutu ile klinik guvenlik performansi
arasindaki iliskiyi gostermek. 8 model karsilastirmasi hazir.

Repo: github.com/goktugozkanmd/medical-ai-failure-atlas
Feedback veya yonlendirme cok degerli olur.

Goktug Ozkan, MD
```

## Kimi / Moonshot AI

**Hedef:** github.com/MoonshotAI veya platform.moonshot.cn
**Konu:** Kimi k2.7 clinical safety behavior

```
Hello Moonshot team,

I tested Kimi k2.7-code on clinical safety benchmarks as part of MedFailBench,
an open-source medical AI safety evaluation project.

Results across clinical vignettes (8 Chinese frontier model comparison):
- Overall: 3.0/5
- Safety: 2.8/5
- Accuracy: 4.4/5 (top tier among all 8 models)

Kimi k2.7 ranks 2nd overall in the 8-model comparison.
Strong accuracy and clinical reasoning.
Safety escalation still needs improvement — like all models tested.

The eval set is public at github.com/goktugozkanmd/medical-ai-failure-atlas
Would love to hear your thoughts or discuss collaboration.

Goktug Ozkan, MD
```

## GLM / Zhipu AI

**Hedef:** github.com/THUDM
**Konu:** GLM-5 clinical safety evaluation

```
Hello Zhipu/GLM team,

I tested GLM-5.2 on clinical safety benchmarks as part of MedFailBench,
an open-source medical AI safety evaluation project.

Results across clinical vignettes (8 Chinese frontier model comparison):
- Overall: 3.2/5 (1st place among all 8 models)
- Safety: 2.4/5
- Accuracy: 4.4/5 (tied for best)
- Clinical grounding: 3.0/5

GLM-5.2 leads the 8-model comparison. Strong accuracy and clinical reasoning.
Safety escalation still needs improvement — like all models tested.

GLM's multimodal capability (5v-turbo) would make an interesting comparison
against text-only models on clinical image interpretation safety.

Repo: github.com/goktugozkanmd/medical-ai-failure-atlas
Happy to share full comparison results and incorporate your feedback.

Goktug Ozkan, MD
```