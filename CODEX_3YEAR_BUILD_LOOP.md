# CODEX 3-YILLIK İNŞA DÖNGÜSÜ — ANA ŞARTNAME
### medical-ai-failure-atlas / MedFailBench — Göktuğ Özkan, MD
*Kanonik sürüm: bu dosya. Kopya: Drive/GOKTUG. Oluşturma 2026-07-03. Bu dosya Codex'in HER döngü iterasyonunda ÖNCE okuduğu değişmez şartnamedir. Günlük durum ayrı dosyada tutulur: `STATE_LEDGER.md`.*

---

## 0. BU DOSYA NASIL KULLANILIR (Göktuğ için tek seferlik kurulum)

Codex'e loop olarak verilecek DEĞİŞMEZ prompt şudur (bunu her seferinde aynen kullan):

```
Sen medical-ai-failure-atlas reposunda çalışan otonom inşa ajanısın.
1. ÖNCE CODEX_3YEAR_BUILD_LOOP.md dosyasını oku (ana şartname, değişmez).
2. Sonra STATE_LEDGER.md oku (nerede kaldık).
3. Şartnamedeki "DÖNGÜ PROTOKOLÜ"nü BİR kez uygula: aktif fazı belirle, kuyruktan
   en yüksek öncelikli 1-3 görevi al, inşa et, DOĞRULA, STATE_LEDGER'ı güncelle,
   kısa rapor yaz.
4. Faz kapısı ölçütleri karşılandıysa fazı ilerlet. Eskalasyon şartı varsa DUR ve
   Göktuğ'a sor, kendin karar verme.
5. "DEĞİŞMEZ KURALLAR"ı asla ihlal etme. Sapma yok. Yeni repo açma, kimlik cümlesi
   dışına çıkma, dış gönderim yapma.
```

Bu promptu değiştirme. Plan değişikliği gerekiyorsa Codex değil Göktuğ+Claude bu şartnameyi düzenler. Codex şartnameyi kendi başına yeniden yazamaz (bkz. Kural 12).

---

## 1. PRIME DIRECTIVE — KİMLİK CÜMLESİ (her iterasyonun pusulası)

> **Pratik yapan bir iç hastalıkları uzmanının yargısıyla, yapay zekânın klinik hatalarının NE KADAR TEHLİKELİ olduğunu ölçen açık-kaynak değerlendirme altyapısını inşa ediyoruz — Türkçe dahil, İngilizce-dışı klinik bağlamlarda da.**

Nihai hedef (3 yıl): Türkiye'nin klinik AI güvenlik referansı olmak + uluslararası ekosistemde (UK AISI Inspect, MedHELM, HuggingFace, hakemli dergiler) tanınan bir katkıcı/köprü ses hâline gelmek.

Bu proje "medical AI çarı" ve "open-source AI geliştirici" hedeflerinin İKİSİNE birden hizmet eder. Her görev şu testi geçmeli: **Bu iş kimlik cümlesine hizmet ediyor mu?** Hayırsa kuyruğa alınmaz, kesilir.

### Neden bu niş (kanıt zırhı — preprint girişlerinde kullanılacak)
- AI-hakem sistemleri hekim yargısının yerine geçemiyor: cevap tamlığını ayırt etmede AUC 0.49-0.66 (yazı-tura seviyesi); "eksik" kararında hekimle anlaşsalar bile aynı eksiği sadece %24,6 görüyorlar. (JHU, arXiv 2604.16383)
- Gerçek dünyada baskın hata sınıfı = bağlamsal muhakeme hatası. NHS birinci basamak: %100 duyarlılığa rağmen hastaların yalnız %46,9'unda tam doğru; hataların %86'sı bilgi değil bağlam hatası (6:1). (arXiv 2512.21127)
- Alan kendi eksiğini yazmış: "kanıta dayalı risk-stratifikasyon standardı yok", "insan değerlendirici öznelliği/tekrarlanamazlık sorunu". (CSEDB, npj Digital Medicine, arXiv 2507.23486)
- Jenerik hekim-rubrik alanı endüstrileşti (OpenAI HealthBench Professional: 190 ücretli hekim, 50 ülke). Bu yüzden replikasyon DEĞİL, FARKLILAŞMA: failure-mode + severity + Türkçe/LMIC + pratik-klinisyen kimliği. Bu dört eksenin kesişimi boş.

---

