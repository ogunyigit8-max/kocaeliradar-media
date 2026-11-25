# Beyoğlu Radar haber kaynakları

Kocaeli Radar'ın kuralı aynen geçerli: haber EN AZ 1 güvenilir kaynaktan (haber sitesi, ajans veya resmi kurum sayfası) web-fetch ile okunup doğrulanmadan paylaşılmaz. Instagram sayfaları yalnızca haberi FARK ETMEK içindir, tek başına kaynak sayılmaz. Görsel/video kopyalanmaz (telif).

## Nasıl taranır (her çalışmada)
- Siteleri tek tek açma. WebSearch'ü `allowed_domains` ile GRUP GRUP çalıştır (aynı turda paralel). Sorgu örnekleri: "Beyoğlu son dakika", "Taksim", "İstiklal Caddesi", "Karaköy", "Kasımpaşa", "Tarlabaşı", "Cihangir", "Beyoğlu yangın", "Beyoğlu su kesintisi", "Beyoğlu elektrik kesintisi", "Taksim kapalı", "İstiklal tramvay".
- Yalnızca son 24 saatteki (son dakika görevinde son 1-2 saatteki) haberleri al; sayfayı web-fetch alt ajanıyla oku.
- Beyoğlu sınırında olan ama başka ilçede kalan olaylar (Şişli, Beşiktaş, Eminönü/Fatih, Kağıthane) yalnızca Beyoğlu'nu doğrudan etkiliyorsa (yol, ulaşım, köprü) alınır; başlıkta doğru ilçe yazılır.
- Okunamayan siteyi aşağıdaki "Okunabilirlik" bölümüne tarihli not olarak ekle.

## Grup 1: Haber siteleri (en iyi okunanlar önce)
haberler.com/beyoglu, sondakika.com/beyoglu, sabah.com.tr, hurriyet.com.tr (liste tarihsiz, habere tıkla), milliyet.com.tr, cumhuriyet.com.tr, yenicaggazetesi.com, turkiyegazetesi.com.tr/beyoglu, ntv.com.tr, cnnturk.com, sozcu.com.tr

## Grup 2: Ajanslar
aa.com.tr, dha.com.tr (listesi okunamıyor; haberi haberler.com/sabah üzerinden oku), iha.com.tr

