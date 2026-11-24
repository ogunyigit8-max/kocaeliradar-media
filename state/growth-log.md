# Kocaeli Radar — Büyüme Analizi Günlüğü

## 2026-11-16 (Pzt, 23:30 TSİ) — ilk analiz
**Kendi metriklerimiz (Windsor.ai, instagram, hesap 17841471927275359):** 107 takipçi, 10 Reels (hepsi 16.11). 15.11 profil erişimi 2.749, +2 takipçi; 16.11 günlük takipçi verisi henüz yok.
| Saat (TSİ) | Konu | Erişim | Atlama (ilk 3 sn) | Ort. izlenme | Beğeni/Paylaşım/Kayıt |
|---|---|---|---|---|---|
| 19:42 | Gebze minibüs kazası (son dakika) | 1.524 | %38 | 9,3 sn | 22/2/1 |
| 06:34 | Esnaf kapanışları (871, %109) | 1.376 | %38 | 11,6 sn | 14/13/4 |
| 14:37 | Valilik sağanak uyarısı | 1.200 | %51 | 5,5 sn | 6/3/1 |
| 06:00 | Darıca enginarı (47 sn) | 1.184 | %41 | 8,9 sn | 4/0/1 |
| 12:37 | COP31 yeşil lojistik | 1.167 | %47 | 7,3 sn | 2/0/1 |
| 11:53 | Elektrik kesintisi (10 ilçe) | 1.140 | %51 | 7,7 sn | 9/9/0 |
| 06:28 | İzmit Körfezi çamur | 187 | %56 | 7,0 sn | 2/0/0 |
| 06:33 | Derince hastane | 182 | %50 | 6,1 sn | 2/0/0 |
| 12:36 | Akaryakıt fiyatları | 157 | %62 | 4,7 sn | 2/0/0 |
| 06:27 | Hava (pastırma yazı) | 127 | %58 | 5,7 sn | 2/0/0 |
- Bulgu: dakikalar içinde peş peşe atılan videolarda dağıtım 1–2 videoda toplanıyor (diğerleri ~150 erişim). → min. 60 dk aralık kuralı.
- Bulgu: somut sayı + insan etkisi olan başlıklar en düşük atlama/en yüksek izlenme. Salt fiyat listesi ve genel hava en zayıf.
- Ses eşleştirmesi (Emre/Aylin) yapılamadı: state/pending.json boş, video başına ses kaydı tutulmuyor. Öneri: üretim görevi pending/breaking kaydına "voice" alanı yazsın.

**Kalite bulguları (tools/news.py incelemesi + ölçüm):**
- Müzik çok yüksek: Gebze videosunda 100 ms pencerelerde konuşma medyanı −14,6 dBFS, konuşma arası taban −19/−20 dBFS → müzik sesin yalnızca ~5–8 dB altında. Kaynaklar anlatım altı müzik için 18–24 dB fark öneriyor. Kodda music(T)*0.5*duck (duck yalnızca −4,4 dB). Öneri: müzik kazancı 0.5→~0.15–0.2, duck 0.4→0.75 (≈−12 dB), müzikte 800–3000 Hz'te 3–6 dB kesme; davul/hi-hat seviyesini düşür.
- Altyazı y=1560 (alt %19) ve kaynak y=1790: Instagram caption/buton alanına giriyor (Hopper: alt %35; TryMyPost: alt 280 px — kaynaklar çelişkili). Öneri: altyazıyı ~y=1380–1420'ye al.
- Altyazı zamanlaması harf sayısıyla tahmin ediliyor. Cartesia SSE `add_timestamps=true` kelime zaman damgası veriyor (Türkçe desteği doğrulanmadı) → gerçek senkron + kelime vurgulu altyazı mümkün.
- Speko ölçümü: Emre 196 kelime/dk ("fast"), Aylin 169 kelime/dk. Emre için Cartesia generation_config speed≈0.9 denenebilir. Alternatif Türkçe ses: Cartesia Azra/Aykut (tiz/sibilans uyarısı var), Azure Elif MAI-Voice-2.1 (ölçülmemiş). Değişiklik için kulak testi gerekli.

