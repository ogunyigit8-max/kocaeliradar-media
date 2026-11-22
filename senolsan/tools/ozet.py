"""Pazar 'Simdiye kadar' ozet Reels'i: ses.py (Fatih sesi, ayni ayarlar) + kurgu.py tarzi (yaklasma, altyazi, muzik).
Kullanim: python3 tools/ozet.py ozetler/2026-11-22/ozet.json
ozet.json: {"satirlar": [{"metin": "...", "resim": "bolumler/b02/cekimler/02.png"}, ...]}
  Son satir resimsiz olabilir (bir onceki resim uzar). Cikti: ayni klasorde ozet_<klasor adi>.mp4
Oylama karti yok; ilk 2 sn ustte "Simdiye kadar...", son 3 sn ustte sari "Bu aksam 19:00 · Yeni bolum" karti."""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import anahtar, istek, json_oku, json_yaz, KOK
from ses import SES_ID, AYAR, kelimeler
from kurgu import T, font_var

DURAK = 0.5


def sure(yol):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", yol],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def main(cfg_yol):
    cfg_yol = os.path.join(KOK, cfg_yol) if not os.path.isabs(cfg_yol) else cfg_yol
    d = os.path.dirname(cfg_yol)
    ad = os.path.basename(d)
    cfg = json_oku(cfg_yol)
    sat = cfg["satirlar"]
    sd = os.path.join(d, "ses"); tmp = os.path.join(d, "_gecici")
    os.makedirs(sd, exist_ok=True); os.makedirs(tmp, exist_ok=True)

    # 1) Her satir ayri seslendirilir (Fatih, ses.py ayarlari), aralara 0.5 sn durak
    parcalar, bas, t = [], [], 0.0
    for i, s in enumerate(sat):
        yol = os.path.join(sd, f"s{i:02d}.mp3")
        mp3 = istek(f"https://api.elevenlabs.io/v1/text-to-speech/{SES_ID}",
                    {"text": s["metin"].replace("...", "... "), "model_id": "eleven_multilingual_v2", "voice_settings": AYAR},
                    {"xi-api-key": anahtar("ELEVENLABS_API_KEY")}, ham=True)
        open(yol, "wb").write(mp3)
        bas.append(t)
        t += sure(yol) + (DURAK if i < len(sat) - 1 else 0)
        parcalar.append(yol)
    f, lbl, giris = [], [], []
    for i, p in enumerate(parcalar):
        giris += ["-i", p]
        f.append(f"[{i}:a]aresample=44100,aformat=channel_layouts=mono[a{i}]"); lbl.append(f"[a{i}]")
        if i < len(parcalar) - 1:
            f.append(f"aevalsrc=0:s=44100:d={DURAK}[s{i}]"); lbl.append(f"[s{i}]")
    f.append("".join(lbl) + f"concat=n={len(lbl)}:v=0:a=1[out]")
    anlatim = os.path.join(sd, "anlatim.mp3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *giris, "-filter_complex", ";".join(f), "-map", "[out]",
                    "-ar", "44100", "-b:a", "192k", anlatim], check=True)
    j = kelimeler(anlatim)
    json_yaz(os.path.join(sd, "kelimeler.json"), j)
    w = [x for x in j["words"] if x.get("type") == "word"]
    son = round(w[-1]["end"] + 1.5, 2)

    # 2) Resim klipleri (resimsiz satir bir oncekine eklenir)
    gruplar = []
    for i, s in enumerate(sat):
        if s.get("resim") or not gruplar:
            gruplar.append([s.get("resim"), bas[i]])
    kes = [g[1] for g in gruplar] + [son]
    kes[0] = 0
    liste = []
    for i, (img, _) in enumerate(gruplar):
        fr = int(round((kes[i + 1] - kes[i]) * 30))
        vf = (f"scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
              f"zoompan=z='1+0.08*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps=30,format=yuv420p")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", os.path.join(KOK, img), "-vf", vf,
                        "-frames:v", str(fr), "-c:v", "libx264", "-crf", "18", "-preset", "fast",
                        os.path.join(tmp, f"k{i}.mp4")], check=True)
        liste.append(f"file 'k{i}.mp4'")
    open(os.path.join(tmp, "liste.txt"), "w").write("\n".join(liste) + "\n")

    # 3) Altyazi (kurgu.py ile ayni tarz) + baslik + son kart
    chunks, cur = [], []
    for x in w:
        cur.append(x)
        if len(cur) >= 3 or re.search(r'[.?!,:]"?$', x["text"]):
            chunks.append(cur); cur = []
    if cur:
        chunks.append(cur)
    ev = []
    for i, c in enumerate(chunks):
        s, e = c[0]["start"], c[-1]["end"] + 0.25
        if i + 1 < len(chunks):
            e = min(e, chunks[i + 1][0]["start"])
        txt = " ".join(x["text"] for x in c).replace('"', "")
        ev.append(f"Dialogue: 0,{T(s)},{T(e)},Alt,,0,0,0,,{{\\pos(540,1400)}}{txt}")
    ev.append(f"Dialogue: 1,{T(0)},{T(2.0)},Bas,,0,0,0,,{{\\pos(540,380)\\fad(0,300)}}Şimdiye kadar...")
    ev.append(f"Dialogue: 1,{T(son - 3)},{T(son)},Kart,,0,0,0,,{{\\pos(540,400)\\fad(250,0)}}Bu akşam 19:00 · Yeni bölüm")
    fnt = font_var()
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Alt,{fnt},72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,6,3,5,60,60,0,162
Style: Bas,{fnt},110,&H00FFFFFF,&H00FFFFFF,&H00000000,&HB4000000,-1,0,0,0,100,100,0,0,1,8,4,5,40,40,0,162
Style: Kart,{fnt},76,&H00000000,&H00FFFFFF,&H0000D7FF,&H0000D7FF,-1,0,0,0,100,100,0,0,3,24,0,5,40,40,0,162

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n"
    open(os.path.join(tmp, "altyazi.ass"), "w", encoding="utf-8").write(ass)

    # 4) Birlestir (kurgu.py ile ayni muzik/ses zinciri)
    muzik = os.path.join(KOK, "sabit", "muzik.mp3")
    fo = son - 2.5
    cikti = os.path.join(d, f"ozet_{ad}.mp4")
    fc = (f"[0:v]subtitles=altyazi.ass[v];"
          f"[1:a]aresample=48000,apad,asplit=2[n][nk];"
          f"[2:a]aresample=48000,volume={cfg.get('muzik_sesi', 0.45)},afade=t=in:d=1.5,afade=t=out:st={fo}:d=2.5[m0];"
          f"[m0][nk]sidechaincompress=threshold=0.05:ratio=3:attack=40:release=600[m];"
          f"[n][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "liste.txt",
                    "-i", anlatim, "-stream_loop", "-1", "-i", muzik,
                    "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", str(son), "-r", "30",
                    "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", cikti],
                   check=True, cwd=tmp)
    print(f"Hazir: {cikti}  sure: {son} sn")


if __name__ == "__main__":
    main(sys.argv[1])
