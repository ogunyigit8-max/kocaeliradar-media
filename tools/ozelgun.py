"""Kocaeli Radar ÖZEL GÜN videosu (Öğretmenler Günü, bayramlar, kandiller, anma günleri). 1080x1920, 30 fps.

Kullanıcı isteği (22.11.2026): özel günlerde güzel, kalbi ısıtan videolar (state/ozel-gunler.md).
celebrate.py tabanlıdır (aynı ışık/konfeti/yazı sprite'ları, aynı -14 LUFS zinciri).

Kullanım:  python3 tools/ozelgun.py ozel.json
ozel.json:
{
  "out": "v/ozel-2026-11-24-ogretmenler-gunu.mp4",
  "mode": "kutlama" | "anma",          # anma: koyu zemin, konfeti/havai fişek yok, sakin müzik
  "date_label": "24 KASIM",              # kapakta üst etiket
  "title": ["ÖĞRETMENLER", "GÜNÜMÜZ", "KUTLU OLSUN"],   # kapak başlığı (0. karede tam görünür)
  "icon": "teacher" | "heart" | "crescent" | "flag" | "star",   # kapak ve sahne simgesi
  "scenes": [                            # 1. sahne kapaktır (big/sub kullanılmaz)
    {"wav": "...", "words": [...]},
    {"wav": "...", "words": [...], "big": ["İZMİT'TEN", "GEBZE'YE"], "sub": "TÜM ÖĞRETMENLERİMİZE", "districts": true},
    {"wav": "...", "words": [...], "big": ["TEŞEKKÜRLER"], "sub": "...", "icon": "heart"}
  ],
  "outro_wav": "..."                     # "Kocaeli Radar'ı takip et..." kapanışı
}
Her sahnede isteğe bağlı "speaker": "EMRE" | "AYLİN".
"""
import json, math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from stories import font, W, H, RED, WHITE  # noqa: E402
import city  # noqa: E402
from news import wav_read, loudnorm_filter, _movavg, _speech_eq, _lowpass, SR  # noqa: E402
from celebrate import (ease, back, make_bg, make_rays, rays_layer, Confetti, Fireworks, gold_text, shine,  # noqa: E402
                       paste_c, ctext, pill, subtitle, speaker_tag, party_music, sfx_pop, sfx_whoosh, outro,
                       GOLD, GOLD2, GOLD3, NAVY, DISTRICTS, A, FPS)

GREEN = (46, 140, 80)


