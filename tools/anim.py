"""Kocaeli Radar haber videoları için konuya uygun ANİMASYONLU SİMGELER (infografik katmanı).

news.py sahnesinde "anim" alanıyla açılır (tek sözlük ya da sözlük listesi):
  "anim": {"type": "fuel", "value": "68,80", "unit": "TL", "dir": "down", "label": "BENZİN"}

Simge haritanın üst-orta bölgesinde (başlığın üstünde) koyu bir daire zemin üzerinde canlanır.
Bunlar olayın canlandırması değil, konuyu anlatan simgelerdir; "TEMSİLİ CANLANDIRMA" etiketi çıkmaz.
Sayı alanları (value/from/to/mag/score) KAYNAKTAKİ değerle birebir yazılmalı; animasyon o değere sayarak varır.

Türler (parametreler isteğe bağlı, köşeli parantez):
  fuel      akaryakıt pompası, ekranda fiyat sayacı, damlayan yakıt      [value, unit="TL", dir=up|down, label]
  price     sallanan fiyat etiketi + ok (zam/indirim, ücret, tarife)     [value, unit="TL", dir, label]
  coins     yağan ve üst üste dizilen madeni paralar (ekonomi, maaş)      [label]
  bus       yolda ilerleyen otobüs, dönen tekerler (toplu taşıma, sefer)  [label (hat no/ad), color=yellow|blue|red]
  tram      ilerleyen tramvay / raylı sistem                              [label]
  school    okul binası, dalgalanan bayrak, isteğe bağlı damga            [stamp (ör. "TATİL")]
  water     musluk, damlayan su; cut=true ise kesinti işareti             [cut]
  gauge     dolan yüzde halkası (baraj doluluk, oran)                     [value (0-100), label]
  football  zıplayan top + skor tabelası                                  [score "2-1", teams ["KOCAELİSPOR","FB"]]
  cones     trafik konileri, şerit bariyer, yanıp sönen ışık (yol çalışması) [label]
  wind      ekranı geçen rüzgâr çizgileri ve savrulan yapraklar (tam ekran) []
  snow      yağan kar taneleri (tam ekran)                                []
  thermo    termometre; cıva from→to arasında hareket eder (sıcaklık)     [from, to, unit="°C"]
  calendar  açılan takvim yaprağı (tarih, son gün, başvuru)               [day, month, label]
  megaphone ses dalgalı megafon (duyuru, uyarı, çağrı)                    [label]
  quake     sismograf çizgisi + sarsılan simge (deprem)                   [mag]
  house     ev + dönen anahtar (konut, TOKİ, kira)                        [label]
  hospital  hastane + atan kalp ritmi çizgisi (sağlık)                    [label]
  factory   bacasından duman çıkan fabrika (sanayi, OSB, istihdam)        [label]
  ship      dalgalarda ilerleyen gemi/feribot (deniz ulaşımı)             [label]
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageChops

from stories import font, W, H, YEL, RED, GRN, WHITE  # noqa: E402

CX, CY, R = W // 2, 640, 300   # simge alanı merkezi ve zemin yarıçapı
DARK = (12, 14, 18)
BLUE = (40, 120, 230)
SKY = (110, 180, 255)
GREY = (150, 155, 165)


def fs(v):
    """Yazı boyutu: animasyon başında 0'a düşmesin, önbellek şişmesin (2 px adım)."""
    return max(8, int(v) // 2 * 2)


def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def back(x):
    """Hafif taşmalı açılış (pop)."""
    x = max(0.0, min(1.0, x)); c = 1.70158
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def tr_parse(v):
    """'68,80' / '1.234,5' / 68.8 -> (float, ondalık hane)."""
    if isinstance(v, (int, float)):
        s = f"{v}"
        return float(v), (len(s.split(".")[1]) if "." in s else 0)
    s = str(v).strip().replace(" ", "")
    if "," in s:
        dec = len(s.split(",")[1]); return float(s.replace(".", "").replace(",", ".")), dec
    if s.count(".") == 1 and len(s.split(".")[1]) != 3:
        return float(s), len(s.split(".")[1])
    return float(s.replace(".", "")), 0


def tr_fmt(x, dec):
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def counter(v, tl, dur=1.3, start_ratio=None, dirn=None):
    """Değere sayarak varan metin. Son değer kaynaktaki metinle birebir aynıdır."""
    try:
        x, dec = tr_parse(v)
    except Exception:
        return str(v)
    if start_ratio is None:
        start_ratio = 0.0   # sıfırdan sayar: ara karelerde "önceki fiyat" sanılacak bir değer görünmez
    e = ease(tl / dur)
    if e >= 0.999:
        return str(v) if isinstance(v, str) else tr_fmt(x, dec)
    return tr_fmt(x * start_ratio + (x - x * start_ratio) * e, dec)


class P:
    """Merkez + ölçek + dönüş ile koordinat dönüştürücü."""
    def __init__(self, cx, cy, s=1.0, ang=0.0):
        self.cx, self.cy, self.s, self.ca, self.sa = cx, cy, s, math.cos(ang), math.sin(ang)

    def __call__(self, x, y):
        x, y = x * self.s, y * self.s
        return (self.cx + x * self.ca - y * self.sa, self.cy + x * self.sa + y * self.ca)

    def pts(self, lst):
        return [self(x, y) for x, y in lst]

    def box(self, x0, y0, x1, y1):
        a, b = self(x0, y0), self(x1, y1)
        return (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1]))

    def r(self, v):
        return v * self.s


