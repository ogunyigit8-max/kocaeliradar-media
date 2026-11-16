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
