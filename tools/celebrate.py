"""Kocaeli Radar KUTLAMA videosu (takipçi eşikleri: 1000, 2000 ...). 1080x1920, 30 fps.

Kullanım:  python3 tools/celebrate.py kutlama.json
kutlama.json:
{
  "out": "v/ozel-1000-takipci.mp4",
  "number": "1000", "headline": "KİŞİYİZ!", "thanks": "TEŞEKKÜRLER KOCAELİ",
  "next_goal": "2000",
  "s1": {"wav": "...", "words": [...]},           # kapak: büyük sayı + başlık (0. karede tam görünür)
  "s2": {"wav": "...", "words": [...], "highlight": {"İZMİT": 100, ...}},   # 12 ilçe çipleri
  "s3": {"wav": "...", "words": [...], "cards": [["SON DAKİKA", 100], ...]}, # 4 hizmet kartı (ms)
  "s4": {"wav": "...", "words": [...], "goal_ms": 4800},                     # soru + sıradaki hedef çubuğu
  "outro_wav": "...",
  "finale": {"wavs": ["emre.wav", "aylin.wav"], "text": "Teşekkürler Kocaeli!"}   # iki spiker AYNI ANDA
}
Her sahnede isteğe bağlı "speaker": "EMRE" | "AYLİN" (altyazının üstünde konuşan spiker etiketi).
Görsel: altın ışık hüzmeleri, konfeti (0. karede de görünür), havai fişek patlamaları, kelime kelime altyazı.
Ses: anlatım + neşeli telifsiz sentetik kutlama müziği (I-V-vi-IV, 124 bpm) konuşma altında ducking'li,
havai fişek/whoosh efektleri; news.py ile aynı -14 LUFS zinciri (loudnorm_filter).
"""
import json, math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from stories import font, W, H, YEL, RED, WHITE  # noqa: E402
import city  # noqa: E402
from news import wav_read, loudnorm_filter, _movavg, _speech_eq, _lowpass, SR  # noqa: E402

A = os.path.join(HERE, "assets")
FPS = 30
GOLD = (255, 196, 40); GOLD2 = (255, 228, 120); GOLD3 = (196, 128, 10)
NAVY = (8, 12, 26)
SUB_Y = 1440
DISTRICTS = city.DISTRICTS


def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def back(x):
    x = max(0.0, min(1.0, x)); c = 1.9
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


# ---------------------------------------------------------------- arka plan
def make_bg():
    yy = np.linspace(0, 1, H)[:, None, None]
    top = np.array([18, 24, 52], np.float32); bot = np.array([4, 6, 14], np.float32)
    g = top * (1 - yy) + bot * yy
    g = np.repeat(g, W, 1)
    # merkezde sıcak altın hale
    X, Y = np.meshgrid(np.arange(W), np.arange(H))
    r = np.sqrt((X - W / 2) ** 2 + ((Y - 640) * 0.8) ** 2)
    halo = np.exp(-(r / 520) ** 2)[..., None] * np.array([120, 80, 10], np.float32)
    return Image.fromarray(np.clip(g + halo, 0, 255).astype(np.uint8)).convert("RGBA")


def make_rays():
    S = 2400
    im = Image.new("L", (S, S), 0); d = ImageDraw.Draw(im)
    n = 18
    for i in range(n):
        a0 = 2 * math.pi * i / n; a1 = a0 + 2 * math.pi / n * 0.45
        d.polygon([(S / 2, S / 2), (S / 2 + S * math.cos(a0), S / 2 + S * math.sin(a0)),
                   (S / 2 + S * math.cos(a1), S / 2 + S * math.sin(a1))], fill=255)
    rr = np.sqrt(((np.arange(S) - S / 2)[None, :]) ** 2 + ((np.arange(S) - S / 2)[:, None]) ** 2)
    fall = np.clip(1 - rr / (S * 0.42), 0, 1) ** 1.6
    a = (np.asarray(im, np.float32) * fall * 0.16).astype(np.uint8)
    return Image.fromarray(a).filter(ImageFilter.GaussianBlur(6))


