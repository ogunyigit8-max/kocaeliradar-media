# Bulut günlük görevi: yeni bölümü üret ve 20:00'de @senolsannesecerdin'e paylaş

Yiğit (sahibi) 19.11.2026'da onayladı: her gün bölüm, yorumlardaki oy çoğunluğuna göre senaryo, Reels + aynı video hikaye,
yorumlara cevap, analize göre ayarları sürekli iyileştirme. Paylaşım için ayrıca onay beklenmez.
Kök klasör: deponun içindeki senolsan/ (aşağıdaki tüm yollar buna göre). Araçlar Python 3 + ffmpeg (tools/).
Anahtarlar ortam değişkeninde: KIE_API_KEY, ELEVENLABS_API_KEY. Bunları ASLA yazdırma, dosyaya ya da depoya koyma.
Önce oku: STRATEJI.md (kurallar + "Güncel ayarlar"; bu tarifle çelişirse o geçerli), hikaye_defteri.md, durum.json, karakter.md.

## 0. Ön kontrol
- Saat dilimi Europe/Istanbul. durum.json'daki son bölümün paylasim_zamani bugünse DUR.
- Windsor get_connectors: instagram hesabı 17841458144556548 yoksa üretimi yap ama paylaşma; bildirimde "Instagram bağlantısı koptu" de.
- durum.json'da tarihi bugün olan 'hazir_bolum' varsa: adım 1'de oyları yine say. Kazanan 'varsayilan_sonuc' ile aynıysa adım 2-5'i ATLA, hazır videoyu (video_url, açık adreste duruyor mu kontrol et) ve hazır açıklamayı ({ORAN} gerçek oranla) kullanarak adım 6'dan devam et. Kazanan farklıysa bölümü adım 2-5 ile yeniden üret. Paylaşımdan sonra 'hazir_bolum' kaydını sil.

## 1. Oyları say + yorumlara cevap
- Windsor get_data: connector instagram, accounts ["17841458144556548"],
  fields [media_id, comment_id, comment_text, comment_username, comment_timestamp], date_preset "last_7dT".
- Sadece son bölümün media_id'si. senolsannesecerdin'in kendi yorumlarını sayma. Her kullanıcı tek oy (en son yorumu).
  Türkçe büyük harfe çevir; secenek_a ya da secenek_b (Türkçe karakterli/karaktersiz: AÇ/AC, GÖTÜR/GOTUR) içeren yorum o seçeneğe oy.
  İkisini de içeren ya da hiçbirini içermeyen sayılmaz.
- Eşitlik/oy yok: hikayeyi daha gerilimli ilerleten seçeneği seç, dürüst cümle kullan ("Kararı ilk izleyiciler verdi"). Oy sayısı UYDURMA.
- durum.json (sonuc, oylar {a,b}) ve hikaye_defteri.md'ye yaz.
- Cevapsız yorumlardan en fazla 10'una reply_to_comment ile kısa, samimi, birbirinden farklı cevap (STRATEJI.md bölüm 2).
  Cevaplananları durum.json "cevaplanan_yorumlar" listesine ekle.

## 2. Yeni bölümü yaz (bXX = sonraki numara, iki haneli)
- hikaye_defteri.md ile tutarlı; kazanan seçimin sonucu hemen ilk satırda görülsün.
- İkinci tekil şahıs, kısa cümleler, 70-100 kelime, TAM 7 satır: 1-6 anlatım (her satır bir resim; 1. satır STRATEJI.md
  kanca kuralı), 6. satırın son cümlesi ters köşe; 7. satır: "<soru>? <a küçük harf>, ya da <b küçük harf>, yaz. <Sonraki> bölümü çoğunluk yazar."
- Yeni iki seçenek: tek kelime, zıt, kolay yazılır (KAÇ/KAL, ARA/SUS...). Seslendirme metninde KÜÇÜK harf.
- Sayıları yazıyla yaz. Gerçek kişi/marka yok. Şiddet ima düzeyinde, kan/vahşet yok.
- bolumler/bXX/satirlar.txt (UTF-8, 7 satır) ve bolumler/bXX/senaryo.md (metin + 6 çekim istemi).

