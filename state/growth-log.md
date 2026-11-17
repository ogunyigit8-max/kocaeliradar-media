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