def rect(d, p, x0, y0, x1, y1, fill, outline=None, w=0):
    d.polygon(p.pts([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]), fill=fill, outline=outline, width=w)


def circ(d, p, x, y, r, fill=None, outline=None, w=0):
    c = p(x, y); rr = p.r(r)
    d.ellipse((c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr), fill=fill, outline=outline, width=w)


def label_tag(d, txt, y, a=255, col=YEL):
    if not txt: return
    f = font(40, 700); tw = f.getlength(txt)
    d.rectangle((CX - tw / 2 - 18, y - 28, CX + tw / 2 + 18, y + 28), fill=(10, 10, 12, int(235 * a / 255)))
    d.rectangle((CX - tw / 2 - 18, y + 28, CX + tw / 2 + 18, y + 33), fill=col + (a,))
    d.text((CX, y), txt, font=f, fill=WHITE + (a,), anchor="mm")


def arrow(d, x, y, dirn, tl, size=70):
    if dirn not in ("up", "down"): return
    bob = 10 * math.sin(tl * 5)
    col = GRN if dirn == "down" else RED
    sgn = 1 if dirn == "down" else -1
    y += bob * sgn
    s = size
    pts = [(x - s * 0.32, y - sgn * s * 0.5), (x + s * 0.32, y - sgn * s * 0.5), (x + s * 0.32, y),
           (x + s * 0.62, y), (x, y + sgn * s * 0.65), (x - s * 0.62, y), (x - s * 0.32, y)]
    d.polygon([(px + 4, py + 5) for px, py in pts], fill=(0, 0, 0, 120))
    d.polygon(pts, fill=col + (255,), outline=(255, 255, 255, 255), width=3)


def backdrop(d, tl, full=False):
    a = ease(tl / 0.35)
    r = R * (0.6 + 0.4 * back(tl / 0.45))
    for k, al in ((26, 60), (12, 110)):
        rr = r + k
        d.ellipse((CX - rr, CY - rr, CX + rr, CY + rr), fill=(0, 0, 0, int(al * a)))
    d.ellipse((CX - r, CY - r, CX + r, CY + r), fill=DARK + (int(215 * a),), outline=YEL + (int(230 * a),), width=6)
    # dönen ince yay
    ang = tl * 90
    d.arc((CX - r - 14, CY - r - 14, CX + r + 14, CY + r + 14), ang, ang + 70, fill=YEL + (int(200 * a),), width=5)
    d.arc((CX - r - 14, CY - r - 14, CX + r + 14, CY + r + 14), ang + 180, ang + 230, fill=WHITE + (int(150 * a),), width=4)


# --------------------------------------------------------------------------- türler
def _fuel(d, a, tl, s):
    p = P(CX - 30, CY + 10, back(tl / 0.5))
    rect(d, p, -120, -170, 80, 190, (40, 40, 46, 255))
    rect(d, p, -110, -160, 70, 180, RED + (255,))
    rect(d, p, -95, -135, 55, -45, (8, 18, 12, 255), (255, 255, 255, 255), 3)
    f = font(fs(p.r(46)), 700)
    d.text(p(-20, -90), counter(s.get("value", ""), tl - 0.3, dirn=s.get("dir")), font=f, fill=(120, 255, 150, 255), anchor="mm")
    rect(d, p, -95, -20, 55, 20, (255, 255, 255, 230))
    lab = (s.get("label") or "YAKIT")[:9]
    d.text(p(-20, 0), lab, font=font(fs(p.r(28)), 700), fill=(20, 20, 24, 255), anchor="mm")
    rect(d, p, -130, 175, 90, 205, (30, 30, 34, 255))
    # hortum + tabanca
    hose = [p(80, -60), p(130, -40), p(150, 40), p(140, 120), p(110, 140)]
    d.line(hose, fill=(25, 25, 28, 255), width=int(p.r(16)), joint="curve")
    noz = P(p(110, 140)[0], p(110, 140)[1], p.s, math.radians(20 + 6 * math.sin(tl * 3)))
    rect(d, noz, -10, -18, 60, 18, (60, 60, 66, 255)); rect(d, noz, 55, -6, 95, 6, (90, 90, 96, 255))
    tip = noz(95, 0)
    for j in range(4):
        ph = (tl * 1.4 + j / 4) % 1.0
        y = tip[1] + 10 + 140 * ph
        rr = p.r(11) * (1 - 0.3 * ph)
        d.ellipse((tip[0] - rr, y - rr * 1.3, tip[0] + rr, y + rr), fill=(255, 200, 40, int(230 * (1 - ph))))
    arrow(d, CX + 190, CY - 170, s.get("dir"), tl)