def rays_layer(rays, t, cy=640):
    r = rays.rotate(t * 7, resample=Image.BILINEAR)
    S = r.size[0]
    a = r.crop((S // 2 - W // 2, S // 2 - cy, S // 2 + W // 2, S // 2 - cy + H))
    lay = Image.new("RGBA", (W, H), GOLD2 + (0,)); lay.putalpha(a)
    return lay


# ---------------------------------------------------------------- parçacıklar
CONF_COLS = [GOLD, GOLD2, (255, 255, 255), RED, (60, 170, 255), (80, 220, 140), (255, 120, 200)]


class Confetti:
    def __init__(self, seed=7):
        self.rng = np.random.default_rng(seed); self.p = []

    def rain(self, n, t0, t1):
        r = self.rng
        for _ in range(n):
            self.p.append(dict(ts=r.uniform(t0, t1), x=r.uniform(-40, W + 40), y=r.uniform(-260, -30),
                               vx=r.normal(0, 30), vy=r.uniform(60, 160), vt=r.uniform(170, 290), tau=0.8,
                               sw=r.uniform(20, 60), om=r.uniform(1.5, 3.5), ph=r.uniform(0, 6.3),
                               rot=r.uniform(0, 6.3), spin=r.normal(0, 4), flip=r.uniform(3, 9),
                               w=r.uniform(14, 24), h=r.uniform(7, 12), c=CONF_COLS[r.integers(len(CONF_COLS))], life=12))

    def burst(self, t, x, y, n=90, power=1300):
        r = self.rng
        for _ in range(n):
            a = r.uniform(-math.pi, 0) if y > H * 0.6 else r.uniform(0, 2 * math.pi)
            v = r.uniform(0.35, 1.0) * power
            self.p.append(dict(ts=t, x=x, y=y, vx=math.cos(a) * v, vy=math.sin(a) * v - 250, vt=r.uniform(200, 320), tau=0.35,
                               sw=r.uniform(10, 40), om=r.uniform(2, 4), ph=r.uniform(0, 6.3),
                               rot=r.uniform(0, 6.3), spin=r.normal(0, 7), flip=r.uniform(4, 10),
                               w=r.uniform(14, 24), h=r.uniform(7, 12), c=CONF_COLS[r.integers(len(CONF_COLS))], life=7))

    def draw(self, d, t):
        for q in self.p:
            u = t - q["ts"]
            if u < 0 or u > q["life"]: continue
            e = 1 - math.exp(-u / q["tau"])
            x = q["x"] + q["vx"] * q["tau"] * e + q["sw"] * math.sin(q["om"] * u + q["ph"])
            y = q["y"] + q["vy"] * q["tau"] * e + q["vt"] * (u - q["tau"] * e)
            if y > H + 40 or x < -60 or x > W + 60: continue
            a = q["rot"] + q["spin"] * u
            s = abs(math.cos(q["flip"] * u)) * 0.85 + 0.15
            w, h = q["w"] / 2, q["h"] / 2 * s
            ca, sa = math.cos(a), math.sin(a)
            pts = [(x + ca * dx - sa * dy, y + sa * dx + ca * dy) for dx, dy in ((-w, -h), (w, -h), (w, h), (-w, h))]
            sh = 0.55 + 0.45 * s
            col = tuple(int(c * sh) for c in q["c"])
            d.polygon(pts, fill=col + (255,))


class Fireworks:
    def __init__(self, seed=3):
        self.rng = np.random.default_rng(seed); self.b = []

    def add(self, t, x, y, col, n=46, R=330):
        r = self.rng
        sp = [(r.uniform(0, 2 * math.pi), r.uniform(0.75, 1.0) * R) for _ in range(n)]
        self.b.append((t, x, y, col, sp))

    def draw(self, d, t, s=0.25):
        """s: çizim ölçeği (glow katmanı küçük çözünürlükte çizilir)."""
        for (t0, x, y, col, sp) in self.b:
            u = t - t0
            if u < 0 or u > 1.6: continue
            if u < 0.12:  # parlama çekirdeği
                rr = (30 + 300 * u) * s
                d.ellipse((x * s - rr, y * s - rr, x * s + rr, y * s + rr), fill=(255, 250, 220, int(255 * (1 - u / 0.12))))
            fade = max(0.0, 1 - u / 1.6) ** 1.3
            for a, R in sp:
                e1 = 1 - math.exp(-u * 4.2); e0 = 1 - math.exp(-max(0, u - 0.12) * 4.2)
                drop = 90 * u * u
                x1 = x + math.cos(a) * R * e1; y1 = y + math.sin(a) * R * e1 + drop
                x0 = x + math.cos(a) * R * e0; y0 = y + math.sin(a) * R * e0 + drop * 0.8
                tw = 0.6 + 0.4 * math.sin(u * 40 + a * 7)
                c = tuple(int(255 - (255 - v) * min(1, u * 2.5)) for v in col)
                d.line((x0 * s, y0 * s, x1 * s, y1 * s), fill=c + (int(255 * fade * tw),), width=max(2, int(9 * s)))
                d.ellipse((x1 * s - 8 * s, y1 * s - 8 * s, x1 * s + 8 * s, y1 * s + 8 * s), fill=(255, 255, 255, int(230 * fade * tw)))


# ---------------------------------------------------------------- yazı sprite'ları
def gold_text(s, size, w=700, stroke=6):
    f = font(size, w)
    bb = f.getbbox(s, stroke_width=stroke)
    tw, th = bb[2] - bb[0] + 40, bb[3] - bb[1] + 40
    m = Image.new("L", (tw, th), 0); ImageDraw.Draw(m).text((20 - bb[0], 20 - bb[1]), s, font=f, fill=255)
    yy = np.linspace(0, 1, th)[:, None]
    stops = [(255, 246, 200), (255, 222, 140), (244, 176, 50), (200, 128, 16)]
    grad = np.stack([np.interp(yy[:, 0], [0, 0.45, 0.55, 1], [c[ch] for c in stops]) for ch in range(3)], -1)
    gi = Image.fromarray(np.repeat(grad[:, None, :], tw, 1).astype(np.uint8))
    out = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    edge = Image.new("L", (tw, th), 0); ImageDraw.Draw(edge).text((20 - bb[0], 20 - bb[1]), s, font=f, fill=255, stroke_width=stroke)
    sh = edge.filter(ImageFilter.GaussianBlur(14))
    out.paste((0, 0, 0, 255), (0, 10), sh.point(lambda v: int(v * 0.8)))
    out.paste((110, 60, 0, 255), (0, 0), edge)
    out.paste(gi, (0, 0), m)
    return out, m


def shine(sprite, mask, t, period=2.4):
    """Yazının üzerinden geçen parlak çizgi."""
    w, h = sprite.size
    ph = (t % period) / period
    cx = -0.3 * w + ph * 1.9 * w
    X, Y = np.meshgrid(np.arange(w), np.arange(h))
    band = np.clip(1 - np.abs((X - cx) + (Y - h / 2) * 0.35) / 60, 0, 1) * (np.asarray(mask, np.float32) / 255)
    lay = Image.new("RGBA", (w, h), (255, 255, 255, 0)); lay.putalpha(Image.fromarray((band * 200).astype(np.uint8)))
    o = sprite.copy(); o.alpha_composite(lay); return o


def paste_c(fr, im, cx, cy, sc=1.0, alpha=1.0):
    if sc != 1.0:
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BICUBIC)
    if alpha < 1.0:
        a = im.getchannel("A").point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def ctext(d, x, y, s, size, fill, w=700, sp=0, anchor="mm", stroke=0, sfill=None):
    f = font(size, w)
    if not sp:
        d.text((x, y), s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill); return
    tw = sum(f.getlength(c) for c in s) + sp * (len(s) - 1); xx = x - tw / 2
    for c in s:
        d.text((xx, y), c, font=f, fill=fill, anchor="lm"); xx += f.getlength(c) + sp


def pill(d, x, y, s, size, bg, fg, padx=28, pady=14, r=None):
    f = font(size, 700); tw = f.getlength(s)
    hh = size * 0.62 + pady
    d.rounded_rectangle((x - tw / 2 - padx, y - hh, x + tw / 2 + padx, y + hh), radius=r if r is not None else hh, fill=bg)
    d.text((x, y), s, font=f, fill=fg, anchor="mm")


# ---------------------------------------------------------------- altyazı
def chunks(words):
    out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= 4 or w["text"][-1:] in ",.;!?":
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out


def subtitle(d, words, tms):
    if not words: return
    ch = None
    for c in chunks(words):
        if c[0]["start_ms"] - 120 <= tms <= c[-1]["end_ms"] + 250: ch = c
    if ch is None:
        prev = [c for c in chunks(words) if c[-1]["end_ms"] < tms]
        if prev and tms - prev[-1][-1]["end_ms"] < 500: ch = prev[-1]
    if ch is None: return
    f = font(62, 700)
    parts = [w["text"] for w in ch]
    tw = sum(f.getlength(p) for p in parts) + f.getlength(" ") * (len(parts) - 1)
    d.rounded_rectangle((W / 2 - tw / 2 - 30, SUB_Y - 52, W / 2 + tw / 2 + 30, SUB_Y + 52), radius=26, fill=(6, 8, 16, 215))
    x = W / 2 - tw / 2
    for w in ch:
        on = w["start_ms"] <= tms <= w["end_ms"] + 80
        d.text((x, SUB_Y), w["text"], font=f, fill=(GOLD if on else WHITE) + (255,), anchor="lm")
        x += f.getlength(w["text"] + " ")


# ---------------------------------------------------------------- sahneler
def icon(d, kind, x, y, s, col):
    d.rounded_rectangle((x - s, y - s, x + s, y + s), radius=s * 0.35, fill=col + (255,))
    k = s * 0.55
    if kind == "alert":
        d.polygon([(x, y - k), (x + k, y + k * 0.8), (x - k, y + k * 0.8)], fill=(255, 255, 255, 255))
        d.text((x, y + k * 0.25), "!", font=font(int(s * 0.9), 700), fill=col + (255,), anchor="mm")
    elif kind == "bolt":
        d.polygon([(x + k * 0.2, y - k), (x - k * 0.6, y + k * 0.1), (x - k * 0.05, y + k * 0.1), (x - k * 0.25, y + k),
                   (x + k * 0.6, y - k * 0.15), (x + k * 0.05, y - k * 0.15)], fill=(20, 20, 20, 255))
    elif kind == "road":
        d.polygon([(x - k * 0.35, y - k), (x + k * 0.35, y - k), (x + k, y + k), (x - k, y + k)], fill=(30, 30, 36, 255))
        for i in range(3):
            yy = y - k + i * k * 0.75
            d.rectangle((x - 4, yy + 4, x + 4, yy + k * 0.45), fill=YEL + (255,))
    elif kind == "ball":
        d.ellipse((x - k, y - k, x + k, y + k), fill=(255, 255, 255, 255), outline=(20, 20, 20, 255), width=4)
        pts = [(x + k * 0.45 * math.cos(a), y + k * 0.45 * math.sin(a)) for a in np.linspace(-math.pi / 2, 1.5 * math.pi, 6)[:-1]]
        d.polygon(pts, fill=(20, 20, 20, 255))


def scene1(fr, d, tl, C, spr):
    # üst etiket
    pill(d, W / 2, 220, city.BRAND, 40, (10, 12, 22, 230), GOLD + (255,), padx=34)
    d.ellipse((W / 2 - 150, 210, W / 2 - 134, 226), fill=RED + (255,)) if False else None
    # halka + dönen ışıltılar
    cx, cy, R = W / 2, 640, 330
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=GOLD + (200,), width=6)
    d.ellipse((cx - R + 22, cy - R + 22, cx + R - 22, cy + R - 22), outline=GOLD2 + (70,), width=2)
    for i in range(24):
        a = 2 * math.pi * i / 24 + tl * 0.6
        rr = 7 + 4 * math.sin(tl * 5 + i)
        px, py = cx + (R + 34) * math.cos(a), cy + (R + 34) * math.sin(a)
        d.ellipse((px - rr, py - rr, px + rr, py + rr), fill=GOLD2 + (220,))
    num, mask = spr["num"]
    pulse = 1 + 0.07 * math.exp(-((tl - 0.35) / 0.12) ** 2) + 0.012 * math.sin(tl * 4)
    paste_c(fr, shine(num, mask, tl), cx, cy - 20, pulse)
    ctext(d, cx, cy + 205, "TAKİPÇİ", 54, WHITE + (255,), sp=14)
    paste_c(fr, spr["head"][0], cx, 1060, 1 + 0.02 * math.sin(tl * 3))
    # teşekkür bandı
    f = font(64, 700); s = C["thanks"]; tw = f.getlength(s)
    d.polygon([(W / 2 - tw / 2 - 60, 1180), (W / 2 + tw / 2 + 60, 1180), (W / 2 + tw / 2 + 40, 1290), (W / 2 - tw / 2 - 40, 1290)], fill=GOLD + (255,))
    d.text((W / 2, 1235), s, font=f, fill=NAVY + (255,), anchor="mm")


