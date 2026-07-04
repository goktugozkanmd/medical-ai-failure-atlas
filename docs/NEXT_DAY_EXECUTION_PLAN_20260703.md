# Next-Day Chinese Frontier Model Execution Plan

Tarih: 2026-07-03 12:00 | Cron run output

## Bugun Bulunan

HF Inference API'de Qwen 2.5-7B ve DeepSeek V3 ucretsiz, anonim erisime acik.
Bu iki model icin OpenRouter API key'e ihtiyac YOK.
Detayli rehber: `docs/FREE_CHINESE_MODEL_ACCESS_GUIDE.md`

## Yarinki Ilk Is (G onaylarsa)

### Adim 1: Qwen 2.5-7B HF uzerinden test (5 dk)

```bash
cd /Users/goktugozkan/Desktop/C0R3/medical-ai-failure-atlas

python3 scripts/run_prompt_set_openai_compatible_v2.py \
  --prompts data/prompt_set_v2_hard_30.tsv \
  --model "Qwen/Qwen2.5-7B-Instruct" \
  --endpoint "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct/v1/chat/completions" \
  --output model_runs/chinese_frontier/qwen25_7b_hf/
```

### Adim 2: DeepSeek V3 HF uzerinden test (5 dk)

```bash
python3 scripts/run_prompt_set_openai_compatible_v2.py \
  --prompts data/prompt_set_v2_hard_30.tsv \
  --model "deepseek-ai/DeepSeek-V3" \
  --endpoint "https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-V3/v1/chat/completions" \
  --output model_runs/chinese_frontier/deepseek_v3_hf/
```

### Adim 3: Skorla ve karsilastir

```bash
python3 scripts/weekly_model_eval.py --model qwen-2.5-7b
python3 scripts/weekly_model_eval.py --model deepseek-v3
```

### Adim 4: Sonuclari outreach taslaklarina ekle

Qwen ve DeepSeek icin gercek rakamlar olunca GitHub issue taslaklari anlamli hale gelir.

## G'nin Yapmasi Gereken (varsa)

1. HF token: Eger anonim tier throttle yerse, HF token olusturup `~/.hermes/.env`'e `HF_TOKEN=...` eklemek rate limit'i yukseltir.
2. OpenRouter key: Daha genis model karsilastirmasi icin. `~/.hermes/.env`'e `OPENROUTER_API_KEY=...` eklenince kalan 8 model de calisir.

## Cikti Hedefi

- Ilk gercek Cinli model karsilastirmasi: DeepSeek V3 vs Qwen 2.5-7B
- 30 klinik guvenlik sorusu uzerinde gercek skorlar
- Dry-run'dan gercek veriye gecis
- Bu sonuclarla GitHub issue taslaklari (QwenLM, deepseek-ai repolarina)