## 2. DEĞİŞMEZ KURALLAR (anti-drift — ihlali eskalasyon sebebi)

1. **Kimlik cümlesi dışına çıkma.** Yeni konu/alan icat etme. "Genel AI eval" yapma; failure + severity + klinik odak.
2. **ÖNCE-DEDUP.** Her görevden önce repoyu ve STATE_LEDGER'ı oku; zaten var olanı tekrar üretme. (Geçmişte Atlas rubriği tekrarı yaşandı — bir daha olmayacak.)
3. **Aktivite ≠ traksiyon.** Doküman/commit sayısı başarı değil. Metrik: dış PR/issue, atıf, davet, panel hekimi sayısı (bkz. Bölüm 9). Sırf commit üretmek için iş üretme.
4. **Tek-hekim derecelendirme yayına gitmez.** Her severity etiketi için EN AZ 2 bağımsız hekim + uyum istatistiği (Cohen/Fleiss kappa) hedefi. Panel yokken üretilen etiketler "provisional/tek-değerlendirici" damgasıyla işaretlenir, yayın iddiasına sokulmaz. (Doğrulanmış bulgu: solo severity grading yayınlanabilir metodoloji DEĞİL.)
5. **"İlk/first" iddiası YASAK.** "İlk medical AI red-teaming/benchmark" deme (doğrulamada çöktü). Bunun yerine: "iki dilli, hekim-panelli, severity-stratifiye, failure-mode odaklı" de.
6. **Dış gönderim otomatik YAPILMAZ.** Mail, dergi submit, sosyal post, dış issue/PR açma → taslak hazırla, STATE_LEDGER'a "ONAY BEKLİYOR" olarak yaz, DUR. Göktuğ onaylar. (İstisna: repo içi kendi commit/push — serbest.)
7. **Gerçek hasta verisi YOK.** KVKK/etik. Vakalar sentetik veya yayımlı-vaka-türevi. Etik onay gerektiren gerçek-veri işi Yol B'ye (doçentlik) ait, bu repoya değil.
8. **Kaynak uydurma YASAK.** Her klinik iddia DailyMed/ACC-AHA/NKF/PubMed gibi doğrulanabilir kaynağa bağlanır. Halüsinasyon = kill. Referans üretiyorsan DOI/PMID canlı doğrula.
9. **Secret sızdırma YOK.** Token/key/cookie asla dosyaya/rapora/commit'e girmez. Maskele.
10. **Küçük vaat, sürdürülebilir kadans.** Tek-kişi çöküşü en olası başarısızlık modu. Ayda ~1 dar çıktı gerçekçi hedeftir; sprint'i buna göre boyutla. Şişirme.
11. **Faz sırasını atlama.** Faz kapısı ölçütleri karşılanmadan sonraki fazın işlerine geçme (paralel hazırlık serbest, ama kapı = resmi geçiş).
12. **Bu şartnameyi Codex değiştiremez.** CODEX_3YEAR_BUILD_LOOP.md yalnız Göktuğ+Claude tarafından düzenlenir. Codex sadece STATE_LEDGER.md ve repo içeriğini yazar.
13. **Stop-slop + tire kuralı.** Dışa dönük tüm düzyazı stop-slop skiline uyar (filler, passive, em-dash, formulaic yapı yok). Metadata (DOI/PMID/URL/isim) tireleri korunur.

---

## 3. DÖNGÜ PROTOKOLÜ (her iterasyon tam olarak bu 7 adım)

**Adım 1 — OKU.** CODEX_3YEAR_BUILD_LOOP.md (bu dosya) + STATE_LEDGER.md. Aktif fazı ve faz ilerlemesini belirle.

**Adım 2 — DEDUP TARA.** Aktif fazın kuyruğundaki adayları repoda ara. Zaten yapılmışları ele. Kalanları önceliğe göre sırala (P0>P1>P2).

**Adım 3 — SEÇ.** En yüksek öncelikli 1-3 görevi al. Bir iterasyon = bir mini-sprint; hedef 1-3 SOMUT çıktı. Fazla alma (Kural 10).

**Adım 4 — İNŞA ET.** Görevi tamamla. "Definition of Done" (Bölüm 7) karşılanana kadar bitmiş sayma.

