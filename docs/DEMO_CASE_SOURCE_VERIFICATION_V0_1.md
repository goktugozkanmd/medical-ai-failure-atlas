# Demo Case Source Verification V0.1

Date checked: 2026 06 29.

Scope: `data/clinical_safety_demo_cases_v0_1.json`.

Decision: cleared for repository demonstration use. These cases are synthetic evaluation examples only. They are not patient data, clinical advice, clinical validation, deployment evidence, ranking evidence, score certification, source truth certification, institutional approval, or endorsement.

1. DEMO001

Status: Verified.

Source: DailyMed sulfamethoxazole and trimethoprim label.

URL: https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=d8239804-d234-491b-965d-89a7796a5e4d&type=display

Claim support checked: the label names warfarin, prothrombin time, and INR monitoring. This supports the danger gate for missed anticoagulant interaction monitoring.

2. DEMO002

Status: Verified.

Source: AHA and ACC chest pain guideline slide set.

URL: https://professional.heart.org/en/-/media/PHD-Files-2/Science-News/2/2021/2021-Chest-Pain-Guideline-Slide-Set-PDF-102821.pdf?sc_lang=en

Claim support checked: the slide set states that abdominal discomfort may occur in patients with diabetes and elderly patients, discourages the misleading atypical descriptor, and recommends structured risk assessment. This supports the danger gate for unsafe reassurance when acute coronary syndrome remains possible.

3. DEMO003

Status: Verified.

Source: National Kidney Foundation pain medicines and kidney disease page.

URL: https://www.kidney.org/kidney-topics/pain-medicines-and-kidney-disease

Claim support checked: the page says people with chronic kidney disease should avoid NSAIDs, especially when eGFR is lower than 60, unless directed by a health care professional. This supports the danger gate for kidney risk ignored in an NSAID request.

Open limits: the sources support the safety gates and reviewer prompts. They do not make these synthetic cases clinical validation, deployment evidence, or complete clinical guidance.
