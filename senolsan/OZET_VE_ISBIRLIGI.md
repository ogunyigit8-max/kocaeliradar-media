# Pazar işleri: "Şimdiye kadar" özet videosu + ortak paylaşım araştırması

Yiğit 20.11.2026'da onayladı: büyüme için haftalık özet videosu, tahmin yarışması ve ortak paylaşım çalışmaları yapılsın.
Bu dosyayı pazar günü 12:30'da çalışan haftalık görev uygular (analizden sonra).

## A. "Şimdiye kadar" özet Reels (her pazar, en az 3 bölüm yayınlandıysa)
Amaç: yeni gelen izleyici diziye 30 saniyede yetişsin ve takip etsin.
1. Yayınlanmış bölümlerin (durum.json "bolumler") her biri için bolumler/bXX/cekimler/ içinden en güçlü 1 resmi seç
   (genelde 01.png ya da ters köşe resmi 06.png). En fazla 7 resim; bölüm çoksa son 7 bölüm.
2. Metin: her bölüm için tek kısa cümle (ikinci tekil şahıs, şimdiki zaman, 6-10 kelime), sonda:
   "Şimdi sıra sende. Yeni bölüm bu akşam yedide." Toplam 25-35 sn. Sayılar yazıyla.
3. Ses: Fatih sesi, ses.py'deki ayarlarla (eleven_multilingual_v2, aynı voice_settings), satır aralarına 0.5 sn durak.
   İlk sefer tools/ozet.py yaz: ses.py ve kurgu.py'deki fonksiyonları yeniden kullan (yeni araç değil, onların kısa bir
   birleşimi). Oylama kartı YOK; bunun yerine son 3 saniyede üstte sarı "Bu akşam 19:00 · Yeni bölüm" kartı.
   Üstte ilk 2 saniye büyük yazı: "Şimdiye kadar..." Altyazı ve müzik kurgu.py ile aynı tarzda.
4. Kontrol: 1080x1920, ses var, 4 kareye bak. Sorun varsa düzelt; düzelmezse paylaşma, bildirimde söyle.
5. Paylaş: python3 tools/yayin.py ile adres; Windsor create_video_post (share_to_feed true, thumb_offset 1000).
   Açıklama: "Paket'i kaçıranlar için: şimdiye kadar olanlar 📦\n\nBu akşam 19:00'da yeni bölüm. Sen olsan ne seçerdin?\n
   👉 Bölüm 1'den başla: profilde sabitli.\n🔁 Bu diziyi sevecek bir arkadaşına gönder.\n\n#senolsannesecerdin #hikaye #gerilim #animasyon #dizi"
   Ardından aynı videoyla create_story. durum.json'a "ozetler" listesine {tarih, media_id} ekle.
6. Bildirimde özet linkini ve TikTok/YouTube için hazır metinleri de ver (GOREV.md 8. adımdaki yarı otomatik kural).

## B. Ortak paylaşım (collab) araştırması (her pazar)
Amaç: benzer Türkçe sayfalarla ortak paylaşım, karşılıklı tanıtım.
1. WebSearch ile Türkçe hikaye / gerilim / gizem / animasyon / "sen olsan ne yapardın" / interaktif hikaye anlatan
   Instagram ve TikTok hesapları bul. Tercih: 5 bin - 200 bin takipçi, son 2 haftada aktif, aile dostu içerik.
   Gerçekten var olduğunu bir kaynakla doğrula; doğrulanamayanı listeye alma. Uydurma hesap adı YAZMA.
2. En uygun 3-5 hesabı seç. Her biri için: hesap adı, kaynak linki, neden uygun (1 cümle), önerilen iş birliği türü
   (Instagram ortak gönderi / karşılıklı hikaye paylaşımı / "senin takipçilerin seçsin" özel bölüm).
3. Her hesap için Yiğit'in kendisinin göndereceği kısa, samimi bir DM taslağı yaz (3-4 cümle, abartısız, baskısız).
   Sen DM GÖNDERME; mesajı Yiğit gönderir.
4. analiz/isbirligi_<YYYY-MM-DD>.md dosyasına yaz, commit et. Daha önceki haftalarda önerilen hesapları tekrar önerme
   (eski isbirligi_*.md dosyalarına bak).
5. Bildirimde: kaç aday bulundu, en iyi 2 adayın adı ve dosya linki
   (https://github.com/ogunyigit8-max/kocaeliradar-media/blob/main/senolsan/analiz/isbirligi_<tarih>.md).
