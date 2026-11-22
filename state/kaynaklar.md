# Kocaeli Radar haber kaynakları

Kullanıcı 21.11.2026'da onayladı: tüm gruplar (yerel siteler, resmi kurumlar, ulusal ajanslar, rakip Instagram sayfaları) taranır. Doğrulama kuralı aynı kalır: haber EN AZ 1 güvenilir kaynaktan (haber sitesi, ajans veya resmi kurum sayfası) web-fetch ile okunup doğrulanmalı. Instagram sayfaları yalnızca haberi FARK ETMEK içindir, tek başına kaynak sayılmaz.

## Nasıl taranır (her çalışmada)
- Siteleri tek tek açma. WebSearch'ü `allowed_domains` ile GRUP GRUP çalıştır (aşağıdaki her grup bir arama; aynı turda paralel gönder). Sorgu örnekleri: "Kocaeli son dakika", "<ilçe> son dakika", "Kocaeli kaza yangın", "Kocaeli kesinti", "Kocaeli uyarı".
- Sonuçlardan yalnızca son 24 saatteki (son dakika görevinde son 1-2 saatteki) haberleri al; sayfayı web-fetch alt ajanıyla oku.
- Okunabilirlik notu: bir site okunamazsa (client_error) aynı haberi başka gruptaki sitelerden oku. Okunabilen/okunamayan siteleri aşağıdaki "Okunabilirlik" bölümüne kısa not olarak ekle (tarihli), ki sonraki çalışmalar okunabilenleri öne alsın.

## Grup 1: Kocaeli geneli büyük yerel siteler
ozgurkocaeli.com.tr, cagdaskocaeli.com.tr, kocaeligazetesi.com.tr, bizimyaka.com, ozgunkocaeli.com.tr, kocaelikentgazetesi.com, kocaelitv.com.tr, bugunkocaeli.com.tr, seskocaeli.com, demokratkocaeli.com, kocaelikoz.com, kocaeligundem.com, kocaelihalkgazetesi.com, haber41.com.tr, kocaelihaberci.com

## Grup 2: Diğer Kocaeli geneli siteler
mavikocaeli.com.tr, 41havadis.com, bizimgazete.com.tr, buyukkocaeli.com.tr, degisenkocaeli.com, finanskocaeli.com, golgegazetesi.com, gundemkocaeli.com.tr, hedefgazetesi.com.tr, kirkbir.com, kocaelihaberdunyasi.com, kocaelimeydan.com, kocaelioncu.com, kocaelipusula.com, kocaelisanayigazetesi.com, kocaelisokak.com, kulishaber.com.tr, mansetmarmara.com, millihakimiyet.com, nefesgazetesi.com, onursalhaber.com.tr, kocaelisonnokta.com, sozkocaeli.com, yakintakipgazetesi.com, mavimarmaragazetesi.com, istekocaeli.com, enkocaeli.com, aydinlikkocaeli.com, kocaeliseyret.com

## Grup 3: Gebze, Darıca, Çayırova, Dilovası
yenigebze.com, yenigebze.com.tr, gebzehaber.net, gebzegundem.com, bizimgebze.com, gazetegebze.com.tr, gebzeyenigun.com, yenibolgegazetesi.com, gebzeilkhaber.com, gebzeyenihaber.com, gebzehurses.com, gebzegazetesi.com, marmaragazetesi.com, bizimdarica.com, daricagazetesi.com.tr

## Grup 4: İzmit doğusu ve körfez ilçeleri (Derince, Körfez, Gölcük, Karamürsel, Başiskele, Kartepe, Kandıra)
derinceekspres.org, korfezgazetesi.com.tr, korfezmanset.com, golcukhaber.com.tr, golcukpostasi.com, golcukvizyongazetesi.com, yenigolcuk.com, haberkaramursel.net, karamurselaktifhaber.com, karamursel.tv, basiskelehaber.com, haberkartepe.com, kartepegazetesi.com.tr, kartepebulteni.com, kandiraninsesi.com

## Grup 5: Ulusal ajanslar ve siteler (Kocaeli sayfaları)
aa.com.tr, dha.com.tr, iha.com.tr, yerel-haberler.haberturk.com, sabah.com.tr, hurriyet.com.tr, sondakika.com, haberler.com, ntv.com.tr, sozcu.com.tr, cnnturk.com

## Grup 6: Resmi kurumlar (doğrulama için en güvenilir)
- Valilik ve il: kocaeli.gov.tr, kocaeli.pol.tr (Emniyet), kocaeli.meb.gov.tr (okul tatili), kocaeli.jandarma.gov.tr
- Belediyeler: kocaeli.bel.tr (Büyükşehir, İSU ve UlaşımPark duyuruları dahil), isu.gov.tr, ulasimpark.com.tr, izmit.bel.tr, gebze.bel.tr, darica.bel.tr, cayirova.bel.tr, dilovasi.bel.tr, korfez.bel.tr, derince.bel.tr, golcuk.bel.tr, karamursel.bel.tr, basiskele.bel.tr, kartepe.bel.tr, kandira.bel.tr
- Afet ve hava: afad.gov.tr, deprem.afad.gov.tr, koeri.boun.edu.tr (Kandilli), mgm.gov.tr (sayfalar JavaScript'li; boş gelirse MGM'yi aktaran haber sitelerine bak)
- Ulaşım ve altyapı: kgm.gov.tr, tcddtasimacilik.gov.tr, sedas.com (elektrik kesintisi), izgaz.com.tr (doğalgaz)

