"""Kocaeli Radar günlük hikâye görselleri.

Kullanım:  python3 tools/stories.py data/YYYY-MM-DD.json
Çıktı:     s/YYYY-MM-DD-hava.jpg, -altin.jpg, -dolar.jpg, -euro.jpg  (1080x1920)

data JSON örneği:
{
  "date": "2026-11-16",
  "weather": {"location": "Kocaeli (İzmit)", "high": 16, "low": 8, "condition": "Parçalı bulutlu",
              "icon": "partly", "rain": 10,
              "next": [{"day": "Salı", "high": 17, "low": 10, "icon": "rain"}, ...],
              "source": "Hava tahmini"},
  "gold":  {"gram_buy": 6276.47, "gram_sell": 6277.52, "quarter_buy": 10290, "quarter_sell": 10374,
            "prev_gram_sell": null, "time": "06:00", "source": "Truncgil Finans"},
  "usd":   {"buy": 50.3806, "sell": 50.3973, "prev_sell": null, "time": "06:00", "source": "Truncgil Finans"},
  "eur":   {"buy": 55.5539, "sell": 55.5865, "prev_sell": null, "time": "06:00", "source": "Truncgil Finans"}
}
icon: sun | partly | cloud | rain | storm | snow | fog
"""
import json, math, os, sys, datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
W, H = 1080, 1920
YEL = (255, 204, 0); RED = (226, 35, 45); GRN = (60, 190, 110); WHITE = (255, 255, 255); BLACK = (10, 10, 12)
GREY = (190, 194, 200)
AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
GUNLER = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

_fc = {}
def font(size, w=700):
    k = (size, w)
    if k not in _fc:
        f = ImageFont.truetype(os.path.join(A, "Oswald.ttf"), size)
        try: f.set_variation_by_axes([w])
        except Exception: pass
        _fc[k] = f
    return _fc[k]

def text(d, xy, s, size, fill, w=700, anchor="la", sp=0):
    f = font(size, w)
    if not sp:
        d.text(xy, s, font=f, fill=fill, anchor=anchor); return
    tw = sum(f.getlength(c) for c in s) + sp * (len(s) - 1)
    x, y = xy
    if anchor[0] == "m": x -= tw / 2
    elif anchor[0] == "r": x -= tw
    for c in s:
        d.text((x, y), c, font=f, fill=fill, anchor="l" + anchor[1]); x += f.getlength(c) + sp

def tr_num(x, dec=2):
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")

def tr_date(iso):
    dt = datetime.date.fromisoformat(iso)
    return f"{dt.day} {AYLAR[dt.month - 1]} {dt.year}", GUNLER[dt.weekday()]

def base(tag, date_iso):
    im = Image.open(os.path.join(A, "story_bg.jpg")).convert("RGBA").resize((W, H))
    d = ImageDraw.Draw(im)
    # top brand bar
    logo = Image.open(os.path.join(A, "logo.jpg")).convert("RGB").resize((104, 104))
    m = Image.new("L", (104, 104), 0); ImageDraw.Draw(m).ellipse([0, 0, 103, 103], fill=255)
    im.paste(logo, (64, 150), m)
    text(d, (186, 166), "KOCAELİ RADAR", 44, WHITE, 700, "la", 3)
    text(d, (188, 222), "@kocaeliradar41", 26, GREY, 500, "la", 1)
    ds, gun = tr_date(date_iso)
    text(d, (W - 64, 168), ds.upper(), 30, WHITE, 600, "ra", 1)
    text(d, (W - 64, 210), gun.upper(), 26, YEL, 600, "ra", 2)
    # tag
    f = font(54, 700); tw = f.getlength(tag) + 6 * len(tag)
    d.rectangle([64, 330, 64 + tw + 60, 420], fill=BLACK + (235,)); d.rectangle([64, 330, 76, 420], fill=YEL)
    text(d, (100, 375), tag, 54, WHITE, 700, "lm", 6)
    return im, d