## Grup 3: Resmi kurumlar (doğrulama için en güvenilir)
- İlçe: beyoglu.bel.tr (Belediye; Duyurular + Haberler okunuyor), beyoglu.gov.tr (Kaymakamlık)
- İstanbul: istanbul.gov.tr (Valilik: yasaklar, okul tatili), ibb.istanbul, uym.ibb.gov.tr (trafik), akom.ibb.istanbul (afet/hava), istanbul.pol.tr
- Ulaşım: metro.istanbul (M2, F1 Taksim-Kabataş füniküler, T2 Taksim-Tünel nostaljik tramvay, F2 Tünel), iett.istanbul, sehirhatlari.istanbul (Karaköy, Kasımpaşa iskeleleri)
- Kesinti: bedas.com.tr (elektrik), iski.istanbul (su), igdas.istanbul (doğalgaz). Bu siteler doğrudan okunamıyor (25.11.2026): kesintiyi "Beyoğlu su kesintisi <tarih>", "BEDAŞ Beyoğlu <tarih>" aramasıyla haber sitelerinden bul; mahalle ve saat yoksa Reels yapma.
- Afet/hava: deprem.afad.gov.tr (JavaScript; AFAD'ı aktaran haberlere bak), Kandilli, mgm.gov.tr

## Grup 4: Kültür ve etkinlik (haftalık "Beyoğlu'nda bu hafta" karuseli için)
tersaneistanbul.com.tr (Winter Town, Salon Tersane), galataport.com, akmistanbul.gov.tr, iksv.org ve salon.iksv.org, arter.org.tr, peramuzesi.org.tr, istanbulmodern.org, nardisjazz.com, garajistanbul.org; bilet siteleri (biletix.com, passo.com.tr, biletinial.com) yalnızca tarih/saat doğrulaması için; oggusto.com/etkinlik-rehberi. Kullanıcı 25.11.2026'da etkinlik/konser haberlerinin hepsinin yayınlanmasını istedi: günde en fazla 2 etkinlik/konser Reels'i, aynı mekan haftada en fazla 2 Reels; TÜM konserler (kullanıcı 25.11.2026) her gün "Bu akşam Beyoğlu'nda konser" karuselinde; reklam tonu yok. Ücret/saat teyit edilmeden yazılmaz.

## Grup 4b: Yol çalışması ve ulaşım (kullanıcı 25.11.2026)
uym.ibb.gov.tr ve ibb.istanbul duyuruları (yol çalışması, trafik düzenlemesi), beyoglu.bel.tr Duyurular, metro.istanbul ve iett.istanbul duyuruları, sehirhatlari.istanbul sefer duyuruları, İSKİ/İGDAŞ kazı çalışmaları. Doğrudan okunamayanlar için aynı bilgiyi aktaran haber sitelerini ara ("<cadde> yol çalışması", "İETT hat değişikliği", "Şehir Hatları sefer iptal").

## Grup 5: Instagram (yalnızca fark etmek için)
Beyoğlu Belediyesi resmi hesabı, İstanbul son dakika ve trafik sayfaları. Kullanıcıdan takip ettiği yerel hesaplar istenecek.
İzlenecek hesaplar (25.11.2026 rakip analizi; tek başına kaynak DEĞİL, yalnızca haberi fark etmek ve gelişmeyi yakalamak için): @beyoglusondakika34, @istanbul.sondakika, @istanbulduysun, @istanbulhaber_, @beyoglubld, @tc_beyoglu. Etkinlik için mekan hesapları: @tersaneistanbul, @akmistanbul, @galataport.

## Siyasi haber kuralı
growth.md'deki kurala uy: siyasi haberden Reels yok; büyük gelişmede en fazla bir sade hikâye/karusel.

## Okunabilirlik (tarihli notlar; görevler ekler)
- 25.11.2026 (hikâye): hava → windbornesystems İstanbul sayfası bayat ("As of" 24.11), buluttan.com İstanbul Beyoğlu okundu ve kullanıldı. finans.truncgil.com ve tcmb.gov.tr doğrudan curl ile 403 (proxy); web-fetch ile okunabildi.
- 25.11.2026: okunabildi → beyoglu.bel.tr (duyuru 24.11), haberler.com/beyoglu (24.11), sondakika.com/beyoglu (liste eski önbellek, 25.10), turkiyegazetesi.com.tr/beyoglu (26.10), hurriyet Beyoğlu listesi (tarihsiz), tersaneistanbul.com.tr, iett.istanbul (yalnızca ana sayfa). Okunamadı → beyoglu.gov.tr, istanbul.gov.tr, uym.ibb.gov.tr, metro.istanbul, bedas.com.tr, iski.istanbul, igdas.istanbul (robots okunamadı); sehirhatlari.istanbul, dha.com.tr/istanbul/beyoglu-haber, sondakika.beyazgazete.com (client_error); halktv.com.tr (robots engeli, 21.11); deprem.afad.gov.tr (JavaScript, veri yok).
- 25.11.2026 (sabah): okunabildi → sondakika.com, sozcu.com.tr, hurriyet.com.tr haber sayfaları, gencgazete.net (BEDAŞ mahalle listesi, Beyoğlu dahil), mansethaber.com, karar.com, bizimcaz.com (Nardis programı), indigodergisi.com (AKM haftalık), habergazetesi.com.tr (günlük İstanbul konser listesi), tersaneistanbul.com.tr/tr/etkinlikler, etko.app (Salon İKSV). Okunamadı → yenicaggazetesi.com (client_error), nnchaber.com (server_error), birgun.net (gövde boş).
- 25.11.2026 (son dakika 10:47): okunabildi → ntv.com.tr, haberturk.com maç programı (sayfa uzun, kesiliyor), sondakika.com haber sayfası (sayfadaki saat render zamanı, yayın tarihi değil). Okunamadı → akom.ibb.istanbul (robots okunamadı).
- 25.11.2026 (son dakika 13:47): okunabildi → sabah.com.tr haber sayfası (Giriş Tarihi yazıyor), sondakika.com/guncel haber sayfası (yayın saati meta'da). Okunamadı → iett.istanbul/Announcement/Detail (server_error).
