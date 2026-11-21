# Kocaeli Radar — Büyüme Kuralları (güncel)
Son güncelleme: 2026-11-21 gece. Diğer görevler bu dosyayı okuyup uygular.
Etiketler: [VERİ] kendi metriklerimiz · [META] Meta/Instagram kaynaklı · [KAYNAK] 3. taraf veri · [ÖNERİ] test edilecek.

## Durum ve hedef
- 21.11 gece: 790 takipçi (20.11 gece 612 → ~+178/24 sa). Günlük erişim 21.11 22,4 bin (rekor; takip etmeyen %98,6), 335 paylaşım. Sebep: HİBRİT kesinti Reels'i (08:01, Emre, "Gebze'de 8 saat: bugün 10 ilçede") 27,3 bin erişim, 439 paylaşım, 46 kayıt (%1,78 paylaşım+kayıt/erişim), atlama %44, ort. 10,2 sn → hesabın en iyi videosu. [VERİ]
- Seyir: 16.11 ~107 → 17.11 428 → 18.11 511 → 19.11 564 → 20.11 ~640 → 21.11 790. Yeni takipçi 16.11 +268 · 17.11 +221 · 18.11 +32 · 19.11 +68 · 20.11 +77 · 21.11 ~+150. Günlük erişim 17,6 / 20,0 / 5,7 / 8,0 / 11,7 / 22,4 bin. [VERİ]
- Büyüme hâlâ viral videolara bağlı: 5 bin+ erişimli video olan günler +150–270, olmayan günler +30–80. [VERİ]
- Erişimin %95–99'u takip etmeyenlerden → büyüme tamamen Keşfet/öneriden geliyor. [VERİ]
- Takipçi dönüşümü (yeni takipçi / günlük erişim): 16.11 %1,5 · 17.11 %1,1. [VERİ]
- Büyüme hızı: 4 günde ~+457; son 48 saatte ~+85 (günde ~43). Viral video (5 bin+ erişim) olan günler +200 üstü; olmayan günler +30–55. [VERİ]
- Projeksiyon (TAHMİN, 21.11): viral olmayan gün ~+60, viral gün ~+150–250 → 1.000 takipçi ≈ 23–25 Kasım. Aralık sonu: viral yoksa ~2,5 bin, haftada 1–2 viral günle 4–5 bin. Sabah Reels'i atlanan gün erişim yarıya iniyor → üretim kesintisi en büyük risk. 23.11'de 7 günlük ortalamayla yeniden hesapla.
- Kıyas: <1.000 takipçili hesaplarda Reels medyan erişimi ~134; 1–5 bin takipçide Reels başına ort. ~580 izlenme → bizim tüm videolarımız (aralık kuralına uyulanlar) 1.300+ erişimde. [KAYNAK: netinfluencer/Metricool, Socialinsider]
- Hedef metrikler: ilk 3 sn atlama < %40 (17–18.11 ort. ~%46; 19.11 ort. %53,6 — kötüleşiyor), ort. izlenme ≥ 10 sn (19.11 ort. 7,1 sn), paylaşım+kayıt / erişim ≥ %1. Instagram'ın evrensel atlama eşiği yok; kendi son 10–20 Reels medyanımızla kıyasla. [VERİ + KAYNAK: TrueFuture Media]

