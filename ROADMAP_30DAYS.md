# MedFailBench — 30 Günlük Yol Haritası

> **Başlangıç:** 2026-07-06 · **Bitiş:** 2026-08-04
> **Sürüm hedefi:** v0.2.1 → v0.3.0 arası görünürlük ve katkı döngüsü
> **Prensip:** Her hafta bir somut, dışarıdan doğrulanabilir artifact çıkar. İçeride kalmasın.

---

## Mevcut Durum Özeti (başlangıç noktası)

| Alan | Durum |
|---|---|
| Sürüm | v0.2.1 yayında, Zenodo DOI aktif |
| Vaka sayısı | Public core assets: 150 scenario-bank rows + 70 prompts. Repo also contains Failure Atlas intake, Turkish, and TR-EN drift preview layers. These are not one validation tier. |
| Model eval | 10 model, rule-based skorlu |
| Leaderboard | HF Space canlı |
| arXiv preprint | DRAFT hazır, submit onay bekliyor |
| MedHELM köprü | Discussion/issue route opened; spec and adapter demo exist; exact upstream wording must be checked before external follow-up |
| Inspect Evals | PR route opened/being reviewed if present; verify live upstream status before claiming completion |
| Klinik panel | 24 vaka hazır, hekim puanlaması bekleniyor |
| Sosyal | Draftlar hazır; dış post G onayı bekler |

---

## Hafta 1 (Gün 1–7) — Landing Temizleme + 3 Sert Bulgu

### Hedef
Public face'i hazır hale getir. 10 model sonuçlarından tartışması zor 3 bulgu çıkar. Bu bulgular sonraki 3 haftanın temelini oluşturacak.

### Görevler

#### 1.1 — Landing Page / README Temizliği (Gün 1–2)
- [ ] README.md: v0.2.1 verilerini net göster, eski erken-altküme referanslarını current claim gibi kullanma
- [ ] Leaderboard tablosunu "worst-case" görünümüyle birlikte öne çıkar — ortalama skoru öne çıkarma, unsafe-tier oranını göster
- [ ] HF Space: Çin frontier modelleri için filtre/gösterim ekle (kullanıcı "Chinese models only" seçebilsin)
- [ ] Repo'da `model_runs/` altındaki JSON'ları README'de doğrudan linkle — üçüncü taraf doğrulayabilsin
- [ ] Repo tag: `v0.2.1` at, GitHub Release oluştur (changelog ile)

#### 1.2 — 3 Sert Bulgu Çıkarımı (Gün 3–5)

