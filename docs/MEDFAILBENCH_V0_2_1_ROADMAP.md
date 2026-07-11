# MedFailBench v0.2.1 Roadmap
> Hedef: v0.2.0 flagship layer'ı gerçek bir işbirlikçi benchmark'a dönüştürmek
> Oluşturma: 2026-07-02 20:00 TRT, son güncelleme: 2026-07-09 TRT
> Durum: AKTIF -- GitHub Discussions ✅, CONTRIBUTING ✅, weekly eval script ✅. Yeni dış eleştiri kapısı: ölçek/yenilik/gap analysis/clinician validation.

## External feedback pivot — 2026-07-09

Ziying Sheng geri bildirimi roadmap'e işlendi. Ana ders: MedFailBench fikri değil, mevcut paket görüntüsü zayıf duruyor. Küçük bağımsız benchmark algısı, sınırlı yenilik/ölçek ve HealthBench/CSEDB gibi mevcut çalışmalar karşısında farkın net olmaması işbirliği şansını düşürüyor.

Bundan sonraki geliştirme yönü:

1. HealthBench, CSEDB ve benzer benchmark'lara karşı açık gap analysis yazılacak.
2. Mevcut açık veri setleri üstüne büyüyen extension plan hazırlanacak.
3. Geniş aday havuzu ile panel-doğrulanmış alt set ayrımı netleşecek.
4. Klinisyen paneli ve inter-rater/adjudication hattı işbirliği öncesi görünür hale gelecek.
5. Büyük ekiplerden işbirliği istemeden önce ölçek + novelty + doğrulama artifact'leri hazır olacak.

## Immediate panelization sprint

Status: in progress for MedFailBench clinician panel v0.1.

Files added in this sprint:

1. `docs/CLINICIAN_PANEL_PROTOCOL_V0_1.md`
2. `docs/CLINICIAN_REVIEW_PACKET_V0_1.md`
3. `docs/templates/CLINICIAN_RATING_FORM_TEMPLATE.md`
4. `docs/CLINICIAN_PANEL_OUTREACH_DRAFTS_V0_1.md`
5. `docs/CLINICIAN_PANEL_PILOT_CASE_SELECTION_V0_1.md`
6. `data/panel_pilot/clinician_panel_pilot_cases_v0_1.tsv`
7. `data/panel_pilot/clinician_panel_rating_sheet_v0_1.tsv`

Next 5 actions:

1. Select 10 to 15 synthetic cases from the current benchmark set. Done for v0.1: 15 synthetic cases selected.
2. Assign reviewer codes and keep reviewer names outside public data unless permission is explicit.
3. Send the packet to 2 to 4 clinicians for independent first pass ratings.
4. Record two ratings per case, then mark severity disagreements of 2 or more points for adjudication.
5. Report raw agreement, exploratory kappa if data allow it, and a clear limitation note before any public summary.

---

## 1. Zenodo DOI

MedFailBench'e kalıcı bir DOI bağlamak, akademik atıf ve preprint referansı için kritik.

**İşlem:**
- Zenodo'da `goktugozkanmd` hesabı aç (GitHub login ile)
- GitHub-Zenodo entegrasyonu kur
- v0.2.0 release'ine DOI bağla
- Preprint içinde DOI referansı ekle

**Blocker:** Zenodo hesabı gerekli. G GitHub üzerinden Zenodo login yapabilir.

**Öncelik:** Yüksek — preprint submit öncesi tamamlanmalı

---

## 2. GitHub Discussions Açma

Topluluk katkısı ve collaborator onboarding için resmi kanal.

**İşlem:**
- GitHub repo ayarlarından Discussions'i etkinleştir
- Kategoriler: `General`, `Ideas`, `Q&A`, `Show and tell`, `Collaboration`
- İlk discussion: "Welcome / How to contribute to MedFailBench"

**Blocker:** Yok — repo admin yetkisi var.

**Öncelik:** Yüksek

---

## 3. Contributor Onboarding Paketi

