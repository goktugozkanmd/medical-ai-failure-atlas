# MedFailBench v0.2.1 Release Checklist

> Single source of truth for the v0.2.1 release process.
> Created: 2026-07-03 03:00 TRT

## 1. Preprint (arXiv-ready)

| Adım | Durum | Not |
|------|-------|-----|
| Abstract ≤1920 chars | ✅ | 74 words, arXiv-compliant |
| LaTeX compiles (`make -C preprint`) | 🔄 | CI workflow var, PR'de otomatik dene |
| Figure 1 (severity distribution) | ✅ | `preprint/figures/severity_distribution.pdf` |
| AI-Assisted Writing Disclosure | ✅ | `main.tex` Section |
| Preprint sections complete | ✅ | 310 lines, 6 sections, 13 references, 2 figures/tables |
| All 13 references verified | ✅ | 2026-07-02 22:00 audit |
| Community review workflow in Future Work | ✅ | Added 2026-07-03 04:00 |
| Limitations expanded (7 items) | ✅ | Collaborator call, 100-case target, Discussions stress-test |
| `.bbl` file generation | 🔄 | `bibtex main` çalıştır, `.bbl`'yi arXiv'e yükle |
| ArXiv PDF preview OK | ❌ | Zenodo DOI alındıktan sonra; LaTeX derleme test edilmeli |

## 2. Zenodo DOI

| Adım | Durum | Blocker |
|------|-------|---------|
| Zenodo hesabı aç (GitHub login) | ❌ | G'nin GitHub hesabıyla Zenodo login yapması gerek |
| GitHub-Zenodo webhook kur | ❌ | Hesap açıldıktan sonra |
| v0.2.0 release'ine DOI bağla | ❌ | Hesap + webhook |
| DOI'yi `main.tex` ve `README.md`'ye ekle | ❌ | DOI alındıktan sonra |

## 3. Community & Collaboration

| Adım | Durum | Not |
|------|-------|-----|
| GitHub Discussions açık | ✅ | #183 welcome post yayında |
| CONTRIBUTING.md onboarding | ✅ | Güncellendi |
| Synthetic case template | ✅ | `docs/templates/SYNTHETIC_CASE_TEMPLATE.md` |
| Issue labels (good-first-issue, vs.) | 🔄 | README'de belirtildi, GitHub'da eklenebilir |
| Collaboration brief | ✅ | `docs/MEDFAILBENCH_COLLABORATION_BRIEF_20260702.md` |
| Collaborator call (#182) | ✅ | Açık, roadmap yorumu eklendi |

## 4. Weekly Evaluation

| Adım | Durum | Not |
|------|-------|-----|
| `scripts/weekly_model_eval.py` | ✅ | 238 satır, 3 model, rule-based scoring |
| İlk gerçek veri run | ❌ | `OPENROUTER_API_KEY` env gerekli |
| Docs güncellemesi | ❌ | İlk run sonrası |
| Cron job kurulumu | ❌ | API key erişimi sonrası |

## 5. Expansion (v0.2.1+)

| Adım | Durum | Priorite |
|------|-------|----------|
| 44 → 100 cases | Plan | Orta |
| İkinci klinisyen reviewer | Gönüllü gerek | Düşük |
| Inter-rater agreement (Cohen's kappa) | Gönüllü gerek | Düşük |
| Lighteval/Inspect integration | Plan | Düşük |
| HF Space model submission form | Fikir | Düşük |

## 6. Visibility & Growth

| Adım | Durum | Not |
|------|-------|-----|
| LinkedIn post | ✅ | Yayında, doğrulandı |
| HF Space canlı | ✅ | 200 OK, severity chart canlı |
| GitHub README badge | ✅ | HF Space badge + live link |
| İkinci growth post | Fikir | Beklemede |
| ArXiv preprint yayın | ❌ | DOI sonrası |
| PubMed/PMC submission | Fikir | Çok uzun vadeli |

## Timeline (Güncellenmiş)

```
Şimdi → Zenodo DOI (G aksiyonu gerek)
    → v0.2.1 release (tag+GitHub Release)
    → ArXiv submit
    → Community growth / collaborator onboarding
    → Weekly eval automation (API key)
```

## Notlar

- Zenodo DOI en kritik blocker. G'nin GitHub-Zenodo login yapması yeterli.
- ArXiv submit öncesi `make -C preprint && bibtex main` ile PDF derlemesi test edilmeli.
- Weekly eval script API key olmadan dry-run modunda test edilebilir.
- GitHub Release v0.2.1 tag oluşturulurken Zenodo DOI otomatik bağlanır (webhook kuruluysa).