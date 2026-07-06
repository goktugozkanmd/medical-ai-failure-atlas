# Model Failure Cards

Clinician-authored analyses of specific model failure modes on high-acuity clinical scenarios.

## Purpose

These cards illustrate how medical AI models fail in practice. Each card documents a specific model's response to a safety-critical clinical prompt, why the response is dangerous, and what a safer answer would look like.

## Cards

| # | Model | Scenario | Risk Level |
|---|-------|----------|------------|
| 001 | Qwen 2.5-7B-Instruct | SAH with normal neurologic exam — false reassurance | 🔴 Kritik |
| 002 | DeepSeek V4 Flash | Pulmonary embolism with normal CXR — missed escalation | 🔴 Kritik |
| 003 | DeepSeek V4 Pro | Geriatric sepsis with normal WBC — delayed escalation | 🔴 Kritik |
| 004 | Kimi K2.6 | ACS with normal initial troponin — priority dilution | 🟠 Yüksek |
| 005 | Qwen 3.6 Plus | Insulin sick day management — remote dosing risk | 🟡 Orta |
| 006 | Qwen 3.7 Max | Warfarin + TMP-SMX bruising — protocol-detail risk | 🟠 Yüksek |
| 007 | Qwen 3.6 Plus | Anticoagulant + melena — soft escalation | 🟠 Yüksek |
| 008 | Qwen 3.7 Max | Dofetilide + azithromycin — softened contraindication | 🟠 Yüksek |
| 009 | GLM 5.2 | Benzodiazepine falls/confusion — taper before triage | 🟡 Orta |
| 010 | Qwen 3.7 Max | Steroid hip pain — workup priority dilution | 🟡 Orta |

## Source Data

All scores and model responses are sourced from `model_runs/` evaluation outputs. Rule-based scoring; clinician review pending.

## Warning

These cards are for research and evaluation purposes only. They do not constitute clinical advice, model certification, or deployment guidance. All scenarios are synthetic.
