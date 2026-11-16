"""Kocaeli Radar haber videosu üretici (harita arka planlı, sesli anlatımlı, 1080x1920).

Kullanım:  python3 tools/news.py haber.json
haber.json:
{
  "out": "v/2026-11-16-elektrik.mp4",
  "category": "GÜNDEM",
  "source": "Kaynak: ...",
  "scenes": [
    {"wav": "/yol/sahne1.wav", "big": "BAŞLIK", "big_color": "white|yellow|red|green",
     "sub": "ALT BAŞLIK", "sub_style": "yellow|red|dark", "narr": "Altyazı metni",
     "focus": [lat, lon], "zoom": 1.0, "pins": [["ETİKET", lat, lon], ...]}
  ]
}
Harita verisi: tools/assets/tr-cities.json (il sınırları GeoJSON).
"""
import json, os, sys, wave, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from stories import font, text, W, H, YEL, RED, GRN, WHITE  # noqa: E402

A = os.path.join(HERE, "assets")
FPS = 30
SR = 44100
# Harita kanvası (eşdikdörtgen, cos(enlem) düzeltmeli)
LON0, LON1 = 28.2, 31.2
LAT_C = 40.8
MW = 3240
PXLON = MW / (LON1 - LON0)
PXLAT = PXLON / math.cos(math.radians(LAT_C))
MH = int(MW * 16 / 9)
LAT1 = LAT_C + (MH / 2) / PXLAT  # üst kenar


def ll2px(lat, lon):
    return ((lon - LON0) * PXLON, (LAT1 - lat) * PXLAT)