def card(im, box, fill=(12, 13, 16, 225), outline=None):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    x0, y0, x1, y1 = box
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([x0 + 8, y0 + 12, x1 + 8, y1 + 12], 28, fill=(0, 0, 0, 160))
    lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    dl.rounded_rectangle(box, 28, fill=fill, outline=outline, width=4 if outline else 0)
    im.alpha_composite(lay)
    return ImageDraw.Draw(im)

def footer(d, src, time=None):
    s = f"Kaynak: {src}" + (f" · {time}" if time else "")
    text(d, (W / 2, 1640), s, 26, GREY, 400, "mm", 1)

# ---------- icons ----------
def sun(d, cx, cy, r):
    for k in range(12):
        a = k * math.pi / 6
        d.line([(cx + math.cos(a) * r * 1.3, cy + math.sin(a) * r * 1.3), (cx + math.cos(a) * r * 1.65, cy + math.sin(a) * r * 1.65)], fill=YEL, width=int(r * 0.16))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=YEL)

def cloud(d, cx, cy, s, col=(235, 238, 242)):
    d.ellipse([cx - s * 0.95, cy - s * 0.15, cx - s * 0.25, cy + s * 0.5], fill=col)
    d.ellipse([cx - s * 0.55, cy - s * 0.55, cx + s * 0.25, cy + s * 0.35], fill=col)
    d.ellipse([cx - s * 0.05, cy - s * 0.35, cx + s * 0.75, cy + s * 0.45], fill=col)
    d.ellipse([cx + s * 0.35, cy - s * 0.05, cx + s * 0.95, cy + s * 0.5], fill=col)
    d.rectangle([cx - s * 0.6, cy + s * 0.1, cx + s * 0.65, cy + s * 0.5], fill=col)

def weather_icon(d, kind, cx, cy, s):
    if kind == "sun": sun(d, cx, cy, s * 0.55)
    elif kind == "partly": sun(d, cx + s * 0.35, cy - s * 0.3, s * 0.38); cloud(d, cx - s * 0.1, cy + s * 0.15, s * 0.8)
    elif kind in ("cloud", "fog"):
        cloud(d, cx + s * 0.25, cy - s * 0.2, s * 0.55, (150, 156, 166)); cloud(d, cx - s * 0.1, cy + s * 0.1, s * 0.8)
        if kind == "fog":
            for k in range(3): d.line([(cx - s * 0.8, cy + s * 0.75 + k * s * 0.18), (cx + s * 0.8, cy + s * 0.75 + k * s * 0.18)], fill=GREY, width=int(s * 0.07))
    elif kind in ("rain", "storm", "snow"):
        cloud(d, cx, cy - s * 0.15, s * 0.85, (170, 176, 186) if kind != "snow" else (235, 238, 242))
        for k in range(4):
            x = cx - s * 0.5 + k * s * 0.33; y = cy + s * 0.55
            if kind == "snow": d.ellipse([x - s * 0.06, y - s * 0.06 + (k % 2) * s * 0.15, x + s * 0.06, y + s * 0.06 + (k % 2) * s * 0.15], fill=WHITE)
            else: d.line([(x + s * 0.06, y), (x - s * 0.06, y + s * 0.3)], fill=(90, 170, 255), width=int(s * 0.08))
        if kind == "storm":
            d.polygon([(cx + s * 0.05, cy + s * 0.25), (cx - s * 0.2, cy + s * 0.7), (cx, cy + s * 0.7), (cx - s * 0.12, cy + s * 1.05), (cx + s * 0.25, cy + s * 0.55), (cx + s * 0.05, cy + s * 0.55)], fill=YEL)

