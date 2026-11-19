"""Kie nano-banana-2 ile resim uretir.
Tek resim:  python3 tools/gorsel.py --prompt "..." --cikti bolumler/b02/cekimler/01.png [--oran 9:16] [--ref karakter/karakter_sayfasi.png]
Toplu (paralel): python3 tools/gorsel.py --toplu bolumler/b02/cekimler.json
  cekimler.json: [{"prompt": "...", "cikti": "bolumler/b02/cekimler/01.png"}, ...]  (hepsine karakter sayfasi referans verilir)"""
import argparse, base64, json, os, sys, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import anahtar, istek, KOK

API = "https://api.kie.ai/api/v1/jobs"
# Depo herkese acik: depodaki dosyalar referans olarak bu adresten verilir (yukleme gerekmez).
RAW = "https://raw.githubusercontent.com/ogunyigit8-max/kocaeliradar-media/main/senolsan/"


def _h():
    return {"Authorization": f"Bearer {anahtar('KIE_API_KEY')}"}


def ref_yukle(yol):
    """Depoda (push edilmis) bir dosyaysa acik GitHub adresini dondurur; degilse Kie'ye yukler."""
    tam = os.path.abspath(yol)
    if tam.startswith(KOK + os.sep):
        url = RAW + os.path.relpath(tam, KOK).replace(os.sep, "/")
        try:
            istek(url, ham=True, deneme=1)
            return url
        except Exception:
            pass
    with open(yol, "rb") as f:
        b = f.read()
    mime = "image/png" if b[:1] == b"\x89" else "image/jpeg"
    r = istek("https://kieai.redpandaai.co/api/file-base64-upload",
              {"base64Data": f"data:{mime};base64," + base64.b64encode(b).decode(), "uploadPath": "images/user-uploads",
               "fileName": os.path.basename(yol)}, _h())
    if not r.get("success"):
        raise RuntimeError(f"Referans yuklenemedi: {r}")
    return r["data"]["downloadUrl"]


def uret(prompt, cikti, oran="9:16", refler=()):
    inp = {"prompt": prompt, "aspect_ratio": oran}
    if refler:
        inp["image_input"] = list(refler)
    r = istek(f"{API}/createTask", {"model": "nano-banana-2", "input": inp}, _h())
    if r.get("code") != 200:
        raise RuntimeError(f"Gorev acilamadi: {r}")
    tid = r["data"]["taskId"]
    for _ in range(120):
        time.sleep(5)
        s = istek(f"{API}/recordInfo?taskId={tid}", basliklar=_h())["data"]
        if s["state"] == "success":
            url = json.loads(s["resultJson"])["resultUrls"][0]
            os.makedirs(os.path.dirname(cikti) or ".", exist_ok=True)
            with open(cikti, "wb") as f:
                f.write(istek(url, ham=True))
            return cikti
        if s["state"] == "fail":
            raise RuntimeError(f"Basarisiz: {s.get('failMsg')}")
    raise RuntimeError("Zaman asimi")


if __name__ == "__main__":
    os.chdir(KOK)
    a = argparse.ArgumentParser()
    a.add_argument("--prompt"); a.add_argument("--cikti"); a.add_argument("--oran", default="9:16")
    a.add_argument("--ref", action="append", default=[]); a.add_argument("--toplu")
    g = a.parse_args()
    if g.toplu:
        isler = json.load(open(g.toplu, encoding="utf-8"))
        ref = [ref_yukle("karakter/karakter_sayfasi.png")]
        def tek(x):
            try:
                return uret(x["prompt"], x["cikti"], x.get("oran", "9:16"), ref) + " TAMAM"
            except Exception as e:
                return f"{x['cikti']} HATA {e}"
        with ThreadPoolExecutor(6) as ex:
            for s in ex.map(tek, isler):
                print(s)
    else:
        refler = [r if r.startswith("http") else ref_yukle(r) for r in g.ref]
        print(uret(g.prompt, g.cikti, g.oran, refler))