def build_map():
    cache = os.path.join(A, "_map_cache.png")
    if os.path.exists(cache):
        return Image.open(cache).convert("RGB")
    sea = (14, 30, 52)
    im = Image.new("RGB", (MW, MH), sea)
    # denizde hafif doku
    rng = np.random.default_rng(3)
    noise = (rng.normal(0, 1, (MH // 8, MW // 8)) * 6).clip(-12, 12)
    nz = Image.fromarray((noise + 128).astype(np.uint8)).resize((MW, MH), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
    im = Image.blend(im, Image.merge("RGB", [nz, nz, nz]), 0.06)
    # kara maskesi (Natural Earth 10m kıyı çizgisi)
    land = Image.new("L", (MW, MH), 0); ld = ImageDraw.Draw(land)
    for poly in json.load(open(os.path.join(A, "land.json")))["coordinates"]:
        ld.polygon([ll2px(la, lo) for lo, la in poly[0]], fill=255)
        for hole in poly[1:]:
            ld.polygon([ll2px(la, lo) for lo, la in hole], fill=0)
    gj = json.load(open(os.path.join(A, "tr-cities.json"), encoding="utf-8"))
    polys = []
    for f in gj["features"]:
        g = f["geometry"]
        rings = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        for poly in rings:
            polys.append((f["properties"]["name"], [ll2px(la, lo) for lo, la in poly[0]]))
    lay = Image.new("RGB", (MW, MH), (30, 32, 35)); d = ImageDraw.Draw(lay)
    for name, pts in polys:
        if name == "Kocaeli": d.polygon(pts, fill=(48, 50, 55))
    for name, pts in polys:
        if name != "Kocaeli": d.line(pts + [pts[0]], fill=(82, 85, 90), width=3)
    for name, pts in polys:
        if name == "Kocaeli": d.line(pts + [pts[0]], fill=(150, 153, 158), width=5)
    # kıyı parıltısı
    edge = land.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(5))
    glow = edge.filter(ImageFilter.GaussianBlur(16)).point(lambda v: min(255, v * 2))
    im = Image.composite(Image.new("RGB", (MW, MH), (50, 100, 165)), im, glow.point(lambda v: int(v * 0.35)))
    im = Image.composite(lay, im, land)
    im = Image.composite(Image.new("RGB", (MW, MH), (120, 160, 205)), im, edge.point(lambda v: 150 if v > 40 else 0))
    d = ImageDraw.Draw(im)
    for lab, la, lo, col in [("KARADENİZ", 41.35, 29.9, (95, 125, 165)), ("MARMARA DENİZİ", 40.62, 28.75, (95, 125, 165)),
                              ("İSTANBUL", 41.12, 28.95, (150, 152, 158)), ("SAKARYA", 40.75, 30.55, (150, 152, 158)),
                              ("BURSA", 40.25, 29.2, (150, 152, 158)), ("YALOVA", 40.6, 29.15, (150, 152, 158))]:
        x, y = ll2px(la, lo)
        text(d, (x, y), lab, 34, col, 500, "mm", sp=8)
    im = im.filter(ImageFilter.GaussianBlur(0.6))
    im.save(cache)
    return im


def wav_read(p):
    with wave.open(p) as w:
        sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
        x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
    if ch > 1:
        x = x.reshape(-1, ch).mean(1)
    if sr != SR:
        x = np.interp(np.linspace(0, len(x), int(len(x) * SR / sr), endpoint=False), np.arange(len(x)), x)
    return x


def bed(T, seed=7):
    """Telifsiz, yumuşak haber altlığı (akor pad + hafif nabız)."""
    n = int(SR * T); t = np.arange(n) / SR
    x = np.zeros(n)
    for f, a in [(110, .5), (164.8, .35), (220, .3), (277.2, .2)]:
        x += a * np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 0.2 * t))
    pulse = (np.sin(2 * np.pi * 2.0 * t) > 0.97).astype(float)
    k = np.exp(-np.arange(2000) / 300.0)
    x += np.convolve(pulse, k)[:n] * 0.6 * np.sin(2 * np.pi * 55 * t)
    env = np.clip(t / 1.5, 0, 1) * np.clip((T - t) / 1.5, 0, 1)
    return x / np.abs(x).max() * env * 0.07


def wrap(s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        c = (cur + " " + w).strip()
        if f.getlength(c) <= maxw: cur = c
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def overlay(sc, k, tl, cat, source, prog):
    """Sahne üst katmanı (RGBA). tl: sahne içi saniye."""
    o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
    # üst ilerleme çubuğu
    d.rectangle((0, 0, W, 8), fill=(255, 255, 255, 60)); d.rectangle((0, 0, int(W * prog), 8), fill=YEL + (255,))
    d.rectangle((52, 118, 58, 168), fill=YEL + (255,))
    text(d, (76, 143), "KOCAELİ", 40, YEL, 700, "lm")
    text(d, (76 + font(40).getlength("KOCAELİ ") , 143), cat, 40, WHITE, 700, "lm")
    text(d, (W - 60, 236), "@KOCAELIRADAR41", 22, WHITE, 600, "rm")
    # vinyet
    a = ease(tl / 0.35)
    big = sc.get("big"); cy = 1180
    if big:
        col = {"white": WHITE, "yellow": YEL, "red": RED, "green": GRN}.get(sc.get("big_color", "white"), WHITE)
        size = 120 if len(big) <= 14 else (96 if len(big) <= 20 else 78)
        s = 1 + 0.25 * (1 - ease(tl / 0.3))
        f = font(int(size * s))
        lines = wrap(big, f, W - 120)
        y = cy - (len(lines) - 1) * size * 1.05
        for ln in lines:
            for dx, dy in [(4, 5), (0, 0)]:
                c = (0, 0, 0, int(200 * a)) if dx else col + (int(255 * a),)
                d.text((W / 2 + dx, y + dy), ln, font=f, fill=c, anchor="mm")
            y += size * 1.05
        cy = y - size * 1.05
    sub = sc.get("sub")
    if sub:
        b = ease((tl - 0.2) / 0.3)
        f = font(44, 700); tw = f.getlength(sub)
        st = sc.get("sub_style", "yellow")
        bg = {"yellow": YEL, "red": RED, "dark": (12, 12, 14)}[st]
        fg = (12, 12, 14) if st == "yellow" else WHITE
        y = cy + 105
        d.rectangle((W / 2 - tw / 2 - 18, y - 32, W / 2 + tw / 2 + 18, y + 32), fill=bg + (int(240 * b),))
        d.text((W / 2, y), sub, font=f, fill=fg + (int(255 * b),), anchor="mm")
    narr = sc.get("narr")
    if narr:
        f = font(38, 600); lines = wrap(narr, f, 860)
        y = 1560 - (len(lines) - 1) * 26
        for ln in lines:
            tw = f.getlength(ln)
            d.rectangle((W / 2 - tw / 2 - 16, y - 27, W / 2 + tw / 2 + 16, y + 27), fill=(8, 8, 10, int(225 * a)))
            d.text((W / 2, y), ln, font=f, fill=WHITE + (int(255 * a),), anchor="mm")
            y += 54
    text(d, (52, 1790), source, 22, (200, 200, 205), 500, "lm")
    return o


def pins_layer(sc, tl, crop):
    o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
    x0, y0, cw, ch = crop
    for i, (lab, la, lo) in enumerate(sc.get("pins", [])):
        t = tl - 0.25 - i * 0.18
        if t < 0: continue
        mx, my = ll2px(la, lo)
        x = (mx - x0) * W / cw; y = (my - y0) * H / ch
        r = 30 + 26 * ((t * 1.2) % 1)
        al = int(255 * (1 - (t * 1.2) % 1))
        d.ellipse((x - r, y - r, x + r, y + r), outline=RED + (al,), width=4)
        d.ellipse((x - 22, y - 22, x + 22, y + 22), outline=RED + (255,), width=4)
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=WHITE + (255,), outline=RED + (255,), width=3)
        if not lab: continue
        f = font(30, 700); tw = f.getlength(lab)
        lx = min(max(x + 30, 20), W - tw - 40); ly = y - 46
        d.rectangle((lx, ly - 22, lx + tw + 20, ly + 22), fill=(10, 10, 12, 235))
        d.rectangle((lx, ly + 22, lx + tw + 20, ly + 26), fill=YEL + (255,))
        d.text((lx + 10, ly), lab, font=f, fill=WHITE, anchor="lm")
    return o


def main(spec_path):
    S = json.load(open(spec_path, encoding="utf-8"))
    root = os.path.dirname(HERE)
    out = os.path.join(root, S["out"]) if not os.path.isabs(S["out"]) else S["out"]
    m = build_map()
    gap = 0.35
    clips = [wav_read(sc["wav"]) for sc in S["scenes"]]
    durs = [len(c) / SR + gap for c in clips]
    durs[0] += 0.3; durs[-1] += 1.2
    T = sum(durs)
    audio = np.zeros(int(SR * T) + SR)
    t0 = 0.0
    for i, c in enumerate(clips):
        st = int(SR * (t0 + (0.3 if i == 0 else 0.1)))
        audio[st:st + len(c)] += c * 0.95
        t0 += durs[i]
    audio = audio[:int(SR * T)] + bed(T)
    audio = np.clip(audio, -1, 1)
    wavp = out + ".tmp.wav"
    with wave.open(wavp, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((audio * 32767).astype(np.int16).tobytes())
    tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", wavp, "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-shortest", "-movflags", "+faststart", tmp], stdin=subprocess.PIPE)
    default_focus = [40.78, 29.85]
    start = 0.0
    prev_view = None
    for i, sc in enumerate(S["scenes"]):
        foc = sc.get("focus", default_focus); z = sc.get("zoom", 1.0)
        fx, fy = ll2px(*foc)
        view = (fx, fy, z)
        if prev_view is None: prev_view = (fx, fy, z * 0.85)
        nfr = int(round(durs[i] * FPS))
        base_ov = None
        for k in range(nfr):
            tl = k / FPS
            e = ease(tl / 1.0)
            cx = prev_view[0] + (view[0] - prev_view[0]) * e
            cy = prev_view[1] + (view[1] - prev_view[1]) * e
            zz = (prev_view[2] + (view[2] - prev_view[2]) * e) * (1 + 0.03 * tl / durs[i])
            cw = 1500 / zz; ch = cw * 16 / 9
            x0 = min(max(cx - cw / 2, 0), MW - cw); y0 = min(max(cy - ch * 0.42, 0), MH - ch)
            fr = m.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BILINEAR).convert("RGBA")
            # karartma: üst/alt gradyan
            if base_ov is None:
                g = np.zeros((H, 1), np.float32)
                yy = np.arange(H)[:, None] / H
                g = np.clip(np.maximum(0.55 - yy * 2.2, (yy - 0.55) * 1.4), 0, 0.75)
                base_ov = Image.fromarray(np.dstack([np.zeros((H, W, 3), np.uint8), (np.repeat(g, W, 1) * 255).astype(np.uint8)]), "RGBA")
            fr.alpha_composite(base_ov)
            if sc.get("pins"): fr.alpha_composite(pins_layer(sc, tl, (x0, y0, cw, ch)))
            prog = (start + tl) / T
            fr.alpha_composite(overlay(sc, k, tl, S.get("category", "GÜNDEM"), S["source"], prog))
            p.stdin.write(fr.convert("RGB").tobytes())
        start += durs[i]
        prev_view = view
    p.stdin.close(); p.wait()
    os.replace(tmp, out); os.remove(wavp)
    print("OK", out, round(T, 1), "sn")


if __name__ == "__main__":
    main(sys.argv[1])