def _price(d, a, tl, s):
    sw = math.radians(8 * math.sin(tl * 2.6) * (1 - ease(tl / 6)) + 3)
    p = P(CX, CY - 120, back(tl / 0.5), sw)
    d.line([p(0, -40), p(0, 30)], fill=(220, 220, 225, 255), width=4)
    tag = [(-150, 30), (110, 30), (170, 120), (170, 300), (-150, 300)]
    d.polygon([(x + 6, y + 8) for x, y in p.pts(tag)], fill=(0, 0, 0, 120))
    d.polygon(p.pts(tag), fill=YEL + (255,), outline=(255, 255, 255, 255), width=4)
    circ(d, p, 110, 85, 16, fill=DARK + (255,))
    val = counter(s.get("value", ""), tl - 0.3, dirn=s.get("dir"))
    f = font(fs(p.r(84 if len(val) <= 6 else 64)), 700)
    d.text(p(10, 185), val, font=f, fill=DARK + (255,), anchor="mm")
    d.text(p(10, 262), s.get("unit", "TL"), font=font(fs(p.r(38)), 700), fill=DARK + (255,), anchor="mm")
    arrow(d, CX + 215, CY - 150, s.get("dir"), tl)


def _coin(d, x, y, r, rot=0.0):
    w = abs(math.cos(rot)) * r + r * 0.15
    d.ellipse((x - w + 3, y - r + 4, x + w + 3, y + r + 4), fill=(0, 0, 0, 120))
    d.ellipse((x - w, y - r, x + w, y + r), fill=(230, 170, 20, 255), outline=(255, 225, 120, 255), width=4)
    if w > r * 0.6:
        d.text((x, y), "TL", font=font(fs(r * 0.8), 700), fill=(140, 95, 0, 255), anchor="mm")


def _coins(d, a, tl, s):
    for i in range(5):  # yığın
        t = tl - 0.3 - i * 0.18
        if t < 0: continue
        y = CY + 170 - i * 34 - 260 * (1 - ease(t / 0.35))
        d.ellipse((CX - 110 - 8, y - 22, CX - 110 + 120, y + 22), fill=(200, 145, 15, 255), outline=(255, 225, 120, 255), width=3)
    rng = np.random.default_rng(11)
    for j in range(9):
        ph = (tl * 0.55 + j / 9) % 1.0
        x = CX - 200 + rng.uniform(0, 400); y = CY - 260 + 460 * ph
        _coin(d, x, y, 34 + rng.uniform(0, 14), tl * 5 + j)
    label_tag(d, s.get("label"), CY + 250)


def _bus(d, a, tl, s, tram=False):
    col = {"yellow": YEL, "blue": BLUE, "red": RED}.get(s.get("color"), BLUE if not tram else (230, 60, 70))
    d.rectangle((CX - R + 30, CY + 120, CX + R - 30, CY + 132), fill=(70, 70, 78, 255))
    for k in range(-4, 5):  # yol çizgileri akar
        x = CX + ((k * 90 - tl * 260) % 900) - 450
        if abs(x - CX) < R - 60:
            d.rectangle((x - 22, CY + 150, x + 22, CY + 158), fill=(240, 240, 240, 200))
    if tram:
        d.line([(CX - R + 40, CY - 175), (CX + R - 40, CY - 175)], fill=(200, 200, 205, 255), width=3)
    x = CX - 520 + 520 * ease(tl / 1.2) + 14 * math.sin(tl * 1.5)
    y = CY + 10 + (3 * math.sin(tl * 18) if tl > 1.2 else 0)
    p = P(x, y, 1.0)
    L = 230 if tram else 210
    d.rounded_rectangle(p.box(-L, -110, L, 85), radius=26, fill=col + (255,), outline=(255, 255, 255, 255), width=4)
    for i in range(5 if tram else 4):
        wx = -L + 30 + i * ((2 * L - 60) / (5 if tram else 4))
        d.rounded_rectangle(p.box(wx, -90, wx + (2 * L - 60) / (5 if tram else 4) - 14, -20), radius=8, fill=(190, 225, 255, 255))
    rect(d, p, -L, 20, L, 34, (255, 255, 255, 200))
    lab = (s.get("label") or "")[:16]
    if lab: d.text(p(0, 55), lab, font=font(34, 700), fill=WHITE + (255,), anchor="mm")
    if tram:
        d.line([p(0, -110), p(-30, -175), p(30, -175)], fill=(40, 40, 46, 255), width=5)
    for wx in ((-L + 70, L - 70) if not tram else (-L + 60, -L + 130, L - 130, L - 60)):
        c = p(wx, 88); rr = 36 if not tram else 26
        d.ellipse((c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr), fill=(25, 25, 28, 255))
        d.ellipse((c[0] - rr * 0.5, c[1] - rr * 0.5, c[0] + rr * 0.5, c[1] + rr * 0.5), fill=(180, 180, 188, 255))
        ang = -tl * 9
        for k in range(3):
            aa = ang + k * 2.094
            d.line([c, (c[0] + math.cos(aa) * rr * 0.5, c[1] + math.sin(aa) * rr * 0.5)], fill=(60, 60, 66, 255), width=4)
    if tl < 1.2:  # hız çizgileri
        for k in range(3):
            yy = y - 60 + k * 45
            d.line([(x - L - 30 - 90, yy), (x - L - 30, yy)], fill=(255, 255, 255, 150), width=5)