def scene2(fr, d, tl, C):
    paste_c(fr, C["_spr"]["ilce"][0], W / 2, 330, back(tl / 0.45) if tl < 0.6 else 1.0)
    pill(d, W / 2, 490, "TEK AİLE", 58, WHITE + (255,), NAVY + (255,), padx=40)
    hl = {k: v / 1000 for k, v in C["s2"].get("highlight", {}).items()}
    cols, cw, ch, gx, gy, y0 = 3, 300, 104, 26, 30, 640
    x0 = W / 2 - (cols * cw + (cols - 1) * gx) / 2
    for i, name in enumerate(DISTRICTS):
        r, c = divmod(i, cols)
        t0 = 0.25 + i * 0.22
        if tl < t0: continue
        s = back((tl - t0) / 0.35)
        x = x0 + c * (cw + gx) + cw / 2; y = y0 + r * (ch + gy) + ch / 2
        w2, h2 = cw / 2 * s, ch / 2 * s
        lit = name in hl and tl >= hl[name]
        glow = lit and tl - hl[name] < 0.5
        if glow:
            g = 1 - (tl - hl[name]) / 0.5
            d.rounded_rectangle((x - w2 - 10 * g, y - h2 - 10 * g, x + w2 + 10 * g, y + h2 + 10 * g), radius=30, fill=GOLD2 + (int(120 * g),))
        d.rounded_rectangle((x - w2, y - h2, x + w2, y + h2), radius=24,
                            fill=(GOLD if lit else (16, 22, 44)) + (240,), outline=GOLD + (255,), width=3)
        if s > 0.5:
            fs = 46 if len(name) <= 8 else 40
            d.text((x, y), name, font=font(int(fs * min(1, s)), 700), fill=(NAVY if lit else WHITE) + (255,), anchor="mm")