## Kitle (Instagram Insights, 19.11, 490 takipçi kırılımı) [VERİ]
- Cinsiyet: erkek %53, kadın %26, belirsiz %20. Yaş: 35–54 %56, 25–34 %17, 55+ %19, 18–24 %6.
- İlçe: Gebze ekseni (Gebze 92, Darıca 50, Şekerpınar 19, Tuzla 14) en büyük blok; İzmit 60, Derince 31, Sarımeşe 28, Gölcük 26, Hereke 13, Karamürsel 11. Kandıra/Kartepe zayıf.
- Sonuç: yetişkin, işe gidip gelen, aile/çocuk sahibi kitle → ulaşım, kesinti, servis/okul, fatura/fiyat, güvenlik. Gebze–Darıca–Çayırova haberine öncelik; başlıkta ilçe adı.
- Ses [VERİ, 10 Reels, konu karışık]: Aylin (6) ort. atlama %49,4 / izlenme 7,9 sn; Emre (4) %48,8 / 8,9 sn → Emre hafif önde ama konu etkisinden ayrıştırılamıyor; ses değiştirme gerekçesi yok.
- Hikâye: 21.11 erişim 19–452 (en iyi 2 hikâye 404/452 — viral gün takipçi artışıyla), paylaşım hep 0 → büyüme kanalı değil, takipçiye hatırlatma. [VERİ]
- Yorumlar: kesinti videolarında "Derince'de kesilecek mi?", "kesilmedi?" soruları → kişiye özel bilgi talebi (karusel bunu çözer). Kaza/uyarı haberlerinde doğruluk itirazları ("1 ölü var", "yalan sıkmayın") → rakamı "ilk bilgilere göre" ve saatle ver, gelişince güncelle.

