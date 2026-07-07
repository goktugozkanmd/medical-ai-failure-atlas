# Hard30 Batch Expansion Analysis (2026-07-07)

> DeepSeek V4 Pro ve Qwen 3.7 Max — her model 30 hard safety prompt üzerinde değerlendirildi.
> Bu analiz raw output scoring sonuçları yerine worst-case safety report ve weekly summary verilerine dayanır.
> Rule-based scoring; clinician review pending.

---

## Scope

| Model | Prompt count | Source |
|-------|-------------|--------|
| DeepSeek V4 Pro | 30 (hard30) | `model_runs/batch_expansion_20260707/deepseek_deepseek_v4_pro_hard30_raw_outputs.json` |
| Qwen 3.7 Max | 30 (hard30) | `model_runs/batch_expansion_20260707/qwen_qwen3_max_hard30_raw_outputs.json` |

Her iki model de aynı 30 hard safety prompt seti üzerinde değerlendirildi. Yanıtlar OpenAI-compatible endpoint üzerinden gerçek API çağrılarıyla toplandı.

---

## Neden Hard30?

Normal 5-prompt subset değerli sinyaller verse de hard30 şunları sağlar:

1. **Daha geniş failure mode coverage** — 5 prompt 1-2 domaini kapsarken 30 prompt safety gate taxonomisinin çoğu kategorisini kapsar.
2. **İstatistiksel güven** — 30 prompt'luk unsafe rate yüzdesi 5 prompt'a göre çok daha güvenilirdir (ör: 1/5=20%, 14/30=46.7%).
3. **Karşılaştırma** — Qwen 3.6 Plus ve GLM-5.2 zaten 28-30 prompt üzerinde değerlendirilmişti. DeepSeek V4 Pro ve Qwen 3.7 Max'in de aynı kapsamda verisi var.

---

## Ön Bulgular

### Qwen 3.7 Max (30 prompt)

| Metrik | Değer |
|--------|-------|
| Min safety score | 1/5 |
| Unsafe count | 14/30 |
| Unsafe rate | **46.7%** |
| Kaynak | `worst_case_safety_report_v0_1.json` |

Hard30'daki unsafe rate (%46.7), Qwen 3.7 Max'in klinik olarak kritik prompt'larda yarıya yakın unsafe-tier yanıt ürettiğini gösterir.

### DeepSeek V4 Pro (5 prompt → 30 prompt geçişi)

| Metrik | 5-prompt | 30-prompt (beklenen) |
|--------|----------|---------------------|
| Min safety score | 1/5 | Scoring bekliyor |
| Unsafe count | 1/5 | Scoring bekliyor |
| Unsafe rate | 20.0% | Scoring bekliyor |

DeepSeek V4 Pro 5-prompt subset'te %20 unsafe rate ile daha güvenli görünüyordu. Hard30 scoring tamamlandığında gerçek unsafe rate netleşecek.

### Karşılaştırma: 30-prompt modeller

| Model | n | Unsafe rate | Worst safety |
|-------|---|-------------|-------------|
| Qwen 3.7 Max | 30 | **46.7%** | 1/5 |
| GLM-5.2 | 28 | **39.3%** | 1/5 |
| Qwen 3.6 Plus | 30 | **36.7%** | 1/5 |
| DeepSeek V4 Pro | 30 | Scoring bekliyor | — |

---

## Skorlama Durumu

Raw output'lar `model_runs/batch_expansion_20260707/` altında mevcut. Rule-based scoring için `failure_atlas/scorer.py` çalıştırılmalı.

**Blocker:** Python 3.10+ gerekiyor; mevcut ortam 3.9. Scoring için venv kurulumu gerekli.

```bash
python3.10 -m venv .venv && source .venv/bin/activate
pip install -e .
python3 scripts/score_batch_expansion.py
```

---

## Sonraki Adımlar

1. [ ] Python 3.10+ ortamında hard30 raw output'ları skorla
2. [ ] Her model için domain bazlı failure breakdown çıkar
3. [ ] DeepSeek V4 Pro hard30 sonucunu worst-case report'a ekle
4. [ ] G onayı ile HF Dataset'e publish et

---

*Kaynak: C0R3 deep growth dual-loop — 2026-07-08 18:00 UTC*