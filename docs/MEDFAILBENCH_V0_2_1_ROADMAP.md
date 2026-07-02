# MedFailBench v0.2.1 Roadmap
> Hedef: v0.2.0 flagship layer'ı gerçek bir işbirlikçi benchmark'a dönüştürmek
> Oluşturma: 2026-07-02 20:00 TRT
> Durum: PLAN — henüz başlamadı

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
| GitHub Discussions aç | Yüksek | Yok | 10 dk |
| Zenodo DOI | Yüksek | G hesabı | 30 dk |
| CONTRIBUTING.md güncelle | Orta | Yok | 20 dk |
| Haftalık eval script | Orta | API key | 1-2 saat |
| ArXiv submit | Yüksek | DOI | 1 saat |
| İkinci klinisyen review | Düşük | Gönüllü | 1-2 hafta |

---

## Next Best Actions (Bu Saat İçin)

1. ~~Preprint referanslarını genişlet~~ ✅ (20:00 run)
2. ~~main.tex'i gerçek eval verisiyle genişlet~~ ✅ (20:00 run)
3. GitHub Discussions'i etkinleştir — **bu saatte yapılabilir**
4. Zenodo hesabı için G'ye bildir — **bu adım kullanıcı gerektirir, şimdilik planla**
