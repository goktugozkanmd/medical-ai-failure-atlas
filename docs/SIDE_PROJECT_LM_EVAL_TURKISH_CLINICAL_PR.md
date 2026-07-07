# Side Project: LM Eval Harness — Turkish Clinical Safety Task PR

> **Kaynak:** Issue #3866 (2026-06-21) — C0R3 tarafından açıldı, hala bekliyor.
> **Aksiyon:** Issue → Label → PR → Merge.
> **Değer:** MedFailBench direkt EleutherAI lm-eval-harness ekosistemine girer.

---

## State

Issue #3866: `[Proposal] New Task: Turkish Clinical Source Support (clinical_safety group)`

| Alan | Değer |
|------|-------|
| Açılış | 2026-06-21 (17 gün beklemede) |
| Label | Yok (eklenmeli: `new-task`) |
| Atanan | Yok |
| Yorum | 1 |
| Durum | **Açık ve implementasyon hazır** |

---

## Yapılacaklar

### Aşama 1 — Issue Canlandırma (G onayı gerektirmez)
- [x] Issue detayı okundu
- [ ] Issue'a `new-task` label ekle (GitHub token gerekli, C0R3'te yok)
- [ ] Issue'a yorum bırak: "Implementation ready, can open PR"

### Aşama 2 — Implementation (G onayı gerektirmez)
- [ ] Fork'tan YAML/JSONL/README dosyalarını çek
- [ ] `lm_eval/tasks/clinical_safety/` dizin yapısını doğrula
- [ ] Task YAML validation: `lm_eval --tasks turkish_clinical_source_support --model dummy`

### Aşama 3 — PR (G onayı gerektirir)
- [ ] Fork branch → upstream PR
- [ ] PR body: issue #3866'ya referans, boundary statement, clinical safety positioning
- [ ] CI bekle ve fix

---

## Teknik Detaylar

```
lm_eval/tasks/clinical_safety/
├── _clinical_safety.yaml              # Group config (clinical_safety)
├── turkish_clinical_source_support.yaml  # Task config (multiple_choice, 10 samples)
├── turkish_clinical_source_support.jsonl # Dataset (10 Turkish MC questions)
├── utils.py                           # Format helpers
└── README.md                          # Boundary + documentation
```

**Group YAML:** `_clinical_safety.yaml`
```yaml
group: clinical_safety
task: turkish_clinical_source_support
```

**Task YAML:** 10 multiple-choice soru, 4 seçenek, 1 doğru cevap
- Output type: `multiple_choice`
- Dataset: lokal JSONL (HF dataset gerekmez)
- Language: Turkish
- Clinical topics: Diabetes, warfarin, COPD, AKI, febrile neutropenia, hyperkalemia, metformin, DOAC bridging, opioid-induced constipation, ACEi monitoring

---

## Riskler

| Risk | Olasılık | Çözüm |
|------|----------|-------|
| Issue stale — maintainer ilgilenmez | Orta | PR açınca otomatik review tetiklenir |
| `new-task` label kapalı | Düşük | Template olarak kullanılır |
| YAML format değişmiş | Düşük | v0.4.9.1 ile uyumlu |
| 10 soru az | Orta | Minimal viable — sonra genişletilebilir |

---

## Değer

- **Visibility:** EleutherAI ekosisteminde "clinical_safety" grubu = yeni kategori öncüsü
- **Upstream PR** #1: lm-eval-harness'e ilk Türkçe tıbbi güvenlik task'ı
- **Positioning:** MedFailBench → lm-eval-harness → binlerce geliştirici kullanır
- **Prestij:** EleutherAI maintainer'ları ile ilişki

---

## Karar

**Kovalanır.** Issue zaten açık, implementasyon hazır.
G onayı ile PR açılmalı.

---

*Kaynak: C0R3 deep growth dual-loop — ai_eval_trends secondary lens*
*2026-07-08 18:00 UTC*