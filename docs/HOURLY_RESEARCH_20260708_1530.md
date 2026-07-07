# Saatlik Araştırma Raporu — 2026-07-08 ~15:30 TRT
## Araştırma Odağı: EU AI Act Compliance + Medikal AI Benchmark Rekabet Analizi + HF Görünürlük

---

## Bulgu 1: 🔥 EU AI Act High-Risk Medical AI — Ağustos 2026 Deadlines (KRİTİK)

- EU AI Act high-risk sınıflandırması Ağustos 2026'da yürürlüğe giriyor
- MDR/IVDR altındaki tıbbi cihazlar **otomatik olarak high-risk AI sistemi** sayılıyor
- Gerekenler: risk yönetim sistemi (Art. 9), doğruluk/sağlamlık (Art. 15), insan gözetimi (Art. 14)
- **Standart bir klinik safety benchmark mevcut DEĞİL.** MedFailBench bu boşluğu doldurabilir.
- Kaynaklar:
  - `https://mdxcro.com/eu-ai-act-medical-devices-samd/`
  - `https://meddeviceguide.com/blog/eu-ai-act-high-risk-classification-guidelines-medical-device-guide`
  - `https://patientguard.com/the-ai-act-omnibus-explained-what-the-2026-eu-rules-mean-for-medical-device-and-ivd-manufacturers/`
  - `https://www.dqsglobal.com/en/explore/blog/ai-act-ai-enabled-medical-devices`

---

## Bulgu 2: Nature Medicine — General-Purpose LLMs > Specialized (Haziran 2026)

- Vishwanath, Krithik et al. (16 yazar). Nature Medicine, 12 June 2026.
- **Finding:** Frontier LLMs outperform specialized clinical AI tools on medical benchmarks
- MedFailBench doğru yönde: frontier modelleri test ediyoruz, specialized araçları değil
- Kaynak: `https://www.nature.com/articles/s41591-026-04431-5`

---

## Bulgu 3: CSEDB — Çin'den Doğrudan Rakip Benchmark (npj Digital Medicine)

- Clinical Safety-Effectiveness Dual-Track Benchmark
- Future Doctor (Çin AI healthcare company) + 32 klinik uzman
- npj Digital Medicine'de yayınlanmış (Aralık 2025/Şubat 2026)
- **Farkımız:**
  - CSEDB: safety + effectiveness dual track, ticari, tek-vendor, Çin regülasyon odağı
  - MedFailBench: worst-case safety, open-source, Çin+Batı model coverage, Türkçe drift, EU AI Act alignment
- Kaynak: `https://briefglance.com/articles/new-medical-ai-benchmark-puts-clinical-safety-before-raw-power`

---

## Bulgu 4: ClinBench.com — Yeni Ticari Rakiplik Platform

- `https://clinbench.com/` — yeni tıbbi AI benchmark karşılaştırma platformu
- Ticari, birden çok benchmark'ı karşılaştırma vaadi
- **Risk:** MedFailBench'in görünürlük alanını daraltabilir
- **Fırsat:** MedFailBench'i ClinBench'te listeletmek? (G onayı gerekir)

---

## Bulgu 5: JAMA AI Mental Health Harm Taxonomy

- JAMA Viewpoint: Specialized or General-Purpose — The Wrong Question for Mental Health AI Safety
- AI mental health zararı için taksonomi geliştirme çağrısı
- MedFailBench'in safety-gate taksonomisine doğrudan paralel
- Kaynak: PubMed 42371659, doi:10.1001/jama.2026.11448

---

## Bulgu 6: DeepSeek Clinical Readiness — Nature Biomedical Engineering?

- DeepSeek-V3 ve R1'in klinik karar desteği benchmark değerlendirmesi
- Nature Medicine'de yayınlanmış (Nisan 2025)
- Bağımsız Çin kaynaklı değerlendirme — MedFailBench'in DeepSeek safety verisi tamamlayıcı
- Kaynak: `https://www.nature.com/articles/s41591-025-03727-2`

---

## Büyüme Yönleri

### Yön A: 🏆 EU AI Act Compliance Positioning (Etki: 🔥🔥🔥🔥🔥 | Hız: 2 gün | Risk: Düşük)
MedFailBench'i EU AI Act conformity assessment audit framework'u olarak konumlandır.
- Mevcut varlıklar yeniden etiketlenir (SAFETY_GATE_TAXONOMY → conformity rubric)
- COMPLIANCE.md asset→requirement mapping oluşturuldu
- Dış onay gereken tek şey: whitepaper yayını

### Yön B: Competitor Differentiation (Etki: 🔥🔥🔥 | Hız: 1 gün | Risk: Düşük)
READ ME'ye competitor karşılaştırma tablosu ekle. CSEDB, MedSafetyBench, HealthBench, ClinBench ile pozisyon farkını netleştir.

### Yön C: Nature Medicine Paper'ı Referans Alma (Etki: 🔥🔥 | Hız: 30 dk | Risk: Yok)
Vishwanath et al. 2026'yı README'de ve preprint'te referans olarak ekle. "General-purpose LLMs > specialized clinical AI" argümanı MedFailBench'in frontier model odağını destekler.

---

## Seçilen Yön: A — EU AI Act Compliance Positioning

### Gerekçe
- En yüksek etki: açık bir regülasyon boşluğuna oturuyor
- En hızlı: yeni model eval gerektirmez, mevcut varlıklar yeniden etiketlenir
- En farklılaştırıcı: hiçbir rakip benchmark compliance odaklı konumlanmamış
- G'nin hedefleriyle uyumlu: akademik/AI prestij + network + görünürlük

### Üretilen
1. `docs/EU_AI_ACT_COMPLIANCE_STRATEGY.md` — tam strateji dokümanı (6 bölüm)
2. `COMPLIANCE.md` — repo kökünde asset→requirement mapping tablosu
3. ROADMAP_30DAYS.md güncellendi — success metric eklendi
4. BAGLAM2 güncellendi — yeni entry eklendi

### Engeller
- Whitepaper yayını G onayı gerektirir
- "Compliance" terimi overclaim riski taşır — "conformity assessment decision-support tool" olarak frame'lenmeli

---

## BAGLAM2 Kaydı

### Araştırılan
- EU AI Act high-risk medical device deadlines → Ağustos 2026, standart benchmark yok
- Nature Medicine → general-purpose LLMs win (Vishwanath 2026)
- CSEDB (Çin) → doğrudan safety benchmark rakibi
- ClinBench.com → ticari benchmarking platform
- JAMA AI mental health harm taxonomy → taksonomi talep ediyor

### Karar
EU AI Act compliance positioning — mevcut varlıkları yeniden etiketle, COMPLIANCE.md ile dokümante et. Dış onay gereken: whitepaper.

### Üretilen
- `docs/EU_AI_ACT_COMPLIANCE_STRATEGY.md`
- `COMPLIANCE.md`
- `docs/HOURLY_RESEARCH_20260708_1530.md` — bu rapor
- BAGLAM2 güncellendi
- ROADMAP_30DAYS.md güncellendi

---

## G Onayı Gerekenler

1. **EU AI Act whitepaper yayını:** "Benchmarking Clinical AI Safety for EU AI Act Conformity" başlıklı bir whitepaper yayınlamak. Onay verirsen hazırlanır.
2. **COMPLIANCE.md'i README'de referans gösterme:** Repo'nun ana sayfasında compliance bağlantısı görünür olacak. Onay vermezsen sadece docs/ klasöründe kalır.