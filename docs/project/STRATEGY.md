# STRATEGY — MedFailBench Konumlandırma

> Goktug Ozkan = klinisyen gözüyle medical AI safety failure ölçen adam.

---

## 1. Pozisyon

Tek cümle: **"Bir klinisyen, tıbbi yapay zeka güvenlik hatalarını hasta zararı perspektifinden ölçen bir altyapı kurdu."**

Bu pozisyonun üç dayanağı var:

| Dayanak | Kanıt (repo'da mevcut) |
|---------|----------------------|
| Klinisyen kimliği | goktugozkanmd — hekim imzası, vakalar klinik gözle yazıldı |
| Ölçme altyapısı | v0.2.1 public core assets: 150 scenario-bank rows + 70 prompts; ayrı Failure Atlas intake, Turkish ve TR-EN drift preview katmanları; 10-model public leaderboard; rule-based scorer; CI/HF-router model runs |
| Hata odaklılık | Safety gate taxonomy, worst-case safety report, failure atlas |

Rakamlar değil, **failure mode sınıflandırması**. Bir model ortalama 52 alabilir — ama worst-case'de 30 prompt'tan 14'ünde unsafe tier'a düşüyorsa (Qwen 3.7 Max), o modelin hasta karşısında ne yaptığı ayrı bir sorudur. Biz o soruyu soran benchmark'ız.

---

## 2. Konumlandırma: "Küçük Repo" Değil, Clinician-Led Benchmark

MedFailBench bir side project değil. Şu anda sahip olduğu ve çoğu benchmark'ın sahip olmadığı şeyler:

- **Gerçek model çıktıları** (simülasyon değil, CI/HF-router üzerinden gerçek API çağrıları)
- **Worst-case safety görünümü** (ortalama gizlemiyor, minimum güvenlik skoru gösteriyor)
- **10 public leaderboard model** ve uzmanlık alanlarına ayrılmış safety promptları
- **Çin modellerine özel kapsam** (Qwen, DeepSeek, GLM, Kimi — batıdaki çoğu benchmark bunları atlar)
- **Türkçe tıbbi dil güvenlik testi** (bilingual drift için açık bir safety-test şablonu)
- **Zenodo DOI + TeX-ready preprint draft** (DOI ile cite edilebilir; arXiv submit endorsement bekler)
- **HuggingFace Space'de canlı leaderboard**

Konumlandırma dili:

> "MedFailBench is a clinician-built benchmark that measures medical AI failure modes — not accuracy, not exam scores, but safety boundary failures."

"Ranking" kelimesinden kaçınılır. "Failure atlas" ve "safety gate" vurgulanır.

---

## 3. Hedef Kitleler ve Erişim Stratejisi

### 3.1 Çin — Model Ekipleri (Qwen, DeepSeek, GLM, Kimi)

**Neden:** Çin modelleri şu an repo'da en çok test edilen gruptur ve worst-case unsafe rate'leri yüksektir (Qwen 3.7 Max: %46.7). Bu, model ekipleri için actionable bir bulgudur.

**Artefakt stratejisi:** `model_runs/` klasöründe JSON formatında, doğrudan alıp kullanabilecekleri yapılandırılmış çıktılar var. `docs/CHINESE_FRONTIER_MODEL_MEDICAL_AI_SAFETY_EVAL.md` zaten yazılmış. `docs/FREE_CHINESE_MODEL_ACCESS_GUIDE.md` mevcut.

**"Bunu kim yaptı?" tetikleyicisi:** Model ekipleri kendi modellerinin worst-case safety score'unu arattıklarında bu repoya düşecekler. JSON çıktıları o kadar temiz ve yapılandırılmış ki, "bu veriyi kim topladı?" diye soracaklar.

### 3.2 ABD — Benchmark Ekosistemi (MedHELM, Inspect Evals, HealthBench)

**Neden:** ABD benchmark ekipleri Chinese model coverage'da zayıf. MedFailBench bu boşluğu doldurur. Ayrıca worst-case safety framing'i HealthBench/MedHELM'de olmayan bir açı.

**Artefakt stratejisi:** `docs/MEDHELM_BRIDGE_SPEC.md`, `docs/MEDHELM_CROSSWALK_DRAFT.md`, `docs/HEALTHBENCH_MEDHELM_MAPPING_NOTE_V0_1.md` zaten mevcut. `outputs/medhelm_adapter_demo_v0_1.json` bir bridge demo'su olarak hazır.

**"Bunu kim yaptı?" tetikleyicisi:** MedHELM upstream issue draft'ı hazır (`docs/MEDHELM_UPSTREAM_ISSUE_DRAFT.md`). Bridge spec öyle yazılmış ki, bir MedHELM/HealthBench contributor'u crosswalk'ı gördüğünde "bunu yapan klinisyen kim?" diye bakacak.

### 3.3 Japonya — Clinical Safety + Bilingual Drift

**Neden:** Japonya, tıbbi AI safety'de aktif ve bilingual (JA/EN) modellerde drift problemi var. Türkçe benchmark'tan ilham alarak kendi dil güvenlik testlerini düşünebilirler. `docs/KURODA_MEETING_PREP_20260703.md` ve `docs/KURODA_MEETING_OUTCOME_20260704.md` zaten bir Japon akademik temasını gösteriyor.

**Artefakt stratejisi:** Turkish MedLLM safety pack (`tr_medllm_safetybench/`), bilingual drift testi için bir template olarak işlev görüyor. "Bu bir Türkçe benchmark, ama metodoloji dil-agnostik" mesajı.

---

## 4. "Beni Görün" Demeyeceğiz — Açık Artefakt Prensibi

Prensip: **Self-promotion değil, self-evident artefact.**

İnsanlara "bana bakın" demek yerine, öyle bir artefakt koyacağız ki, kendi kendini anlatan, kendi kendini meşrulaştıran, ve "bunu kim yaptı?" sorusunu doğal olarak doğuran bir şey olacak.

### Uygulanmış örnekler:

| Artefakt | Neden "bunu kim yaptı?" dedirtir |
|----------|----------------------------------|
| Worst-case safety report | Ortalama skorun sakladığı unsafe-tier promptları doğrudan gösterir |
| 10-model Çin karşılaştırması | Qwen, DeepSeek, GLM ve Kimi ailelerini aynı safety-gate çerçevesinde yan yana gösterir |
| MedHELM bridge spec | Bir klinisyenin upstream benchmark formatına bridge yazdığını gösterir |
| HF Space live leaderboard | Repoda kod var, Space canlı çalışıyor — talk değil, walk |
| CI/HF-router eval (gerçek çıktılar) | Simülasyon yok, gerçek model çağrıları, doğrulanabilir JSON çıktıları |

### Yapılmayacaklar:

- ❌ "Beni takip edin" tarzı self-promotion
- ❌ Aşırı iddialı başlıklar ("Dünyanın ilk/en iyi/benzersiz")
- ❌ Klinik doğrulama/ranking/sertifika ima etme
- ❌ Körü körüne model eleştirisi (veri konuşur)

---

## 5. 90 Günlük Odak

| Ay | Odak | Çıktı |
|----|------|-------|
| Ay 1 | Worst-case safety report'u zenginleştir, model ekiplerine issue olarak aç | Çin model ekiplerinden en az 1 yanıt |
| Ay 2 | MedHELM/HealthBench bridge'i tamamla, upstream PR gönder | En az 1 ABD benchmark ekosisteminde görünürlık |
| Ay 3 | arXiv preprint yayınla, Kuroda temasını derinleştir | Preprint + Japon akademik bağ |

---

## 6. Tek Cümle Özet

> MedFailBench, bir klinisyenin gözüyle medical AI safety failure'ı ölçen, açık artefaktlarla "bunu kim yaptı?" dedirten, Çin-ABD-Japonya üçgeninde kendine yer bulan bir benchmark altyapısıdır.

---

*Sürüm: v1.0 — Goktug Ozkan — 2026*
