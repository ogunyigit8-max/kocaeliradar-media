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
     "focus": [lat, lon], "zoom": 1.0, "pins": [["ETİKET", lat, lon], ...],
     "words": [{"text": "Gebze'de", "start_ms": 100, "end_ms": 500}, ...]}
  ]
}
"sim" (isteğe bağlı): olayın TEMSİLİ canlandırması; ekranda otomatik "TEMSİLİ CANLANDIRMA" etiketi çıkar.
   {"type":"crash","at":[lat,lon],"road":[[lat,lon],...],"t_hit":1.9}  iki araç yaklaşır, çarpışır, çakarlar yanar
       (t_hit≈0.05 verilirse doğrudan olay sonrası görüntü: devrilmiş araçlar + çakar)
   {"type":"road","road":[[lat,lon],...],"status":"traffic"|"closed"}   yoğun trafik akışı / yol kapandı
   {"type":"rain","storm":true}   yağış (+şimşek)     {"type":"fire","at":[lat,lon]}   yangın + duman
   {"type":"outage","at":[lat,lon],"r":160}   bölgesel elektrik/su kesintisi
   KULLANICI İSTEĞİ (17.11.2026): simüle edilebilen HER olayı simüle et; her videoda olaya uyan en az bir
   "sim" sahnesi olsun (kaza→crash, trafik/yol çalışması/kapanma→road, yağış/fırtına/sel→rain, yangın→fire,
   elektrik/su/doğalgaz kesintisi→outage). Uygun tür yoksa sim koyma, zorlama.
   Kurallar: yalnızca kaynakta yazan olayı canlandır (kaza türü, yer, yol); ayrıntı uydurma; can kaybı olan
   olaylarda çarpışma animasyonu yerine sakin "road"/pin kullan; kaza sahnelerinde zoom 2.4-2.8.
   Yol koordinatları (yaklaşık): D-100 Gebze-İzmit [[40.835,29.30],[40.82,29.37],[40.805,29.42],[40.797,29.455],
   [40.79,29.50],[40.78,29.56],[40.775,29.62],[40.765,29.75],[40.765,29.92]]; TEM [[40.84,29.30],[40.83,29.45],
   [40.80,29.60],[40.78,29.80],[40.77,29.95],[40.75,30.10]].
"anim" (isteğe bağlı, KULLANICI İSTEĞİ 21.11.2026: "görsel ne kadar animasyonlu olursa o kadar iyi"):
   konuya uyan ANİMASYONLU SİMGE (tools/anim.py başındaki tür listesine bak). Örnek:
   {"type":"fuel","value":"68,80","unit":"TL","dir":"down","label":"BENZİN"}  (akaryakıt: pompa + fiyat sayacı)
   Türler: fuel, price, coins, bus, tram, school, water, gauge, football, cones, wind, snow, thermo,
   calendar, megaphone, quake, house, hospital, factory, ship.
   KURAL: HER HABER VİDEOSUNDA en az 2 sahnede (mümkünse kapak sahnesi dahil) konuya uyan bir "anim" kullan;
   haritanın göründüğü sahnelerin çoğunda simge olsun. "sim" ile aynı sahnede de kullanılabilir (sim haritada,
   anim üst-ortada). Örnek eşleşmeler: akaryakıt→fuel; zam/indirim/ücret/tarife→price; maaş/ekonomi→coins;
   otobüs/sefer/hat→bus; tramvay/raylı→tram; okul/tatil→school (stamp "TATİL"); su kesintisi→water cut;
   baraj/oran→gauge; maç→football (score); yol çalışması→cones; fırtına→wind; kar→snow; sıcaklık→thermo;
   tarih/başvuru/son gün→calendar; duyuru/uyarı→megaphone; deprem→quake; konut/TOKİ→house; sağlık→hospital;
   sanayi/OSB→factory; feribot/deniz→ship. Sayılar (value, score, mag, from/to) KAYNAKTAKİ değerle birebir.
   Simge 0. karede (kapak) tam görünür; sayılar sıfırdan sayarak gerçek değere varır.
SESLENDİRME METNİ: her cümleyi TTS'e göndermeden önce `python3 tools/tr_numbers.py "<cümle>"` ile çevir
   (sayılar bütün okunur: 1000 -> bin, D-100 -> Deyüz, 17.30 -> on yedi otuz, %109 -> yüzde yüz dokuz,
   95,60 TL -> doksan beş lira altmış kuruş). Altyazı (narr) metninde rakamlar olduğu gibi kalır.