def _school(d, a, tl, s):
    p = P(CX, CY + 40, back(tl / 0.5))
    rect(d, p, -200, -60, 200, 170, (225, 205, 170, 255), (255, 255, 255, 255), 3)
    d.polygon(p.pts([(-230, -60), (0, -190), (230, -60)]), fill=RED + (255,), outline=(255, 255, 255, 255), width=3)
    circ(d, p, 0, -105, 30, fill=WHITE + (255,)); d.line([p(0, -105), p(0, -125)], fill=DARK + (255,), width=4)
    d.line([p(0, -105), p(14, -105)], fill=DARK + (255,), width=4)
    for wx in (-150, -80, 50, 120):
        rect(d, p, wx, -30, wx + 40, 20, (120, 180, 230, 255)); rect(d, p, wx, 60, wx + 40, 110, (120, 180, 230, 255))
    rect(d, p, -35, 70, 35, 170, (120, 70, 40, 255))
    # bayrak direği + dalgalanan bayrak
    d.line([p(160, -60), p(160, -260)], fill=(220, 220, 225, 255), width=6)
    pts = []
    for i in range(13):
        u = i / 12; xx = 160 + 120 * u; yy = -255 + 10 * math.sin(tl * 6 - u * 5) * u
        pts.append(p(xx, yy))
    for i in range(12, -1, -1):
        u = i / 12; xx = 160 + 120 * u; yy = -185 + 10 * math.sin(tl * 6 - u * 5) * u
        pts.append(p(xx, yy))
    d.polygon(pts, fill=RED + (255,))
    c = p(205, -220 + 10 * math.sin(tl * 6 - 1.9) * 0.4)
    d.ellipse((c[0] - 18, c[1] - 18, c[0] + 18, c[1] + 18), fill=WHITE + (255,))
    d.ellipse((c[0] - 10, c[1] - 16, c[0] + 22, c[1] + 16), fill=RED + (255,))
    st = s.get("stamp")
    if st and tl > 0.9:
        k = ease((tl - 0.9) / 0.25); sc = 1.8 - 0.8 * k
        f = font(fs(78 * sc), 700); tw = f.getlength(st)
        sp = P(CX, CY + 90, 1.0, math.radians(-12))
        d.polygon(sp.pts([(-tw / 2 - 26, -58 * sc), (tw / 2 + 26, -58 * sc), (tw / 2 + 26, 58 * sc), (-tw / 2 - 26, 58 * sc)]),
                  outline=RED + (int(255 * k),), width=8, fill=(255, 255, 255, int(200 * k)))
        d.text((CX, CY + 90), st, font=f, fill=RED + (int(255 * k),), anchor="mm")


def _water(d, a, tl, s):
    p = P(CX - 40, CY - 40, back(tl / 0.5))
    rect(d, p, -200, -60, 40, 10, (190, 195, 205, 255), (255, 255, 255, 255), 3)
    rect(d, p, 10, -60, 70, 90, (190, 195, 205, 255), (255, 255, 255, 255), 3)
    rect(d, p, -60, -110, -20, -60, (160, 165, 175, 255))
    hw = P(p(-40, -120)[0], p(-40, -120)[1], p.s, math.radians(tl * 40 if not s.get("cut") else 0))
    rect(d, hw, -70, -12, 70, 12, RED + (255,))
    tip = p(40, 95)
    cut = s.get("cut") and tl > 1.0
    if not cut:
        for j in range(3):
            ph = (tl * 1.3 + j / 3) % 1.0
            y = tip[1] + 250 * ph ** 1.6; rr = p.r(18)
            d.polygon([(tip[0], y - rr * 1.8), (tip[0] - rr, y), (tip[0] + rr, y)], fill=SKY + (230,))
            d.ellipse((tip[0] - rr, y - rr, tip[0] + rr, y + rr), fill=SKY + (230,))
    ry = tip[1] + 260
    for j in range(3):
        ph = (tl * 0.9 + j / 3) % 1.0
        rw = 30 + 140 * ph
        d.ellipse((tip[0] - rw, ry - rw * 0.25, tip[0] + rw, ry + rw * 0.25), outline=SKY + (int(200 * (1 - ph) * (0.3 if cut else 1)),), width=4)
    if cut:
        k = ease((tl - 1.0) / 0.3); r = 150 * k
        d.ellipse((CX - r, CY - r, CX + r, CY + r), outline=RED + (255,), width=18)
        d.line([(CX - r * 0.7, CY + r * 0.7), (CX + r * 0.7, CY - r * 0.7)], fill=RED + (255,), width=18)


