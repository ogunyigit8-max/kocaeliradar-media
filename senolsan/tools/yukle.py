"""Yerel dosyayi Kie'nin gecici deposuna yukler, herkese acik adresini yazar (Instagram paylasimi icin).
Kullanim: python3 tools/yukle.py bolumler/b02/b02.mp4"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import anahtar, istek, cok_parcali


def yukle(yol, klasor="videos/senolsan"):
    govde, tur = cok_parcali({"uploadPath": klasor, "fileName": os.path.basename(yol)}, {"file": yol})
    r = istek("https://kieai.redpandaai.co/api/file-stream-upload", govde,
              {"Authorization": f"Bearer {anahtar('KIE_API_KEY')}", "Content-Type": tur})
    if not r.get("success"):
        raise RuntimeError(f"Yukleme basarisiz: {r}")
    return r["data"]["downloadUrl"]


if __name__ == "__main__":
    print(yukle(sys.argv[1]))