# ---------------------------------------------------------------- simgeler
def draw_icon(d, kind, cx, cy, s, t, a=255):
    """Basit, animasyonlu vektör simgeler (telifsiz, elle çizilir)."""
    bob = 8 * math.sin(t * 2.2)
    cy = cy + bob
    if kind == "teacher":  # yazı tahtası + elma + kalem
        bw, bh = s * 1.5, s * 0.95
        d.rounded_rectangle((cx - bw, cy - bh, cx + bw, cy + bh), radius=18, fill=(120, 72, 30, a))
        d.rounded_rectangle((cx - bw + 18, cy - bh + 18, cx + bw - 18, cy + bh - 18), radius=10, fill=(30, 74, 52, a))
        # tebeşir yazısı (yazılıyor efekti)
        txt = "TEŞEKKÜRLER"
        k = int(len(txt) * min(1, max(0, (t - 0.2) / 1.2)))
        d.text((cx, cy - 8), txt[:max(k, 0)] if t > 0.05 else txt, font=font(int(s * 0.33), 700), fill=(240, 240, 230, a), anchor="mm")
        d.line((cx - bw * 0.6, cy + bh * 0.42, cx + bw * 0.6, cy + bh * 0.42), fill=(240, 240, 230, int(a * 0.6)), width=4)
        # elma (sağ alt)
        ax, ay, r = cx + bw - 10, cy + bh + 6, s * 0.36
        d.ellipse((ax - r, ay - r * 0.9, ax + r * 0.15, ay + r), fill=(214, 40, 40, a))
        d.ellipse((ax - r * 0.15, ay - r * 0.9, ax + r, ay + r), fill=(214, 40, 40, a))
        d.ellipse((ax - r * 0.55, ay - r * 0.55, ax - r * 0.25, ay - r * 0.1), fill=(255, 160, 160, a))
        d.line((ax, ay - r * 0.85, ax + 6, ay - r * 1.35), fill=(90, 50, 20, a), width=8)
        d.ellipse((ax + 6, ay - r * 1.45, ax + r * 0.75, ay - r * 1.05), fill=(70, 170, 70, a))
        # kalem (sol alt)
        px, py = cx - bw + 20, cy + bh + 24
        d.polygon([(px, py), (px + s * 0.9, py - s * 0.18), (px + s * 0.95, py - s * 0.05), (px + 5, py + 13)], fill=(250, 196, 40, a))
        d.polygon([(px, py), (px + 5, py + 13), (px - 26, py + 14)], fill=(240, 210, 170, a))
    elif kind == "heart":
        k = s * (1 + 0.08 * math.sin(t * 6))
        d.ellipse((cx - k, cy - k * 0.9, cx, cy + k * 0.1), fill=RED + (a,))
        d.ellipse((cx, cy - k * 0.9, cx + k, cy + k * 0.1), fill=RED + (a,))
        d.polygon([(cx - k * 0.98, cy - k * 0.25), (cx + k * 0.98, cy - k * 0.25), (cx, cy + k * 1.1)], fill=RED + (a,))
    elif kind == "crescent":
        d.ellipse((cx - s, cy - s, cx + s, cy + s), fill=GOLD2 + (a,))
        d.ellipse((cx - s * 0.55, cy - s * 1.05, cx + s * 1.25, cy + s * 0.85), fill=(0, 0, 0, 0))
        star(d, cx + s * 0.75, cy - s * 0.1, s * 0.3, GOLD2 + (a,), t)
    elif kind == "flag":
        wv = [(cx - s * 1.4 + i * s * 0.28, cy - s * 0.85 + 10 * math.sin(t * 4 + i * 0.7)) for i in range(11)]
        wb = [(x, y + s * 1.7) for x, y in reversed(wv)]
        d.polygon(wv + wb, fill=(227, 10, 23, a))
        d.ellipse((cx - s * 0.75, cy - s * 0.5, cx + s * 0.25, cy + s * 0.5), fill=WHITE + (a,))
        d.ellipse((cx - s * 0.55, cy - s * 0.4, cx + s * 0.25, cy + s * 0.4), fill=(227, 10, 23, a))
        star(d, cx + s * 0.45, cy, s * 0.28, WHITE + (a,), 0)
    else:  # star
        star(d, cx, cy, s, GOLD2 + (a,), t)


def star(d, x, y, r, col, t):
    rot = t * 0.4
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.42
        ang = -math.pi / 2 + i * math.pi / 5 + rot
        pts.append((x + rr * math.cos(ang), y + rr * math.sin(ang)))
    d.polygon(pts, fill=col)


# ---------------------------------------------------------------- sahneler
def cover(fr, d, tl, C):
    pill(d, W / 2, 120, "KOCAELİ RADAR", 36, (10, 12, 22, 230), GOLD + (255,), padx=30)
    pill(d, W / 2, 225, C.get("date_label", ""), 46, GOLD + (255,), NAVY + (255,), padx=40)
    ys = [470 + i * 175 for i in range(len(C["_title"]))]
    for i, (sp, mk) in enumerate(C["_title"]):
        pulse = 1 + 0.03 * math.exp(-((tl - 0.3 - i * 0.12) / 0.12) ** 2) + 0.008 * math.sin(tl * 3 + i)
        paste_c(fr, shine(sp, mk, tl + i * 0.3) if C["mode"] == "kutlama" else sp, W / 2, ys[i], pulse)
    draw_icon(d, C.get("icon", "star"), W / 2, ys[-1] + 300, 150, tl)


