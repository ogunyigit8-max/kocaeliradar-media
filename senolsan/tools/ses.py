"""Bolumun seslendirmesini uretir (Fatih sesi), satir sonlarina 0.35 sn durak koyar, kelime zamanlarini cikarir,
kurgu.json'u (resim kesimleri, flas, oylama karti) yazar.
Kullanim: python3 tools/ses.py b02 KAC KAL
Girdi: bolumler/<b>/satirlar.txt -> tam 7 dolu satir. 1-6 anlatim (her biri bir resim), 7 oylama satiri.
Secenek kelimeleri metinde KUCUK harfle yazilmali (buyuk harfi ses uzatiyor). 6. satirin son cumlesi ters kosedir."""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import anahtar, istek, cok_parcali, json_yaz, KOK

SES_ID = "7VqWGAWwo2HMrylfKrcm"  # Fatih (dizinin sabit sesi)
AYAR = {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35, "speed": 0.88}
TR_KUCUK = str.maketrans("IİÇĞÖŞÜ", "ıiçğöşü")


def kucuk(s):
    return s.translate(TR_KUCUK).lower()


def norm(s):
    return re.sub(r"[^\w]|[\d_]", "", kucuk(s))


def kelimeler(dosya):
    govde, tur = cok_parcali({"model_id": "scribe_v1", "language_code": "tur", "timestamps_granularity": "word"}, {"file": dosya})
    j = istek("https://api.elevenlabs.io/v1/speech-to-text", govde,
              {"xi-api-key": anahtar("ELEVENLABS_API_KEY"), "Content-Type": tur})
    if not j.get("words"):
        raise RuntimeError(f"Konusma yaziya cevrilemedi: {str(j)[:300]}")
    return j


def ek(kelime):
    v = re.findall(r"[aeıioöuü]", kucuk(kelime))
    v = v[-1] if v else "a"
    return {"a": "mı", "ı": "mı", "e": "mi", "i": "mi", "o": "mu", "u": "mu", "ö": "mü", "ü": "mü"}[v]


def wbas(x):
    return x["end"] - 0.6 if x["end"] - x["start"] > 0.8 else x["start"]


def main(bolum, a, b, muzik_sesi=0.45):
    d = os.path.join(KOK, "bolumler", bolum)
    sd = os.path.join(d, "ses"); os.makedirs(sd, exist_ok=True)
    satirlar = [s.strip() for s in open(os.path.join(d, "satirlar.txt"), encoding="utf-8-sig") if s.strip()]
    if len(satirlar) != 7:
        sys.exit(f"satirlar.txt tam 7 dolu satir olmali, {len(satirlar)} var")

    # 1) Seslendirme
    metin = ' <break time="0.8s" /> '.join(s.replace("...", "... ") for s in satirlar)
    mp3 = istek(f"https://api.elevenlabs.io/v1/text-to-speech/{SES_ID}",
                {"text": metin, "model_id": "eleven_multilingual_v2", "voice_settings": AYAR},
                {"xi-api-key": anahtar("ELEVENLABS_API_KEY")}, ham=True)
    ham = os.path.join(sd, "ham.mp3")
    open(ham, "wb").write(mp3)

    # 2) Satir sonlarina 0.35 sn durak
    w = [x for x in kelimeler(ham)["words"] if x.get("type") == "word"]
    sonlar = [norm(s.split()[-1]) for s in satirlar[:6]]
    segs, bas, si = [], 0.0, 0
    for i in range(len(w) - 1):
        if si >= len(sonlar):
            break
        if norm(w[i]["text"]) == sonlar[si]:
            kes = (w[i]["end"] + w[i + 1]["start"]) / 2
            segs.append((bas, kes)); bas = kes; si += 1
    segs.append((bas, 999))
    f, lbl = [], []
    for i, (s0, s1) in enumerate(segs):
        f.append(f"[0:a]atrim=start={s0:.3f}:end={s1:.3f},asetpts=PTS-STARTPTS[a{i}]"); lbl.append(f"[a{i}]")
        if i < len(segs) - 1:
            f.append(f"aevalsrc=0:s=44100:d=0.35[s{i}]"); lbl.append(f"[s{i}]")
    f.append("".join(lbl) + f"concat=n={len(lbl)}:v=0:a=1[out]")
    anlatim = os.path.join(sd, "anlatim.mp3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", ham, "-filter_complex", ";".join(f), "-map", "[out]",
                    "-ar", "44100", "-b:a", "192k", anlatim], check=True)

    # 3) Son kelime zamanlari
    j = kelimeler(anlatim)
    json_yaz(os.path.join(sd, "kelimeler.json"), j)
    w = [x for x in j["words"] if x.get("type") == "word"]
    ilk = [norm(s.split()[0]) for s in satirlar]
    basl, p = [], 0
    for li in range(7):
        bul = next((q for q in range(p, len(w)) if norm(w[q]["text"]) == ilk[li]), None)
        if bul is None:
            sys.exit(f"Satir {li + 1} baslangici bulunamadi: {ilk[li]}")
        basl.append(wbas(w[bul])); p = bul + 1
    cumleler = [c for c in re.split(r"(?<=[.!?:])\s+", satirlar[5]) if norm(c)]
    tk = norm(cumleler[-1].split()[0])
    flas = basl[5] + 1
    for x in w:
        if x["start"] >= basl[5] and norm(x["text"]) == tk:
            flas = wbas(x)
    son = round(w[-1]["end"] + 1.5, 2)
    cfg = {
        "kesimler": [round(max(0.5, basl[i] - 0.15), 2) for i in range(1, 6)],
        "flas": round(flas - 0.02, 2),
        "oylama_bas": round(basl[6] - 0.3, 2),
        "oylama_ust": f"{a} {ek(a)}, {b} {ek(b)}?",
        "oylama_alt": "Yoruma yaz",
        "son": son,
        "muzik_sesi": muzik_sesi,
    }
    json_yaz(os.path.join(d, "kurgu.json"), cfg)
    print(f"Ses: {anlatim}  sure: {son} sn")
    print(json.dumps(cfg, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else 0.45)