def _gauge(d, a, tl, s):
    try:
        v, dec = tr_parse(s.get("value", 0))
    except Exception:
        v, dec = 0.0, 0
    v = max(0.0, min(100.0, v)); e = ease((tl - 0.2) / 1.4)
    r = 200
    d.ellipse((CX - r, CY - r - 20, CX + r, CY + r - 20), outline=(60, 64, 72, 255), width=40)
    col = RED if v < 35 else (YEL if v < 65 else GRN)
    if e > 0:
        d.arc((CX - r, CY - r - 20, CX + r, CY + r - 20), -90, -90 + 360 * v / 100 * e, fill=col + (255,), width=40)
    # su dalgası iç dolgu
    lvl = (CY + r - 60) - (2 * r - 80) * (v / 100) * e
    pts = [(CX - 150 + i * 10, lvl + 8 * math.sin(tl * 4 + i * 0.5)) for i in range(31)]
    poly = pts + [(CX + 150, CY + r - 60), (CX - 150, CY + r - 60)]
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).ellipse((CX - 155, CY - 175, CX + 155, CY + 135), fill=255)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).polygon(poly, fill=(40, 130, 230, 150))
    lay.putalpha(ImageChops.multiply(lay.getchannel("A"), m))
    d._image.alpha_composite(lay)
    txt = ("%" + tr_fmt(v * e, dec)) if e < 0.999 else ("%" + (str(s["value"]) if isinstance(s.get("value"), str) else tr_fmt(v, dec)))
    d.text((CX, CY - 20), txt, font=font(110, 700), fill=WHITE + (255,), anchor="mm")
    label_tag(d, s.get("label"), CY + 245)


def _football(d, a, tl, s):
    sc = s.get("score")
    if sc:
        teams = s.get("teams") or ["", ""]
        d.rounded_rectangle((CX - 250, CY - 250, CX + 250, CY - 140), radius=16, fill=(10, 10, 12, 240), outline=YEL + (255,), width=4)
        d.text((CX, CY - 195), sc.replace("-", " - "), font=font(70, 700), fill=YEL + (255,), anchor="mm")
        d.text((CX - 235, CY - 195), teams[0][:11], font=font(28, 700), fill=WHITE + (255,), anchor="lm")
        d.text((CX + 235, CY - 195), teams[1][:11] if len(teams) > 1 else "", font=font(28, 700), fill=WHITE + (255,), anchor="rm")
    # çim
    d.chord((CX - R + 6, CY - R + 6, CX + R - 6, CY + R - 6), 20, 160, fill=(40, 140, 60, 230))
    ph = (tl * 1.25) % 1.0; hgt = 230 * (1 - (2 * ph - 1) ** 2)
    by = CY + 150 - hgt; bx = CX + 60 * math.sin(tl * 1.3)
    sq = 1 - 0.18 * max(0, 1 - hgt / 30)
    sh = 1 - hgt / 300
    d.ellipse((bx - 70 * sh, CY + 205, bx + 70 * sh, CY + 225), fill=(0, 0, 0, 110))
    r = 72
    d.ellipse((bx - r / sq, by - r * sq, bx + r / sq, by + r * sq), fill=WHITE + (255,), outline=(20, 20, 24, 255), width=4)
    rot = tl * 4
    for k in range(5):
        aa = rot + k * 2 * math.pi / 5
        cx, cy = bx + math.cos(aa) * r * 0.62, by + math.sin(aa) * r * 0.62 * sq
        d.regular_polygon((cx, cy, r * 0.2), 5, rotation=math.degrees(aa), fill=(20, 20, 24, 255))
    d.regular_polygon((bx, by, r * 0.27), 5, rotation=math.degrees(rot), fill=(20, 20, 24, 255))


def _cone(d, x, y, s):
    d.polygon([(x - 50 * s, y), (x + 50 * s, y), (x + 12 * s, y - 150 * s), (x - 12 * s, y - 150 * s)], fill=(255, 120, 20, 255))
    d.polygon([(x - 34 * s, y - 45 * s), (x + 34 * s, y - 45 * s), (x + 27 * s, y - 75 * s), (x - 27 * s, y - 75 * s)], fill=WHITE + (255,))
    d.polygon([(x - 22 * s, y - 100 * s), (x + 22 * s, y - 100 * s), (x + 16 * s, y - 125 * s), (x - 16 * s, y - 125 * s)], fill=WHITE + (255,))
    d.rectangle((x - 66 * s, y - 6 * s, x + 66 * s, y + 10 * s), fill=(230, 100, 10, 255))


