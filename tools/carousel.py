"""Kocaeli Radar liste karuseli üretici (Instagram karusel, 1080x1350 JPEG + 1080x1920 hikâye kapağı).

Neden: günlük planlı kesinti listesi Reels olarak her gün tekrarlanınca erişimi düştü (9,1 bin -> 1,9 bin).
Liste tipi servis bilgisi karuselde aranabilir, kaydedilebilir ve "gönder" ile paylaşılır (kullanıcı onayı 19.11.2026).

Kullanım:  python3 tools/carousel.py karusel.json
karusel.json:
{
  "out_dir": "c/2026-11-20-elektrik",          # depoda; 4 günden eskiler silinir
  "category": "ELEKTRİK KESİNTİSİ",            # üst bant
  "date": "20 Kasım 2026 Cuma",
  "title": "Bugün 7 ilçede elektrik kesintisi",  # kapak büyük başlık (ilçe/sayı önde, ≤ ~40 karakter)
  "highlight": "En uzun: Dilovası'nda 8 saat",   # kapakta sarı bant (en çarpıcı bilgi)
  "focus": [lat, lon], "zoom": 1.3,              # isteğe bağlı kapak haritası odağı
  "pins": [["DİLOVASI", 40.78, 29.53]],          # isteğe bağlı kapak pinleri
  "groups": [ {"name": "GEBZE", "items": [["Arapçeşme, Sultan Orhan", "09.00-17.00"], ...]}, ... ],
  "note": "Arıza bildirimi: SEDAŞ 186",          # son karede
  "source": "Kaynak: SEDAŞ · 20 Kasım 2026"
}
Çıktı: out_dir/01.jpg (kapak), 02..NN.jpg (liste), son kare (kaydet/gönder/takip), out_dir/story.jpg (9:16).
Karusel en fazla 10 kare: liste 8 kareyi aşarsa son satırlar "… ve N adres daha (tam liste: SEDAŞ)" olur.
Paylaşım: Windsor.ai execute_action(action "create_carousel_post", params {"image_urls": [raw URL'ler], "caption"}).
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from stories import font, YEL, RED, WHITE, GREY  # noqa: E402

CW, CH = 1080, 1350
BG = (18, 20, 24)
PANEL = (30, 33, 38)
MARGIN = 72
ROW_H = 74
LIST_TOP = 300
LIST_BOTTOM = 1170
MAX_SLIDES = 10


def tr_upper(s):
    return s.replace("i", "İ").replace("ı", "I").upper()


def arrow(d, x, y, s, col):
    """Sağa ok (fontta → glifi yok)."""
    d.rectangle((x, y - s * 0.12, x + s * 0.6, y + s * 0.12), fill=col)
    d.polygon([(x + s * 0.5, y - s * 0.42), (x + s, y), (x + s * 0.5, y + s * 0.42)], fill=col)


def count_names(items):
    """Benzersiz mahalle sayısı (aynı mahalle farklı saatlerde tekrar edebilir)."""
    return len({p.strip() for n, _ in items for p in n.replace(" ve ", ",").split(",") if p.strip()})


def span(hours):
    """Saat aralıklarından en erken başlangıç - en geç bitiş ("09.00-12.00", "14.00-17.00" -> "09.00-17.00")."""
    hs = [h.replace(" ", "") for h in hours if h and "-" in h]
    if not hs:
        return ""
    a = min(h.split("-")[0] for h in hs); b = max(h.split("-")[1] for h in hs)
    return f"{a}-{b}"


def wrap(s, f, maxw):
    out, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if f.getlength(t) <= maxw or not cur:
            cur = t
        else:
            out.append(cur); cur = w
    if cur: out.append(cur)
    return out


def map_bg(focus, zoom, pins, w, h):
    try:
        import news
        m = news.build_map()
        la, lo = focus or (40.79, 29.75)
        cx, cy = news.ll2px(la, lo)
        sw, sh = w / zoom, h / zoom
        crop = m.crop((int(cx - sw / 2), int(cy - sh / 2), int(cx + sw / 2), int(cy + sh / 2))).resize((w, h), Image.LANCZOS)
        d = ImageDraw.Draw(crop)
        for lab, pla, plo in pins or []:
            px, py = news.ll2px(pla, plo)
            x = (px - (cx - sw / 2)) * zoom; y = (py - (cy - sh / 2)) * zoom
            d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=RED, outline=WHITE, width=4)
            f = font(34, 600); tw = f.getlength(lab)
            lx = x + 22 if x + 42 + tw < w - 20 else x - 42 - tw
            d.rectangle((lx, y - 26, lx + 20 + tw, y + 26), fill=(10, 10, 12))
            d.rectangle((lx, y + 26, lx + 20 + tw, y + 31), fill=YEL)
            d.text((lx + 10, y), lab, font=f, fill=WHITE, anchor="lm")
        return crop
    except Exception:
        return Image.new("RGB", (w, h), BG)


def header(d, cat, page, total):
    d.rectangle((0, 0, CW, 10), fill=YEL)
    d.rectangle((MARGIN, 56, MARGIN + 8, 112), fill=YEL)
    d.text((MARGIN + 26, 84), "KOCAELİ RADAR", font=font(46, 700), fill=WHITE, anchor="lm")
    f = font(30, 600); tw = f.getlength(cat)
    d.rectangle((CW - MARGIN - tw - 36, 60, CW - MARGIN, 108), fill=RED)
    d.text((CW - MARGIN - 18, 84), cat, font=f, fill=WHITE, anchor="rm")
    if total:
        d.text((CW - MARGIN, CH - 60), f"{page}/{total}", font=font(30, 500), fill=GREY, anchor="rm")


def footer(d, source):
    d.text((MARGIN, CH - 60), source, font=font(28, 400), fill=GREY, anchor="lm")


def cover(spec, total):
    im = map_bg(spec.get("focus"), spec.get("zoom", 1.2), spec.get("pins"), CW, CH)
    # okunurluk için alt ve üst karartma
    sh = Image.new("L", (CW, CH), 0); sd = ImageDraw.Draw(sh)
    for y in range(CH):
        a = 150 if y < 180 else int(70 + 185 * max(0, (y - 420) / (CH - 420)))
        sd.line((0, y, CW, y), fill=min(235, a))
    im = Image.composite(Image.new("RGB", (CW, CH), (8, 9, 11)), im, sh)
    d = ImageDraw.Draw(im)
    header(d, spec["category"], 1, total)
    d.text((MARGIN, 760), tr_upper(spec["date"]), font=font(36, 500), fill=YEL, anchor="ls")
    f = font(96, 700); lines = wrap(tr_upper(spec["title"]), f, CW - 2 * MARGIN)
    if len(lines) > 3:
        f = font(80, 700); lines = wrap(tr_upper(spec["title"]), f, CW - 2 * MARGIN)
    y = 800
    for ln in lines:
        d.text((MARGIN + 3, y + 3), ln, font=f, fill=(0, 0, 0), anchor="la")
        d.text((MARGIN, y), ln, font=f, fill=WHITE, anchor="la"); y += int(f.size * 1.12)
    if spec.get("highlight"):
        fh = font(42, 600); hl = wrap(spec["highlight"], fh, CW - 2 * MARGIN - 40)[:2]
        y += 20
        for ln in hl:
            tw = fh.getlength(ln)
            d.rectangle((MARGIN, y, MARGIN + tw + 40, y + 64), fill=YEL)
            d.text((MARGIN + 20, y + 32), ln, font=fh, fill=(12, 12, 14), anchor="lm"); y += 72
    d.text((CW - MARGIN - 70, CH - 130), "MAHALLEN LİSTEDE Mİ?  KAYDIR", font=font(40, 700), fill=YEL, anchor="rm")
    arrow(d, CW - MARGIN - 52, CH - 130, 52, YEL)
    footer(d, spec.get("source", ""))
    return im


def summary_slide(spec, page, total):
    """2. kare kendi başına anlaşılır olmalı (Instagram geçilen karuseli 2. kareyle yeniden gösterebilir)."""
    im = Image.new("RGB", (CW, CH), BG); d = ImageDraw.Draw(im)
    header(d, spec["category"], page, total)
    d.text((MARGIN, 190), spec.get("summary_title", "Kısaca: hangi ilçede ne kadar?"), font=font(58, 700), fill=WHITE, anchor="lm")
    d.text((MARGIN, 252), spec["date"], font=font(36, 500), fill=GREY, anchor="lm")
    gs = spec["groups"]; n = len(gs)
    rh = min(118, (1180 - 320) // max(1, n))
    y = 320
    for g in gs:
        cnt = count_names(g["items"])
        hours = sorted({h for _, h in g["items"] if h})
        d.rectangle((MARGIN, y, CW - MARGIN, y + rh - 14), fill=PANEL)
        d.rectangle((MARGIN, y, MARGIN + 10, y + rh - 14), fill=YEL)
        cy = y + (rh - 14) / 2
        d.text((MARGIN + 34, cy), tr_upper(g["name"]), font=font(int(min(54, (rh - 14) * 0.62)), 700), fill=YEL, anchor="lm")
        d.text((CW / 2 - 40, cy), f"{cnt} mahalle", font=font(int(min(42, (rh - 14) * 0.55)), 500), fill=WHITE, anchor="lm")
        d.text((CW - MARGIN - 24, cy), span(hours),
               font=font(int(min(42, (rh - 14) * 0.55)), 600), fill=WHITE, anchor="rm")
        y += rh
    footer(d, spec.get("source", ""))
    return im


def paginate(groups):
    """Grupları kareye sığdır: (grup adı, [satırlar]) listelerinden kareler. Satır = (mahalle, saat)."""
    fn = font(40, 500); maxw = CW - 2 * MARGIN - 300
    rows = []
    for g in groups:
        rows.append(("H", tr_upper(g["name"])))
        for name, hours in g["items"]:
            for i, ln in enumerate(wrap(name, fn, maxw)):
                rows.append(("R", ln, hours if i == 0 else ""))
    cap = (LIST_BOTTOM - LIST_TOP) // ROW_H
    n = -(-len(rows) // cap)
    cap = min(cap, -(-len(rows) // max(1, n)) + 1)  # kareleri dengeli doldur (son kare boş kalmasın)
    slides, cur, last_h = [], [], None
    for r in rows:
        if r[0] == "H": last_h = r[1]
        if len(cur) >= cap or (r[0] == "H" and len(cur) >= cap - 1):
            slides.append(cur); cur = []
            if r[0] == "R": cur.append(("H", last_h + " (devam)"))
        cur.append(r)
    if cur: slides.append(cur)
    return slides


def list_slide(rows, spec, page, total):
    im = Image.new("RGB", (CW, CH), BG); d = ImageDraw.Draw(im)
    header(d, spec["category"], page, total)
    d.text((MARGIN, 190), spec.get("list_title", "Mahalle mahalle liste"), font=font(52, 700), fill=WHITE, anchor="lm")
    d.text((MARGIN, 248), spec["date"], font=font(34, 500), fill=GREY, anchor="lm")
    y = LIST_TOP; odd = False
    for r in rows:
        if r[0] == "H":
            d.rectangle((MARGIN, y + 8, CW - MARGIN, y + ROW_H - 6), fill=PANEL)
            d.rectangle((MARGIN, y + 8, MARGIN + 10, y + ROW_H - 6), fill=YEL)
            d.text((MARGIN + 32, y + ROW_H / 2 + 1), r[1], font=font(44, 700), fill=YEL, anchor="lm"); odd = False
        else:
            if odd: d.rectangle((MARGIN, y, CW - MARGIN, y + ROW_H), fill=(23, 25, 30))
            d.text((MARGIN + 32, y + ROW_H / 2), r[1], font=font(40, 500), fill=WHITE, anchor="lm")
            if r[2]: d.text((CW - MARGIN - 20, y + ROW_H / 2), r[2], font=font(40, 600), fill=WHITE, anchor="rm")
            odd = not odd
        y += ROW_H
    footer(d, spec.get("source", ""))
    return im


def end_slide(spec, page, total):
    im = Image.new("RGB", (CW, CH), BG); d = ImageDraw.Draw(im)
    header(d, spec["category"], page, total)
    y = 330
    for big, small in [("GÖNDER", "Listede mahallesi olan birine"), ("KAYDET", "Gün içinde tekrar bakmak için"),
                       ("TAKİP ET", "Kocaeli'deki gelişmeleri kaçırma")]:
        d.text((MARGIN, y), big, font=font(92, 700), fill=YEL if big != "TAKİP ET" else RED, anchor="la")
        d.text((MARGIN, y + 112), small, font=font(42, 400), fill=WHITE, anchor="la"); y += 240
    if spec.get("note"):
        f = font(44, 600); tw = f.getlength(spec["note"])
        d.rectangle((MARGIN, 1080, MARGIN + tw + 40, 1150), fill=PANEL)
        d.text((MARGIN + 20, 1115), spec["note"], font=f, fill=WHITE, anchor="lm")
    footer(d, spec.get("source", ""))
    return im


def story(cov):
    st = Image.new("RGB", (1080, 1920), BG)
    blur = cov.resize((1080, 1920)).filter(ImageFilter.GaussianBlur(30))
    st.paste(Image.eval(blur, lambda v: int(v * 0.45)))
    st.paste(cov, (0, 285))
    return st


def main(p):
    spec = json.load(open(p, encoding="utf-8"))
    out = spec["out_dir"]; os.makedirs(out, exist_ok=True)
    slides = paginate(spec["groups"])
    if len(slides) > MAX_SLIDES - 3:
        rest = sum(1 for s in slides[MAX_SLIDES - 3:] for r in s if r[0] == "R")
        slides = slides[:MAX_SLIDES - 3]
        slides[-1] = slides[-1][:-1] + [("R", f"… ve {rest} satır daha (tam liste kaynakta)", "")]
    total = len(slides) + 3
    ims = ([cover(spec, total), summary_slide(spec, 2, total)]
           + [list_slide(s, spec, i + 3, total) for i, s in enumerate(slides)] + [end_slide(spec, total, total)])
    files = []
    for i, im in enumerate(ims, 1):
        f = os.path.join(out, f"{i:02d}.jpg"); im.save(f, "JPEG", quality=92, optimize=True); files.append(f)
    story(ims[0]).save(os.path.join(out, "story.jpg"), "JPEG", quality=92, optimize=True)
    for f in files + [os.path.join(out, "story.jpg")]:
        assert os.path.getsize(f) < 8 * 1024 * 1024, f
    print(json.dumps({"slides": files, "story": os.path.join(out, "story.jpg")}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