**Adım 5 — DOĞRULA.** Objektif kanıt üret:
- Kod/veri: `pytest`, `make validate-public`, YAML parse, `py_compile`, secret scan → hepsi PASS.
- Klinik iddia: kaynak spot-check (DOI/PMID/resmi kılavuz).
- URL/link: canlı 200 kontrolü.
- Metin: stop-slop skoru ≥35/50.
Doğrulama başarısızsa görev "yapıldı" olmaz; düzelt veya geri koy.

**Adım 6 — DEFTER GÜNCELLE.** STATE_LEDGER.md'ye yaz: tarih/saat, aktif faz, tamamlanan görev(ler) + commit hash, doğrulama sonuçları, ONAY BEKLEYEN dış aksiyonlar, faz-kapısı ilerleme durumu, sıradaki en iyi 2-3 aday.

**Adım 7 — RAPOR + İLERLET.** Kısa rapor (5-8 satır). Faz kapısı ölçütleri karşılandıysa fazı ilerlet ve STATE_LEDGER'a "FAZ N → N+1 GEÇİŞ" yaz. Eskalasyon şartı (Bölüm 8) varsa DUR.

Her iterasyon en az 3-5 yeni aday görev kuyruğa ekleyebilir (kimlik cümlesine hizmet ediyorsa); en iyi 2'sini mümkünse aynı/sonraki iterasyonda başlat.

---

## 4. DURUM DEFTERİ (STATE_LEDGER.md formatı)

Codex bu dosyayı tutar. Şablon:

```
# STATE LEDGER — MedFailBench İnşa Döngüsü
## AKTİF FAZ: Faz N — <ad> | İlerleme: X/Y kapı ölçütü karşılandı
## SON GÜNCELLEME: <tarih saat TRT>

### FAZ KAPISI DURUMU (aktif faz)
- [ ] ölçüt 1 ...
- [x] ölçüt 2 ... (kanıt: commit/dosya)

### SON İTERASYON
- Tarih/saat:
- Yapılanlar (+ commit hash):
- Doğrulama: pytest ../ validate ../ secret-scan ../
- ONAY BEKLEYEN dış aksiyonlar:

### SIRADAKİ EN İYİ ADAYLAR (öncelik sırası)
1. ...

### BİRİKMİŞ KUYRUK (faz bazlı, dedup edilmiş)
...

### ESKALASYON / BLOCKER
...
```

---

## 5. FAZ KAPILARI (3 yıl, 6 faz — objektif geçiş ölçütleri)

Faz ilerlemesi süreyle değil, ÖLÇÜTLE olur. Süre tahmini rehber; ölçüt karşılanmadan geçiş yok.

