# Beyoğlu Radar özel günler kuralı (Kocaeli Radar kuralı, kullanıcı 22.11.2026'da istedi; 25.11.2026'da Beyoğlu'na uyarlandı)

"Özel günlerde (Öğretmenler Günü, bayramlar, kandiller vb.) mutlaka güzel, kalbi ısıtan videolar paylaşalım; bunu unutmayalım."

## Kural
- Aşağıdaki takvimdeki her gün için 1 ÖZEL GÜN VİDEOSU paylaşılır (önce HİKÂYE, sonra REELS), ONAY BEKLEMEDEN.
- Video bir GÜN ÖNCE sabah görevinde hazırlanır ve beyoglu/state/ozelgun.json'a "ready" olarak kaydedilir; özel günün sabahı sabah görevi bu videoyu İLK paylaşır (~08:00). O gün haber videosu sayısı 4 yerine 3'tür (1. haber videosu 12:31 slotuna kayar).
- Bir gün iki özel güne denk gelirse tek video yapılır; öncelik: dini bayram / milli bayram > kandil > diğer günler (ör. 8 Mart 2027: arefe yerine Kadınlar Günü; 19 Mayıs 2027: Kurban Bayramı 4. günü yerine 19 Mayıs).
- Beyoğlu/İstanbul'u etkileyen A seviyesi bir felaket (büyük deprem, can kaybı) olduysa kutlama tonlu video paylaşılmaz; yerine sakin, saygılı kısa bir mesaj yapılır ya da ertelenir (bildirimde yaz).

## Ton ve içerik
- KUTLAMA günleri: sıcak, samimi, içten; Beyoğlu'na ve semtlerine dokunan bir cümle (ör. "Kasımpaşa'dan Cihangir'e tüm öğretmenlerimiz"). Abartısız, reklam kokmayan. Işık, konfeti, yumuşak renkler.
- ANMA günleri (10 Kasım, 18 Mart, 15 Temmuz, 17 Ağustos): sakin, saygılı; konfeti/havai fişek YOK, koyu zemin, ağır ve yumuşak fon müziği. 17 Ağustos: kayıpları rahmetle anma + deprem hazırlığı hatırlatması (İstanbul için önemli).
- DİNİ günler: "Kandiliniz mübarek olsun", "Bayramınız mübarek olsun" gibi herkesi kucaklayan, sade ifadeler; fıkhi/tartışmalı içerik yok.
- Siyaset, parti, kişi övgüsü YOK. Gerçek kişi fotoğrafı/telifli görsel/müzik YOK; animasyonlu grafik kullan.
- Bilgi verilecekse (ör. tarih, yıl sayısı) yalnızca doğrulanmış bilgi; uydurma YOK.

## Teknik (diğer kurallar aynen geçerli)
- İlk karede (kapak) günün başlığı tam görünür (ör. "ÖĞRETMENLER GÜNÜMÜZ KUTLU OLSUN").
- Her videoda fon müziği; -14 LUFS; 1080x1920; kalite kontrolü (0. kare + 2 ara kare Read, ffprobe, ebur128 -16..-12 LUFS).
- Sayılar bütün okunur (tools/tr_numbers.py). Ses Emre/Aylin; istenirse celebrate.py'deki gibi ikisi birlikte konuşabilir.
- Araç: tools/ozelgun.py (yoksa ilk sefer tools/celebrate.py tabanlı yazılır: "mode": "kutlama" | "anma"; test edilip commit edilir). 15-25 sn, 3-4 sahne + kapanış "Beyoğlu Radar'ı takip et"; RADAR_CITY=beyoglu ile çalıştır ("districts": true 12 semt çipini gösterir).
- Caption: ilk satır günün mesajı + emoji (anmada emoji yok veya 🇹🇷/🤍) + 2 satır içten metin + tek etkileşim çağrısı (ör. "Unutamadığın öğretmenini etiketle 👇", "Bayram mesajını yorumlara yaz") + growth.md hashtag seti (en fazla 5, #beyoğlu #beyogluradar dahil, + #öğretmenlergünü gibi gün etiketi).

## Takvim (dini tarihler: Diyanet takvimini aktaran haberler — Milli Gazete, CNN Türk; 22.11.2026'da okundu)
| Tarih | Gün | Özel gün | Tür |
|---|---|---|---|
| 10.12.2026 | Perşembe | Regaip Kandili | dini |
| 01.01.2027 | Cuma | Yeni yıl | kutlama |
| 04.01.2027 | Pazartesi | Miraç Kandili | dini |
| 22.01.2027 | Cuma | Berat Kandili | dini |
| 08.02.2027 | Pazartesi | Ramazan'ın ilk günü (Hoş geldin Ramazan) | dini |
| 05.03.2027 | Cuma | Kadir Gecesi | dini |
| 08.03.2027 | Pazartesi | Dünya Kadınlar Günü | kutlama |
| 09.03.2027 | Salı | Ramazan Bayramı (1. gün) | dini |
| 14.03.2027 | Pazar | Tıp Bayramı (sağlık çalışanlarına teşekkür) | kutlama |
| 18.03.2027 | Perşembe | Çanakkale Zaferi ve Şehitleri Anma Günü | anma |
| 23.04.2027 | Cuma | 23 Nisan Ulusal Egemenlik ve Çocuk Bayramı | kutlama |
| 09.05.2027 | Pazar | Anneler Günü | kutlama |
| 16.05.2027 | Pazar | Kurban Bayramı (1. gün) | dini |
| 19.05.2027 | Çarşamba | 19 Mayıs Atatürk'ü Anma, Gençlik ve Spor Bayramı | kutlama |
| 20.06.2027 | Pazar | Babalar Günü | kutlama |
| 15.07.2027 | Perşembe | 15 Temmuz Demokrasi ve Milli Birlik Günü | anma |
| 13.08.2027 | Cuma | Mevlid Kandili | dini |
| 17.08.2027 | Salı | 17 Ağustos 1999 Marmara Depremi anması | anma |
| 30.08.2027 | Pazartesi | 30 Ağustos Zafer Bayramı | kutlama |
| 06.10.2027 | Çarşamba | İstanbul'un kurtuluşu (6 Ekim 1923) | kutlama |
| 29.10.2027 | Cuma | 29 Ekim Cumhuriyet Bayramı | kutlama |
| 10.11.2027 | Çarşamba | Atatürk'ü anma | anma |
| 24.11.2027 | Çarşamba | Öğretmenler Günü | kutlama |
| 24.12.2027 | Cuma | Miraç Kandili | dini |

Takvim bitmeden (Kasım 2027) Beyoğlu sabah görevi 2028 tarihlerini güvenilir kaynaktan ekler.

Beyoğlu notu: siyasi kural (growth.md) özel günlerde de geçerli; 29 Mayıs gibi siyasi tartışmaya açık günlerde yalnızca sade tarih bilgisi, demeç/parti dili yok.
