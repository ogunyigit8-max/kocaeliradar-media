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
- 23.11.2026 08:35: okunabildi → ozgunkocaeli.com.tr/sondakika-haberleri (en yeni 00:03), sondakika.com/kocaeli-izmit (08:14 kopyası). Okunamadı (client_error) → istekocaeli.com, bugunkocaeli.com.tr.
- 23.11.2026 09:35: okunabildi → ozgunkocaeli.com.tr/sondakika-haberleri (en yeni 00:03), sondakika.com/kocaeli-izmit (22.11 14:32), haberturk deprem listesi. Okunamadı (PROVENANCE_REQUIRED) → istekocaeli.com.
- 23.11.2026 10:35: okunabildi → ozgunkocaeli.com.tr/sondakika-haberleri (en yeni 00:03), haberturk.com (MGM sarı kod 06:26). Okunamadı (client_error) → istekocaeli.com, gundemkocaeli.com.tr.
- 23.11.2026 11:35: okunabildi → milliyet.com.tr deprem galerisi (09:55). Okunamadı → duzcedamla.com, istekocaeli.com (client_error), habersosyal.com.tr (SERVER_ERROR).
- 23.11.2026 12:35: okunabildi → haberturk.com (AKOM 11:19), ozgunkocaeli.com.tr (valilik uyarısı). Okunamadı → sondakika.com/kocaeli (PROVENANCE_REQUIRED), kocaeligundem.com (client_error).
- 23.11.2026 13:35: okunabildi → haber41.com.tr (eski 08.01 fırtına haberi), ozgunkocaeli.com.tr/sondakika-haberleri (en yeni 00:03). Okunamadı (client_error) → cagdaskocaeli.com.tr ana sayfa.
- 23.11.2026 14:35: okunabildi → kartepebulteni.com (eski haber, 10.07). sondakika.com/kocaeli-izmit yine eski önbellek (27.10). Okunamadı (client_error) → seskocaeli.com.
- 23.11.2026 15:35: okunabildi → golcukpostasi.com, haberturk.com. Okunamadı (client_error) → seskocaeli.com, enkocaeli.com, kocaelikoz.com, ozgurkocaeli.com.tr.
- 24.11.2026 22:35: okunabildi → sabah.com.tr/son-depremler/kocaeli (kayıt yok), haberler.com/kocaeli (eski önbellek 27.10). Okunamadı (client_error) → ozgurkocaeli.com.tr, istekocaeli.com, seskocaeli.com.
- 24.11.2026 23:35: okunabildi → sondakika.com/kocaeli (yine eski önbellek 27.10). Okunamadı (client_error) → seskocaeli.com, istekocaeli.com.
- 25.11.2026 00:35: okunabildi → hurriyet.com.tr (MGM 24.11 21:35), ozgunkocaeli.com.tr (00:05, Bolu kazası), haberturk.com (eski 2024 sayfası).
- 25.11.2026 01:35: okunabildi → sondakika.com/kocaeli (en yeni 24.11 23:19). Okunamadı (client_error) → noktagazetesi.com.tr, istekocaeli.com.
- 25.11.2026 02:35: okunabildi → sondakika.com/kocaeli (en yeni 24.11 23:19); okunamadı (client_error) → cagdaskocaeli.com.tr haber sayfası.
- 25.11.2026 03:35: okunabildi → sondakika.com/kocaeli-kaza (en yeni 21.11). Okunamadı (client_error) → ozgurkocaeli.com.tr ana sayfa.
- 25.11.2026 05:35: okunamadı (client_error) → kocaeligazetesi.com.tr, cagdaskocaeli.com.tr, seskocaeli.com haber sayfaları (valilik fırtına uyarısı).
