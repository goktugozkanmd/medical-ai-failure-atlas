# TUYZE Health AI Safety Readiness Companion

Date: 2026 06 18

Status: public field readiness companion.

Purpose: give Turkish health AI teams a practical safety readiness companion that aligns with public TÜYZE signals around health data, medical decision support, big data, education, and institutional collaboration.

This is an independent Medical AI Failure Atlas public artifact. It is not an official TÜYZE document, not a TÜSEB document, not a partnership claim, not an application, not a submission, and not an endorsement claim.

## Source signals

### THSRC001: TÜYZE public institute page

Official source: https://tuyze.tuseb.gov.tr/

Checked fact: the public site lists TÜYZE as the Türkiye Sağlık Veri Araştırmaları ve Yapay Zeka Uygulamaları Enstitüsü.

Field read: a health AI safety readiness companion should center health data quality, source support, review readiness, and responsible claim language.

### THSRC002: TÜYZE public institute page

Official source: https://tuyze.tuseb.gov.tr/

Checked fact: the public site lists Büyük Veri Birimi, Tıbbi Karar Destek Sistemleri Birimi, and Akıllı Medikal Cihaz Teknolojileri Birimi.

Field read: safety readiness should cover data quality, decision support limitations, device adjacent risk, and human review handoff.

### THSRC003: TÜYZE public institute page

Official source: https://tuyze.tuseb.gov.tr/

Checked fact: the public site lists Sağlık Veri Organizasyonu Bilim Kurulu and Yapay Zeka Bilim Kurulu.

Field read: teams should separate technical model claims from data governance, clinical review, and source support claims.

### THSRC004: TÜYZE public institute page

Official source: https://tuyze.tuseb.gov.tr/

Checked fact: the public site reports Sağlıkta Yapay Zeka Seminerleri with Marmara University Faculty of Medicine and TÜSEB TÜYZE collaboration between 08 April and 20 May 2026.

Field read: clinician AI literacy is an active public signal and can be supported with open checklists.

### THSRC005: TÜYZE public institute page

Official source: https://tuyze.tuseb.gov.tr/

Checked fact: the public news feed includes 2026 institutional visits and collaboration signals, including HAVELSAN, Halk Sağlığı Genel Müdürlüğü, İzmir İl Sağlık Müdürlüğü, and sectoral AI clustering activity.

Field read: readiness work should be concrete enough for public institutions, hospitals, companies, and academic teams to reuse before a formal project route exists.

## Readiness checks

### THSRR001: Health data fitness

Question: Does the team describe where the data came from, what it represents, what it excludes, and whether labels can change over time?

Use: require a short data fitness card before any model performance claim.

### THSRR002: Decision support limits

Question: Does the team state what the model must not decide alone?

Use: require a human review handoff for diagnosis, triage, treatment, referral, device use, and administrative risk.

### THSRR003: Source support

Question: Does each medical or policy claim have direct support from a named source?

Use: require claim level source support rather than a citation list only.

### THSRR004: Turkish clinical context

Question: Does the team explain whether the evidence, language, coding, population, and workflow match Türkiye health settings?

Use: separate global benchmark performance from local field readiness.

### THSRR005: Failure mode disclosure

Question: Does the team show examples where the system should abstain, flag uncertainty, or ask for expert review?

Use: treat failure examples as a public safety asset, not as a reputational risk.

### THSRR006: Data governance route

Question: Does the team say whether it uses public synthetic data, deidentified data, institutional data, or patient data?

Use: block patient data claims unless authorization, ethics route, and data governance are explicit.

### THSRR007: Public claim hygiene

Question: Does the project avoid saying clinically validated, ready for clinical use, official, approved, endorsed, or deployed unless that is independently verified?

Use: keep public language credible and reusable.

## Field package

This companion can support:

1. TÜYZE aligned readiness outreach.
2. Hospital AI literacy workshops.
3. TÜSEB or TÜBİTAK preparation memos.
4. TEKNOFEST health AI team safety reviews.
5. Medical AI Failure Atlas source and failure review issues.

## Immediate public use

Recommended public issue text:

> Türkiye health AI teams need a practical safety readiness layer before model claims become institutional or clinical claims. We published an independent TÜYZE aligned Health AI Safety Readiness Companion covering data fitness, decision support limits, source support, local context, failure disclosure, governance route, and public claim hygiene.

## Truth state

1. No official TÜYZE claim.
2. No official TÜSEB claim.
3. No endorsement claim.
4. No partner claim.
5. No application claim.
6. No submission claim.
7. No patient data included.
8. No medical advice.
9. No clinical deployment claim.
10. No clinical validation claim.

## Runnable check

```bash
make tuyze_health_ai_safety_readiness_companion
```