def scene3(fr, d, tl, C):
    paste_c(fr, C["_spr"]["724"][0], W / 2, 320, back(tl / 0.45) if tl < 0.6 else 1.0)
    ctext(d, W / 2, 490, "SİZİN İÇİN TAKİPTEYİZ", 56, WHITE + (255,), sp=4)
    kinds = [("alert", RED), ("bolt", YEL), ("road", (60, 150, 255)), ("ball", (30, 160, 80))]
    for i, (label, ms) in enumerate(C["s3"]["cards"]):
        t0 = ms / 1000
        if tl < t0 - 0.1: continue
        e = ease((tl - t0 + 0.1) / 0.4)
        y = 650 + i * 170; x = W / 2 + (1 - e) * 900
        d.rounded_rectangle((x - 430, y - 66, x + 430, y + 66), radius=30, fill=(14, 20, 40, 235), outline=GOLD + (int(255 * e),), width=3)
        k, col = kinds[i]
        icon(d, k, x - 340, y, 46, col)
        d.text((x - 260, y), label, font=font(64, 700), fill=WHITE + (255,), anchor="lm")
        if tl - t0 > 0.3:
            ck = min(1, (tl - t0 - 0.3) / 0.25)
            d.line([(x + 330, y), (x + 352, y + 22 * ck), (x + 352 + 40 * ck, y - 26 * ck)], fill=GOLD + (255,), width=10)