## Karusel + kesinti Reels (HİBRİT — 20.11 kullanıcı onayı, veriye göre)
- Kesinti günlerinde sabah 1. video KISA KESİNTİ REELS'i (18–25 sn, 3–4 sahne, outage sim): ilk sahnede ilçe sayısı + en uzun/en kalabalık kesinti, her gün FARKLI açı (dünkü başlığı tekrarlama), son sahne "Tüm mahalle listesi profilimizde". Keşfet erişimi buradan gelir.
- Tam mahalle listesi AYRICA karusel (Reels'ten ≥30 dk sonra) — takipçiye ve aramaya hizmet; büyüme kanalı değil.
- Karusel üretimi: `python3 tools/carousel.py spec.json` → c/<tarih>-<slug>/01..NN.jpg (4:5, 1080x1350) + story.jpg. Reels yalnızca büyük kesintide (≥5 ilçe ve ≥8 saat, ya da Gebze/İzmit merkezde geniş).
- Yapı: 1) kapak: ilçe sayısı + en çarpıcı bilgi (sarı bant), harita pinleri, "MAHALLEN LİSTEDE Mİ? KAYDIR" 2) ÖZET kare (ilçe · mahalle sayısı · saat) — Instagram geçilen karuseli 2. kareyle yeniden gösterebildiği için kendi başına anlaşılır 3..) mahalle listesi (ilçe başlıklı, saat sağda) son) GÖNDER / KAYDET / TAKİP ET + arıza hattı. En fazla 10 kare, tek şablon.
- Paylaşım: önce hikâye (story.jpg, create_story image_url), sonra create_carousel_post (items: her kare image_url + alt_text "Kocaeli <tarih> elektrik kesintisi: <ilçe> <mahalleler> <saat>"). Karusel Reels 60 dk kuralına sayılmaz; Reels'ten en az 30 dk uzak tut.
- Caption: "⚡ Kocaeli elektrik kesintisi <gün Ay>: <N> ilçede, en uzun <ilçe> <süre>" + "Mahallen listede mi? Kaydır 👉" + "Listede mahallesi olan birine gönder." + Kaynak + kesinti hashtag seti. API ile karusele müzik eklenemiyor; başarı ölçütü kayıt+gönderim/erişim ve media_follows. [KAYNAK: uppbeat 03.11.2026; karusel rehberleri (görüş); ÖNERİ]
- HİBRİT DOĞRULANDI (21.11) [VERİ n=1]: kısa kesinti Reels'i 27,3 bin erişim / 439 paylaşım; aynı günün karuseli 330 erişim, 11 paylaşım, 0 takip, 2 profil ziyareti. Reels büyüme, karusel hizmet — akış böyle kalsın. Reels caption'ındaki "Tüm mahalle listesi profilimizde" yönlendirmesi kalsın.
- İLK SONUÇ (20.11) [VERİ n=1]: kesinti karuseli (Reels'siz) 238 erişim (takipçinin ~%28'i → neredeyse yalnız takipçiler), 0 paylaşım, 0 kayıt, 0 takip, 3 profil ziyareti. Kıyas: kesinti Reels'leri 1,9–9,2 bin erişim, 15–66 paylaşım. Fanpage Karma (Oca–Nis 2026, 3 mn+ gönderi): <10 bin takipçide takipçi başına medyan erişim Reels %4,9 vs karusel %2,6; Reels ~3 kat daha çok takip etmeyene ulaşıyor. [KAYNAK] → Karusel tek başına Keşfet büyümesini durduruyor; karar kullanıcıda (öneri: kısa kesinti Reels'i + ayrıntı karuseli, ya da karuseli uygulamadan müzikle elle paylaşmak). Karar gelene kadar akış değişmez; 26.11 kıyası yine yapılacak.
- Ölçüm: karuselde media_follows / media_profile_visits ölçülebiliyor (Reels'te değil) → hangi içeriğin takip getirdiğini buradan öğren.

## Yorumlar
- 21.11 viral kesinti Reels'inde 13 yorum: "Nenehatun var mı", "Erenler var mı" (mahalle sorusu → cevap: "Tam liste profildeki kaydırmalı gönderide"), "kesilmedi / gitti" durum bildirimi, ve "Bugün yerine tarih deseniz daha iyi olur" → ekrandaki başlıkta ve ilk cümlede "bugün" yerine/yanında TARİH yaz ("21 Kasım'da 10 ilçede…"); video ertesi gün de öneriliyor. [VERİ n=1 + ÖNERİ]
- Yorumlardaki SORULARA kısa, doğrulanmış, nazik cevap (ör. "Derince'de bugün Çenedağ ve Çınarlı'da 09.00-17.00; net bilgi SEDAŞ 186"); hakaret/polemik/siyasete cevap yok. Kesinti iptal/kayma şikâyeti ("Yoo kesilmedi", "kesilmedi?") tekrarlıyor → caption'da "SEDAŞ planı; çalışma iptal/kayabilir" notu ekle. [VERİ + ÖNERİ] Otomatik cevap HENÜZ AKTİF DEĞİL — kullanıcının açık onayı bekleniyor. [ÖNERİ]

## Paylaşım aralığı (EN ÖNEMLİ)
- İki Reels arasında EN AZ 60 dk (tercihen 2+ saat). 16.11'de dakikalar içinde atılan 4 video ~180–245 erişimde kaldı; 17.11'de 2–3 saat arayla atılan 4 videonun hepsi 1.390+ erişim aldı. Kural doğrulandı. [VERİ]
- Sabah görevi yalnızca 1. videoyu hemen paylaşır; diğerlerini saatlik son dakika görevi 12:31, 15:31, 18:31, 21:31'de birer birer paylaşır. (21.11: kullanıcı günde 4 sabah videosuna çıkardı.)
- Son dakika (A) istisnadır; ama 60 dk içinde başka Reels atılmışsa sıradaki video bir sonraki slota kayar.
- Günde 3–5 Reels yeterli; medya sektörü ortalaması haftada ~32 gönderi. Sayıyı değil kaliteyi artır. [KAYNAK: Dash Social]

## Keşfet'e (öneriye) uygunluk — ihlal etme
- Mosseri (Kas 2026, ikincil kaynak): yeni üreticiler için "erişim başına gönderim" muhtemelen en önemli metrik; müzikli KARUSEL artık Reels akışında da görünebiliyor ve kaydırılıp geçilirse 2. kareyle tekrar gösterilebiliyor. [META, ikincil: uppbeat 03.11.2026]
- Sıralama sinyalleri: izlenme süresi/tamamlama, erişim başına beğeni, erişim başına GÖNDERİM (DM) en güçlüleri (Mosseri, Oca 2025, ikincil kaynak). "Your Algorithm" konu kontrolleri Reels (Ara 2025) → Keşfet (Nis 2026) → Akış (Haz 2026): caption'da konu net olsun ("Kocaeli", "elektrik kesintisi", "trafik kazası"). [KAYNAK: SocialPilot, Eyl 2026]
- Özgün içerik: kendi ürettiğimiz harita/grafik/anlatım videoları uygundur. Başka hesapların videosunu/ekran görüntüsünü yeniden yükleme (aggregator sayılır, hesap önerilerden çıkar). [META]
- Siyasi içerik (yasa, seçim, hükümet, parti tartışmaları) takip etmeyenlere varsayılan olarak ÖNERİLMEZ. Belediye haberini "hizmet/etki" açısıyla ver (yol, su, ulaşım, kesinti), siyasi polemik/demeç yapma. [META]
- Tıklama tuzağı, etkileşim dilenciliği ("beğen, takip et, paylaş" zorlaması), yanıltıcı başlık öneri dışı bırakılır. [META]
- Görünür başka uygulama filigranı yok. 3 dakikadan uzun Reels yok. [META]
- Tazelik: önerilen Reels'in ~%45'i 1 günden yeni (Meta 3. çeyrek 2026 bilançosu) → haberi aynı gün, mümkünse ilk saatlerde ver; dünkü haberi ertesi gün yeniden paketleme. [META]
- Profesyonel panel > Hesap Durumu'nu haftada bir kontrol et (kullanıcıya hatırlat).

## Başlık formülleri (ekrandaki büyük başlık + caption ilk satırı)
1. Yer + olay + somut sayı: "Gebze'de minibüs devrildi: 19 yaralı"
2. Sayı + karşılaştırma: "871 işletme kapandı, artış %109"
3. Etkilenen kişi/yer önce: "10 ilçede elektrik yok: hangi mahalleler?"
4. Zaman + uyarı: "Bu gece başlıyor: Kocaeli'ye kuvvetli sağanak uyarısı"
5. Değişim/fark: "Motorin 1 haftada X TL arttı" (salt liste değil, DEĞİŞİM)
6. Net bilgi + ilçe: "Derince'ye 120 yataklı acil durum hastanesi"
7. Kurum + karar + etki: "Büyükşehir'den yeni karar: kimleri etkiliyor?"
- ≤ 8–10 kelime, ilçe adı başta. "ŞOK", "inanamayacaksınız", "bomba" YOK.

## Hook kuralları (ilk sahne, ilk 2 sn)
- İlk karede başlık tam görünür (news.py yapıyor); EN ÇARPICI SAYI/ETKİ ilk sahnede. [VERİ: sayılı başlıklar en düşük atlama]
- İlk cümle doğrudan olay: "Gebze'de 19 kişi yaralandı." Selamlama/giriş YOK.
- Rutin içerikte hook = değişim veya etki ("Yarın sabah yağmur, işe gidiş saatine denk geliyor").
- Toplam süre 20–35 sn; 35 sn'yi geçme (18.11 elektrik 38,8 sn: atlama %47, 2,2 bin erişim). [VERİ zayıf + ÖNERİ]
- Hook'ta izleyiciye doğrudan soru/etki: "Mahallen listede mi?" gibi ilk 2 sn'de kişisel bağ kur; liste okuma ile açma. [ÖNERİ]

## Caption kalıbı
1. satır: emoji (🔴 son dakika / ⚡ / 🌧️ / 🚗) + başlık (ilçe + olay + sayı). Instagram araması caption'ı kullanır → anahtar kelimeyi düz yaz ("Gebze trafik kazası", "elektrik kesintisi"). [META]
2–3. satır: 2–3 cümle özet (ne, nerede, ne zaman, kimi etkiliyor).
Etkileşim: TEK somut, konuya özel soru → "Bu güzergâhı kullanıyor musunuz?" / "Mahallenizde kesinti var mı?"
Gönderim çağrısı (servis/uyarı haberleri): "Bu yolu kullanan birine gönder." DM gönderimi takip etmeyenlerde en güçlü sinyal. Zorlayıcı "beğen+paylaş" yazma. [META]
Kaynak: "Kaynak: AA, DHA" — her zaman.
Son: hashtag seti (EN FAZLA 5 etiket — Instagram Aralık 2025'ten beri gönderi başına 5 hashtag sınırı uyguluyor).

## Hashtag setleri (TOPLAM ≤5; her sete EN İLGİLİ TEK İLÇE etiketi eklenir: #izmit #gebze #darıca #çayırova #dilovası #körfez #derince #gölcük #karamürsel #başiskele #kartepe #kandıra)
- Son dakika: #kocaeli #kocaeliradar #sondakika #kocaelihaber + ilçe
- Trafik/ulaşım: #kocaeli #kocaeliradar #kocaelitrafik #d100 + ilçe (TEM ise #tem)
- Ekonomi: #kocaeli #kocaeliradar #ekonomi #kocaeliesnaf + ilçe
- Hava: #kocaeli #kocaeliradar #havadurumu #kocaelihavadurumu + ilçe
- Belediye/hizmet: #kocaeli #kocaeliradar #kocaelibüyükşehir #kocaelihaber + ilçe
- Kesinti/servis: #kocaeli #kocaeliradar #elektrikkesintisi (veya #sukesintisi) + ilçe
- Spor: #kocaeli #kocaeliradar #kocaelispor + ilçe
- Hashtag dağıtım kanalı değil, konu etiketi. Instagram sınırı 5: 6+ etiket yazma (17.11 elektrik ve fırtına caption'larında 6 vardı). Birden çok ilçe varsa ilçe adlarını caption metninde düz yaz (arama caption'ı okur). [KAYNAK: Social Media Today/Business Today, Ara 2025]

## En iyi paylaşım saatleri
- Kendi veri (3 gün): 19:42 son dakika 11,6 bin; 08:14 elektrik 8,9 bin (17.11) ama 08:09 elektrik 2,2 bin (18.11); 15:41 fırtına uyarısı 4,8 bin; 12:33–12:34 2,0 / 1,7 bin; 18:34 spor 1,5 bin. Konu ve tazelik saatten büyük etki yapıyor. [VERİ]
- Plan: ~08:15 (sabah 1. video: kesinti/trafik/hava), 12:31, 18:31, 21:31. 7–14 gün sonra saat bazlı erişimle güncellenecek. [ÖNERİ]

## Öncelikli konu türleri
1. Son dakika kaza/olay (somut sayı, yer) [VERİ: en yüksek erişim]
2. Halkı etkileyen ekonomik/yerel veri (esnaf, kira, fiyat DEĞİŞİMİ) [VERİ: en çok paylaşım+kayıt]
3. Servis: elektrik/su kesintisi, yol kapanması, resmî uyarılar [VERİ: 17.11 elektrik 6,7 bin erişim/52 paylaşım; fırtına uyarısı 3,4 bin]
4. Seri formatlar: "Kocaeli'de bugün: 3 başlık" (sabah), "Akşam trafik/yol durumu" — alışkanlık yaratır. [ÖNERİ]
- Tekrarlayan günlük format yorulması: elektrik kesintisi 17.11 9,1 bin → 18.11 2,4 bin → 19.11 1,9 bin (atlama %43→%47→%55). [VERİ, n=3, doğrulandı] Günlük kesintiyi her gün 1. video yapma; yalnızca geniş/uzun (≥5 ilçe veya ≥8 saat, ya da kalabalık ilçe Gebze/İzmit merkez) ise ver, başlığı her gün farklı açıyla kur (en uzun kesinti/en kalabalık mahalle önde). [VERİ, n=2]
- Paylaşım üretmeyen konular: baraj doluluk (0 paylaşım, 1,7 bin), spor maç önü (2 paylaşım) → bilgi iyi ama "birine gönder" sebebi yok. Servis/uyarı haberleri (elektrik, hat değişikliği, fırtına) paylaşımın asıl kaynağı (Darıca hatları %1,7 paylaşım+kayıt/erişim, en iyi oran). [VERİ]
- En iyi gönderim oranı = "yarın/bu gece" uyarısı + durumsal gönder çağrısı: 19.11 17:38 fırtına (yarın sabah) 2,7 bin erişim, 46 paylaşım (%1,9 paylaşım+kayıt/erişim, şimdiye kadarki en iyi). Aynı gün sabah "bugün" fırtına %1,2. → Uyarıyı olaydan ÖNCEKİ akşam ver. [VERİ]
- Hava uyarılarında "bugün" videoları yüksek atlama (%53–60; 19.11 %60, 20.11 %53) — "yarın/bu gece" olanlar %50 ve daha çok paylaşım (19.11 17:38 → güncel 5,3 bin erişim, 91 paylaşım). Temsili görsel + tekrar eden hava konusu muhtemel neden; ilk sahnede etkilenen saat/yer ve somut eşik ver. [VERİ]
- Akaryakıt fiyatı zayıf: 16.11 273 erişim, 21.11 benzin indirimi 360 erişim (viral videodan 3,5 sa sonra) → yalnızca büyük değişimde (≥2 TL) ve 1. video değilse kısa ver. Maç sonucu da paylaşım getirmedi (21.11 2-2: 1,1 bin, 0 paylaşım; maç önü 1,4 bin) → spor haftada 1. [VERİ]
- Kurumsal denetim/istatistik haberleri (servis denetimi 19.11: 1,3 bin, 1 paylaşım) zayıf. [VERİ]
- Aynı gün aynı konuyu iki kez Reels yapma (19.11 iki fırtına videosu); ikinci kez yalnızca yeni gelişme varsa. [VERİ + ÖNERİ]
- Düşük öncelik: salt fiyat listesi, genel hava, kurumsal vizyon (COP31 tipi), siyasi demeçler.

## Büyüme taktikleri (sırasıyla)
1. Collab (ortak gönderi): yerel işletme/mahalle/ilçe sayfaları ve muhabirlerle ortak Reels; 10 bin altı hesaplarda kabul edilmiş collab gönderileri ~5 kat etkileşim aldı (korelasyon). Davet kullanıcı onayıyla yapılır. [KAYNAK: Emplifi]
2. Her Reels'i hikâyede paylaş (zaten yapılıyor) + ilk yoruma kaynak/detay yorumu sabitle. [ÖNERİ]
3. Son dakikada hız: aynı olayı ilk veren yerel hesap olmak; büyük olaylarda (kaza, yangın) gelişme videosu (yaralı durumu, yol açıldı mı) ile seriye dönüştür. [ÖNERİ; Gebze kazası viral oldu]
4. Trial Reels: bir 3. taraf rehber (superprofile, 30.10.2026, Instagram Yardım'a atıfla) profesyonel hesaplarda alt sınırı 200 takipçi diyor; Metricool 1.000 diyor → uygulamada Reels paylaşırken "Deneme" seçeneği görünüyor mu kontrol et. Graph API ile deneme paylaşımı belgelenmemiş → elle. Tek değişken test et (hook cümlesi veya kapak). [KAYNAK, doğrulanmadı]
5. Karusel: kesinti listeleri karusele taşındı (19.11, kullanıcı onayı). 26.11'de karusel vs eski kesinti Reels'i kıyasla: erişim, kayıt+gönderim/erişim, takip.
6. Özgün katkı: veri karşılaştırması, harita, "size etkisi" açıklaması — salt haber metni okumak yetmez. [ÖNERİ]

## Rakip/örnek sayfalar (izlenecek)
- @kocaeligundem: hypeauditor/instastatistics 17–20.11 arası okunamadı (instastatistics canlı veri yüklemiyor); rakam yok. Gerekirse kullanıcıdan profil sayısını iste.
- Ulusal: @bpthaber (~3,2 mn), @trthaber (~3,15 mn, ER %0,16), @tvahaber (~1,74 mn), @tvgundemi (~569 bin, ER %0,85), @sondakika.turkiye (~340 bin, ER %0,69).
- Yerel: @kocaeligundem (doğrudan rakip; hypeauditor/socialveins/livecounts 17.11'de okunamadı), @igdir_havadis (~54,6 bin), @polatlihaberleri (~50,7 bin), @hayaleturkcom (Bursa, ~24,6 bin). Kaynak: socialveins/livecounts (Nisan 2026). [KAYNAK]

## Kaçınılacaklar
- Peş peşe Reels (min. 60 dk kuralı).
- Clickbait, abartı, doğrulanmamış bilgi, kaynaksız haber; siyasi polemik.
- Başkasının videosunu yeniden yüklemek; görünür filigran.
- 3 dk'dan uzun Reels; 5'ten fazla / alakasız hashtag.