def generic(fr, d, tl, C, S, k):
    big = C["_big"][k]
    s = back(tl / 0.45) if tl < 0.6 else 1.0
    if S.get("districts"):
        y0 = 260
        for i, (sp, _) in enumerate(big):
            paste_c(fr, sp, W / 2, y0 + i * 150, max(0.01, s))
        if S.get("sub"):
            pill(d, W / 2, y0 + len(big) * 150 + 10, S["sub"], 48, WHITE + (255,), NAVY + (255,), padx=36)
        cols, cw, ch, gx, gy, gy0 = 3, 300, 96, 26, 26, y0 + len(big) * 150 + 130
        x0 = W / 2 - (cols * cw + (cols - 1) * gx) / 2
        for i, name in enumerate(DISTRICTS):
            r, c = divmod(i, cols)
            t0 = 0.2 + i * 0.16
            if tl < t0: continue
            e = back((tl - t0) / 0.35)
            x = x0 + c * (cw + gx) + cw / 2; y = gy0 + r * (ch + gy) + ch / 2
            w2, h2 = cw / 2 * e, ch / 2 * e
            lit = tl - t0 < 0.6
            d.rounded_rectangle((x - w2, y - h2, x + w2, y + h2), radius=24,
                                fill=(GOLD if lit else (16, 22, 44)) + (240,), outline=GOLD + (255,), width=3)
            if e > 0.5:
                fs = 44 if len(name) <= 8 else 38
                d.text((x, y), name, font=font(int(fs * min(1, e)), 700), fill=(NAVY if lit else WHITE) + (255,), anchor="mm")
        return
    draw_icon(d, S.get("icon", C.get("icon", "star")), W / 2, 380, 130, tl)
    y0 = 700
    for i, (sp, _) in enumerate(big):
        paste_c(fr, sp, W / 2, y0 + i * 150, max(0.01, s))
    if S.get("sub"):
        a = ease((tl - 0.4) / 0.4)
        if a > 0:
            pill(d, W / 2, y0 + len(big) * 150 + 40, S["sub"], 50, (255, 255, 255, int(255 * a)), NAVY + (int(255 * a),), padx=38)


# ---------------------------------------------------------------- müzik
def calm_music(T, seed=4):
    """Anma için ağır, yumuşak pad (minör akorlar, yavaş zarf)."""
    n = int(SR * T); t = np.arange(n) / SR; x = np.zeros(n)
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    prog = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
    bar = 4.0
    for k in range(int(T / bar) + 1):
        st = int(k * bar * SR); L = min(int(bar * 1.6 * SR), n - st)
        if L <= 0: break
        tt = np.arange(L) / SR
        env = np.sin(np.pi * np.clip(tt / (bar * 1.6), 0, 1)) ** 1.5
        sig = sum(np.sin(2 * np.pi * hz(m) * tt) + 0.3 * np.sin(2 * np.pi * hz(m) * 2.001 * tt) for m in prog[k % 4])
        sig += 0.6 * np.sin(2 * np.pi * hz(prog[k % 4][0] - 12) * tt)
        x[st:st + L] += sig * env
    x = _lowpass(x, 3500)
    env = np.clip(t / 1.0, 0, 1) * np.clip((T - t) / 1.5, 0, 1)
    return x / (np.abs(x).max() + 1e-9) * env


def warm_music(T):
    """Kutlama: celebrate.py'deki neşeli müziğin daha yumuşak (100 bpm) hali."""
    return party_music(T, bpm=100, seed=11)