## 3. Resimler (6 adet, 9:16)
- Her istem: [sahne, ışık, kamera açısı, renkler] + karakter.md "Sabit tarif" cümlesi kelimesi kelimesine + karakter.md "Stil satırı"
  + STRATEJI.md'deki resim istemi ek kuralı. Yeni karakter gerekiyorsa renkleriyle tarif et, hikaye_defteri.md'ye sabit tarif ekle.
- bolumler/bXX/cekimler.json yaz: [{"prompt": "...", "cikti": "bolumler/bXX/cekimler/01.png"}, ... 06]
- `cd senolsan && python3 tools/gorsel.py --toplu bolumler/bXX/cekimler.json` (6'sı paralel, karakter sayfası referans).
- Her resme Read ile bak: Emre turuncu mont + siyah kask + turuncu çanta, okunur yazı/logo yok, sahne doğru.
  Bozuğu tek tek yeniden üret: `python3 tools/gorsel.py --prompt "..." --cikti ... --ref karakter/karakter_sayfasi.png` (en fazla 1 kez).

## 4. Ses
- `python3 tools/ses.py bXX <A BÜYÜK> <B BÜYÜK> <STRATEJI.md müzik sesi>` (Fatih sesi, duraklar, kurgu.json).
- Süre STRATEJI.md hedefinin dışındaysa metni kısalt/uzat ve tekrar üret.

## 5. Video
- `python3 tools/kurgu.py bXX` -> bolumler/bXX/bXX.mp4 (müzik: sabit/muzik.mp3, değiştirme).
- Kontrol: ffprobe 1080x1920 + ses akışı; ffmpeg ile 3-4 kare çıkar ve Read ile bak (altyazı okunur, yüzün üstünde değil,
  Türkçe harfler doğru, oylama kartı görünüyor). Sorun varsa düzelt, düzelmeden paylaşma.

## 6. Paylaş (20:00)
- 20:00'den önceyse 20:00'e kadar bekle (sleep). Geçtiyse hemen paylaş.
- url=$(python3 tools/yayin.py bolumler/bXX/bXX.mp4)  (videoyu senolsan/v/ içine koyar, push eder, açık GitHub adresini verir;
  önceki adımların değişiklikleri de o anda commit edilmiş olsun ki çakışma olmasın)
- Windsor execute_action: connector instagram, account 17841458144556548, action create_video_post,
  params {video_url: url, caption, share_to_feed: true, thumb_offset: 2000}. Hata olursa 60 sn bekle, bir kez tekrar dene.
- Açıklama ve oylama yorumu: STRATEJI.md "Güncel ayarlar" kalıpları. Oran sadece gerçek oy varsa ("Siz seçtiniz: %NN AÇ.").
- create_comment ile oylama yorumu; sonra create_story {video_url: url} (video 60 sn'den uzunsa ilk 59 sn'yi bXX_hikaye.mp4 olarak kesip yayin.py ile ayrı koy).
- durum.json'a yeni bölüm (no, klasor, media_id, oylama_yorum_id, hikaye_id, paylasim_zamani ISO +03:00, secenek_a, secenek_b,
  sonuc null, oylar null), son_bolum artır. hikaye_defteri.md'ye bölüm özeti + açık sırlar.

## 7. Kaydet
- mp4 sadece senolsan/v/ içinde olur (yayin.py koyar, 4 günden eskisini siler). Bölüm klasörlerine mp4 koyma.
- git add senolsan; commit (user.name "Sen Olsan", user.email noreply@anthropic.com);
  `git pull --rebase origin main` sonra `git -c push.negotiate=true push origin HEAD:main`. Depodaki başka klasörlere DOKUNMA.

## 8. Bildirim
PushNotification (<routine_summary> etiketiyle), sade Türkçe, 4-6 satır: oy sonucu, bölümün tek cümlelik özeti,
Reels + hikaye paylaşıldı mı (varsa link), kaç yoruma cevap verildi, sorun varsa ne.
