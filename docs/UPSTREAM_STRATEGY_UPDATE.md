# Upstream Strategy Update — 2026-07-07

## Durum Tespiti: HELM Maintenance Mode

HELM (Stanford CRFM) **maintenance mode** baslatti: 1 Haziran 2026.
- Son release: v0.5.16 (30 Nisan 2026)
- Son commit: 5 Haziran 2026
- Yeni scenario PR kabulu: belirsiz/dusuk ihtimal
- Kaynak: README.md + docs sayfasi

MedHELM Epic PR #3787 (MiguelAFH) hala open, ama Ağustos 2025'ten beri bekliyor.
Epic Systems ortakligiyla NoteSummaryScenario ekliyor — PDSQI-9 rubrigi kullaniyor.
MedHELM ayri bir repo degil, HELM'in icine gomulu.

### Etki

Önceki STATE_LEDGER P0 maddesi "MedHELM native benchmark" artik guncel degil.
HELM maintenance modunda yeni benchmark kabul etmez. MedHELM'e native benchmark
yapmak icin gereken efor, olasi geri donuse degmez.

## Yeni Strateji: Dual-Track Upstream Contribution

### Track A: Inspect Evals (UK AISI) — AKTIF, KANITLI

Inspect Evals PR'larimiz:
- #1892: MERGED (system_message -> setup)
- #1893: MERGED (system_message + use_tools -> setup)
- #1897: OPEN (typo fix, review bekliyor)

Inspect'e MedFailBench eval'i eklemek:
- `inspect_evals` altina medfailbench task'i
- Kendi scorer'imizi Inspect formatina cevir
- En az 10 senaryo ile proof-of-concept

### Track B: LM Evaluation Harness (EleutherAI) — YENI FIRSAT

- HuggingFace ekosistemiyle dogrudan entegre
- YAML-based task tanimi (Python gerekmez)
- HF dataset'ten otomatik yukleme
- Model sonuclarimizi HF dataset olarak yayinlayabiliriz
- LLM-as-judge destegi yerleşik

### Track C: HF Dataset Publishing — KOMPLEMAN

- Run sonuclarimizi HF dataset'e cevir
- `goktugozkanmd/medfailbench-v02-results` adiyla yayinla
- Her model run'u ayri config altinda
- README ile dokumante et

## Karsilastirma

| Platform | Aktivite | Entry barrier | Bizim avantajimiz |
|----------|----------|---------------|-------------------|
| Inspect Evals | YUKSEK | Orta (Python task + scorer) | 2 PR merged, 1 open |
| LM Eval Harness | YUKSEK | Dusuk (YAML task) | HF entegrasyonu, TR data |
| HELM/MedHELM | DUSUK (maintenance) | Yuksek (Python scenario class) | MedHELM baglantimiz var ama kapanmis olabilir |

## Karar

**P0 guncellemesi:** ~MedHELM native benchmark~ -> **Inspect Evals + LM Eval Harness dual task hazirligi**

Inspect Evals'e MedFailBench task'i eklemek, az once merged olan PR'larimizin
gorunurlugunu katlayarak artirir. Ayrica UK AISI ekosisteminde kalici varlik
kazandirir.

LM Evaluation Harness yolu daha hizli: YAML + HF dataset ile haftalar degil
gunler icinde calisir benchmark. Ayrica `helm-run`'dan daha yaygin kullaniliyor.

## Uygulama Sirasi

1. **(BU SAAT)** MedFailBench verisini LM Eval Harness task YAML formatina cevir
2. Inspect Evals task Python dosyasi hazirla (G onayi gerektirir)
3. HF Dataset'e model sonuclarini yukle (G onayi gerektirir)
4. G onayi ile parallel: Inspect PR + HF dataset push

## Dosyalar (bu sessionda uretilen)

- `docs/UPSTREAM_STRATEGY_UPDATE.md` — bu dosya
- `leaderboard/medfailbench_evals.yaml` — LM Eval Harness task draft
- `leaderboard/medfailbench_inspect_task.py` — Inspect Evals task draft
- `leaderboard/medfailbench_mmlu_format.jsonl` — MMLU-format test data