Collaborator issue (#182) somut adımlara bağlanmalı.

**İşlem:**
- `CONTRIBUTING.md` güncelle — net adımlar: (1) issue seç/oluştur, (2) branch aç, (3) synthetic case ekle, (4) PR aç
- Synthetic case template dosyası oluştur (`templates/SYNTHETIC_CASE.md`)
- Issue labels ekle: `good-first-issue`, `synthetic-case`, `safety-gate-review`, `wording-review`
- README'de "How to Contribute" section'ı güncelle

**Blocker:** Yok

**Öncelik:** Orta

---

## 4. Weekly Evaluation Automation

Haftalık model response evaluation'ı manuel run yerine cron job'a bağla.

**İşlem:**
- OpenRouter API üzerinden model response çekme scripti (`scripts/run_weekly_eval.sh`)
- Rule-based scoring scripti (`scripts/score_outputs.py`)
- Her hafta otomatik çalışan cron job
- Sonuçları `docs/MEDFAILBENCH_WEEKLY_MODEL_RESPONSE_EVAL.md`'ye ekle

**Blocker:** OpenRouter API key'ine terminal erişimi gerekir.

**Öncelik:** Orta

---

## 5. İkinci Klinisyen Review (Inter-Rater)

Single-clinician review en büyük limitation. En az 1 ek klinisyen review gerekli.

**İşlem:**
- Collaboration brief üzerinden potansiyel reviewer ara
- 10-15 random case'i ikinci bir klinisyene gönder
- Inter-rater agreement (Cohen's kappa) hesapla
- Sonucu preprint Limitations section'ına ekle

**Blocker:** Gönüllü klinisyen bulunması gerekir.

**Öncelik:** Düşük (ama preprint için değerli)

---

## 6. ArXiv Preprint Submission

MedFailBench preprint'ini arXiv'e yükle.

**İşlem:**
- arXiv `cs.CL` veya `cs.AI` kategorisinde submit
- LaTeX kaynağını arXiv formatına uygun hale getir
- DOI eklendikten sonra submit

**Blocker:** Zenodo DOI öncesi submit anlamsız. Önce DOI, sonra preprint.

**Öncelik:** Yüksek (DOI sonrası)

---

## Timeline

| Adım | Öncelik | Blocker | Tahmini Süre |
|------|---------|---------|-------------|
|| GitHub Discussions aç | ✅ Yüksek | — | ✅ (21:00 run) |
|| Zenodo DOI | Yüksek | G hesabı | 30 dk |
|| CONTRIBUTING.md güncelle | ✅ Orta | — | ✅ (21:00 run) |
|| Reference hallucination audit | ✅ Kritik | — | ✅ (22:00 run) |
|| Preprint Discussion genişletme | ✅ Orta | — | ✅ (23:00 run) |
|| Haftalık eval script | ✅ Orta | API key | ✅ (02:00 run) |
|| ArXiv submit | Yüksek | DOI | 1 saat |
|| İkinci klinisyen review | Düşük | Gönüllü | 1-2 hafta |
|| Release checklist doc | ✅ | — | ✅ (03:00 run) |

---

## Next Best Actions (Güncel — 2026-07-09 TRT)

1. ~~Preprint referanslarını genişlet~~ ✅ (20:00 run)
2. ~~main.tex'i gerçek eval verisiyle genişlet~~ ✅ (20:00 run)
3. ~~GitHub Discussions'i etkinleştir~~ ✅ (21:00 run)
4. ~~CONTRIBUTING.md güncelle~~ ✅ (21:00 run)
5. ~~Weekly eval script oluştur~~ ✅ (02:00 run)
6. ~~Release checklist doc oluştur~~ ✅ (03:00 run)
7. ⏳ `docs/COMPETITIVE_GAP_ANALYSIS_HEALTHBENCH_CSEDB.md` — dış eleştiri sonrası kritik yeni kapı
8. ⏳ `docs/OPEN_DATASET_EXTENSION_PLAN.md` — küçük standalone benchmark algısını kırmak için
9. ⏳ README/landing novelty dili — HealthBench/CSEDB yerine geçme iddiası yok; farklı failure-mode extension konumu net
10. ⏳ Klinisyen panel görünürlüğü — iki bağımsız puanlama + adjudication + uzmanlık etiketi
11. ⏳ ArXiv submit — gap analysis ve novelty dili temizlendikten sonra
12. **Yeni iş adayları:** (a) HF Space'e model submission formu ekle, (b) İkinci growth post/LinkedIn brief taslağı, (c) Lighteval/Inspect entegrasyon planı, (d) Preprint'i açık veri seti extension planına hazırla, (e) Collaborator onboarding dashboard