def scene4(fr, d, tl, C):
    s = back(tl / 0.45) if tl < 0.6 else 1.0
    paste_c(fr, C["_spr"]["q1"][0], W / 2, 260, s)
    paste_c(fr, C["_spr"]["q2"][0], W / 2, 450, s)
    # konuşma balonu
    bx, by = W / 2, 690
    e = back((tl - 1.2) / 0.4) if tl > 1.2 else 0
    if e > 0:
        w2, h2 = 380 * e, 120 * e
        d.rounded_rectangle((bx - w2, by - h2, bx + w2, by + h2), radius=60 * e, fill=WHITE + (255,))
        d.polygon([(bx - 160 * e, by + h2 - 4), (bx - 230 * e, by + h2 + 70 * e), (bx - 80 * e, by + h2 - 4)], fill=WHITE + (255,))
        if e > 0.8:
            d.text((bx - 40, by), "YORUMLARA YAZ", font=font(66, 700), fill=NAVY + (255,), anchor="mm")
            for j in range(3):
                yy = by + 6 * math.sin(tl * 8 - j * 0.9)
                d.ellipse((bx + 250 + j * 34 - 11, yy - 11, bx + 250 + j * 34 + 11, yy + 11), fill=GOLD3 + (255,))
    # sıradaki hedef çubuğu
    g0 = C["s4"].get("goal_ms", 4800) / 1000
    if tl > g0 - 1.6:
        a = ease((tl - g0 + 1.6) / 0.4)
        ctext(d, W / 2, 940, "SIRADAKİ HEDEF", 46, (200, 205, 220, int(255 * a)), sp=10)
        x0, x1, y = 150, W - 150, 1040
        d.rounded_rectangle((x0, y - 34, x1, y + 34), radius=34, fill=(20, 26, 50, int(240 * a)), outline=GOLD + (int(255 * a),), width=3)
        fill = 0.5 * ease((tl - g0) / 1.0) if tl > g0 else 0
        if fill > 0.01:
            d.rounded_rectangle((x0 + 6, y - 28, x0 + 6 + (x1 - x0 - 12) * fill, y + 28), radius=28, fill=GOLD + (255,))
        xm = (x0 + x1) / 2
        d.line((xm, y - 40, xm, y + 40), fill=WHITE + (int(160 * a),), width=3)
        d.text((xm, y + 80), C["number"], font=font(44, 700), fill=GOLD + (int(255 * a),), anchor="mm")
        d.text((x1, y + 80), C["next_goal"], font=font(44, 700), fill=WHITE + (int(255 * a),), anchor="rm")
        d.text((x1 + 0, y - 80), "🎯" if False else "", font=font(40), fill=WHITE + (0,))


def outro(fr, d, tl, C):
    logo = C["_spr"]["logo"]
    s = back(tl / 0.5)
    paste_c(fr, logo, W / 2, 560, max(0.01, s))
    a = int(255 * ease((tl - 0.3) / 0.4))
    paste_c(fr, C["_spr"]["kr"][0], W / 2, 990, 1.0, a / 255)
    ctext(d, W / 2, 1110, city.HANDLE, 56, (220, 225, 240, a))
    p = 1 + 0.05 * math.sin(tl * 6)
    if tl > 0.6:
        f = font(int(70 * p), 700); tw = f.getlength("TAKİP ET")
        d.rounded_rectangle((W / 2 - tw / 2 - 60 * p, 1215 - 58 * p, W / 2 + tw / 2 + 60 * p, 1215 + 58 * p), radius=58 * p, fill=RED + (255,))
        d.text((W / 2, 1215), "TAKİP ET", font=f, fill=WHITE + (255,), anchor="mm")