def _cones(d, a, tl, s):
    # bariyer
    k = ease((tl - 0.1) / 0.4)
    bx0, bx1, by = CX - 230, CX + 230, CY - 40
    d.rectangle((bx0 + 20, by, bx0 + 34, by + 150), fill=(200, 200, 205, int(255 * k)))
    d.rectangle((bx1 - 34, by, bx1 - 20, by + 150), fill=(200, 200, 205, int(255 * k)))
    d.rectangle((bx0, by - 50, bx1, by + 10), fill=WHITE + (int(255 * k),))
    for i in range(8):
        x = bx0 + i * 60
        d.polygon([(x, by + 10), (x + 30, by + 10), (x + 60, by - 50), (x + 30, by - 50)], fill=RED + (int(255 * k),))
    on = int(tl * 3) % 2 == 0
    for lx in (bx0 + 27, bx1 - 27):
        rr = 26 if on else 18
        d.ellipse((lx - rr, by - 80 - rr, lx + rr, by - 80 + rr), fill=(255, 190, 0, 255 if on else 120))
        if on: d.ellipse((lx - 50, by - 130, lx + 50, by - 30), fill=(255, 190, 0, 50))
    for i, x in enumerate((CX - 170, CX, CX + 170)):
        t = tl - 0.35 - i * 0.15
        if t < 0: continue
        drop = 200 * (1 - back(t / 0.4))
        _cone(d, x, CY + 230 - drop, 0.95)
    label_tag(d, s.get("label"), CY - 225)


def _wind(d, a, tl, s, full=True):
    rng = np.random.default_rng(21)
    for j in range(16):
        y0 = rng.uniform(260, 1000); sp = rng.uniform(0.7, 1.3); ln = rng.uniform(220, 420)
        x = ((rng.uniform(0, W) + tl * 900 * sp) % (W + ln * 2)) - ln
        pts = [(x + u, y0 + 18 * math.sin((x + u) / 90 + tl * 2)) for u in range(0, int(ln), 20)]
        if len(pts) > 1: d.line(pts, fill=(235, 240, 255, int(150 * sp)), width=int(4 * sp), joint="curve")
    for j in range(10):
        ph = (tl * 0.45 * rng.uniform(0.8, 1.2) + j / 10) % 1.0
        x = -60 + (W + 120) * ph; y = rng.uniform(300, 950) + 60 * math.sin(tl * 3 + j)
        aa = tl * 6 + j
        d.ellipse((x - 20, y - 9, x + 20, y + 9), fill=(120, 180, 70, 230)) if j % 2 else d.ellipse((x - 18, y - 8, x + 18, y + 8), fill=(220, 150, 40, 230))
        d.line([(x - math.cos(aa) * 22, y - math.sin(aa) * 8), (x + math.cos(aa) * 22, y + math.sin(aa) * 8)], fill=(60, 80, 30, 200), width=2)


_SNOW = None


def _snow(d, a, tl, s):
    global _SNOW
    if _SNOW is None:
        rng = np.random.default_rng(8); _SNOW = (rng.uniform(0, W, 170), rng.uniform(0, H, 170), rng.uniform(0.5, 1.4, 170))
    d.rectangle((0, 0, W, H), fill=(200, 215, 235, 30))
    for x, y, v in zip(*_SNOW):
        yy = (y + tl * 260 * v) % (H + 40) - 20; xx = (x + 40 * math.sin(tl * 1.5 + y)) % W
        r = 4 + 6 * v
        d.ellipse((xx - r, yy - r, xx + r, yy + r), fill=(255, 255, 255, int(150 + 80 * (v - 0.5))))


def _thermo(d, a, tl, s):
    try:
        f0, _ = tr_parse(s.get("from", s.get("to", 0))); f1, dec = tr_parse(s.get("to", 0))
    except Exception:
        f0, f1, dec = 0.0, 0.0, 0
    lo, hi = min(f0, f1) - 6, max(f0, f1) + 6
    e = ease((tl - 0.4) / 1.6); v = f0 + (f1 - f0) * e
    x, top, bot = CX - 60, CY - 230, CY + 130
    d.rounded_rectangle((x - 34, top, x + 34, bot), radius=34, fill=(235, 235, 240, 255), outline=(255, 255, 255, 255), width=4)
    d.ellipse((x - 70, bot - 30, x + 70, bot + 110), fill=(235, 235, 240, 255), outline=(255, 255, 255, 255), width=4)
    col = BLUE if f1 < f0 else RED
    lvl = bot - (bot - top - 30) * (v - lo) / (hi - lo)
    d.rectangle((x - 18, lvl, x + 18, bot + 10), fill=col + (255,))
    d.ellipse((x - 52, bot - 12, x + 52, bot + 92), fill=col + (255,))
    for i in range(7):
        yy = top + 30 + i * (bot - top - 40) / 6
        d.line([(x + 40, yy), (x + 62, yy)], fill=(220, 220, 225, 255), width=4)
    unit = s.get("unit", "°C")
    txt = (tr_fmt(v, dec) if e < 0.999 else str(s.get("to"))) + unit
    d.text((CX + 130, CY - 40), txt, font=font(100, 700), fill=WHITE + (255,), anchor="mm")
    if f1 != f0: arrow(d, CX + 130, CY + 90, "down" if f1 < f0 else "up", tl, 60) if f1 > f0 else _arrow_blue(d, CX + 130, CY + 90, tl)