def change_badge(d, cx, cy, cur, prev):
    if not prev: return
    ch = (cur - prev) / prev * 100
    col = GRN if ch > 0.005 else RED if ch < -0.005 else GREY
    arrow = "▲" if ch > 0.005 else "▼" if ch < -0.005 else "■"
    s = f"{'+' if ch > 0 else ''}{tr_num(ch, 2)}%  DÜNE GÖRE"
    f = font(34, 600); tw = f.getlength(s) + 70
    d.rounded_rectangle([cx - tw / 2, cy - 34, cx + tw / 2, cy + 34], 34, fill=col + (60,), outline=col, width=3)
    tri = [(cx - tw / 2 + 30, cy + 10), (cx - tw / 2 + 50, cy + 10), (cx - tw / 2 + 40, cy - 10)] if arrow == "▲" else \
          [(cx - tw / 2 + 30, cy - 10), (cx - tw / 2 + 50, cy - 10), (cx - tw / 2 + 40, cy + 10)] if arrow == "▼" else \
          [(cx - tw / 2 + 31, cy - 9), (cx - tw / 2 + 49, cy - 9), (cx - tw / 2 + 49, cy + 9), (cx - tw / 2 + 31, cy + 9)]
    d.polygon(tri, fill=col)
    text(d, (cx - tw / 2 + 64, cy), s, 34, WHITE, 600, "lm", 1)

# ---------- stories ----------
def story_weather(D, out):
    w = D["weather"]; im, d = base("HAVA DURUMU", D["date"])
    d = card(im, (64, 470, W - 64, 1150))
    text(d, (W / 2, 530), w.get("location", "KOCAELİ").upper(), 36, YEL, 600, "mm", 6)
    weather_icon(d, w.get("icon", "partly"), W / 2 - 200, 760, 200)
    text(d, (W / 2 + 40, 700), f"{round(w['high'])}°", 210, WHITE, 700, "lm")
    text(d, (W / 2 + 60, 850), f"EN DÜŞÜK {round(w['low'])}°", 44, GREY, 600, "lm", 2)
    text(d, (W / 2, 1000), w["condition"].upper(), 56, WHITE, 700, "mm", 3)
    if w.get("rain") is not None:
        text(d, (W / 2, 1080), f"YAĞIŞ İHTİMALİ %{round(w['rain'])}", 38, (120, 190, 255), 600, "mm", 2)
    nx = w.get("next", [])[:3]
    if nx:
        d = card(im, (64, 1190, W - 64, 1520))
        cw = (W - 128) / len(nx)
        for i, n in enumerate(nx):
            cx = 64 + cw * (i + 0.5)
            text(d, (cx, 1240), n["day"].upper(), 34, YEL, 600, "mm", 2)
            weather_icon(d, n.get("icon", "partly"), cx, 1340, 70)
            text(d, (cx, 1460), f"{round(n['high'])}° / {round(n['low'])}°", 46, WHITE, 700, "mm")
    footer(d, w.get("source", "Hava tahmini") + " · Tahmini değerlerdir")
    im.convert("RGB").save(out, quality=92)

def story_price(D, key, tag, title, out):
    p = D[key]; im, d = base(tag, D["date"])
    d = card(im, (64, 520, W - 64, 1290), outline=YEL)
    text(d, (W / 2, 600), title, 44, YEL, 600, "mm", 6)
    text(d, (W / 2, 780), tr_num(p["sell"], 4 if key != "gold" else 2), 190 if key != "gold" else 170, WHITE, 700, "mm")
    text(d, (W / 2, 900), "SATIŞ (TL)", 36, GREY, 600, "mm", 4)
    d.line([(160, 980), (W - 160, 980)], fill=(70, 72, 78), width=2)
    text(d, (W / 2 - 200, 1060), "ALIŞ", 32, GREY, 600, "mm", 3)
    text(d, (W / 2 - 200, 1120), tr_num(p["buy"], 4 if key != "gold" else 2), 60, WHITE, 700, "mm")
    if key == "gold" and p.get("quarter_sell"):
        text(d, (W / 2 + 200, 1060), "ÇEYREK SATIŞ", 32, GREY, 600, "mm", 3)
        text(d, (W / 2 + 200, 1120), tr_num(p["quarter_sell"], 0), 60, WHITE, 700, "mm")
    else:
        text(d, (W / 2 + 200, 1060), "SAAT", 32, GREY, 600, "mm", 3)
        text(d, (W / 2 + 200, 1120), p.get("time", ""), 60, WHITE, 700, "mm")
    change_badge(d, W / 2, 1210, p["sell"], p.get("prev_sell"))
    text(d, (W / 2, 1400), "Yatırım tavsiyesi değildir.", 30, GREY, 400, "mm", 1)
    footer(d, p.get("source", ""), p.get("time"))
    im.convert("RGB").save(out, quality=92)