def finale(fr, d, tl, C):
    s = back(tl / 0.4)
    paste_c(fr, C["_spr"]["tes"][0], W / 2, 560, max(0.01, s) * (1 + 0.03 * math.sin(tl * 5)))
    s2 = back((tl - 0.25) / 0.4)
    if s2 > 0: paste_c(fr, C["_spr"]["koc"], W / 2, 790, max(0.01, s2))
    # kalp + iki spiker
    a = ease((tl - 0.5) / 0.4)
    if a > 0:
        hx, hy, k = W / 2, 1020, 46 * (1 + 0.08 * math.sin(tl * 7))
        d.ellipse((hx - k, hy - k * 0.9, hx, hy + k * 0.1), fill=RED + (int(255 * a),))
        d.ellipse((hx, hy - k * 0.9, hx + k, hy + k * 0.1), fill=RED + (int(255 * a),))
        d.polygon([(hx - k * 0.98, hy - k * 0.25), (hx + k * 0.98, hy - k * 0.25), (hx, hy + k * 1.1)], fill=RED + (int(255 * a),))
        pill(d, W / 2 - 230, 1020, "EMRE", 50, (16, 22, 44, int(240 * a)), WHITE + (int(255 * a),), padx=34)
        pill(d, W / 2 + 230, 1020, "AYLİN", 50, (16, 22, 44, int(240 * a)), WHITE + (int(255 * a),), padx=34)
    ctext(d, W / 2, 1200, city.HANDLE, 50, (220, 225, 240, int(255 * a)))


def speaker_tag(d, name, tl):
    a = ease(tl / 0.3)
    f = font(34, 700); tw = f.getlength(name)
    x, y = W / 2, SUB_Y - 92
    d.rounded_rectangle((x - tw / 2 - 52, y - 24, x + tw / 2 + 22, y + 24), radius=24, fill=GOLD + (int(240 * a),))
    # mikrofon simgesi
    mx = x - tw / 2 - 30
    d.rounded_rectangle((mx - 7, y - 15, mx + 7, y + 4), radius=7, fill=NAVY + (int(255 * a),))
    d.arc((mx - 12, y - 8, mx + 12, y + 12), 0, 180, fill=NAVY + (int(255 * a),), width=3)
    d.line((mx, y + 12, mx, y + 18), fill=NAVY + (int(255 * a),), width=3)
    d.text((x + 6, y), name, font=f, fill=NAVY + (int(255 * a),), anchor="mm")


# ---------------------------------------------------------------- müzik
def party_music(T, bpm=124, seed=9):
    n = int(SR * T); t = np.arange(n) / SR; x = np.zeros(n); rng = np.random.default_rng(seed)
    beat = 60.0 / bpm; bar = beat * 4
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    prog = [(48, [60, 64, 67]), (43, [59, 62, 67]), (45, [60, 64, 69]), (41, [60, 65, 69])]  # C G Am F

    def add(st, sig, g=1.0):
        i = int(st * SR)
        if i >= n or i < 0: return
        L = min(len(sig), n - i); x[i:i + L] += sig[:L] * g
    kL = int(SR * 0.3); kt = np.arange(kL) / SR
    kick = np.sin(2 * np.pi * (50 + 110 * np.exp(-kt * 35)) * kt) * np.exp(-kt * 10)
    cL = int(SR * 0.18); ct = np.arange(cL) / SR
    clap = sum(np.concatenate([np.zeros(int(SR * o)), rng.normal(0, 1, cL)])[:cL] for o in (0, 0.008, 0.017)) * np.exp(-ct * 22) * 0.25
    hL = int(SR * 0.09); hat = rng.normal(0, 1, hL); hat = (hat - np.convolve(hat, np.ones(6) / 6, "same")) * np.exp(-np.arange(hL) / SR * 30) * 0.16
    for b in range(int(T / beat) + 1):
        tb = b * beat
        add(tb, kick, 0.85)
        if b % 2 == 1: add(tb, clap)
        add(tb + beat / 2, hat)
    def saw(f, tt):
        return sum(np.sin(2 * np.pi * f * k * tt) / k for k in range(1, 7))
    for k in range(int(T / bar) + 1):
        root, ch = prog[k % 4]; tb = k * bar
        # parlak akor stab'ları (offbeat, house tarzı)
        for q in range(4):
            sl = int(SR * beat * 0.45); st_ = np.arange(sl) / SR
            stab = sum(saw(hz(m), st_) + saw(hz(m) * 1.006, st_) for m in ch) * np.exp(-st_ * 7)
            add(tb + q * beat + beat / 2, stab, 0.045)
        # bas (sekizlik, oktav sıçramalı)
        for q in range(8):
            bl = int(SR * beat / 2); bt = np.arange(bl) / SR
            m = root - 12 + (12 if q % 2 else 0)
            add(tb + q * beat / 2, np.tanh(2.2 * np.sin(2 * np.pi * hz(m) * bt)) * np.exp(-bt * 7), 0.2)
        # pluck arpej (onaltılık)
        arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 24]
        for q in range(16):
            al = int(SR * 0.2); at = np.arange(al) / SR; m = arp[q % 4]
            add(tb + q * beat / 4, (np.sin(2 * np.pi * hz(m) * at) + 0.3 * np.sin(4 * np.pi * hz(m) * at)) * np.exp(-at * 14), 0.07)
        # glockenspiel melodisi (her bar 2 nota)
        mel = [ch[2] + 24, ch[0] + 24]
        for j, m in enumerate(mel):
            gl = int(SR * 0.8); gt = np.arange(gl) / SR
            add(tb + j * beat * 2, (np.sin(2 * np.pi * hz(m) * gt) + 0.25 * np.sin(2 * np.pi * hz(m) * 2.76 * gt)) * np.exp(-gt * 4), 0.06)
    x = _lowpass(x, 11000)
    env = np.clip(t / 0.15, 0, 1) * np.clip((T - t) / 1.2, 0, 1)
    return x / (np.abs(x).max() + 1e-9) * env