def _arrow_blue(d, x, y, tl):
    bob = 10 * math.sin(tl * 5); y += bob; s = 60
    pts = [(x - s * 0.32, y - s * 0.5), (x + s * 0.32, y - s * 0.5), (x + s * 0.32, y), (x + s * 0.62, y), (x, y + s * 0.65), (x - s * 0.62, y), (x - s * 0.32, y)]
    d.polygon(pts, fill=SKY + (255,), outline=(255, 255, 255, 255), width=3)


def _calendar(d, a, tl, s):
    p = P(CX, CY, back(tl / 0.5), math.radians(-4 + 4 * ease(tl / 0.6)))
    rect(d, p, -170, -190, 170, 200, (250, 250, 252, 255), (255, 255, 255, 255), 3)
    rect(d, p, -170, -190, 170, -90, RED + (255,))
    for rx in (-100, 100):
        rect(d, p, rx - 12, -220, rx + 12, -160, (60, 60, 66, 255))
    d.text(p(0, -140), (s.get("month") or "").upper()[:8], font=font(fs(p.r(52)), 700), fill=WHITE + (255,), anchor="mm")
    k = ease((tl - 0.3) / 0.5)
    fp = P(CX, CY + p.r(-90) * 0 + 0, p.s)
    day = str(s.get("day", ""))
    d.text(p(0, 60), day, font=font(fs(p.r(190) * (0.6 + 0.4 * k)), 700), fill=(20, 20, 24, int(255 * k)), anchor="mm")
    if tl < 0.8:  # kalkan sayfa
        fl = 1 - ease(tl / 0.8)
        d.polygon(p.pts([(-170, -90), (170, -90), (170, -90 + 290 * fl), (-170, -90 + 290 * fl * 0.85)]), fill=(225, 225, 230, 255))
    label_tag(d, s.get("label"), CY + 250)


def _megaphone(d, a, tl, s):
    p = P(CX - 60, CY - 20, back(tl / 0.5), math.radians(-12 + 3 * math.sin(tl * 4)))
    d.polygon(p.pts([(-120, -40), (60, -130), (60, 130), (-120, 40)]), fill=YEL + (255,), outline=(255, 255, 255, 255), width=4)
    rect(d, p, -170, -45, -115, 45, RED + (255,))
    rect(d, p, -110, 40, -70, 130, (60, 60, 66, 255))
    d.ellipse(p.box(45, -130, 85, 130), fill=(230, 180, 0, 255))
    o = p(90, 0)
    for j in range(3):
        ph = (tl * 1.1 + j / 3) % 1.0
        rr = 60 + 170 * ph
        d.arc((o[0] - rr, o[1] - rr, o[0] + rr, o[1] + rr), -40 - 12, 40 - 12, fill=WHITE + (int(255 * (1 - ph)),), width=10)
    label_tag(d, s.get("label"), CY + 250)


def _quake(d, a, tl, s):
    sh = 10 * math.sin(tl * 40) * max(0, 1 - ((tl - 0.6) % 2.4) / 0.8) if tl > 0.6 else 0
    y0 = CY + 40
    pts = []
    for i in range(0, 2 * R - 60, 6):
        x = CX - R + 30 + i
        u = (i + tl * 300) / 40
        burst = max(0, 1 - abs(((x - CX) + tl * 300) % 700 - 350) / 120)
        amp = 6 + 130 * burst * abs(math.sin(u * 3.1))
        pts.append((x, y0 + amp * math.sin(u * 5.3)))
    d.line(pts, fill=(255, 90, 80, 255), width=5)
    d.line([(CX - R + 30, y0), (CX + R - 30, y0)], fill=(255, 255, 255, 60), width=2)
    # sarsılan ev simgesi
    hx = CX + sh; hy = CY - 150
    d.polygon([(hx - 80, hy), (hx, hy - 70), (hx + 80, hy)], fill=WHITE + (255,))
    d.rectangle((hx - 62, hy, hx + 62, hy + 80), fill=WHITE + (255,))
    d.rectangle((hx - 16, hy + 30, hx + 16, hy + 80), fill=DARK + (255,))
    if s.get("mag"):
        d.text((CX, CY + 200), "M " + str(s["mag"]), font=font(80, 700), fill=YEL + (255,), anchor="mm")


def _house(d, a, tl, s):
    p = P(CX - 40, CY + 20, back(tl / 0.5))
    d.polygon(p.pts([(-200, -40), (0, -200), (200, -40)]), fill=RED + (255,), outline=(255, 255, 255, 255), width=4)
    rect(d, p, -165, -40, 165, 170, (245, 240, 230, 255), (255, 255, 255, 255), 3)
    rect(d, p, -40, 60, 40, 170, (120, 70, 40, 255))
    for wx in (-130, 70):
        rect(d, p, wx, 0, wx + 60, 60, (120, 180, 230, 255))
    rect(d, p, 100, -170, 140, -90, (130, 130, 138, 255))
    k = P(CX + 190, CY + 160, 1.0, math.radians(-30 + 60 * ease((tl - 0.5) / 0.6) + 5 * math.sin(tl * 3)))
    circ(d, k, 0, 0, 48, fill=YEL + (255,), outline=(255, 255, 255, 255), w=4); circ(d, k, 0, 0, 18, fill=DARK + (255,))
    rect(d, k, 40, -12, 160, 12, YEL + (255,)); rect(d, k, 120, 12, 135, 40, YEL + (255,)); rect(d, k, 145, 12, 160, 32, YEL + (255,))
    label_tag(d, s.get("label"), CY + 255)


