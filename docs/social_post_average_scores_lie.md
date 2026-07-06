# Social Post: Average Scores Hide Unsafe Medical Answers

**Purpose:** Single strong post for X and LinkedIn. Short, shareable, evidence-backed.

---

## English Version

### Average scores hide unsafe medical answers.

We tested 10 models on clinician-authored synthetic safety cases. The averages told only part of the story.

The worst-case view showed the risk.

| Model | Avg Safety | Min Safety | Unsafe Rate |
|-------|-----------|------------|-------------|
| Qwen 3.7 Max | 45.3 | 1/5 | 46.7% |
| GLM-5.2 | 47.1 | 1/5 | 39.3% |
| Qwen 3.6 Plus | 46.7 | 1/5 | 36.7% |
| Kimi K2.6 | 40.0 | 1/5 | 50.0% |

A model can average 45/100 on safety and still fail to keep urgent escalation visible in high-acuity chest-pain cases.

That is not a knowledge gap. It is a **safety boundary failure** — false reassurance after an early negative test.

Clinically, harm comes from the worst answer, not the average.

This is why we built MedFailBench: synthetic clinician-authored cases testing escalation boundaries, remote dosing safety, false reassurance, and evidence overclaim — not medical knowledge recall. Rule-based scoring; external clinician panel validation pending.

Open-source. No patient data. No model ranking. A failure-mode atlas.

Repo: https://github.com/goktugozkanmd/medical-ai-failure-atlas
Demo: https://huggingface.co/spaces/goktugozkanmd/medical-ai-failure-atlas
DOI: https://doi.org/10.5281/zenodo.21205535

#MedicalAI #PatientSafety #LLMEvaluation #AIethics

---

## Turkish Version (Türkçe)

### Ortalama skorlar güvensiz tıbbi cevapları gizler.

10 modeli klinisyen tarafından hazırlanmış sentetik güvenlik vakalarında test ettik. Ortalamalar hikayenin sadece bir kısmını gösterdi.

En kötü durum tablosu riski gösterdi.

| Model | Ort. Güvenlik | Min. Güvenlik | Güvensiz Oranı |
|-------|--------------|---------------|----------------|
| Qwen 3.7 Max | 45.3 | 1/5 | %46.7 |
| GLM-5.2 | 47.1 | 1/5 | %39.3 |
| Qwen 3.6 Plus | 46.7 | 1/5 | %36.7 |
| Kimi K2.6 | 40.0 | 1/5 | %50.0 |

Bir model güvenlikte ortalama 45/100 alabilir ve yüksek riskli göğüs ağrısı vakasında acil değerlendirme sınırını yeterince görünür tutamayabilir.

Bu bir bilgi eksikliği değil. Bu bir **güvenlik sınırı hatası** — erken negatif test sonrası yanlış güven vermek.

Klinikte zarar ortalama cevaptan değil, en kötü cevaptan gelir.

MedFailBench'i bu yüzden kurduk: sentetik, klinisyen tarafından hazırlanmış vakalarla eskalasyon sınırlarını, uzaktan doz güvenliğini, yanlış güven vermeyi ve kanıt abartısını test ediyor. Tıbbi bilgi hatırlama değil. Rule-based skor; dış klinisyen panel doğrulaması bekliyor.

Açık kaynak. Hasta verisi yok. Model sıralaması yok. Bir hata tipi atlası.

Repo: https://github.com/goktugozkanmd/medical-ai-failure-atlas
Demo: https://huggingface.co/spaces/goktugozkanmd/medical-ai-failure-atlas
DOI: https://doi.org/10.5281/zenodo.21205535

#MedicalAI #HastaGüvenliği #YapayZeka #Tıp

---

## Usage Notes

- **For X:** Use the English version as the main post. Turkish version as a thread reply or separate post.
- **For LinkedIn:** Use either version. The table renders well on LinkedIn.
- **Data source:** `model_runs/worst_case_safety_report_v0_1.json` — rule-based scoring, clinician panel validation in progress.
- **Key disclaimer (include if challenged):** All cases are synthetic. No patient data. Not clinical validation. Not a model ranking claim.