def sfx_pop(rng):
    L = int(SR * 0.9); tt = np.arange(L) / SR
    boom = np.sin(2 * np.pi * (60 + 80 * np.exp(-tt * 20)) * tt) * np.exp(-tt * 9) * 0.5
    crackle = np.zeros(L)
    for _ in range(60):
        i = int(rng.uniform(0.08, 0.8) * SR); k = int(SR * 0.006)
        if i + k < L: crackle[i:i + k] += rng.normal(0, 1, k) * np.exp(-np.arange(k) / k * 4) * rng.uniform(0.1, 0.35)
    return boom + crackle * np.exp(-tt * 2.5)


def sfx_whoosh(rng):
    L = int(SR * 0.45); tt = np.arange(L) / SR
    nz = rng.normal(0, 1, L); nz = nz - np.convolve(nz, np.ones(30) / 30, "same")
    return nz * np.sin(np.pi * tt / tt[-1]) ** 2 * 0.12


# ---------------------------------------------------------------- ana akış
def main(spec):
    C = json.load(open(spec))
    out = os.path.join(os.path.dirname(HERE), C["out"])
    scenes = [C["s1"], C["s2"], C["s3"], C["s4"]]
    wavs = [wav_read(s["wav"]) for s in scenes]
    PRE = 0.25
    durs = [PRE + len(w) / SR + 0.45 for w in wavs]
    cta = wav_read(C["outro_wav"])
    OUT = len(cta) / SR + 0.9
    fv = []
    for fp in C["finale"]["wavs"]:   # iki spiker aynı anda: ses başlangıçları hizalanır
        w_ = wav_read(fp); on = int(np.argmax(np.abs(w_) > 0.02 * np.abs(w_).max()))
        fv.append(w_[max(0, on - int(SR * 0.01)):])
    L = max(len(v) for v in fv); both = np.zeros(L)
    for v in fv: both[:len(v)] += v * 0.62
    FIN = 0.35 + L / SR + 1.9
    T = sum(durs) + OUT + FIN
    starts = np.cumsum([0] + durs + [OUT])
    rng = np.random.default_rng(5)
    # ---- ses
    n = int(SR * T); voice = np.zeros(n); fx = np.zeros(n)
    for st, w in zip(starts[:4], wavs):
        i = int(SR * (st + PRE)); voice[i:i + len(w)] += w[:n - i]
    i = int(SR * (starts[4] + 0.35)); voice[i:i + len(cta)] += cta[:n - i]
    i = int(SR * (starts[5] + 0.35)); voice[i:i + len(both)] += both[:n - i]
    bursts = [(0.2, W * 0.25, 420, GOLD2), (0.75, W * 0.78, 360, (255, 120, 200)), (1.4, W * 0.5, 230, (120, 200, 255)),
              (starts[4] + 0.15, W * 0.25, 380, GOLD2), (starts[4] + 0.7, W * 0.75, 330, (120, 255, 180)),
              (starts[5] + 0.3, W * 0.2, 330, GOLD2), (starts[5] + 0.55, W * 0.8, 300, (255, 120, 200)),
              (starts[5] + 1.1, W * 0.5, 260, (120, 200, 255)), (starts[5] + 1.6, W * 0.3, 1300, GOLD), (starts[5] + 1.9, W * 0.72, 1260, (255, 255, 255))]
    for bt, *_ in bursts:
        p = sfx_pop(rng); j = int(SR * bt); fx[j:j + len(p)] += p[:n - j] * 0.35
    for st in starts[1:6]:
        p = sfx_whoosh(rng); j = int(SR * (st - 0.2)); fx[j:j + len(p)] += p[:n - j]
    venv = _movavg(np.abs(voice), 2205)
    gate = _movavg(np.clip(venv / (venv.max() * 0.08 + 1e-9), 0, 1), int(SR * 0.35))
    duck = 1 - 0.62 * np.clip(gate * 1.5, 0, 1)
    audio = voice + fx * (1 - 0.4 * np.clip(gate, 0, 1)) + _speech_eq(party_music(T)) * 0.22 * duck
    audio = np.clip(audio, -1, 1)
    wavp = out + ".tmp.wav"
    with wave.open(wavp, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((audio * 32767).astype(np.int16).tobytes())
    # ---- görüntü
    bg = make_bg(); rays = make_rays()
    spr = {"num": gold_text(C["number"], 330), "head": gold_text(C.get("headline", "KİŞİYİZ!"), 170),
           "ilce": gold_text(city.DISTRICTS_LABEL, 190), "724": gold_text("7/24", 200),
           "q1": gold_text(city.WHERE_Q[0], 150), "q2": gold_text(city.WHERE_Q[1], 150), "kr": gold_text(city.BRAND, 110),
           "tes": gold_text("TEŞEKKÜRLER", 175)}
    kf = font(190, 700); kb = kf.getbbox(city.CITY + "!", stroke_width=6)
    ki = Image.new("RGBA", (kb[2] - kb[0] + 40, kb[3] - kb[1] + 40), (0, 0, 0, 0))
    ImageDraw.Draw(ki).text((20 - kb[0], 20 - kb[1]), city.CITY + "!", font=kf, fill=WHITE + (255,), stroke_width=6, stroke_fill=(110, 60, 0, 255))
    spr["koc"] = ki
    lg = Image.open(city.asset("logo.jpg")).convert("RGBA").resize((560, 560), Image.LANCZOS)
    mk = Image.new("L", (560, 560), 0); ImageDraw.Draw(mk).ellipse((0, 0, 559, 559), fill=255); lg.putalpha(mk)
    spr["logo"] = lg
    C["_spr"] = spr
    conf = Confetti(); conf.rain(140, -7.0, T); conf.burst(0.2, W * 0.15, H * 0.9, 80); conf.burst(0.2, W * 0.85, H * 0.9, 80)
    conf.burst(starts[5] + 0.3, W * 0.15, H * 0.95, 110); conf.burst(starts[5] + 0.3, W * 0.85, H * 0.95, 110)
    conf.burst(starts[5] + 0.35, W / 2, -40, 90, 800)
    for st in starts[1:4]: conf.burst(st + 0.05, W / 2, -40, 50, 700)
    fw = Fireworks()
    for bt, bx, by, col in bursts: fw.add(bt, bx, by, col)
    tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", wavp, "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p",
                          "-af", loudnorm_filter(wavp), "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", "-movflags", "+faststart", tmp],
                         stdin=subprocess.PIPE)
    fns = [lambda fr, d, tl: scene1(fr, d, tl, C, spr), lambda fr, d, tl: scene2(fr, d, tl, C),
           lambda fr, d, tl: scene3(fr, d, tl, C), lambda fr, d, tl: scene4(fr, d, tl, C), lambda fr, d, tl: outro(fr, d, tl, C),
           lambda fr, d, tl: finale(fr, d, tl, C)]
    words = [s.get("words") for s in scenes] + [None, None]
    spk = [s.get("speaker") for s in scenes] + [C.get("outro_speaker"), None]
    total = int(round(T * FPS))
    for k in range(total):
        t = k / FPS
        si = int(np.searchsorted(starts, t, side="right") - 1); si = min(si, 5)
        tl = t - starts[si]
        fr = bg.copy()
        fr.alpha_composite(rays_layer(rays, t, 560 if si >= 4 else 640))
        # içerik katmanı (sahne girişinde aşağıdan kayma)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        fns[si](lay, d, tl)
        if si > 0 and tl < 0.35:
            off = int((1 - ease(tl / 0.35)) * 140)
            lay = lay.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, -off), resample=Image.BILINEAR)
        fr.alpha_composite(lay)
        # havai fişek ışıması (küçük katmanda bulanıklaştırılıp büyütülür)
        gs = 0.5
        gl = Image.new("RGBA", (int(W * gs), int(H * gs)), (0, 0, 0, 0)); fw.draw(ImageDraw.Draw(gl), t, gs)
        if gl.getbbox():
            glow = gl.filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BILINEAR)
            fr.alpha_composite(glow); fr.alpha_composite(gl.resize((W, H), Image.BILINEAR))
        cl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); conf.draw(ImageDraw.Draw(cl), t); fr.alpha_composite(cl)
        # geçiş flaşı
        if si > 0 and tl < 0.18:
            fl = Image.new("RGBA", (W, H), GOLD2 + (int(110 * (1 - tl / 0.18)),)); fr.alpha_composite(fl)
        top = ImageDraw.Draw(fr)
        top.rectangle((0, 0, W, 10), fill=(255, 255, 255, 50)); top.rectangle((0, 0, int(W * t / T), 10), fill=GOLD + (255,))
        if words[si] or spk[si]:
            sl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sl)
            if spk[si]: speaker_tag(sd, spk[si], tl)
            if words[si]: subtitle(sd, words[si], (tl - PRE) * 1000)
            fr.alpha_composite(sl)
        p.stdin.write(fr.convert("RGB").tobytes())
    p.stdin.close(); p.wait()
    os.replace(tmp, out); os.remove(wavp)
    print("OK", out, round(T, 1), "sn")


if __name__ == "__main__":
    main(sys.argv[1])
