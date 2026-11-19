"""Ortak yardimcilar: anahtarlar ortam degiskenlerinden okunur (KIE_API_KEY, ELEVENLABS_API_KEY).
Anahtarlar ASLA dosyaya, depoya ya da ekrana yazilmaz."""
import json, os, sys, time, urllib.request, urllib.error, uuid, mimetypes

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # senolsan/


def anahtar(ad):
    v = os.environ.get(ad, "").strip().strip('"')
    # Bulut ortaminda anahtari ag vekili (proxy) istege kendisi ekler; degisken yoksa yer tutucu gonder.
    return v or "proxy-tarafindan-eklenir"


def istek(url, veri=None, basliklar=None, yontem=None, ham=False, deneme=3):
    basliklar = dict(basliklar or {})
    govde = None
    if veri is not None and not isinstance(veri, (bytes, bytearray)):
        govde = json.dumps(veri, ensure_ascii=False).encode("utf-8")
        basliklar.setdefault("Content-Type", "application/json")
    elif veri is not None:
        govde = veri
    son_hata = None
    for i in range(deneme):
        try:
            req = urllib.request.Request(url, data=govde, headers=basliklar, method=yontem or ("POST" if govde is not None else "GET"))
            with urllib.request.urlopen(req, timeout=300) as r:
                b = r.read()
                return b if ham else json.loads(b.decode("utf-8"))
        except urllib.error.HTTPError as e:
            son_hata = f"HTTP {e.code}: {e.read()[:500]!r}"
            if e.code < 500 and e.code != 429:
                break
        except Exception as e:  # ag hatasi
            son_hata = repr(e)
        time.sleep(5 * (i + 1))
    raise RuntimeError(f"Istek basarisiz ({url.split('?')[0]}): {son_hata}")


def cok_parcali(alanlar, dosyalar):
    """multipart/form-data govdesi. alanlar: {ad: deger}, dosyalar: {ad: yol}"""
    sinir = uuid.uuid4().hex
    parcalar = []
    for k, v in alanlar.items():
        parcalar.append(f"--{sinir}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode("utf-8"))
    for k, yol in dosyalar.items():
        ad = os.path.basename(yol)
        tur = mimetypes.guess_type(ad)[0] or "application/octet-stream"
        with open(yol, "rb") as f:
            icerik = f.read()
        parcalar.append(f"--{sinir}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{ad}\"\r\nContent-Type: {tur}\r\n\r\n".encode("utf-8") + icerik + b"\r\n")
    parcalar.append(f"--{sinir}--\r\n".encode("utf-8"))
    return b"".join(parcalar), f"multipart/form-data; boundary={sinir}"


def json_oku(yol):
    with open(yol, encoding="utf-8") as f:
        return json.load(f)


def json_yaz(yol, veri):
    os.makedirs(os.path.dirname(yol) or ".", exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)