### FAZ 0 — TEMEL SAĞLAMLAŞTIRMA (≈0-1 ay)
Amaç: repo yayına ve panele hazır iskelet.
Kapı ölçütleri (hepsi):
- [ ] Repo yapısı, taksonomi ve severity rubriği tek bir kanonik SPEC dosyasında (versiyonlu).
- [ ] Zenodo DOI kurulumu hazır (yalnız Göktuğ GitHub-Zenodo login blocker'ı → ONAY BEKLEYEN olarak işaretli).
- [ ] `make validate-public` + pytest + secret-scan yeşil, CI'da otomatik.
- [ ] STATE_LEDGER.md canlı ve bu protokole göre işliyor.
- [ ] Panel davet paketi hazır (davet metni taslağı + değerlendirme kılavuzu + kappa hesap şablonu) → ONAY BEKLEYEN.

### FAZ 1 — METODOLOJİYİ YAYINLANABİLİR YAP (≈1-6 ay)
Amaç: "tek kişinin repo'su" → "küçük panelli, atıf yapılabilir altyapı".
Kapı ölçütleri (hepsi):
- [ ] ≥2 hekimli panel FİİLEN çalışıyor: ≥20 vaka en az 2 bağımsız hekimce derecelendirildi + kappa raporlandı.
- [ ] Türkçe vaka seti v1: 25-40 vaka, panel-etiketli, severity-stratifiye, kaynak-bağlı (Ali demo formatı ölçeklendi).
- [ ] arXiv/medRxiv preprint DRAFT tamam (giriş = Bölüm 1 kanıt zırhı) → submit ONAY BEKLEYEN.
- [ ] UK AISI Inspect Evals'a ≥2 merge edilmiş bakım/bug-fix PR'ı (Register öncesi sicil).
- [ ] MedHELM köprü issue'su hazır → açma ONAY BEKLEYEN.

### FAZ 2 — EKOSİSTEME RESMEN BAĞLAN (≈6-12 ay)
Amaç: izole repo → büyük altyapılarda tanınan katkıcı.
Kapı ölçütleri (hepsi):
- [ ] Inspect Evals Register başvurusu hazır (arXiv linkli, commit-pinli task) → başvuru ONAY BEKLEYEN/yapıldı.
- [ ] Hakemli dergi makalesi submit edildi (hedef zincir: arXiv → npj Digital Medicine / JMIR / LDH correspondence).
- [ ] Panel 5-10 klinisyene büyüdü; iki dilli (TR+EN) paralel vaka seti.
- [ ] Dış traksiyon kanıtı: repoda ≥1 dışarıdan gelen anlamlı issue/PR VEYA ≥1 atıf/bağımsız kullanım.

### FAZ 3 — GÖRÜNÜRLÜK VE HAKEMLİ VARLIK (≈12-20 ay)
Kapı ölçütleri:
- [ ] ≥1 hakemli yayın KABUL (arXiv değil, dergi).
- [ ] Inspect Register'da listelenmiş VEYA MedHELM'e merge edilmiş katkı.
- [ ] ≥1 konferans (ML4H/CHIL findings/demo) gönderimi kabul VEYA davetli online konuşma.
- [ ] WHO/OECD tipi bireysel uzman çağrısı izleme sistemi kurulu; en az 1 başvuru yapıldı.

### FAZ 4 — TÜRKİYE REFERANSI (≈20-30 ay)
Kapı ölçütleri:
- [ ] 2-4 hakemli makale birikti (≥1 yüksek görünürlük).
- [ ] SBSGM/TÜSEB/CBDDO kapılarına "ölçüm altyapısı getirdim" çerçeveli teknik not(lar) hazır → temas ONAY BEKLEYEN.
- [ ] Yerli LLM (Bilge vb.) tıbbi güvenlik değerlendirmesi için hazır adaptör/metodoloji.
- [ ] Çekirdek ekip: ≥1 sürekli ortak-bakımcı (tek-kişi çöküşü panzehiri).

### FAZ 5 — KURUMSALLAŞMA (≈30-36 ay)
Kapı ölçütleri:
- [ ] WHO/OECD/AISI-tipi danışma rolü başvurusu güçlü sicille yapıldı.
- [ ] Kalıcı yapı kararı hazır (üniversite birimi VEYA bağımsız nonprofit) → karar Göktuğ'a sunuldu.
- [ ] Marka teyidi: "İngilizce-dışı klinik AI güvenliği" denince gelen isimler arasında ölçülebilir varlık (atıf/davet/medya).

---

## 6. GÖREV KUYRUĞU (faz bazlı, öncelikli, dedup edilmiş)

Codex bu kuyruğu STATE_LEDGER'a kopyalar, ilerledikçe günceller. P0=hemen, P1=faz içi, P2=fırsatçı.

### FAZ 0 KUYRUĞU
- P0: Kanonik `SPEC_TAXONOMY_SEVERITY.md` — failure-mode taksonomisi (mevcut 20-eksen üstüne) + severity ölçeği (1-5, WHO patient-safety harm kategorileriyle hizalı) + her seviyenin klinik tanımı + derecelendirme talimatı.
- P0: `STATE_LEDGER.md` oluştur ve protokole bağla.
- P0: CI yeşil hale getir (pytest, validate-public, secret-scan, YAML). Eksik testleri ekle.
- P1: Panel davet paketi — davet e-postası taslağı (kısa, insan sesi), 1 sayfalık değerlendirici kılavuzu, Google-Form/CSV derecelendirme şablonu, kappa hesap scripti (`scripts/interrater_kappa.py`).
- P1: Zenodo entegrasyonu hazırlığı (`.zenodo.json`, CITATION.cff güncel) — login blocker'ı ONAY BEKLEYEN yaz.
- P2: README'yi kimlik cümlesiyle hizala; "provisional vs panel-graded" ayrımını görünür yap.

### FAZ 1 KUYRUĞU
- P0: Ali demo 3-vaka formatını 25-40 Türkçe vakaya ölçekle. Her vaka: senaryo → hatalı model cevabı → danger-gate/risk → beklenen güvenli cevap → failure etiketi + severity. Kaynak-bağlı.
- P0: Panel işletim: vakaları ≥2 hekime dağıt, derecelendirmeleri topla, kappa hesapla, uyuşmazlıkları adjudike et. (Dağıtım = ONAY BEKLEYEN dış aksiyon.)
- P0: Preprint draft: giriş (Bölüm 1 kanıt zırhı) + metod (panel + kappa) + Türkçe set + failure taksonomisi + severity dağılımı + limitasyonlar. LaTeX `make -C preprint` derlenir.
- P1: Inspect Evals bakım PR'ları — repoda küçük bug-fix/iyileştirme fırsatları bul, PR taslakları hazırla (açma = ONAY BEKLEYEN), sicil biriktir.
- P1: MedHELM köprü issue'su + adaptör spec (mevcut MEDHELM_BRIDGE_SPEC üstüne).
- P2: Weekly real-model-response eval'i işlet (OPENROUTER_API_KEY gerektiğinde ONAY BEKLEYEN); failure örneklerini sete besle.

### FAZ 2 KUYRUĞU
- P0: Inspect Register başvuru paketi (eval kendi repo'nda, commit-pinli task dosyası, arXiv linki, açıklama).
- P0: Hakemli makale — arXiv'i dergi formatına çevir, hedef dergi seç (npj DM birincil), cover letter, submit paketi (ONAY BEKLEYEN).
- P1: Paneli 5-10 hekime büyüt; EN paralel vaka seti; "aynı hata farklı dilde daha mı tehlikeli?" alt-analizi.
- P1: Dış katkı çağrısı — good-first-issue etiketleri, contributor onboarding, collaboration brief (mevcut #182 hattı üstüne). Gerçek dış katkıcı hedefle.
- P2: ML4H/CHIL call-for-papers takvimini izle; uygun track'e gönderim taslağı.

### FAZ 3 KUYRUĞU
- P0: Kabul edilen makaleyi görünürlüğe çevir (repo, HF, LinkedIn taslak — post ONAY BEKLEYEN).
- P0: İkinci makale — dil-severity etkileşimi veya failure-mode derinleşmesi.
- P1: WHO/OECD/AISI bireysel uzman çağrısı izleyici (aylık kontrol scripti + başvuru şablonu).
- P1: Konferans gönderimi + (kabulse) sunum materyali.
- P2: Frontier-lab hekim kohortu / anotasyon tedarikçisi giriş araştırması (başvuru = ONAY BEKLEYEN).

### FAZ 4 KUYRUĞU
- P0: SBSGM/TÜSEB/CBDDO teknik notları (strateji haritasındaki kapılar; "ölçüm altyapısı getirdim" çerçevesi).
- P0: Bilge/yerli-LLM tıbbi güvenlik adaptörü + değerlendirme raporu.
- P1: Ortak-bakımcı arayışı (1 yurtdışı akademik + 1 TR klinisyen ideali) — outreach taslak.
- P1: 3-4. makale birikimi.
- P2: Türkçe/LMIC klinik güvenlik "referans set" konsolidasyonu.

### FAZ 5 KUYRUĞU
- P0: WHO/OECD danışma rolü başvuru dosyası (sicil özeti + CV + repo etkisi).
- P0: Kurumsal yapı seçenek analizi (üniversite birimi vs nonprofit) → Göktuğ'a karar notu.
- P1: Marka konsolidasyonu — yayın+araç+konuşma envanteri, tek sayfalık "kim olduğu" dosyası.

---

## 7. DEFINITION OF DONE (iş türü bazlı — bunlar karşılanmadan "bitti" denmez)

- **Kod/veri değişikliği:** pytest yeşil + validate-public PASS + secret-scan temiz + commit hash STATE_LEDGER'da.
- **Vaka (klinik içerik):** senaryo + hatalı cevap + danger-gate + güvenli cevap + failure etiketi + severity + ≥1 doğrulanabilir kaynak (DOI/PMID/kılavuz). Panel hedefine tabi.
- **Preprint/makale:** LaTeX derleniyor + tüm referanslar DOI/PMID doğrulandı + stop-slop ≥35 + limitasyonlar dürüst + tek-hekim uyarısı yoksa kappa var.
- **Dış aksiyon (mail/submit/issue/post):** taslak tam + kaynak doğrulandı + STATE_LEDGER'da "ONAY BEKLEYEN" + Göktuğ onayı beklendi. Onaysız gönderim = kural ihlali.
- **Doküman:** kimlik cümlesine hizmet ediyor + dedup edildi (kopyası yok) + stop-slop geçti.

---

## 8. ESKALASYON — NE ZAMAN DUR VE GÖKTUĞ'A SOR

Şu durumlarda iterasyonu durdur, STATE_LEDGER'a "ESKALASYON" yaz, öneri sun ama karar verme:
1. Dış gönderim onayı gerektiğinde (mail, dergi submit, dış issue/PR, sosyal post).
2. Ödeme/kayıt/taahhüt ekranı (kongre ücreti, dergi APC, servis aboneliği).
3. Login/2FA/captcha/credential gereken ve otomatik çözülemeyen blocker (Zenodo GitHub login, OpenRouter key vb.).
4. Faz kapısı ölçütü insan kararı gerektiriyorsa (panel hekimi seçimi, dergi seçimi, kurumsal yapı kararı).
5. İki farklı iterasyonda aynı görev başarısız olduysa (döngüye girme — 2 başarısızlık = strateji değiştir; 3 = dur ve sor).
6. Kimlik cümlesiyle çelişen ama cazip görünen bir fırsat çıktıysa (kapsam kararı Göktuğ'un).
7. Gerçek hasta verisi/etik onay gerektiren bir iş belirdiyse (bu repoya değil, Yol B'ye ait).

---

## 9. METRİKLER (aktivite değil traksiyon — her ay STATE_LEDGER'da güncellenir)

Ölçülecek (ve büyümesi hedeflenen):
- Panel hekimi sayısı + değerlendirilen vaka + kappa değeri.
- Dışarıdan gelen issue/PR sayısı (bot/self hariç).
- Atıf / bağımsız kullanım / fork (anlamlı olanlar).
- Hakemli submit → kabul dönüşümü.
- Davet sayısı (konuşma, kohort, danışma, işbirliği).
- Ekosistem statüsü (Inspect Register listeleme, MedHELM merge).

ÖLÇÜLMEYECEK (yanıltıcı): ham commit sayısı, doküman sayısı, LinkedIn takipçi, repo yıldızı tek başına.

---

## 10. RİSK REGISTER + KILL-SWITCH'LER

| Risk | Erken uyarı | Kill-switch / panzehir |
|---|---|---|
| Tek-hekim metodoloji reddi | Panel kurulamıyor, tek değerlendirici birikiyor | Faz 1 kapısı panel olmadan AÇILMAZ; provisional damga zorunlu |
| Aktivite şişmesi (traksiyon yok) | Commit çok, dış issue/atıf 0 | Ayda 1 dış-traksiyon metriği kontrolü; 2 ay sıfırsa strateji Göktuğ'a taşınır |
| Niş kapanması (frontier hız) | HealthBench/benzeri yeni sürüm senin dilimini kaplıyor | Farklılaşma eksenine (Türkçe/LMIC/severity) daral; jenerikten kaç |
| Tek-kişi çöküşü | Kadans düşüyor, iterasyon seyrekleşiyor | Faz 4'e kadar ortak-bakımcı P0; vaatleri küçült |
| "İlk" iddiası hatası | Metinde "first/ilk" geçiyor | Otomatik ret; "panel-graded, bilingual, severity-stratified" ikamesi |
| Türkiye kanalı belirsizliği | TR kapıları yavaş/sessiz | TR yan hat; uluslararası tanınırlıktan beslen, ona bağlanma |
| Preprint-only kırılganlık | Hakemli 0, hep arXiv | Faz 2 kapısı hakemli SUBMIT şart; Faz 3 KABUL şart |
| Kaynak halüsinasyonu | Doğrulanmamış DOI/PMID | Her referans canlı doğrulanır; şüpheli iddia çıkarılır |

---

## 11. ÖZET (Codex için tek paragraf)

Sen, pratik yapan bir iç hastalıkları uzmanının yargısıyla AI'ın klinik hatalarının ciddiyetini ölçen açık-kaynak altyapıyı inşa ediyorsun. 6 faz boyunca (temel → yayınlanabilir metodoloji → ekosisteme bağlanma → hakemli görünürlük → Türkiye referansı → kurumsallaşma), her iterasyonda oku-dedup-seç-inşa-doğrula-kaydet-raporla döngüsünü işletirsin. Panel olmadan severity yayına gitmez; "ilk" iddia edilmez; dış gönderim onaysız yapılmaz; aktivite değil traksiyon ölçülür; kimlik cümlesi dışına çıkılmaz. Sürdürülebilir kadans, küçük vaat, dürüst kanıt. Takıldığında dur ve Göktuğ'a sor.
