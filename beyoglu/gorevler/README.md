# Beyoğlu Radar zamanlanmış görevleri

Bu klasördeki dosyalar Beyoğlu Radar'ın (Instagram @beyogluradar34) zamanlanmış görevlerinin TAM metinleridir. Kocaeli Radar'ın 4 görevinden birebir uyarlandı (25.11.2026, kullanıcı: "kocaeli radardaki tüm kuralları beyoğluna uyarla").

| Dosya | Görev | Saat (Europe/Istanbul) | Kocaeli karşılığı |
|---|---|---|---|
| sabah.md | Sabah haber videoları + kesinti Reels/karuseli + özel gün + Perşembe etkinlik karuseli | 07:37 | 07:52 |
| sondakika.md | 7/24 son dakika, sıradaki sabah videoları, maç programı/sonuçları, 1000 takipçi | her saat :46 | :31 |
| hikaye.md | Günlük 4 hikâye (hava, altın, dolar, euro) | 09:13 | 08:58 |
| buyume.md | Büyüme ve kalite analizi | 23:37 | 23:17 |

Saatler Kocaeli görevleriyle aynı dakikaya denk gelmesin diye kaydırıldı (aynı depoya push ediyorlar).

## Kocaeli'den farklar
- Tüm çıktılar `beyoglu/` altında: `beyoglu/v/` (Reels), `beyoglu/s/` (hikâye), `beyoglu/c/` (karusel), `beyoglu/data/` (hikâye verisi), `beyoglu/state/` (kurallar ve durum). Araçlar `RADAR_CITY=beyoglu` ile çalışır.
- Kaynaklar `beyoglu/state/kaynaklar.md`; kurallar `beyoglu/state/growth.md` (siyasi haber kuralı dahil).
- Kesinti: SEDAŞ/İSU yerine BEDAŞ (arıza 186) ve İSKİ (arıza 185). Mahalle ve saat doğrulanmazsa kesinti Reels'i ve karuseli yapılmaz.
- Spor: Kocaelispor yerine Kasımpaşa (Beyoğlu'nun takımı); Galatasaray, Fenerbahçe, Beşiktaş aynı. Trabzonspor yalnızca UEFA maçında.
- Günde en fazla 3 sabah videosu (Beyoğlu haber hacmi günde 2–3, 19–21.11 taraması).
- Ek format: Perşembe akşamı "Beyoğlu'nda bu hafta sonu" etkinlik karuseli.
- 1000 takipçi kutlama videosu henüz yok; takipçi 900'ü geçince büyüme görevi hazırlar.

## Açma
Görevler, Instagram hesabı Windsor.ai'ye bağlanıp hesap kimliği (`{{HESAP_ID}}`) öğrenilince bu metinlerle oluşturulur. Metindeki `{{HESAP_ID}}` gerçek kimlikle değiştirilir. PR #1 (şehir ayarı) main'e birleşmeden görevler çalışmaz.
