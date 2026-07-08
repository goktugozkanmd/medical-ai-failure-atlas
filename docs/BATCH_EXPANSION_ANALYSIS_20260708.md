# Hard30 Batch Expansion Analysis (2026-07-08)

> DeepSeek V4 Pro ve Qwen 3.7 Max — her model 30 hard safety prompt üzerinde değerlendirildi.
> Bu analiz 2026-07-08 kapanisinda local rule scoring ile guncellendi.
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

| Metrik | 5-prompt public snapshot | 30-prompt local rule score |
|--------|--------------------------|----------------------------|
| Mean safety score | 52.0 / 100 | 3.9 / 5 |
| Unsafe label count | 1/5 | 1/30 |
| Unsafe scenario IDs | Not expanded here | H027 |
| Main triggered gate | Not expanded here | `unsafe_discharge_reassurance` |

DeepSeek V4 Pro hard30 raw outputlari 2026-07-08'de local rule scorer ile skorlandi. Bu sonucu public worst-case table ile karistirma: skor olcegi ve scorer ciktisi farkli dosyada tutuldu.

### Karşılaştırma: 30-prompt modeller

| Model/run | n | Source | Unsafe label count | Note |
|-----------|---|--------|--------------------|------|
| Qwen 3.7 Max public worst-case snapshot | 30 | `model_runs/worst_case_safety_report_v0_1.json` | 14/30 | Existing public snapshot. |
| GLM-5.2 public worst-case snapshot | 28 | `model_runs/worst_case_safety_report_v0_1.json` | 11/28 | Existing public snapshot. |
| Qwen 3.6 Plus public worst-case snapshot | 30 | `model_runs/worst_case_safety_report_v0_1.json` | 11/30 | Existing public snapshot. |
| DeepSeek V4 Pro hard30 local rule score | 30 | `model_runs/batch_expansion_20260707/deepseek_deepseek_v4_pro_hard30_rule_scores.json` | 1/30 | New local score; needs manual review before public claim update. |
| Qwen 3.7 Max hard30 local rule score | 30 | `model_runs/batch_expansion_20260707/qwen_qwen3_max_hard30_rule_scores.json` | 3/30 | New local score; kept separate from existing public worst-case snapshot. |

---

## Skorlama Durumu

Raw output'lar `model_runs/batch_expansion_20260707/` altında mevcut. Rule-based scoring tamamlandi ve ciktisi ayni klasore yazildi.

**Local check:** Python 3.14 ortaminda skorlandi. Yeni API cagrisi veya paid model run yapilmadi.

```bash
python3 - <<'PY'
from failure_atlas.scorer import score_raw_output
score_raw_output(
    'model_runs/batch_expansion_20260707/deepseek_deepseek_v4_pro_hard30_raw_outputs.json',
    'data/scoring_rubric_v0_3.json',
    output_path='model_runs/batch_expansion_20260707/deepseek_deepseek_v4_pro_hard30_rule_scores.json',
)
score_raw_output(
    'model_runs/batch_expansion_20260707/qwen_qwen3_max_hard30_raw_outputs.json',
    'data/scoring_rubric_v0_3.json',
    output_path='model_runs/batch_expansion_20260707/qwen_qwen3_max_hard30_rule_scores.json',
)
PY
```

---

## Sonraki Adımlar

1. [x] Hard30 raw output'lari local rule scorer ile skorla.
2. [ ] Her model için domain bazlı failure breakdown çıkar.
3. [ ] DeepSeek V4 Pro hard30 sonucunu manual review sonrasi public table'a ekleyip eklememeye karar ver.
4. [ ] G onayı ile HF Dataset'e publish et.

---

*Kaynak: C0R3 deep growth dual-loop + Codex local scoring closure — 2026-07-08*
