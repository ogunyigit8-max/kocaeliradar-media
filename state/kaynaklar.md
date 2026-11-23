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
- 22.11.2026 17:35: Okunamadı → sondakika.com/kocaeli (PROVENANCE_REQUIRED), kocaelikoz.com, istekocaeli.com, seskocaeli.com (client_error).
- 22.11.2026 18:35: okunabildi → ozgunkocaeli.com.tr (haber sayfası), golcukpostasi.com, hurriyet.com.tr. Okunamadı (client_error) → demokratkocaeli.com, kocaelitv.com.tr, istekocaeli.com.
- 22.11.2026 20:35: okunamadı (client_error) → seskocaeli.com/kocaeli-son-dakika-haberler, ozgurkocaeli.com.tr ana sayfa.
- 22.11.2026 21:35: okunabildi → sondakika.com/kocaeli (en yeni 20:53), cumhuriyet.com.tr (deprem listesi 08:59). haberler.com/kocaeli eski önbellek (27.10). Okunamadı (client_error) → enkocaeli.com, istekocaeli.com.
- 22.11.2026 22:35: okunabildi ama eski önbellek → sondakika.com/kocaeli (27.10), sondakika.com/kocaeli-kaza (24.10); hurriyet okul tatili galerisi 2022 tarihli.
- 22.11.2026 23:35: okunabildi → haberler.com/kocaeli (20:54 kopyası). Okunamadı (client_error) → istekocaeli.com, kocaeligundem.com.
- 23.11.2026 01:35: okunabildi → sondakika.com/kocaeli (en yeni 22.11 20:53), tekkocaeli.com (eski haber). Okunamadı (client_error) → istekocaeli.com.
- 23.11.2026 02:35: Okunamadı → demokratkocaeli.com (client_error), koeri.boun.edu.tr (http/https yönlendirme döngüsü).
- 23.11.2026 03:35: okunabildi → sondakika.com/kocaeli (en yeni 22.11 20:53). Okunamadı (client_error) → istekocaeli.com, demokratkocaeli.com.
- 23.11.2026 04:35: okunabildi → sondakika.com/kocaeli-izmit (en yeni 22.11 13:41), sabah.com.tr/son-depremler/kocaeli (kayıt yok).
- 23.11.2026 05:35: Okunamadı (client_error) → enkocaeli.com (haber sayfası).
- 23.11.2026 08:20 (sabah): okunabildi → kocaelikentgazetesi.com (kesinti listesi), ozgunkocaeli.com.tr, sondakika.com/kocaeli, ntv, dha, milligazete, tgrthaber, karar, trthaber, haberturk.com/gundem, mavikocaeli, gazetevatan, timeturk. Okunamadı (client_error) → kocaelitv, cagdaskocaeli, kocaelibarisgazetesi, kocaeligazetesi, kocaelidenge, demokratkocaeli, seskocaeli, noktagazetesi, aydinlik, iha; golcukhaber (ROBOTS); kocaeli.bel.tr/haberler 404.
- 23.11.2026 08:35: okunabildi → ozgunkocaeli.com.tr/sondakika-haberleri (en yeni 00:03), sondakika.com/kocaeli-izmit (08:14 kopyası). Okunamadı (client_error) → istekocaeli.com, bugunkocaeli.com.tr.
- 23.11.2026 09:35: okunabildi → ozgunkocaeli.com.tr/sondakika-haberleri (en yeni 00:03), sondakika.com/kocaeli-izmit (22.11 14:32), haberturk deprem listesi. Okunamadı (PROVENANCE_REQUIRED) → istekocaeli.com.
- 23.11.2026 10:35: okunabildi → ozgunkocaeli.com.tr/sondakika-haberleri (en yeni 00:03), haberturk.com (MGM sarı kod 06:26). Okunamadı (client_error) → istekocaeli.com, gundemkocaeli.com.tr.
