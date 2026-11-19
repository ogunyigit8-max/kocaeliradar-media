"""Bolum videosunu birlestirir: resimler (yavas yaklasma) + anlatim + altyazi + oylama karti + flas + muzik.
Kullanim: python3 tools/kurgu.py b02   -> bolumler/b02/b02.mp4
Gerekenler: bolumler/<b>/cekimler/01..06.png, ses/anlatim.mp3, ses/kelimeler.json, kurgu.json.
Muzik: bolumler/<b>/ses/muzik.mp3 yoksa sabit/muzik.mp3 (dizinin sabit muzigi)."""
import glob, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import json_oku, KOK

FONT = "DejaVu Sans"


def font_var():
    try:
        out = subprocess.run(["fc-match", "-f", "%{family}", "DejaVu Sans:bold"], capture_output=True, text=True).stdout
        return out.split(",")[0] or FONT
    except Exception:
        return FONT


def T(s):
    h = int(s // 3600); m = int((s % 3600) // 60); x = s % 60
    return f"{h}:{m:02d}:{x:05.2f}"


def main(bolum):
    d = os.path.join(KOK, "bolumler", bolum)
    cfg = json_oku(os.path.join(d, "kurgu.json"))
    imgs = sorted(glob.glob(os.path.join(d, "cekimler", "*.png")))
    cuts = [0] + list(cfg["kesimler"]) + [cfg["son"]]
    if len(cuts) - 1 != len(imgs):
        sys.exit(f"Kesim sayisi ({len(cuts) - 1}) resim sayisiyla ({len(imgs)}) uyusmuyor")
    tmp = os.path.join(d, "_gecici"); os.makedirs(tmp, exist_ok=True)

    # 1) Her resim icin yavas yaklasan klip
    liste = []
    for i, img in enumerate(imgs):
        fr = int(round((cuts[i + 1] - cuts[i]) * 30))
        vf = (f"scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
              f"zoompan=z='1+0.08*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps=30,format=yuv420p")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", img, "-vf", vf, "-frames:v", str(fr),
                        "-c:v", "libx264", "-crf", "18", "-preset", "fast", os.path.join(tmp, f"k{i}.mp4")], check=True)
        liste.append(f"file 'k{i}.mp4'")
    open(os.path.join(tmp, "liste.txt"), "w").write("\n".join(liste) + "\n")

    # 2) Altyazi (en fazla 3 kelimelik parcalar)
    w = [x for x in json_oku(os.path.join(d, "ses", "kelimeler.json"))["words"] if x.get("type") == "word"]
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
        if c[0]["end"] - c[0]["start"] > 0.8:
            s = c[0]["end"] - 0.6
        if i + 1 < len(chunks):
            e = min(e, chunks[i + 1][0]["start"])
        txt = " ".join(x["text"] for x in c).replace('"', "")
        ev.append(f"Dialogue: 0,{T(s)},{T(e)},Alt,,0,0,0,,{{\\pos(540,1400)}}{txt}")
    ob, os_ = float(cfg["oylama_bas"]), float(cfg["son"])
    ev.append(f"Dialogue: 1,{T(ob)},{T(os_)},Oy,,0,0,0,,{{\\pos(540,420)\\fad(250,0)}}{cfg['oylama_ust']}")
    ev.append(f"Dialogue: 1,{T(ob + 0.4)},{T(os_)},OyAlt,,0,0,0,,{{\\pos(540,560)\\fad(250,0)}}{cfg['oylama_alt']}")
    f = font_var()
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Alt,{f},72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,6,3,5,60,60,0,162
Style: Oy,{f},98,&H0000D7FF,&H00FFFFFF,&H00000000,&HB4000000,-1,0,0,0,100,100,0,0,1,8,4,5,40,40,0,162
Style: OyAlt,{f},68,&H00FFFFFF,&H00FFFFFF,&H00000000,&HB4000000,-1,0,0,0,100,100,0,0,1,6,3,5,40,40,0,162

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n"
    open(os.path.join(tmp, "altyazi.ass"), "w", encoding="utf-8").write(ass)

    # 3) Birlestir
    fl, fl2 = float(cfg["flas"]), float(cfg["flas"]) + 0.12
    fo = os_ - 2.5
    mv = float(cfg.get("muzik_sesi") or 0.6)
    muzik = os.path.join(d, "ses", "muzik.mp3")
    if not os.path.exists(muzik):
        muzik = os.path.join(KOK, "sabit", "muzik.mp3")
    cikti = os.path.join(d, f"{bolum}.mp4")
    fc = (f"[0:v]drawbox=x=0:y=0:w=iw:h=ih:color=white@0.85:t=fill:enable='between(t,{fl},{fl2})',subtitles=altyazi.ass[v];"
          f"[1:a]aresample=48000,apad,asplit=2[n][nk];"
          f"[2:a]aresample=48000,volume={mv},afade=t=in:d=1.5,afade=t=out:st={fo}:d=2.5[m0];"
          f"[m0][nk]sidechaincompress=threshold=0.05:ratio=3:attack=40:release=600[m];"
          f"[n][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "liste.txt",
                    "-i", os.path.join(d, "ses", "anlatim.mp3"), "-stream_loop", "-1", "-i", muzik,
                    "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", str(os_), "-r", "30",
                    "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", cikti],
                   check=True, cwd=tmp)
    print(f"Hazir: {cikti}")


if __name__ == "__main__":
    main(sys.argv[1])
