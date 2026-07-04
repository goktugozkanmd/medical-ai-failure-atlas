# Free Chinese Frontier Model Access Guide

MedFailBench'in Cinli model degerlendirmesi icin OpenRouter'a alternatif ucretsiz rotalar.
Su an OpenRouter API key tanimli degil. Bu rehber para harcamadan gercek model ciktisi almanin yollarini gosterir.

## Yontem 1: HuggingFace Inference API (UCRETSIZ)

Bazi Cinli modeller HF'de ucretsiz inference sunuyor.

| Model | HF Repo | Inference Status | Calisiyor mu? |
|-------|---------|-----------------|---------------|
| Qwen 2.5 7B | `Qwen/Qwen2.5-7B-Instruct` | warm | EVET |
| DeepSeek V3 | `deepseek-ai/DeepSeek-V3` | warm | EVET |
| GLM-4 9B | `THUDM/glm-4-9b-chat` | none | HAYIR |

**Kullanim (HF Inference API — OpenAI-uyumlu endpoint):**

```python
import requests, json

# Qwen ve DeepSeek bu endpoint'te calisir (ucretsiz, rate-limited)
url = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct/v1/chat/completions"

payload = {
    "model": "Qwen/Qwen2.5-7B-Instruct",
    "messages": [{"role": "user", "content": "..."}],
    "max_tokens": 500,
    "temperature": 0.1
}

# HF token olmadan da calisir (anonim tier), ama token ile daha yuksek rate limit
headers = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer $HF_TOKEN"  # opsiyonel
}

resp = requests.post(url, json=payload, headers=headers)
print(resp.json()["choices"][0]["message"]["content"])
```

**HF icin DeepSeek:**
```python
url = "https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-V3/v1/chat/completions"
```

**Rate limit:** Anonim tier'da dakikada ~10 istek. 30 promptluk eval seti icin yeterli.

**Limitasyon:** Qwen 2.5-7B ve DeepSeek V3 buyuk modeller. HF inference queue'ya girebilir (ozellikle DeepSeek V3). Bekleme suresi olabilir.

## Yontem 2: Zhipu/GLM Resmi API

**Endpoint:** `https://open.bigmodel.cn/api/paas/v4/chat/completions`
**Docs:** `https://docs.bigmodel.cn/cn/guide/start/introduction`
**Kayit:** `https://open.bigmodel.cn/` — Cin telefonu gerektirebilir.
**Ucretsiz tier:** Yeni kullanicilara token kredisi veriyor olabilir. Kayit sonrasi kontrol edilmeli.

GLM modelleri: `glm-4-flash` (ucretsiz), `glm-4-plus`, `glm-4-air`

## Yontem 3: Moonshot/Kimi Resmi API

**Endpoint:** `https://api.moonshot.cn/v1/chat/completions`
**Docs:** `https://platform.moonshot.cn/docs`
**Kayit:** `https://platform.moonshot.cn/` — Cin telefonu gerektiriyor.
**Ucretsiz tier:** Yeni kullanicilara 15 yuan (~$2) kredi.

Kimi modelleri: `moonshot-v1-8k`, `moonshot-v1-32k`, `moonshot-v1-128k`

## Yontem 4: DeepSeek Resmi API

**Endpoint:** `https://api.deepseek.com/v1/chat/completions`
**Docs:** `https://platform.deepseek.com/api-docs`
**Kayit:** `https://platform.deepseek.com/` — email ile kayit mumkun.
**Fiyat:** Cok ucuz — ~$0.14/1M input token. 30 prompt x 500 token = ~$0.002 (neredeyse bedava).

DeepSeek modelleri: `deepseek-chat` (V3), `deepseek-reasoner` (R1)

## Yontem 5: OpenRouter (PARALI ama en kolay)

Mevcut pipeline bu yontem icin hazir. `~/.hermes/.env` icine `OPENROUTER_API_KEY` eklenince calisir.

**Tahmini maliyet:** 30 prompt x 10 model x 500 token = ~$2-5 tek seferlik.

## ONCELIK SIRASI

1. **DeepSeek resmi API** — en ucuz, en kolay kayit, email yeterli
2. **HF Inference API (Qwen + DeepSeek)** — tamamen ucretsiz, hemen simdi kullanilabilir
3. **OpenRouter** — `~/.hermes/.env`'e key eklenince calisir
4. **Zhipu/Moonshot** — Cin telefonu gerekebilir, yedek rota

## Su An Yapilabilecekler (API key'siz)

1. HF Inference API ile Qwen 2.5-7B ve DeepSeek V3 test edilebilir
2. DeepSeek resmi API'ye kayit olunup $5 yuklenirse tum model ailesi test edilebilir
3. HF endpoint'leri OpenAI-uyumlu oldugu icin mevcut `run_prompt_set_openai_compatible_v2.py` script'i endpoint URL degistirilerek kullanilabilir

## HF API icin Script Adaptasyonu

```bash
# Qwen HF uzerinden (ucretsiz):
python3 scripts/run_prompt_set_openai_compatible_v2.py \
  --prompts data/prompt_set_v2_hard_30.tsv \
  --model "Qwen/Qwen2.5-7B-Instruct" \
  --endpoint "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct/v1/chat/completions" \
  --output model_runs/chinese_frontier/

# DeepSeek HF uzerinden (ucretsiz):
python3 scripts/run_prompt_set_openai_compatible_v2.py \
  --prompts data/prompt_set_v2_hard_30.tsv \
  --model "deepseek-ai/DeepSeek-V3" \
  --endpoint "https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-V3/v1/chat/completions" \
  --output model_runs/chinese_frontier/
```

## Blocking Issues

- HF Inference API: anonim tier rate limit'i dar. 30 prompt arka arkaya gonderilirse throttle yiyebilir.
- DeepSeek V3 HF'te cok talep goruyor — queue bekleme suresi uzun olabilir.
- Cozum: prompt'lari 5'erli batch'ler halinde, aralarinda 10sn bekleyerek gonder.