def _hospital(d, a, tl, s):
    p = P(CX, CY - 40, back(tl / 0.5))
    rect(d, p, -190, -120, 190, 150, (245, 245, 250, 255), (255, 255, 255, 255), 3)
    for wx in (-160, -100, 60, 120):
        rect(d, p, wx, -90, wx + 40, -40, (120, 180, 230, 255)); rect(d, p, wx, 20, wx + 40, 70, (120, 180, 230, 255))
    rect(d, p, -40, 70, 40, 150, (120, 180, 230, 255))
    pul = 1 + 0.12 * max(0, math.sin(tl * 7)) ** 8
    q = P(CX, CY - 220, pul)
    rect(d, q, -70, -24, 70, 24, RED + (255,)); rect(d, q, -24, -70, 24, 70, RED + (255,))
    y = CY + 190; pts = []
    for i in range(0, 520, 8):
        x = CX - 260 + i; u = ((i - tl * 260) % 260)
        dy = -90 if 120 < u < 130 else (60 if 130 <= u < 140 else (-20 if 110 < u <= 120 else 0))
        pts.append((x, y + dy))
    d.line(pts, fill=GRN + (255,), width=6)
    label_tag(d, s.get("label"), CY + 270)


def _factory(d, a, tl, s):
    p = P(CX, CY + 40, back(tl / 0.5))
    rect(d, p, -220, 0, 220, 170, (130, 135, 145, 255), (255, 255, 255, 255), 3)
    d.polygon(p.pts([(-220, 0), (-220, -80), (-110, 0), (-110, -80), (0, 0), (0, -80), (110, 0)]), fill=(150, 155, 165, 255))
    rect(d, p, 130, -230, 180, 0, (110, 70, 60, 255))
    for wx in (-190, -110, -30, 50):
        rect(d, p, wx, 50, wx + 50, 100, YEL + (255,) if int(tl * 2 + wx) % 3 else (255, 230, 140, 255))
    top = p(155, -235)
    for j in range(7):
        ph = (tl * 0.5 + j / 7) % 1.0; r = 20 + 55 * ph
        d.ellipse((top[0] + 90 * ph - r, top[1] - 200 * ph - r, top[0] + 90 * ph + r, top[1] - 200 * ph + r), fill=(200, 200, 205, int(170 * (1 - ph))))
    label_tag(d, s.get("label"), CY + 260)


def _ship(d, a, tl, s):
    bob = 10 * math.sin(tl * 2.2); x = CX - 200 + 200 * ease(tl / 1.4) + 8 * math.sin(tl)
    p = P(x, CY + 40 + bob, 1.0, math.radians(2 * math.sin(tl * 2)))
    d.polygon(p.pts([(-230, 0), (230, 0), (180, 90), (-200, 90)]), fill=RED + (255,), outline=(255, 255, 255, 255), width=4)
    rect(d, p, -150, -80, 130, 0, (245, 245, 250, 255)); rect(d, p, -90, -140, 70, -80, (245, 245, 250, 255))
    for wx in range(-130, 120, 45):
        circ(d, p, wx + 15, -40, 13, fill=(120, 180, 230, 255))
    rect(d, p, 80, -210, 115, -140, YEL + (255,))
    for j in range(3):
        yy = CY + 140 + j * 35
        pts = [(CX - R + 30 + i, yy + 12 * math.sin(i / 40 + tl * 3 + j)) for i in range(0, 2 * R - 60, 10)]
        d.line(pts, fill=SKY + (230 - j * 50,), width=8)
    label_tag(d, s.get("label"), CY + 260)


TYPES = {"fuel": _fuel, "price": _price, "coins": _coins, "bus": _bus, "tram": lambda d, a, tl, s: _bus(d, a, tl, s, True),
         "school": _school, "water": _water, "gauge": _gauge, "football": _football, "cones": _cones, "wind": _wind,
         "snow": _snow, "thermo": _thermo, "calendar": _calendar, "megaphone": _megaphone, "quake": _quake,
         "house": _house, "hospital": _hospital, "factory": _factory, "ship": _ship}
FULL = {"wind", "snow"}   # zemin dairesi olmadan tüm ekrana yayılanlar


def anim_layer(sc, tl):
    items = sc.get("anim")
    if isinstance(items, dict): items = [items]
    o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
    if not items: return o
    if sc.get("_static"):
        tl += 2.2   # kapak sahnesi: 0. karede simge tam açılmış ve sayılar son değerinde görünür
    if any(it.get("type") not in FULL for it in items):
        backdrop(d, tl)
    for it in items:
        fn = TYPES.get(it.get("type"))
        if fn: fn(d, 1.0, tl, it)
    return o