**Kaynaklar:**
- Algoritma (izlenme süresi, beğeni/erişim, gönderim/erişim; 3 dk sınırı; orijinallik): https://blckalpaca.at/en/knowledge-base/social-media/social-media-algorithms-distribution/instagram-algorithm-2026 , https://creatorflow.so/blog/instagram-algorithm/ , https://www.reeldrop.io/learn/instagram-algorithm (blog aktarımları; Meta birincil kaynağı açılmadı)
- Güvenli alan: https://www.hopperhq.com/blog/instagram-reel-size/ , https://www.trymypost.com/blog/instagram-reels-safe-zones-text-placement-2026
- Müzik seviyesi: https://www.overseeros.com/blog/background-music-volume-under-voiceover , https://vidpros.com/fix-background-music-too-loud-video/
- Cartesia zaman damgası: https://docs.cartesia.ai/api-reference/tts/sse.md , https://docs.cartesia.ai/examples/tts-sse-with-timestamps.md
- İzlenecek rakip: @kocaeligundem (https://hypeauditor.com/instagram/kocaeligundem/ — rakamlar okunmadı)

**Bildirilen öneriler (tekrar bildirme):** (1) min. 60 dk paylaşım aralığı, (2) müzik seviyesini düşürme, (3) altyazıyı güvenli alana taşıma, (4) Cartesia kelime zaman damgası, (5) Emre hız 0.9, (6) pending kaydına voice alanı.

## 2026-11-16 (Pzt, ~23:55 TSİ) — kullanıcı tüm önerileri onayladı, uygulandı
**Kod (tools/news.py, tools/grab_tts.py):**
- Müzik: kazanç 0.5→0.20, ducking yalnızca konuşma izinden, derinlik 0.4→0.65, yumuşak atak/bırakma, müzikte 800–3000 Hz ~−5 dB. Test: konuşma/müzik ayrımı ~10 dB → ~23 dB.
- Ses zinciri: kompresör + ölçümlü sabit kazanç + limitör (tek geçiş loudnorm kısa videoda −17/−18 LUFS'ta kalıyordu; yeni zincir −14,3 LUFS, tepe −1,2 dBFS).
- Altyazı y 1560→1400, kaynak satırı 1790→1478 (Instagram alt arayüzü dışında); punto 44→48; konuşulan kelime sarı vurgulu.
- Kelime senkronu: sahneye "words" (Speko audio_transcribe word_timestamps, gemini-3.5-transcribe; Türkçe testte çalıştı, 100 ms çözünürlük) eklenirse altyazı kelime kelime senkron; yoksa eski tahmin. grab_tts.py imzalı ses URL'lerini urls.json'a yazıyor.
- Emre: Speko synthesize "speed": 0.9 (196 → ~176 kelime/dk). Aylin 1.0.
**Görev akışı:** sabah görevi yalnızca 1. Reels'i hemen paylaşır; diğerlerini saatlik son dakika görevi 12:31, 18:31, 21:31'de paylaşır (min. 60 dk aralık; yeni görev oluşturma izni reddedildi, kullanıcı saatlik göreve eklemeyi seçti). Son dakika kayıtlarına voice + reel_posted_at alanı. Büyüme görevi artık küçük, test edilmiş iyileştirmeleri uygulayabilir.
**Araştırma (rakip/benchmark):**
- Ulusal: @bpthaber ~3,23 mn (https://livecounts.org/instagram-takipci-sayaci/bpthaber), @trthaber ~3,15 mn ER %0,16, @tvahaber ~1,74 mn ER %0,29, @tvgundemi ~569 bin ER %0,85, @sondakika.turkiye ~340 bin ER %0,69 (https://socialveins.com/influencer/instagram/<hesap>, Nisan 2026). Yerel: @igdir_havadis ~54,6 bin, @polatlihaberleri ~50,7 bin, @hayaleturkcom ~24,6 bin; @kocaeligundem verisi okunamadı.
- Benchmark: 1–5 bin takipçi yıllık takipçi büyümesi ~%22, Reels başına ort. ~580 izlenme (https://www.socialinsider.io/instagram-engagement-report-2025/ , https://www.socialinsider.io/tr/social-media-benchmarks/instagram); <1.000 takipçide Reels medyan erişimi 134 (https://www.netinfluencer.com/instagram-carousels-outperform-reels-for-larger-accounts-content-performance-benchmarks-show/); Reels erişiminin ~%47'si takip etmeyenlerden (https://www.fanpagekarma.com/insights/tiktok-vs-instagram-reach/); medya sektörü aylık takipçi büyümesi %0,9, haftada ~32 gönderi (https://dashsocial.com/social-media-benchmarks/media-industry); 10 bin altı collab gönderileri ~5x etkileşim (https://www.netinfluencer.com/instagram-collaboration-posts-outperform-standard-content-analysis-finds/).
- Keşfet kuralları: özgünlük, siyasi içerik takip etmeyenlere önerilmez, clickbait/etkileşim dilenciliği öneri dışı (https://creators.instagram.com/recommendations-and-originality , https://themarkup.org/automated-censorship/2024/03/25/instagram-creators-check-if-your-posts-are-political); Trial Reels ≥1.000 takipçi (https://www.thekeyword.co/news/instagram-expands-trial-reels-to-all-public-creators-with-1k-or-more-followers).
- 0–1.000 takipçi için güvenilir büyüme benchmark'ı bulunamadı.
**Bildirilen/uygulanan (tekrar bildirme):** önceki 6 öneri uygulandı; yeni öneriler: collab daveti (kullanıcı onayı gerekir), haftalık Hesap Durumu kontrolü, seri formatlar.

## 2026-11-17 (~02:10 TSİ) — kullanıcı onayı: sayı okuma + simülasyon
- tools/tr_numbers.py: TTS metninde sayılar bütün okunur (1000→bin, D-100→"Deyüz" (ayrı "de yüz" yazınca TTS 0,35 sn duraksıyordu), 17.30→on yedi otuz, %109→yüzde yüz dokuz, 95,60 TL→doksan beş lira altmış kuruş). Speko transcribe testinde sayılar bütün olarak tanındı.
- tools/news.py "sim": crash / road (traffic|closed) / rain / fire / outage temsili canlandırma; ekranda otomatik "TEMSİLİ CANLANDIRMA" etiketi, caption'a "Görseller temsilidir.". Kullanıcı: simüle edilebilen her olay simüle edilsin. Örnek (Gebze kazası) −14,2 LUFS, tepe −1,7 dBFS.
- grab_tts.py: Speko sonuç dosya adı biçimi değişmişti (…-<sayı>-<ek>.txt), sıralama düzeltildi.
- Sabah ve son dakika görev talimatları güncellendi (tr_numbers + sim + pending/breaking "sim" alanı). Büyüme görevi: sim'li ve sim'siz videoların izlenme/atlama farkını takip etsin.

## 2026-11-17 (Sal, ~23:30 TSİ) — günlük analiz
**Hesap (Windsor.ai, önbellek; TRIAL planda force_refresh yok):** 428 takipçi (16.11 analizinde 107). Yeni takipçi 15.11 +2, 16.11 +268 (17.11 henüz 0/eksik). Günlük erişim 15.11 2.753 · 16.11 17.617 · 17.11 14.827; takip etmeyen payı %99,5 / %98,2.
| Saat (TSİ) | Video | Ses | Sim | Süre | Erişim | Atlama | Ort. izl. | Payl.+Kayıt/Erişim |
|---|---|---|---|---|---|---|---|---|
| 16.11 19:42 | Gebze minibüs kazası (güncel) | ? | – | 31,9 sn | 11.301 | %37,9 | 13,7 sn | %0,70 (69 payl.) |
| 17.11 08:14 | Elektrik kesintisi 8 saat | Aylin | ✓ | 34,2 sn | 6.664 | %43,5 | 9,2 sn | %0,89 (52 payl.) |
| 17.11 12:33 | Darıca 26 hat | Emre | ✓ | 33,6 sn | 1.394 | %43,3 | 8,0 sn | %0,93 |
| 17.11 15:41 | Fırtına uyarısı (B) | Emre | ✓ | 29,5 sn | 3.360 | %57,1 | 6,5 sn | %0,63 |
| 17.11 18:34 | Kocaelispor–Fenerbahçe | Aylin | – | 27,8 sn | 1.393 | %42,2 | 8,9 sn | %0,22 (0 payl.) |
- Aralık kuralı doğrulandı: 17.11'de 2–3 saat arayla 4 video → hepsi 1.390+; 16.11 peş peşe 4 video → 179–245.
- Yeni ses/altyazı sürümü (17.11) vs eski (16.11, kümelenmeyenler): ort. atlama %46,5 vs %44,3, ort. izlenme 8,1 vs 9,1 sn → fark yok/örneklem küçük. Aynı konu: elektrik %50,8→%43,5 atlama, 7,7→9,2 sn (iyileşme); hava uyarısı %49,9→%57,1 (kötüleşme). Ses (Emre/Aylin) ve sim etkisi n=2'de ayrıştırılamıyor; 7 gün sonra tekrar bak.
- Hashtag: Instagram Aralık 2025'ten beri gönderi başına 5 hashtag sınırı uyguluyor; 17.11 elektrik/fırtına caption'larında 6 vardı → growth.md kuralı ≤5 (tek ilçe) yapıldı.
- Meta 3. çeyrek bilançosu: önerilen Reels'in ~%45'i 1 günden yeni; Reels artık Reels dizilerini sıralıyor → tazelik/hız kuralı eklendi.
- Kod değişikliği yok: yeni sürüm 1 günlük, veriyle değerlendirilmeden ses/altyazıya dokunulmadı. 0. kare kontrolü (fırtına, elektrik): başlık ilk karede tam görünür.
- @kocaeligundem: hypeauditor erişilemedi, socialveins/livecounts izin zaman aşımı → rakam yok.
**Kaynaklar:** https://keywordseverywhere.com/news/instagram-algorithm-updates/ (16.11.2026; Q3 bilanço, Features testi, Nisan orijinallik), https://metricool.com/instagram-news/ (Trial Reels aylık sınır, skip/share rate Insights'ta), https://www.truefuturemedia.com/articles/lower-instagram-reels-skip-rate , https://metricool.com/instagram-reel-analytics/ , https://www.socialmediatoday.com/news/instagram-implements-new-limits-on-hashtag-use/808309/ , https://www.businesstoday.in/technology/news/story/no-more-hashtag-stuffing-instagram-limits-hashtag-usage-to-just-5-per-reel-and-post-507444-2025-12-19
**Bildirilen (tekrar bildirme):** Windsor.ai TRIAL planda — deneme bitince günlük analiz durur; karar: ücretli plan ya da Supermetrics (instagram_insights/IGI, bağlı) ile yedek. Hashtag ≤5 kuralı bilgi olarak iletildi.

## 2026-11-18 (Çar, ~23:30 TSİ) — günlük analiz
**Hesap (Windsor.ai):** 511 takipçi (17.11: 428). Yeni takipçi 16.11 +268 · 17.11 +221 · 18.11 ~+83 (gün içi). Günlük erişim 17.11 20.021 (takip etmeyen %98,7), 18.11 3.314 (eksik). Dönüşüm 17.11 %1,1. Projeksiyon (tahmin): 1.000 takipçi ≈ 21–25 Kasım.
| Saat (TSİ) | Video | Ses | Sim | Süre | Erişim | Atlama | Ort. izl. | Payl.+Kayıt/Erişim |
|---|---|---|---|---|---|---|---|---|
| 17.11 08:14 | Elektrik kesintisi | Aylin | ✓ | 34,2 | 8.930 | %43,4 | 9,8 | %0,87 (65 payl.) |
| 17.11 12:33 | Darıca 26 hat | Emre | ✓ | 33,6 | 1.963 | %42,8 | 9,4 | %1,73 |
| 17.11 15:41 | Fırtına uyarısı | Emre | ✓ | 29,5 | 4.785 | %55,7 | 7,3 | %0,65 |
| 17.11 18:34 | Kocaelispor maç önü | Aylin | – | 27,8 | 1.539 | %42,9 | 8,9 | %0,32 |
| 18.11 08:09 | Elektrik kesintisi (7 ilçe) | Aylin | ✓ | 38,8 | 2.157 | %47,0 | 8,6 | %1,30 |
| 18.11 12:34 | Baraj doluluk | Emre | – | 32,3 | 1.661 | %49,0 | 9,6 | %0,12 (0 payl.) |
- 18.11'de yalnızca 2 Reels (18:31/21:31 slotları boş) → günlük erişim düşük.
- Aynı format ertesi gün: elektrik 8,9 bin → 2,2 bin; growth.md'ye "tekrarlayan format yorulması" kuralı eklendi. Baraj/spor: paylaşım yok → "gönder" sebebi olmayan konular.
- Ses/sim: Emre vs Aylin ve sim'li vs sim'siz farkı hâlâ konu etkisinden ayrıştırılamıyor (n küçük). Kod değişikliği yok (veri desteği yetersiz).
- @kocaeligundem: hypeauditor client_error; rakam yok.
**Kaynaklar:** https://www.socialpilot.co/es/blog/instagram-reels-algorithm (Eyl 2026: Your Algorithm Reels→Keşfet→Akış, Nis 2026 orijinallik/aggregator, 3 dk öneri sınırı), https://www.pulse-advertising.com/resources/social-media-news/instagram-algorithm-changes-2026/
**Bildirilen:** yok (yeni karar gerektiren öneri yok, kod değişikliği yok).

## 2026-11-19 (Per, ~23:30 TSİ) — günlük analiz
**Hesap (Windsor.ai):** 564 takipçi (18.11: 511, +53). Yeni takipçi (kesin) 18.11 +32 (gün içi tahmin +83 idi). Günlük erişim 18.11 5.695 · 19.11 6.051 (takip etmeyen %96,9). Büyüme ~220/gün → ~43/gün (son 48 sa). Projeksiyon (tahmin): 1.000 ≈ 29.11–1.12; haftada 1 viral günle 25–27.11.
| Saat (TSİ) | Video | Süre | Erişim | Atlama | Ort. izl. | Payl.+Kayıt/Erişim |
|---|---|---|---|---|---|---|
| 18.11 08:09 | Elektrik kesintisi (güncel) | 38,8 | 2.441 | %46,8 | 8,8 | %1,15 |
| 18.11 12:34 | Baraj doluluk (güncel) | 32,3 | 1.803 | %48,6 | 9,6 | %0,11 |
| 19.11 08:09 | Fırtına bugün 75 km | ? | 2.319 | %60,5 | 5,9 | %1,16 |
| 19.11 12:33 | Elektrik Dilovası (3. gün) | ? | 1.865 | %54,5 | 6,9 | %0,75 |
| 19.11 17:38 | Fırtına yarın sabah (B) | ? | 2.742 | %51,1 | 8,5 | %1,86 (46 payl.) |
| 19.11 18:41 | Servis denetimi | ? | 1.279 | %48,6 | 7,2 | %0,08 |
- Ses: pending.json/breaking.json boş (alan temizlenmiş) → bugünkü videoların ses bilgisi yok; ses/sim karşılaştırması yapılamadı. Görevler "voice" bilgisini log/commit mesajına da yazarsa analiz mümkün olur.
- Elektrik format yorulması 3. günde doğrulandı (9,1→2,4→1,9 bin). "Yarın" uyarısı + durumsal gönder çağrısı en iyi paylaşım oranı. 19.11 atlama ort. %53,6 (kötüleşme; konu tekrarı olası neden).
- Kod değişikliği yok (veriyle desteklenen ses/altyazı değişikliği yok; atlama artışı konu tekrarıyla açıklanabiliyor).
- @kocaeligundem: instastatistics/hypeauditor yine rakam vermedi.
**Kaynaklar:** https://uppbeat.io/blog/creator-news/whats-working-on-instagram-right-now-carousels-and-sends-says-adam-mosseri (03.11.2026: müzikli karusel Reels akışında; gönderim/erişim yeni üreticiler için en önemli metrik), https://influencermarketinghub.com/instagram-sends-per-reach-playbook/ (durumsal gönder çağrısı; sayısal çağrı = etkileşim dilenciliği), https://ground.news/article/instagram-reels-algorithm-2026-how-it-works-and-what-changed (Kasım'da yeni algoritma değişikliği yok)
**Bildirilen (tekrar bildirme):** büyüme yavaşlaması uyarısı; öneri: elektrik kesintisi listesini Reels yerine müzikli karusel (+hikâye) olarak test et; Reels'i yalnızca büyük kesintide kullan.

## 2026-11-19 (~23:40 TSİ) — kullanıcı onayı: kesinti listesi → karusel + derin veri analizi
- Yeni araç tools/carousel.py: 4:5 (1080x1350) JPEG karusel + 9:16 hikâye kapağı. Yapı: kapak (harita + pin, ilçe sayısı, sarı vurgu bandı, "MAHALLEN LİSTEDE Mİ? KAYDIR" + ok) → ÖZET kare (ilçe · mahalle sayısı · saat; 2. kare kendi başına anlaşılır) → dengeli doldurulan mahalle listesi kareleri → GÖNDER/KAYDET/TAKİP ET + arıza hattı. Türkçe büyük harf (i→İ), en fazla 10 kare, 8 MB sınırı kontrolü. Test: 19.11 listesiyle 5 kare + 70 satırlık zorlama testiyle 10 kare; karelere bakıldı (taşma yok, Türkçe karakter doğru).
- Kaynaklara göre seçimler (çoğu görüş/vendor blogu, sayıları doğrulanmamış): tek fikir/kare, kaydırma işareti yalnız kapakta, 2. kare kritik (Mosseri: geçilen karusel 2. kareyle yeniden gösterilebilir), son karede kayıt/gönder çağrısı, tek şablon, 4:5 ve oranları karıştırmama, alt metin. Windsor API karusele müzik ekleyemiyor.
- Sabah görevi talimatı güncellendi: kesinti listesi Reels değil karusel (adım 2b/7b), hikâye + create_carousel_post (alt_text'li), pending.json'da 7 günlük batch'ler korunur (ses analizi için), c/ 4 günde temizlenir. Büyüme görevi talimatı: karusel media_follows/profile_visits, yorum temaları, haftalık kitle, hikâye metrikleri.
- Derin veri [VERİ]: kitle %53 erkek, %56'sı 35–54 yaş; Gebze–Darıca–Şekerpınar–Tuzla bloğu en büyük, sonra İzmit. Hikâye erişimi 22–56 (takipçinin ~%4–10'u). Profil bağlantı tıklaması 0. Yorumlar: kesintide kişiye özel soru, kaza/uyarıda doğruluk itirazı. Hesap Instagram Login ile bağlı → Reels repost metriği alınamıyor (Facebook Login ile yeniden bağlanırsa açılır).
**Kaynaklar:** https://instacarousel.com/blog/instagram-carousel-guide-2026/ , https://www.adpicto.com/en/blog/instagram-carousel-best-practices-2026 , https://carouselpost.io/digest/carousel-slide-count-hook-tips-2026 , https://niemanlab.org/2021/07/the-new-york-times-is-using-instagram-slides-and-twitter-cards-to-make-stories-more-digestible , https://mobileanddigitaljournalism.substack.com/p/the-carousel-post-an-overview , https://journalism.co.uk/tip-of-the-day/tip-create-slides-and-cards-on-social-media-to-increase-audience-engagement/s419/a850360
**Bildirilen (tekrar bildirme):** karusel uygulandı; yorumlara otomatik cevap önerisi (onay bekliyor); Facebook Login ile yeniden bağlama önerisi.

## 2026-11-20 (Cum, ~23:30 TSİ) — günlük analiz
**Hesap (Windsor.ai):** 612 takipçi (19.11 gece 564). Yeni takipçi (kesin) 19.11 +68. Günlük erişim 19.11 7.991 (takip etmeyen %96,9) · 20.11 3.745 (gün içi). Sabah Reels'i Speko (TTS) bağlantısı koptuğu için üretilemedi (pending.json notu); 18:31/21:31 slotları da boş. Projeksiyon (tahmin): ~+50/gün → 1.000 ≈ 27–29.11.
| Saat (TSİ) | İçerik | Ses | Erişim | Atlama | Ort. izl. | Payl.+Kayıt/Erişim |
|---|---|---|---|---|---|---|
| 19.11 17:38 | Fırtına yarın sabah (güncel) | Emre | 5.335 | %50,3 | 9,7 | %1,87 (91 payl.) |
| 19.11 18:41 | Servis denetimi (güncel) | Aylin | 1.457 | %49,3 | 7,1 | %0,07 |
| 20.11 07:58 | KARUSEL kesinti 12 ilçe (7 kare) | – | 174 | – | – | %0 (0 takip, 3 profil ziyareti) |
| 20.11 14:06 | Sağanak uyarısı (A, bugün) | Aylin | 2.882 | %53,4 | 6,7 | %0,97 |
- İlk karusel çok zayıf: erişim 174 (takipçinin ~%28'i), kesinti Reels'leri 1,9–9,2 bin. Fanpage Karma verisi (<10 bin takipçi: Reels takipçi başına erişim %4,9 vs karusel %2,6; takip etmeyene ~3 kat) bununla uyumlu. n=1, karusel erişimi günlerce birikebilir; 26.11 kıyası sürüyor.
- Ses ilk kez ayrıştırıldı (pending.json voice): Aylin 6 video ort. atlama %49,4 / 7,9 sn; Emre 4 video %48,8 / 8,9 sn. Konu karışık, karar yok.
- Hava "bugün" videoları yüksek atlama (%53–60), "yarın" uyarısı en iyi paylaşım. Yorum: "Yoo kesilmedi" → kesinti iptal/kayma notu önerisi growth.md'ye.
- Hikâye: erişim 30–48, paylaşım 0. Speko bakiyesi 9,30 USD (20.11 20:21 UTC).
- Kod değişikliği yok (veriyle desteklenen küçük kalite değişikliği yok).
- @kocaeligundem: hypeauditor yine 4xx.
**Kaynaklar:** https://www.fanpagekarma.com/insights/instagram-format-reach/ (07.08.2026; 3 mn+ gönderi, Oca–Nis 2026), https://buffer.com/resources/instagram-reach-engagement-analysis/ (Eki 2024: Reels erişimi karuselin 1,36 katı, karusel etkileşimi 1,12 katı)
**Bildirilen (tekrar bildirme):** karusel ilk sonucu zayıf → karar önerisi: kesinti için kısa Reels + ayrıntı karuseli (hibrit) ya da karuseli müzikle elle paylaşma; sabah Speko kopukluğu ve düşük Speko bakiyesi uyarısı.
- 20.11 ~23:45 kullanıcı: "en mantıklı hangisiyse öyle devam" → HİBRİT seçildi: kesinti günlerinde sabah 1. video kısa kesinti Reels'i + ayrıntı karuseli (≥30 dk sonra). Sabah görevi talimatı güncellendi; Speko araçları görünmezse ToolSearch ile bekleyip yeniden deneme adımı eklendi. Speko maliyeti ~0,03–0,04 USD/video (ledger) → 9,30 USD birkaç hafta yeter.

## 2026-11-21 (Cmt, ~23:30 TSİ) — günlük analiz
**Hesap (Windsor.ai):** 790 takipçi (20.11 gece 612 → ~+178/24 sa). Yeni takipçi (kesin) 20.11 +77. Günlük erişim 20.11 11.654 · 21.11 22.386 (rekor, takip etmeyen %98,6, 335 paylaşım). Projeksiyon (tahmin): 1.000 ≈ 23–25.11.
| Saat (TSİ) | İçerik | Ses | Erişim | Atlama | Ort. izl. | Payl.+Kayıt/Erişim |
|---|---|---|---|---|---|---|
| 20.11 14:06 | Sağanak uyarısı (güncel) | Aylin | 4.141 | %51,9 | 7,5 | %0,87 |
| 21.11 08:01 | HİBRİT kesinti Reels (10 ilçe, Gebze 8 sa) | Emre | 27.269 | %44,0 | 10,2 | %1,78 (439 payl., 46 kayıt) |
| 21.11 08:33 | Kesinti karuseli | – | 330 | – | – | %3,3 (11 payl., 0 takip, 2 profil) |
| 21.11 12:35 | Benzin 68,80 TL | Aylin | 360 | %46,7 | 8,5 | %1,1 |
| 21.11 15:33 | Kocaelispor–FB maç önü | Emre | 1.369 | %40,3 | 8,0 | %0,15 |
| 21.11 21:38 | Kocaelispor 2-2 FB (B) | Aylin | 1.141 | %52,8 | 7,5 | %0 |
- Hibrit akış (kısa kesinti Reels'i + karusel) ilk günde hesabın en iyi videosunu üretti; karusel yine yalnız takipçiye (330). Akış korunuyor.
- Akaryakıt fiyatı n=2 zayıf (273, 360); maç sonucu 0 paylaşım. growth.md konu önceliği güncellendi.
- Yorumlar: mahalle soruları ("Nenehatun var mı"), "kesilmedi/gitti", "Bugün yerine tarih deseniz" → başlıkta tarih kuralı (ÖNERİ) growth.md'ye.
- Hikâye erişimi 19–452, paylaşım 0.
- Kod değişikliği yok (veriyle desteklenen kalite değişikliği yok; en iyi video mevcut ayarlarla geldi).
- Rakip rakamı bugün aranmadı (açı: Trial Reels uygunluğu).
**Kaynaklar:** https://superprofile.bio/guides/instagram-trial-reels (30.10.2026: profesyonel hesapta 200 takipçi, kişiselde 1.000; Instagram Yardım'a atıf), https://metricool.com/instagram-trial-reels/ (03.07.2026: 1.000 takipçi; 72 sa otomatik paylaşım; tek değişken test)
**Bildirilen (tekrar bildirme):** Trial Reels muhtemelen şimdiden açık olabilir → uygulamada "Deneme" seçeneğini kontrol et, elle hook testi önerisi.

## 2026-11-22 (Paz, ~23:30 TSİ) — günlük analiz + HAFTALIK ÖZET
**Hesap (Windsor.ai):** 846 takipçi (21.11 gece 790 → +56). Yeni takipçi (kesin) 21.11 +150. Günlük erişim 21.11 25.417 (rekor) · 22.11 7.138 (gün içi, takip etmeyen %95,4). Hafta 16–22.11: ~+740 takipçi, ~95 bin erişim; 7 gün ort. ~+125/gün, son 5 gün ~+77/gün. Projeksiyon (tahmin): 1.000 ≈ 24–25.11; Aralık sonu 3–5 bin.
| Saat (TSİ) | İçerik | Ses | Erişim | Atlama | Ort. izl. | Payl.+Kayıt/Erişim |
|---|---|---|---|---|---|---|
| 21.11 08:01 | Hibrit kesinti Reels (güncel) | Emre | 28.666 | %44,0 | 10,3 | %1,77 (459 payl.) |
| 22.11 08:08 | Kesinti Reels 4 ilçe | Aylin | 3.289 | %44,4 | 8,0 | %1,31 |
| 22.11 08:40 | Kesinti karuseli | – | 169 | – | – | %0 (0 takip, 4 profil) |
| 22.11 12:34 | Yarın okul var (MEB takvimi) | Emre | 2.261 | %52,2 | 9,6 | %2,88 (55 payl., 10 kayıt) |
| 22.11 15:36 | Sıcaklık 13 derece düşüyor | Aylin | 1.513 | %65,6 | 5,9 | %0,33 |
| 22.11 18:38 | Yarın fırtına 90 km (B) | Emre | 2.034 | %54,2 | 7,2 | %1,38 |
- Hafta en iyi: 21.11 kesinti Reels 28,7 bin; 16.11 Gebze minibüs kazası 11,8 bin; 17.11 kesinti 9,4 bin. En kötü: 16.11 hava tahmini 249, Körfez çamuru 262, akaryakıt 281 (hepsi aralık kuralı öncesi peş peşe). Karuseller 256 / 372 / 169, toplam 0 takip.
- Ses (18 Reels): Aylin atlama %50,9 / 7,8 sn; Emre %48,4 / 8,8 sn. Konu karışık.
- Kitle (664 kırılım): Gebze 92→143, İzmit 60→88, Darıca 50→60, Derince 31→48; cinsiyet/yaş değişmedi (erkek %53, 35–54 %52).
- Yorumlar: fırtına videosunda "Okul tatil mi / Valimiz tatil yok mu" → okul tatili kararı bilgisi kuralı growth.md'ye. Kesinti videosunda mahalle soruları ve "gitmedi/kesilmedi" sürüyor.
- Hikâye erişimi 33–80, paylaşım 0.
- Kod değişikliği yok (konuşma zaten 0,3 sn'de başlıyor; atlama farkları konu kaynaklı).
- @kocaeligundem: hypeauditor yine okunamadı.
**Kaynaklar:** https://keywordseverywhere.com/news/instagram-algorithm-updates/ (21.11: 17.11 içerik koruma aracı Instagram üreticilerine açılıyor; Eki–Kas'ta Keşfet'e özgü doğrulanmış değişiklik yok), https://www.pulse.bot/digital-marketing/news/human-speech-and-presence-help-drive-reels-engagement-26291baf-0b96-441f-aefa-8af987fa02e8 (Social Media Today/Emplifi, Mar 2026: ilk 3 sn konuşma ~%25 daha iyi 10 sn tutma)
**Bildirilen (tekrar bildirme):** haftalık özet; öneriler: içerik korumayı uygulamada aç, okul tatili kararı takibi/notu, sesi varsayılan Emre yapma seçeneği (kullanıcı kararı).

## 2026-11-24 (Sal, ~23:30 TSİ) — günlük analiz
**Hesap (Windsor.ai, önbellek):** 891 takipçi (22.11 gece 846). Yeni takipçi 22.11 +53 · 23.11 +27. Günlük erişim 22.11 10.487 · 23.11 6.717 (takip etmeyen %96) · 24.11 576. Projeksiyon (tahmin): 1.000 ≈ 27–29.11.
**ÜRETİM KESİNTİSİ:** 24.11 sabah görevi `USAGE_LIMIT_REACHED` ile başarısız; 23.11 16:33 → 24.11 22:27 arası depoda hiç commit/paylaşım yok (saatlik görev de çalışmamış görünüyor). Öğretmenler Günü videosu (v/ozel-2026-11-24-ogretmenler-gunu.mp4) hazır ama PAYLAŞILMADI (ozelgun.json "ready"). 23.11 büyüme analizi kaydı da yok.
| Saat (TSİ) | İçerik | Ses | Erişim | Atlama | Ort. izl. | Payl.+Kayıt/Erişim |
|---|---|---|---|---|---|---|
| 22.11 18:38 | Yarın fırtına 90 km (güncel) | Emre | 3.721 | %51,0 | 7,9 | %2,07 |
| 23.11 08:02 | Kesinti Reels 8 ilçe | Aylin | 6.355 | %46,8 | 8,6 | %2,28 (140 payl.) |
| 23.11 08:33 | Kesinti karuseli | – | 242 | – | – | %1,2 (0 takip, 6 profil) |
| 23.11 12:34 | Sarı kod sağanak/fırtına (bugün) | Aylin | 2.063 | %58,3 | 7,4 | %0,97 |
| 23.11 15:34 | Tapuda güvenli ödeme (ulusal) | Emre | 295 | %59,5 | 5,5 | %0,7 |
| 24.11 22:29 / 22:31 | Öğretmen konutu / İzmit 8 tutuklama (2 dk arayla) | – | 116 / 99 (erken) | – | – | – |
- Kesinti Reels'i 3 gün üst üste en iyi video (28,9 bin / 3,7 bin / 6,4 bin); karuseller 0 takip. Hibrit sürüyor. "Bugün" hava uyarısı yine yüksek atlama (%58), "yarın" uyarısı %2,1 oran.
- Yorumlar: okul tatili soruları sürüyor; kesintide mahalle adı.
- Kod değişikliği yok (veriyle desteklenen küçük kalite değişikliği yok; kullanım limiti sorunu nedeniyle test videosu üretilmedi).
- Algoritma: 18.11 sonrası doğrulanmış sıralama değişikliği yok (Content Protection yayılıyor). @kocaeligundem: hypeauditor yine okunamadı.
**Kaynaklar:** https://keywordseverywhere.com/news/instagram-algorithm-updates/ (son güncelleme 18.11, kontrol 23.11)
**Bildirilen (tekrar bildirme):** kullanım limiti nedeniyle sabah görevi başarısız + 30 saatlik paylaşım boşluğu + Öğretmenler Günü videosu paylaşılmadı; görev sayısını/sıklığını azaltma önerisi (saatlik tarama → 2 saatte bir veya gece 01–06 arası kapalı).