10 model sonucundan çıkarılacak bulgular (data'ya dayalı, yorum değil):

**Bulgu #1 — Ortalama gizliyor: worst-case unsafe oranları kabul edilemez düzeyde**

> Qwen 3.7 Max: 30 promptun 14'ünde (%46.7) safety score 1–2/5 (unsafe tier).
> GLM-5.2: 28 promptun 11'inde (%39.3) unsafe tier.
> Qwen 3.6 Plus: 30 promptun 11'inde (%36.7) unsafe tier.
> Ortalama safety skorları 40–52 arası "kabul edilebilir" görünüyorsa da, tek bir unsafe yanıtın klinik sonucu vardır. Ortalama değil, worst-case konuş.

**Bulgu #2 — Source support: DeepSeek ailesi tutarlı biçimde zayıf**

> DeepSeek V4 Pro, V4 Flash, V3.2 — üçü de source support'da 48.0.
> Bu, "model bilmiyor" değil "destek olmadan iddia ediyor" demek. Kaynak bağlamayan tıbbi iddia, klinisyen gözünde en tehlikeli failure mode'lardan biri.

**Bulgu #3 — Çin frontier modelleri safety'de alt kümede kümeleniyor**

> 10 modelin 9'u Çin kökenli model ailesinden geliyor. Safety score'da en yüksek Çin modeli Qwen 2.5-7B (52.0) — bu da bu alt kümedeki küçük modellerden biri.
> Llama 3.1-8B (ABD) en yüksek safety'ye sahip (60.0).
> Daha büyük ≠ daha güvenli: Qwen 3.7 Max (en büyük Qwen) en düşük safety ortalamasına sahip (45.3) ve en yüksek unsafe oranına sahip (%46.7).
> Parametre sayısı arttıkça safety'nin düşmesi, benchmark'ın ölçtüğü şeyin (escalation, missing variable, source support) ölçekle çözülmeyen bir problem olduğunu gösteriyor.

- [ ] Bu 3 bulguyu `docs/HARD_FINDINGS_V0_2_1.md` olarak yaz (harici link verilebilir, alıntılanabilir)
- [ ] Her bulgu için: spesifik prompt ID'leri, ham model çıktısı örneği, rule-based skor gerekçesi

#### 1.3 — Hafta 1 Çıktısı
- [ ] Temiz landing page
- [ ] GitHub Release v0.2.1
- [ ] 3 bulgu dokümanı (dışarıdan doğrulanabilir, alıntılanabilir)

---

## Hafta 2 (Gün 8–14) — Çin Modelleri Raporu + Çoklu Platform Yayın

### Hedef
Çin modelleri için bağımsız kısa rapor. Bu raporu GitHub + HuggingFace + arXiv üzerinden yayınla. Rapor, Hafta 1 bulgularının derinlemesine versiyonu.

### Görevler

#### 2.1 — Çin Frontier Modelleri Kısa Raporu (Gün 8–11)
Kapsam: Qwen (2.5-7B, 3.6 Plus, 3.7 Max), DeepSeek (V4 Pro, V4 Flash, V3.2), GLM-5.2, Kimi (K2.6, K2.7 Code) — toplam 9 Çin-family model run.

- [ ] `docs/CHINESE_FRONTIER_SAFETY_REPORT.md` oluştur:
  - Family-by-family karşılaştırma tablosu
  - Her family için: safety trend, source support pattern, boundary pattern
  - Worst-case unsafe oranları family bazında
  - Spesifik failure örnekleri (prompt ID + ham çıktı + neden unsafe)
  - **Dikkat:** "Çin modelleri kötü" demek yok. "Bu modellerin bu benchmark'da bu pattern'leri var" demek var. Veri konuşur.
- [ ] İngilizce yaz (uluslararası erişim için), Türkçe executive summary ekle

#### 2.2 — arXiv Preprint Submit (Gün 12)
- [ ] `preprint/main.tex`'i güncelle: 10-model sonuçlarını + 3 bulguyu ekle
- [ ] Worst-case safety analizini formal section olarak ekle
- [ ] Çin frontier karşılaştırma tablosunu preprint'e dahil et
- [ ] tectonic build → PDF üret → arXiv submit
- [ ] Submit sonrası arXiv ID'yi README'ye ekle

#### 2.3 — Çoklu Platform Dağıtım (Gün 13–14)
- [ ] **GitHub:** Raporu repo'da `docs/` altında yayınla, GitHub Release'e linkle
- [ ] **HuggingFace:** Model sonuçlarını dataset olarak HF'ye yükle (`goktugozkanmd/medfailbench-v02-results`), Space'e linkle
- [ ] **arXiv:** Preprint submit tamam, arXiv ID alındıktan sonra her yerde referans ver
- [ ] Rapor için tek sayfalık özet görseli hazırla (failure rate bar chart, family comparison)

#### 2.4 — Hafta 2 Çıktısı
- [ ] Çin modelleri güvenlik raporu (bağımsız doküman)
- [ ] arXiv preprint submit edildi
- [ ] HF dataset + GitHub release güncellendi

---

## Hafta 3 (Gün 15–21) — MedHELM/Inspect Katkısı + Hedefli Public Post

### Hedef
MedFailBench'in ekosistem katkısını görünür kıl. MedHELM ve UK AISI Inspect Evals tarafında somut, alıntılanabilir katkı üret. Sonra bunu hedefli şekilde duyur.

### Görevler

#### 3.1 — MedHELM Katkısı (Gün 15–17)
- [ ] MedHELM discussion/issue hattını canlı kontrol et: maintainer yanıtı geldiyse, önerilen senaryo ailesinden bir mini-PR hazırla
- [ ] MedFailBench → MedHELM adaptörü yaz: en az 3 vaka'yı HELM-compatible scenario format'ına dönüştür (`scripts/medfailbench_to_medhelm_adapter.py`)
- [ ] Adapter'ın çalıştığını kanıtla: bir MedHELM scenario'su MedFailBench rubric'iyle skorlanabilsin
- [ ] MedHELM maintainer'larına güncel progress ile geri dön

#### 3.2 — UK AISI Inspect Evals Katkısı (Gün 18–19)
- [ ] Inspect Evals repo hattını canlı kontrol et: issue/PR zaten açıksa takip et, açılmadıysa küçük bakım/bug-fix PR rotası seç
- [ ] 1–2 bakım/bug-fix PR'ı hedefle: Inspect'in medical scenario test'lerinde küçük iyileştirme
- [ ] PR'lar merge edilirse: bunu STATE_LEDGER'da "Faz 1 kapı ölçütü" olarak işaretle

#### 3.3 — Hedefli Public Post (Gün 20–21)
Sosyal medyada "ben bir benchmark yaptım" demek yerine "ben ekosisteme şu katkıyı verdim" de.

- [ ] **LinkedIn post:** "MedFailBench'in MedHELM'e köprüsü: medical AI safety gate'lerini HELM formatına çeviren adaptör" — teknik, somut, katkı odaklı
- [ ] **X thread:** arXiv preprint + Çin model raporu + MedHELM adaptör — 3 tweet'lik thread, her tweet bir platform linki
- [ ] **Hedefli:** Post'u etiketle:
  - MedHELM maintainers
  - UK AISI Inspect team
  - HELM/Stanford CRFM
  - Çin model ekipleri (Qwen, DeepSeek, GLM, Kimi) — saygılı, "feedback için açık" tonuyla

#### 3.4 — Hafta 3 Çıktısı
- [ ] MedHELM adaptörü (çalışan kod + en az 3 dönüştürülmüş senaryo)
- [ ] Inspect Evals'da açılmış issue / merge edilmiş PR
- [ ] 1 LinkedIn + 1 X thread, ekosistem katkısına odaklı

---

## Hafta 4 (Gün 22–30) — Cold Outreach + Görünürlük Amplifikasyonu

### Hedef
İlk 3 haftanın artifact'lerini doğru insanlara ulaştır. Model ekiplerine doğrudan feedback gönder. Toplulukta "bu adam ciddi bir şey yapıyor" algısı oluştur.

### Görevler

#### 4.1 — Model Ekiplerine Cold Outreach (Gün 22–25)
Her Çin model ekibi için özelleştirilmiş, kısa, veri-odaklı mesaj:

- [ ] **Qwen (Alibaba):** Worst-case unsafe oranı (%46.7 for 3.7 Max) + spesifik prompt örnekleri. "İşte 3 prompt'ta modelinizin verdiği yanıtlar ve safety skoru. İçeride test etmek isterseniz prompt set'i açık."
- [ ] **DeepSeek:** Source support tutarlı 48.0 → "Modeliniz kaynak bağlamadan tıbbi iddia veriyor. İşte 5 örnek."
- [ ] **GLM (Zhipu):** %39.3 unsafe tier → "İşte hangi safety gate'lerinde fail ettiği."
- [ ] **Kimi (Moonshot):** En düşük safety skorları → "İşte missing-variable ve escalation-wording örnekleri."

**Ton:** Suçlayıcı değil. "Veriyi paylaşıyorum, kullanmak isterseniz açık" tonu. AMA sonuçları net.

- [ ] Outreach mesajlarını `docs/MODEL_TEAM_FEEDBACK_OUTREACH.md` olarak taslağa koy (G onayından sonra gönderim)
- [ ] Llama/Meta ekibine: "Sizin model en yüksek safety'de, işte karşılaştırmalı veri" — olumlu feedback

#### 4.2 — LinkedIn/X Görünürlük Amplifikasyonu (Gün 26–28)
Amaç: veriyle ses çıkarma, varlığını hissettirme, tartışma başlatma.

- [ ] **LinkedIn carousels/infographic:** "10 Model, 3 Sert Bulgu" — görsel, paylaşılabilir format
- [ ] **X:** Bulgu bazlı thread'ler (her bulgu için ayrı thread, ayrı gün):
  - Gün 26: "Ortalama sizi kandırır" — worst-case unsafe oranları
  - Gün 27: "Kaynak olmadan iddia" — DeepSeek source support
  - Gün 28: "Daha büyük ≠ daha güvenli" — Çin model scale vs safety
- [ ] **Reddit:** r/LocalLLaMA ve r/MachineLearning'de "Clinician-built medical AI safety benchmark — 10 model results" başlıklı post (H-N kurallarına uygun)
- [ ] **HackerNews:** "Show HN: Medical AI Failure Atlas — clinician-built benchmark" (düşük saman kağıdı, yüksek içerik)

#### 4.3 — 30. Gün Değerlendirmesi (Gün 29–30)
- [ ] ROADMAP'i gözden geçir: hangi görevler tamam, hangileri ertelendi
- [ ] STATE_LEDGER.md'yi güncelle: 30 günün kazanımlarını yaz
- [ ] Sonraki 30 gün için rough plan (v0.3.0 hedefleri)
- [ ] Metrik topla: GitHub stars, HF Space views, arXiv downloads, outreach yanıt oranları

#### 4.4 — Hafta 4 Çıktısı
- [x] 4 model ekibine personalized feedback gönderimi (G onayı sonrası)
- [x] 3 X thread + 1 LinkedIn carousel + 1 Reddit post + 1 HN post
- [x] 30-gün değerlendirme dokümanı

---

## Başarı Ölçütleri (30. günde)

| Metrik | Hedef |
|---|---|
| GitHub stars | ≥ 100 (başlangıç ~50 tahmini) |
| arXiv preprint indirme | ≥ 50 |
| HF Space unique visitors | ≥ 500 |
| Model ekibi yanıtı | ≥ 2/4 ekip yanıt verdi |
| MedHELM/Inspect katkısı | ≥ 1 merge veya maintainer onayı |
| Dış alıntılanma | ≥ 1 blog/tweet/forum'da alıntı |

---

## Riskler ve Mitigasyonlar

| Risk | Etki | Mitigasyon |
|---|---|---|
| Model ekipleri yanıtsız kalır | Düşük | Public veri zaten değerli; outreach bonus. Yanıt olmasa da rapor yayınlandı. |
| arXiv reddi | Orta | Preprint'i medRxiv'e fallback olarak hazırla. Format sorununu önceden çöz. |
| "Anti-Çin" algısı | Yüksek | Raporda dil çok dikkatli: veri odaklı, family bazında, yorum değil. Llama dahil tüm modeller aynı kritere tabi. |
| Clinician panel gecikmesi | Orta | 30-gün planı rule-based skorlara dayanır; panel onayı sonraki faz. |
| HN/Reddit düşük etkileşim | Düşük | Başlık ve zamanlama optimize et. En azından arXiv + GitHub referansı kalıcı. |

---

## Bağımlılıklar ve Onaylar

- **G onayı gerektiren:** Model ekibi outreach gönderimi, arXiv submit, sosyal medya postları
- **Dış bağımlılık:** MedHELM maintainer yanıtı, Inspect Evals PR review, arXiv review süreci
- **Ön koşul:** Hafta 1 bulguları olmadan Hafta 2–4 anlamlı değil. Sıra önemli.

---

> Bu yol haritası canlı bir dokümandır. Her hafta sonu güncellenir.
> Sahibi: G · Hazırlayan: Mercury · Son güncelleme: 2026-07-06