## Grup 7: Rakip/yerel Instagram sayfaları (yalnızca haberi fark etmek için)
@cagdaskocaeligazetesi, @bugunkocaeli, @kocaeli.koz, @enkocaeli, @aydinlikkocaeli, @istekocaelicom, @kocaelimeydan
- WebSearch ile "site:instagram.com <hesap>" veya hesap adı + "son dakika" ara. Burada görülen haberi Grup 1-6'daki bir siteden doğrulamadan PAYLAŞMA. Görselleri/videoları kullanma (telif).

## Okunabilirlik (tarihli notlar; görevler ekler)
- 22.11.2026 04:32: okunabildi → sondakika.com/kocaeli (en yeni 21.11 21:29), ozgunkocaeli.com.tr/sondakika-haberleri. Okunamadı (client_error) → istekocaeli.com, cagdaskocaeli.com.tr.
- 22.11.2026 05:35: okunabildi → ozgunkocaeli.com.tr/sondakika-haberleri (önbellek eski), ntv.com.tr/deprem/kocaeli. Okunamadı → sondakika.com/kocaeli (PROVENANCE_REQUIRED), kocaelikoz.com (client_error).
- 22.11.2026 06:32: okunabildi → sondakika.com/kocaeli (en yeni 21.11 21:29), sondakika.com/kocaeli-yangin (eski önbellek 25.10), ozgunkocaeli.com.tr/sondakika-haberleri (eski önbellek). Okunamadı (client_error) → istekocaeli.com, kocaelitv.com.tr.
- 22.11.2026 07:35: okunabildi → sondakika.com/kocaeli (en yeni 21.11 21:29), ozgunkocaeli.com.tr/sondakika-haberleri (eski önbellek). Okunamadı (client_error) → istekocaeli.com.
- 22.11.2026 08:15 (sabah): okunabildi → ozgunkocaeli.com.tr (haber sayfaları), daricagazetesi.com.tr, mavikocaeli.com.tr, golcukpostasi.com, hurriyet.com.tr, ntv.com.tr, milligazete.com.tr, politikam.com. Okunamadı (client_error) → cagdaskocaeli.com.tr, kocaelikoz.com, kocaelitv.com.tr, kocaeligazetesi.com.tr; sondakika.com ve mgm.gov.tr/sunum (PROVENANCE_REQUIRED).
- 22.11.2026 08:35: okunabildi → sondakika.com/kocaeli (eski önbellek, 27.10). Okunamadı (client_error) → kocaeligazetesi.com.tr.
- 22.11.2026 09:35: okunabildi → sondakika.com/kocaeli-izmit (en yeni 21.11), haberler.com/kocaeli (kısmi), kocaelimeydan.com. Okunamadı → istekocaeli.com, kocaeligundem.com (client_error), koeri.boun.edu.tr (yönlendirme döngüsü).
- 22.11.2026 10:35: okunabildi → ozgunkocaeli.com.tr/sondakika-haberleri (eski önbellek), sondakika.com/kocaeli-izmit (en yeni 21.11 17:30), gebzehaber.net (tarihsiz). Okunamadı (client_error) → istekocaeli.com, enkocaeli.com, bugunkocaeli.com.tr.
- 22.11.2026 11:35: okunabildi → sondakika.com/kocaeli-izmit (en yeni 21.11 17:30), hurriyet.com.tr (MGM sarı kod 21 il, Kocaeli yok). Okunamadı (client_error) → ozgurkocaeli.com.tr.
- 22.11.2026 12:35: okunabildi → sabah.com.tr/son-depremler/kocaeli (kayıt yok). Okunamadı → seskocaeli.com, istekocaeli.com (client_error), sondakika.com/kocaeli (PROVENANCE_REQUIRED).
- 22.11.2026 13:35: okunabildi → hurriyet.com.tr (haber sayfası), haberler.com/kocaeli (12:02 kopyası, 22.11 yeni Kocaeli haberi yok). Okunamadı → bugunkocaeli.com.tr, seskocaeli.com (client_error), kocaeli.gov.tr (ROBOTS_UNREACHABLE).
- 22.11.2026 14:32: okunabildi → aa.com.tr, memurlar.net (20-21.11 sarı kod 24 il, eski). Okunamadı (client_error) → kocaelikoz.com, kocaeligazetesi.com.tr, ensonhaber.com, kocaelibarisgazetesi.com.
- 22.11.2026 15:37: okunabildi → sondakika.com/kocaeli (en yeni 14:56), hurriyet.com.tr. Okunamadı (client_error) → seskocaeli.com.
- 22.11.2026 16:35: okunabildi → hurses.com.tr, medyahaber.com. Okunamadı (client_error) → seskocaeli.com, kocaelikoz.com, haberglobal.com.
- 22.11.2026 17:35: Okunamadı → sondakika.com/kocaeli (PROVENANCE_REQUIRED), kocaelikoz.com, istekocaeli.com, seskocaeli.com (client_error).