# ---------------------------------------------------------------- ana akış
def main(spec):
    C = json.load(open(spec))
    C.setdefault("mode", "kutlama")
    kut = C["mode"] == "kutlama"
    out = os.path.join(os.path.dirname(HERE), C["out"])
    scenes = C["scenes"]
    wavs = [wav_read(s["wav"]) for s in scenes]
    PRE = 0.25
    durs = [PRE + len(w) / SR + 0.5 for w in wavs]
    cta = wav_read(C["outro_wav"])
    OUT = len(cta) / SR + 1.0
    T = sum(durs) + OUT
    starts = np.cumsum([0] + durs)
    NS = len(scenes)
    rng = np.random.default_rng(5)
    # ---- ses
    n = int(SR * T); voice = np.zeros(n); fx = np.zeros(n)
    for st, w in zip(starts[:NS], wavs):
        i = int(SR * (st + PRE)); voice[i:i + len(w)] += w[:n - i]
    i = int(SR * (starts[NS] + 0.35)); voice[i:i + len(cta)] += cta[:n - i]
    bursts = []
    if kut:
        bursts = [(0.2, W * 0.22, 380, GOLD2), (0.8, W * 0.78, 340, (255, 120, 200)),
                  (starts[NS] + 0.2, W * 0.25, 360, GOLD2), (starts[NS] + 0.7, W * 0.75, 320, (120, 255, 180))]
        for bt, *_ in bursts:
            p = sfx_pop(rng); j = int(SR * bt); fx[j:j + len(p)] += p[:n - j] * 0.25
    for st in starts[1:NS + 1]:
        p = sfx_whoosh(rng); j = int(SR * (st - 0.2)); fx[j:j + len(p)] += p[:n - j] * (1.0 if kut else 0.5)
    venv = _movavg(np.abs(voice), 2205)
    gate = _movavg(np.clip(venv / (venv.max() * 0.08 + 1e-9), 0, 1), int(SR * 0.35))
    duck = 1 - 0.62 * np.clip(gate * 1.5, 0, 1)
    mus = warm_music(T) if kut else calm_music(T)
    audio = voice + fx * (1 - 0.4 * np.clip(gate, 0, 1)) + _speech_eq(mus) * (0.22 if kut else 0.26) * duck
    audio = np.clip(audio, -1, 1)
    wavp = out + ".tmp.wav"
    with wave.open(wavp, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((audio * 32767).astype(np.int16).tobytes())
    # ---- görüntü
    if kut:
        bg = make_bg(); rays = make_rays()
    else:
        yy = np.linspace(0, 1, H)[:, None, None]
        g = np.array([22, 24, 30], np.float32) * (1 - yy) + np.array([6, 7, 10], np.float32) * yy
        bg = Image.fromarray(np.repeat(g, W, 1).astype(np.uint8)).convert("RGBA"); rays = None
    tsz = 150 if max(len(s) for s in C["title"]) <= 11 else 120
    C["_title"] = [gold_text(s, tsz) for s in C["title"]]
    C["_big"] = [[gold_text(s, 118 if len(s) <= 12 else 96) for s in sc.get("big", [])] for sc in scenes]
    spr = {"kr": gold_text("KOCAELİ RADAR", 110)}
    lg = Image.open(city.asset("logo.jpg")).convert("RGBA").resize((560, 560), Image.LANCZOS)
    mk = Image.new("L", (560, 560), 0); ImageDraw.Draw(mk).ellipse((0, 0, 559, 559), fill=255); lg.putalpha(mk)
    spr["logo"] = lg
    C["_spr"] = spr
    conf = Confetti(); fw = Fireworks()
    if kut:
        conf.rain(110, -7.0, T); conf.burst(0.2, W * 0.15, H * 0.9, 70); conf.burst(0.2, W * 0.85, H * 0.9, 70)
        conf.burst(starts[NS] + 0.3, W / 2, -40, 90, 800)
        for bt, bx, by, col in bursts: fw.add(bt, bx, by, col)
    tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", wavp, "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p",
                          "-af", loudnorm_filter(wavp), "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", "-movflags", "+faststart", tmp],
                         stdin=subprocess.PIPE)
    words = [s.get("words") for s in scenes] + [None]
    spk = [s.get("speaker") for s in scenes] + [None]
    total = int(round(T * FPS))
    for k in range(total):
        t = k / FPS
        si = int(np.searchsorted(starts, t, side="right") - 1); si = min(si, NS)
        tl = t - starts[si]
        fr = bg.copy()
        if rays is not None:
            fr.alpha_composite(rays_layer(rays, t, 560 if si >= NS else 640))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        if si == 0:
            cover(lay, d, tl, C)
        elif si < NS:
            generic(lay, d, tl, C, scenes[si], si)
        else:
            outro(lay, d, tl, C)
        if si > 0 and tl < 0.35:
            off = int((1 - ease(tl / 0.35)) * 140)
            lay = lay.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, -off), resample=Image.BILINEAR)
        fr.alpha_composite(lay)
        if kut:
            gs = 0.5
            gl = Image.new("RGBA", (int(W * gs), int(H * gs)), (0, 0, 0, 0)); fw.draw(ImageDraw.Draw(gl), t, gs)
            if gl.getbbox():
                glow = gl.filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BILINEAR)
                fr.alpha_composite(glow); fr.alpha_composite(gl.resize((W, H), Image.BILINEAR))
            cl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); conf.draw(ImageDraw.Draw(cl), t); fr.alpha_composite(cl)
            if si > 0 and tl < 0.18:
                fl = Image.new("RGBA", (W, H), GOLD2 + (int(90 * (1 - tl / 0.18)),)); fr.alpha_composite(fl)
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