def to_video(jpg, wav, mp4, T=8.0, fps=30):
    """Görselden sesli, hafif yakınlaşan kısa hikâye videosu üretir."""
    import subprocess, numpy as np
    im = Image.open(jpg).convert("RGB")
    big = im.resize((int(W * 1.06), int(H * 1.06)), Image.LANCZOS)
    tmp = mp4[:-4] + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                          "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-shortest", "-movflags", "+faststart", tmp], stdin=subprocess.PIPE)
    N = int(T * fps)
    for i in range(N):
        u = i / (N - 1); z = 1.0 + 0.05 * (0.5 - 0.5 * math.cos(math.pi * u))
        cw, ch = big.width / z / 1.06 * 1.0, big.height / z / 1.06
        cw, ch = W / z * 1.06 / 1.06, H / z
        x0 = (big.width - cw * 1.06) / 2; y0 = (big.height - ch * 1.06) / 2
        fr = big.crop((x0, y0, x0 + cw * 1.06, y0 + ch * 1.06)).resize((W, H), Image.BILINEAR)
        a = min(1.0, i / 9.0) * min(1.0, (N - 1 - i) / 9.0)
        arr = (np.asarray(fr, dtype=np.float32) * a).astype(np.uint8)
        p.stdin.write(arr.tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, mp4)
    else: raise SystemExit("ffmpeg failed: " + mp4)

def is_rainy(w):
    return w.get("icon") in ("rain", "storm") or (w.get("rain") or 0) >= 50

if __name__ == "__main__":
    import sounds
    D = json.load(open(sys.argv[1]))
    root = os.path.dirname(HERE); os.makedirs(os.path.join(root, "s"), exist_ok=True)
    pre = os.path.join(root, "s", D["date"])
    T = 8.0
    story_weather(D, pre + "-hava.jpg")
    w = D["weather"]
    if is_rainy(w):
        sounds.save(sounds.rain(T, heavy=(w.get("rain") or 0) >= 75 or w.get("icon") == "storm", thunder=w.get("icon") == "storm"), pre + "-hava.wav")
    else:
        sounds.save(sounds.wind(T), pre + "-hava.wav")
    g = dict(D["gold"]); g["sell"] = g["gram_sell"]; g["buy"] = g["gram_buy"]; g["prev_sell"] = g.get("prev_gram_sell"); D["gold"] = g
    for key, tag, title, name, seed in (("gold", "ALTIN", "GRAM ALTIN", "altin", 3), ("usd", "DOLAR", "ABD DOLARI / TL", "dolar", 4), ("eur", "EURO", "EURO / TL", "euro", 5)):
        story_price(D, key, tag, title, f"{pre}-{name}.jpg")
        p = D[key]; mood = 0 if not p.get("prev_sell") else (1 if p["sell"] > p["prev_sell"] else -1 if p["sell"] < p["prev_sell"] else 0)
        sounds.save(sounds.market(T, mood, seed), f"{pre}-{name}.wav")
    for name in ("hava", "altin", "dolar", "euro"):
        to_video(f"{pre}-{name}.jpg", f"{pre}-{name}.wav", f"{pre}-{name}.mp4", T)
        os.remove(f"{pre}-{name}.wav")
    print("ok", pre, "rainy" if is_rainy(w) else "dry")