"words" (isteğe bağlı, önerilir): o sahnenin WAV'ı için Speko audio_transcribe
(language "tr", word_timestamps true) çıktısındaki "words" listesi aynen yapıştırılır.
Altyazı kelime kelime konuşmayla senkron olur; yoksa süre harf sayısıyla tahmin edilir.
Harita verisi: tools/assets/tr-cities.json (il sınırları GeoJSON).
"""
import json, os, sys, wave, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from stories import font, text, W, H, YEL, RED, GRN, WHITE  # noqa: E402
from anim import anim_layer  # noqa: E402

A = os.path.join(HERE, "assets")
FPS = 30
SR = 44100
# Altyazı ve kaynak satırı Instagram Reels arayüzünün (alt açıklama + sağ butonlar) dışında
SUB_Y = 1400
SRC_Y = 1478
# Ses miksi: anlatım altındaki müzik ~18-20 dB geride olmalı (anlatım netliği)
MUSIC_GAIN = 0.20     # müzik taban seviyesi (eski: 0.5); konuşma altında ~22-23 dB geride
DUCK_DEPTH = 0.65     # konuşma sırasında müziği ek ~-9 dB kıs (eski: 0.4 ≈ -4 dB)
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
    # arazi dokusu
    rng2 = np.random.default_rng(11)
    tex = np.zeros((MH, MW), np.float32)
    for sc_, amp in [(96, 4), (24, 3), (6, 2.5)]:
        n_ = rng2.normal(0, 1, (MH // sc_ + 2, MW // sc_ + 2)).astype(np.float32)
        tex += np.asarray(Image.fromarray(n_).resize((MW, MH), Image.BICUBIC)) * amp
    lay = Image.fromarray(np.clip(np.asarray(lay, np.float32) + tex[..., None], 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(lay)
    # ilçe sınırları
    dj = json.load(open(os.path.join(A, "tr-districts-marmara.json"), encoding="utf-8"))
    for f in dj["features"]:
        g = f["geometry"]
        rings = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        for poly in rings:
            pts = [ll2px(la, lo) for lo, la in poly[0]]
            d.line(pts + [pts[0]], fill=(92, 96, 102), width=2)
    for name, pts in polys:
        if name != "Kocaeli": d.line(pts + [pts[0]], fill=(98, 101, 106), width=3)
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
    return x / np.abs(x).max() * env * 0.13


def ig_icon(d, x, y, s):
    """Instagram benzeri basit kamera simgesi (beyaz çizgi)."""
    d.rounded_rectangle((x, y, x + s, y + s), radius=s * 0.28, outline=WHITE, width=max(2, s // 12))
    r = s * 0.22; cx, cy = x + s / 2, y + s / 2
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=WHITE, width=max(2, s // 12))
    d.ellipse((x + s * 0.72, y + s * 0.18, x + s * 0.82, y + s * 0.28), fill=WHITE)


def ig_badge(size):
    """Renkli Instagram rozeti (RGBA)."""
    n = size; yy, xx = np.mgrid[0:n, 0:n] / n
    t = np.clip((xx * 0.5 + (1 - yy) * 0.7), 0, 1)[..., None]
    c1 = np.array([255, 196, 70]); c2 = np.array([235, 45, 110]); c3 = np.array([120, 60, 210])
    col = np.where(t < 0.5, c1 + (c2 - c1) * (t / 0.5), c2 + (c3 - c2) * ((t - 0.5) / 0.5))
    im = Image.fromarray(col.astype(np.uint8), "RGB").convert("RGBA")
    mask = Image.new("L", (n, n), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, n - 1, n - 1), radius=n * 0.27, fill=255)
    im.putalpha(mask)
    d = ImageDraw.Draw(im); m_ = n * 0.2; w_ = max(3, n // 14)
    d.rounded_rectangle((m_, m_, n - m_, n - m_), radius=n * 0.17, outline=WHITE, width=w_)
    r = n * 0.16; d.ellipse((n / 2 - r, n / 2 - r, n / 2 + r, n / 2 + r), outline=WHITE, width=w_)
    d.ellipse((n * 0.66, n * 0.27, n * 0.73, n * 0.34), fill=WHITE)
    return im


def speech_bounds(x):
    e = np.convolve(x ** 2, np.ones(441) / 441, "same")
    idx = np.where(e > (e.max() * 0.01))[0]
    return (idx[0] / SR, idx[-1] / SR) if len(idx) else (0, len(x) / SR)


def _norm(w):
    import re as _re
    w = w.lower().replace("i̇", "i").replace("’", "'")
    return _re.sub(r"[^\wçğıöşü]", "", w)


def word_times(narr_words, stt_words):
    """Altyazı kelimelerine (narr) STT kelime zaman damgalarını eşle (difflib ile hizalama).
    stt_words: Speko audio_transcribe(word_timestamps=true) çıktısındaki 'words' listesi
    ([{"text","start_ms","end_ms"}]). Eşleşmeyen kelimeler komşularından enterpole edilir.
    Döner: [(başlangıç_sn, bitiş_sn), ...] (narr_words ile aynı uzunlukta) veya None."""
    import difflib
    if not stt_words or not narr_words:
        return None
    a = [_norm(w) for w in narr_words]; b = [_norm(w["text"]) for w in stt_words]
    tm = [None] * len(a)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            w = stt_words[blk.b + k]; tm[blk.a + k] = (w["start_ms"] / 1000, w["end_ms"] / 1000)
    if sum(t is not None for t in tm) < max(2, len(a) * 0.4):
        return None  # hizalama zayıf -> eski yönteme dön
    t0 = stt_words[0]["start_ms"] / 1000; t1 = stt_words[-1]["end_ms"] / 1000
    known = [i for i, t in enumerate(tm) if t is not None]
    for i in range(len(tm)):
        if tm[i] is not None: continue
        lo = max([k for k in known if k < i], default=None); hi = min([k for k in known if k > i], default=None)
        s = tm[lo][1] if lo is not None else t0; e = tm[hi][0] if hi is not None else t1
        n_gap = (hi if hi is not None else len(tm)) - (lo if lo is not None else -1) - 1
        pos = i - (lo if lo is not None else -1) - 1
        step = max(e - s, 0.01) / n_gap
        tm[i] = (s + step * pos, s + step * (pos + 1))
    return tm


def make_chunks(narr, x, offset, maxw=3, stt=None):
    """Altyazıyı 2-3 kelimelik parçalara böl.
    stt (kelime zaman damgaları) varsa her kelime gerçek konuşma anına göre zamanlanır;
    yoksa konuşma süresine harf sayısıyla yayılır.
    Döner: [(başlangıç, bitiş, metin, [(kelime, k_başlangıç, k_bitiş), ...]), ...]"""
    words = narr.split()
    groups = []; cur = []
    for i, w in enumerate(words):
        cur.append(i)
        if len(cur) >= maxw or w[-1] in ".,;:!?":
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    wt = word_times(words, stt) if stt else None
    if wt is None:
        a, b = speech_bounds(x)
        tot = sum(len(w) + 1 for w in words) or 1; t = a; wt = []
        for w in words:
            dt = (b - a) * (len(w) + 1) / tot; wt.append((t, t + dt)); t += dt
    out = []
    for gi, g in enumerate(groups):
        s = wt[g[0]][0] + offset
        e = (wt[groups[gi + 1][0]][0] + offset) if gi + 1 < len(groups) else (wt[g[-1]][1] + offset + 0.3)
        out.append((s - 0.05, e, " ".join(words[i] for i in g), [(words[i], wt[i][0] + offset, wt[i][1] + offset) for i in g]))
    return out


def whoosh(seed=0):
    n = int(SR * 0.7); t = np.arange(n) / SR; rng = np.random.default_rng(seed)
    noise = rng.normal(0, 1, n)
    env = np.exp(-((t - 0.25) / 0.12) ** 2)
    sweep = np.cumsum(noise) ; sweep -= np.convolve(sweep, np.ones(60) / 60, "same")
    hit = np.sin(2 * np.pi * 58 * t) * np.exp(-t * 7) * (t > 0.25)
    y = sweep / (np.abs(sweep).max() + 1e-9) * env * 0.5 + np.roll(hit, 0) * 0.55
    return y


def outro_frame(m, tl, prog):
    """Kapanış: KOCAELİ RADAR + Instagram + TAKİP ET."""
    fr = m.crop((int(MW * 0.25), int(MH * 0.30), int(MW * 0.25 + 1500), int(MH * 0.30 + 2667))).resize((W, H), Image.BILINEAR).convert("RGBA")
    fr.alpha_composite(Image.new("RGBA", (W, H), (5, 6, 8, 205)))
    d = ImageDraw.Draw(fr)
    d.rectangle((0, 0, W, 8), fill=(255, 255, 255, 60)); d.rectangle((0, 0, int(W * prog), 8), fill=YEL + (255,))
    a = ease(tl / 0.5)
    text(d, (W / 2, 820), "KOCAELİ", 64, WHITE + (int(255 * a),), 500, "mm", sp=14)
    text(d, (W / 2, 930), "RADAR", 150, WHITE + (int(255 * a),), 700, "mm")
    b = ease((tl - 0.3) / 0.4)
    if b > 0:
        sz = int(120 * (0.6 + 0.4 * b)); badge = ig_badge(sz)
        fr.alpha_composite(badge, (int(W / 2 - sz / 2), int(1100 - sz / 2)))
        text(d, (W / 2, 1215), "@KOCAELIRADAR41", 44, WHITE, 600, "mm")
    c = ease((tl - 0.8) / 0.35)
    if c > 0:
        f = font(int(44 * (0.7 + 0.3 * c)), 700); tw = f.getlength("TAKİP ET")
        pulse = 1 + 0.04 * math.sin(tl * 6)
        hw = (tw / 2 + 26) * pulse; hh = 38 * pulse
        d.rectangle((W / 2 - hw, 1300 - hh, W / 2 + hw, 1300 + hh), fill=RED + (255,))
        d.text((W / 2, 1300), "TAKİP ET", font=f, fill=WHITE, anchor="mm")
    return fr


def music(T, bpm=100, seed=5):
    """Telifsiz sentetik haber müziği: davul, bas, akor ve arpej (Am-F-C-G)."""
    n = int(SR * T); t = np.arange(n) / SR; x = np.zeros(n); rng = np.random.default_rng(seed)
    beat = 60.0 / bpm; bar = beat * 4
    prog = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [55, 60, 64]), (55, [55, 59, 62])]
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    def add(st, sig):
        i = int(st * SR)
        if i >= n: return
        L = min(len(sig), n - i); x[i:i + L] += sig[:L]
    kL = int(SR * 0.35); kt = np.arange(kL) / SR
    kick = np.sin(2 * np.pi * (45 + 90 * np.exp(-kt * 30)) * kt) * np.exp(-kt * 9) * 0.9
    hL = int(SR * 0.05); hat = rng.normal(0, 1, hL); hat = (hat - np.convolve(hat, np.ones(8) / 8, "same")) * np.exp(-np.arange(hL) / SR * 90) * 0.18
    sL = int(SR * 0.2); st_ = np.arange(sL) / SR
    snare = (rng.normal(0, 1, sL) * 0.5 + np.sin(2 * np.pi * 190 * st_)) * np.exp(-st_ * 18) * 0.35
    nb = int(T / beat) + 1
    for b in range(nb):
        tb = b * beat
        if b % 4 in (0, 2): add(tb, kick)
        if b % 4 in (1, 3): add(tb, snare)
        add(tb, hat); add(tb + beat / 2, hat * 0.7)
    for k in range(int(T / bar) + 1):
        root, ch = prog[k % 4]; tb = k * bar
        L = int(SR * bar); tt = np.arange(L) / SR
        pad = sum(np.sin(2 * np.pi * hz(m) * tt) + 0.3 * np.sin(2 * np.pi * hz(m) * 2.003 * tt) for m in ch)
        add(tb, pad * np.clip(tt / 0.3, 0, 1) * np.clip((bar - tt) / 0.3, 0, 1) * 0.07)
        for q in range(8):  # bas sekizlikler
            bl = int(SR * beat / 2); bt = np.arange(bl) / SR
            add(tb + q * beat / 2, np.tanh(2 * np.sin(2 * np.pi * hz(root - 12) * bt)) * np.exp(-bt * 6) * 0.22)
        arp = ch + [ch[1] + 12]
        for q in range(8):
            al = int(SR * 0.3); at = np.arange(al) / SR; m = arp[q % 4] + 12
            add(tb + q * beat / 2, (np.sin(2 * np.pi * hz(m) * at) + 0.4 * np.sin(4 * np.pi * hz(m) * at)) * np.exp(-at * 9) * 0.08)
    x = _lowpass(x, 9000)
    env = np.clip(t / 0.8, 0, 1) * np.clip((T - t) / 1.2, 0, 1)
    return x / (np.abs(x).max() + 1e-9) * env


def _lowpass(x, fc):
    try:
        from scipy.signal import butter, sosfilt
        return sosfilt(butter(2, fc, btype="low", fs=SR, output="sos"), x)
    except Exception:
        return x


def loudnorm_filter(wavp, I=-14.0):
    """Ses zinciri: hafif konuşma kompresörü -> ölçülen değere göre sabit kazanç (-14 LUFS)
    -> tepe limitörü (~-1.9 dBFS). Tek geçişli loudnorm kısa videolarda hedefin 3-4 LU
    altında kalıyordu; bu zincir hedefe doğrusal (pompalamasız) ulaşır."""
    pre = "acompressor=threshold=0.1:ratio=3:attack=5:release=120:makeup=1.6"
    lim = "alimiter=limit=0.8:attack=2:release=50:level=false"
    import re as _re
    def meas(chain):
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", wavp, "-af", chain + ",ebur128", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        return float(_re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])
    try:
        gain = I - meas(pre)
        for _ in range(3):  # limitörün yediği seviyeyi telafi ederek hedefe yaklaş
            got = meas(f"{pre},volume={gain:.2f}dB,{lim}")
            if abs(got - I) < 0.3: break
            gain = max(-20.0, min(24.0, gain + (I - got)))
        return f"{pre},volume={gain:.2f}dB,{lim}"
    except Exception:
        return f"{pre},loudnorm=I={I}:TP=-1.5:LRA=11"


def _movavg(x, k):
    """Hızlı hareketli ortalama (kümülatif toplam, 'same' hizalı)."""
    c = np.cumsum(np.concatenate([np.zeros(k // 2 + 1), x, np.zeros(k - k // 2)]))
    return (c[k:k + len(x)] - c[:len(x)]) / k


def _speech_eq(x):
    """Müzikte konuşma bandını (≈800-3000 Hz) ~5 dB oy: anlatım daha net duyulur."""
    try:
        from scipy.signal import butter, sosfilt
        band = sosfilt(butter(2, [800, 3000], btype="band", fs=SR, output="sos"), x)
        return x - 0.45 * band
    except Exception:
        return x


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
    ig_icon(d, W - 60 - 98, 190, 34)
    text(d, (W - 60, 240), "@KOCAELIRADAR41", 20, WHITE, 600, "rm")
    # vinyet
    # İlk sahnede başlık 0. kareden itibaren tam görünür (Instagram kapak/akış önizlemesi için)
    st0 = sc.get("_static", False)
    a = 1.0 if st0 else ease(tl / 0.35)
    big = sc.get("big"); cy = 1180
    if big:
        col = {"white": WHITE, "yellow": YEL, "red": RED, "green": GRN}.get(sc.get("big_color", "white"), WHITE)
        size = 120 if len(big) <= 14 else (96 if len(big) <= 20 else 78)
        s = 1.0 if st0 else 1 + 0.25 * (1 - ease(tl / 0.3))
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
        b = 1.0 if st0 else ease((tl - 0.2) / 0.3)
        f = font(44, 700); tw = f.getlength(sub)
        st = sc.get("sub_style", "yellow")
        bg = {"yellow": YEL, "red": RED, "dark": (12, 12, 14)}[st]
        fg = (12, 12, 14) if st == "yellow" else WHITE
        y = cy + 105
        d.rectangle((W / 2 - tw / 2 - 18, y - 32, W / 2 + tw / 2 + 18, y + 32), fill=bg + (int(240 * b),))
        d.text((W / 2, y), sub, font=f, fill=fg + (int(255 * b),), anchor="mm")
    chunk = None
    for c0, c1, txt, wl in sc.get("_chunks", []):
        if c0 <= tl < c1: chunk = (txt, wl)
    # Altyazı: Instagram'ın alt arayüzünden (açıklama/butonlar) uzak, güvenli bölgede.
    # Konuşulan kelime sarı vurgulanır (kelime zaman damgasıyla senkron).
    if chunk:
        txt, wl = chunk
        f = font(48, 700); sp = f.getlength(" "); tw = f.getlength(txt); y = SUB_Y
        d.rectangle((W / 2 - tw / 2 - 20, y - 36, W / 2 + tw / 2 + 20, y + 36), fill=(8, 8, 10, 230))
        x = W / 2 - tw / 2
        for w, w0, w1 in wl:
            col = YEL if w0 <= tl < max(w1, w0 + 0.12) else WHITE
            d.text((x, y), w, font=f, fill=col, anchor="lm"); x += f.getlength(w) + sp
    text(d, (W / 2, SRC_Y), source, 24, (205, 205, 210), 500, "mm")
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


# ---------------------------------------------------------------------------
# OLAY SİMÜLASYONU (temsili canlandırma). Sahnede "sim" alanı ile açılır:
#   {"type": "crash", "at": [lat, lon], "road": [[lat, lon], ...]}   iki araç yaklaşır, çarpışma, çakar
#   {"type": "road",  "road": [[lat, lon], ...], "status": "closed"|"traffic"}  yol kapandı / yoğunluk
#   {"type": "rain",  "storm": true}                                   yağmur (+ şimşek)
#   {"type": "fire",  "at": [lat, lon]}                                yangın parıltısı + duman
#   {"type": "outage","at": [lat, lon], "r": 160}                      bölgesel kesinti (karanlık alan)
# Simülasyon olan sahnelerde ekranda "TEMSİLİ CANLANDIRMA" etiketi otomatik çıkar
# (izleyici gerçek görüntü sanmasın; yanıltıcı içerik Keşfet'ten düşer).
# ---------------------------------------------------------------------------
_RAIN = None


def _to_scr(la, lo, crop):
    x0, y0, cw, ch = crop
    mx, my = ll2px(la, lo)
    return ((mx - x0) * W / cw, (my - y0) * H / ch)


def _along(pts, f):
    """Kırık çizgi üzerinde 0..1 oranındaki nokta ve yön açısı."""
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    L = sum(seg) or 1; t = max(0.0, min(1.0, f)) * L
    for i, s in enumerate(seg):
        if t <= s or i == len(seg) - 1:
            a = t / s if s else 0
            p = (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * a, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * a)
            return p, math.atan2(pts[i + 1][1] - pts[i][1], pts[i + 1][0] - pts[i][0])
        t -= s
    return pts[-1], 0.0


def _car(d, c, ang, col, L=66, Wd=32, tilt=0.0):
    """Üstten görünüm araç (dönük dikdörtgen + ön cam)."""
    ang += tilt
    ca, sa = math.cos(ang), math.sin(ang)
    def P(u, v): return (c[0] + u * ca - v * sa, c[1] + u * sa + v * ca)
    body = [P(-L / 2, -Wd / 2), P(L / 2, -Wd / 2), P(L / 2, Wd / 2), P(-L / 2, Wd / 2)]
    d.polygon([(x + 3, y + 4) for x, y in body], fill=(0, 0, 0, 140))
    d.polygon(body, fill=col + (255,), outline=(20, 20, 24, 255))
    d.polygon([P(L * 0.12, -Wd * 0.38), P(L * 0.32, -Wd * 0.38), P(L * 0.32, Wd * 0.38), P(L * 0.12, Wd * 0.38)], fill=(30, 40, 55, 255))


def _road(d, pts, prog, col=(255, 204, 0), w=14):
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    L = sum(seg); tgt = L * prog; acc = 0.0; out = [pts[0]]
    for i, s in enumerate(seg):
        if acc + s <= tgt: out.append(pts[i + 1]); acc += s
        else:
            a = (tgt - acc) / s if s else 0
            out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * a, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * a)); break
    if len(out) >= 2:
        d.line(out, fill=col + (70,), width=w + 16, joint="curve")
        d.line(out, fill=col + (230,), width=w, joint="curve")


def sim_layer(sc, tl, crop):
    global _RAIN
    s = sc["sim"]; typ = s.get("type")
    o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
    road = [_to_scr(la, lo, crop) for la, lo in s.get("road", [])]
    if typ in ("crash", "road") and len(road) >= 2:
        _road(d, road, ease(tl / 0.8), RED if s.get("status") == "closed" else YEL)
    if typ == "crash":
        at = _to_scr(*s["at"], crop); t_hit = s.get("t_hit", 1.6)
        if len(road) >= 2:  # çarpışma noktasına yol üzerinden yaklaşan iki araç
            k = min(range(len(road)), key=lambda i: math.dist(road[i], at))
            pa = road[:k + 1] + [at] if k > 0 else [road[0], at]
            pb = list(reversed(road[k:])) + [at] if k < len(road) - 1 else [road[-1], at]
        else:
            pa = [(at[0] - 380, at[1] + 40), at]; pb = [(at[0] + 380, at[1] - 30), at]
        f = ease(min(tl / t_hit, 1.0)) * 0.97 + 0.03 * min(tl / t_hit, 1.0)
        after = max(0.0, tl - t_hit)
        for path, col, side, tilt_dir in ((pa, (245, 245, 248), -1, 1), (pb, YEL, 1, -1)):
            rp = list(reversed(path)); Lr = sum(math.dist(rp[i], rp[i + 1]) for i in range(len(rp) - 1)) or 1
            p, ang = _along(rp, min(1.0, 420 * (1 - f) / Lr)); ang += math.pi  # çarpışma noktasına 420 px'ten yaklaş
            if after > 0:  # çarpışma sonrası savrulma/devrilme
                kick = min(after / 0.35, 1.0)
                p = (at[0] + side * 34 * kick, at[1] + side * 18 * kick)
                _car(d, p, ang, col, tilt=tilt_dir * 1.2 * ease(kick))
            else:
                _car(d, p, ang, col)
        if after > 0:
            # darbe parlaması + şok halkaları
            fl = max(0.0, 1 - after / 0.45)
            if fl > 0:
                r = 40 + 220 * (1 - fl)
                d.ellipse((at[0] - r, at[1] - r, at[0] + r, at[1] + r), fill=(255, 240, 200, int(160 * fl)))
                for j in range(10):
                    a = j * math.pi / 5 + 0.3
                    d.line([(at[0] + math.cos(a) * 30, at[1] + math.sin(a) * 30),
                            (at[0] + math.cos(a) * (60 + 140 * (1 - fl)), at[1] + math.sin(a) * (60 + 140 * (1 - fl)))],
                           fill=(255, 220, 120, int(230 * fl)), width=6)
            for j in range(3):
                ph = ((after * 0.9) - j * 0.33) % 1.0
                r = 30 + 150 * ph
                d.ellipse((at[0] - r, at[1] - r, at[0] + r, at[1] + r), outline=RED + (int(200 * (1 - ph)),), width=5)
            # ambulans/polis çakarı
            if after > 0.5:
                blink = int(tl * 6) % 2
                for dx, col in ((-16, (230, 40, 50)), (16, (40, 110, 255))):
                    on = (dx < 0) == bool(blink)
                    rr = 26 if on else 12
                    d.ellipse((at[0] + dx - rr, at[1] - 70 - rr, at[0] + dx + rr, at[1] - 70 + rr), fill=col + (230 if on else 110,))
    elif typ == "road" and s.get("status") == "closed" and len(road) >= 2:
        c, _ = _along(road, 0.5); a = min(1.0, max(0.0, (tl - 0.6) / 0.3)); r = 46 * (0.6 + 0.4 * a)
        d.ellipse((c[0] - r - 8, c[1] - r - 8, c[0] + r + 8, c[1] + r + 8), fill=(255, 255, 255, int(235 * a)))
        d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=RED + (int(255 * a),))
        d.rectangle((c[0] - r * 0.6, c[1] - 7, c[0] + r * 0.6, c[1] + 7), fill=(255, 255, 255, int(255 * a)))
    elif typ == "road" and len(road) >= 2:  # yoğun trafik: yol boyunca akan araç noktaları
        for j in range(18):
            p, _ = _along(road, ((j / 18) + tl * 0.05) % 1.0)
            d.ellipse((p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7), fill=(RED if j % 3 else YEL) + (230,))
    elif typ == "fire":
        at = _to_scr(*s["at"], crop); g = 0.75 + 0.25 * math.sin(tl * 9) * math.sin(tl * 5.3)
        for r, al in ((150, 45), (100, 80), (60, 140), (30, 220)):
            rr = r * g; d.ellipse((at[0] - rr, at[1] - rr, at[0] + rr, at[1] + rr), fill=(255, 120 + (30 if r < 60 else 0), 20, al))
        rng = np.random.default_rng(5)
        for j in range(26):
            ph = (tl * 0.35 + j / 26) % 1.0; dx = rng.uniform(-40, 40) + 70 * ph * rng.uniform(0.3, 1)
            r = 18 + 60 * ph
            d.ellipse((at[0] + dx - r, at[1] - 40 - 330 * ph - r, at[0] + dx + r, at[1] - 40 - 330 * ph + r), fill=(70, 70, 75, int(110 * (1 - ph))))
    elif typ == "outage":
        at = _to_scr(*s["at"], crop); r = s.get("r", 160) * (1 + 0.04 * math.sin(tl * 3))
        fl = 1.0 if (int(tl * 7) % 9) else 0.55
        d.ellipse((at[0] - r, at[1] - r, at[0] + r, at[1] + r), fill=(0, 0, 0, int(170 * fl)), outline=YEL + (200,), width=4)
    if typ == "rain":
        if _RAIN is None:
            rng = np.random.default_rng(42); _RAIN = (rng.uniform(0, W, 260), rng.uniform(0, H, 260), rng.uniform(0.6, 1.4, 260))
        xs, ys, sp = _RAIN
        d.rectangle((0, 0, W, H), fill=(10, 20, 35, 60))
        for x, y, v in zip(xs, ys, sp):
            yy = (y + tl * 1900 * v) % (H + 80) - 40; xx = (x - tl * 260 * v) % W
            d.line([(xx, yy), (xx - 9 * v, yy + 46 * v)], fill=(190, 210, 235, int(120 * v)), width=2)
        if s.get("storm") and (1.1 < (tl % 3.2) < 1.22 or 1.3 < (tl % 3.2) < 1.36):
            d.rectangle((0, 0, W, H), fill=(235, 240, 255, 110))
    # zorunlu etiket
    f = font(28, 700); lab = "TEMSİLİ CANLANDIRMA"; tw = f.getlength(lab)
    d.rectangle((52, 196, 52 + tw + 28, 240), fill=(10, 10, 12, 215)); d.rectangle((52, 196, 58, 240), fill=RED + (255,))
    d.text((70, 218), lab, font=f, fill=WHITE, anchor="lm")
    return o


def main(spec_path):
    S = json.load(open(spec_path, encoding="utf-8"))
    root = os.path.dirname(HERE)
    out = os.path.join(root, S["out"]) if not os.path.isabs(S["out"]) else S["out"]
    m = build_map()
    S["scenes"][0]["_static"] = True  # kapak karesi: ilk sahnenin başlığı ilk karede görünür
    gap = 0.35
    clips = [wav_read(sc["wav"]) for sc in S["scenes"]]
    durs = [len(c) / SR + gap for c in clips]
    durs[0] += 0.3; durs[-1] += 0.6
    cta = wav_read(S["outro_wav"]) if S.get("outro_wav") else None
    OUT = max(3.6, (len(cta) / SR + 1.1) if cta is not None else 0)
    T = sum(durs) + OUT
    audio = np.zeros(int(SR * T) + SR)
    voice = np.zeros_like(audio)
    t0 = 0.0
    for i, c in enumerate(clips):
        st = int(SR * (t0 + (0.3 if i == 0 else 0.1)))
        audio[st:st + len(c)] += c * 0.95; voice[st:st + len(c)] += c
        S["scenes"][i]["_chunks"] = make_chunks(S["scenes"][i].get("narr", ""), c, (0.3 if i == 0 else 0.1),
                                                stt=S["scenes"][i].get("words"))
        if i > 0:
            wz = whoosh(i); ws = max(0, int(SR * (t0 - 0.25)))
            audio[ws:ws + len(wz)] += wz[:len(audio) - ws] * 0.35
        t0 += durs[i]
    wz = whoosh(99); ws = int(SR * (t0 - 0.25)); audio[ws:ws + len(wz)] += wz * 0.4
    if cta is not None:
        cs = int(SR * (t0 + 0.35)); audio[cs:cs + len(cta)] += cta[:len(audio) - cs] * 0.95
        voice[cs:cs + len(cta)] += cta[:len(audio) - cs]
    audio = audio[:int(SR * T)]
    # ducking yalnızca konuşma izinden (whoosh'lar hariç), yumuşak atak/bırakma (~0.35 sn)
    venv = _movavg(np.abs(voice[:int(SR * T)]), 2205)
    gate = np.clip(venv / (venv.max() * 0.08 + 1e-9), 0, 1)
    gate = _movavg(gate, int(SR * 0.35))
    duck = 1 - DUCK_DEPTH * np.clip(gate * 1.5, 0, 1)
    audio = audio + _speech_eq(music(T)) * MUSIC_GAIN * duck
    audio = np.clip(audio, -1, 1)
    wavp = out + ".tmp.wav"
    with wave.open(wavp, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((audio * 32767).astype(np.int16).tobytes())
    tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", wavp, "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
                          "-af", loudnorm_filter(wavp), "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", "-movflags", "+faststart", tmp], stdin=subprocess.PIPE)
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
            if sc.get("sim"): fr.alpha_composite(sim_layer(sc, tl, (x0, y0, cw, ch)))
            if sc.get("pins"): fr.alpha_composite(pins_layer(sc, tl, (x0, y0, cw, ch)))
            if sc.get("anim"): fr.alpha_composite(anim_layer(sc, tl))
            prog = (start + tl) / T
            fr.alpha_composite(overlay(sc, k, tl, S.get("category", "GÜNDEM"), S["source"], prog))
            p.stdin.write(fr.convert("RGB").tobytes())
        start += durs[i]
        prev_view = view
    for k in range(int(round(OUT * FPS))):
        tl = k / FPS
        p.stdin.write(outro_frame(m, tl, (start + tl) / T).convert("RGB").tobytes())
    p.stdin.close(); p.wait()
    os.replace(tmp, out); os.remove(wavp)
    print("OK", out, round(T, 1), "sn")


if __name__ == "__main__":
    main(sys.argv[1])
