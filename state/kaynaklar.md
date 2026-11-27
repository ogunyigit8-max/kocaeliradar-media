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
- 26.11.2026 05:35: okunabildi → sondakika.com/kocaeli (05:30 damgalı, en yeni 26.11 01:49 spor).
- 26.11.2026 07:35: okunabildi → golcukpostasi.com (eski 15.10 haberi). Okunamadı (PROVENANCE_REQUIRED) → sondakika.com/kocaeli.
- 26.11.2026 08:00 (sabah): okunabildi → ozgunkocaeli.com.tr (26.11 kesinti listesi, 25.11 18:07), sondakika.com haber sayfası (motorin), isinolsa.com/akaryakit-fiyatlari/kocaeli, mavikocaeli.com.tr (ana sayfa + haber), kocaelimeydan.com/sondakika-haberleri, gebzeilkhaber.com, gebzehaber.net. Okunamadı → kocaelitv.com.tr, cagdaskocaeli.com.tr, kocaeligazetesi.com.tr, gundemkocaeli.com.tr, 24saatgazetesi.com (client_error); yenigebze.com.tr, golcukhaber.com.tr (ROBOTS_UNREACHABLE); yerel-haberler.haberturk.com, kocaelimeydan haber sayfası (PROVENANCE_REQUIRED).
- 26.11.2026 08:35: okunabildi → sondakika.com/kocaeli. Okunamadı (client_error) → noktagazetesi.com.tr, istekocaeli.com.
- 26.11.2026 10:35: okunabildi → fotomac.com.tr, haberturk.com/spor, ajansspor.com, hurriyet.com.tr/sporarena (maç saat/kanal). Okunamadı → ozgurkocaeli.com.tr (client_error); aa.com.tr haber metni boş.
- 26.11.2026 11:35: okunabildi → sondakika.com/kocaeli (11:30 damgalı, en yeni 26.11 01:49).
- 26.11.2026 12:35: okunabildi → sondakika.com/kocaeli (footer 12:22, öğe saatleri tutarsız/önbellek olabilir).
- 26.11.2026 13:35: okunabildi → sondakika.com/kocaeli (13:33). Okunamadı (client_error) → ozgurkocaeli.com.tr.
- 26.11.2026 14:35: okunabildi → sondakika.com/kocaeli (14:28). Okunamadı (client_error) → kocaelidenge.com.
- 26.11.2026 18:35: okunabildi → sondakika.com/kocaeli (18:33 damgalı, bugün en yeni 15:46). Okunamadı (client_error) → seskocaeli.com haber, istekocaeli.com.
- 26.11.2026 23:35: okunamadı → sondakika.com/kocaeli (PROVENANCE_REQUIRED), istekocaeli.com (client_error).
- 27.11.2026 01:35: okunabildi → sondakika.com/kocaeli (01:33 damgalı, en yeni 27.11 01:30), ntv.com.tr deprem listesi. Okunamadı (client_error) → istekocaeli.com, seskocaeli.com.
- 27.11.2026 02:35: okunabildi → sondakika.com/kocaeli (footer 02:33, en yeni 27.11 01:30).
- 27.11.2026 03:35: okunabildi → sondakika.com/kocaeli (footer 03:34, en yeni 27.11 01:30).
- 27.11.2026 04:35: okunabildi → sondakika.com/kocaeli-izmit (04:32 damgalı, en yeni 23.11), sondakika.com/kocaeli-kaza (en yeni 21.11).
