"""Şehir ayarı: hangi hesap için üretim yapılacağını seçer.

RADAR_CITY ortam değişkeni (varsayılan "kocaeli") -> tools/cities/<ad>.json
Örnek:  RADAR_CITY=beyoglu python3 tools/news.py beyoglu/v/haber.json
Kocaeli için hiçbir şey ayarlamaya gerek yok; çıktı eskisiyle birebir aynıdır.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = os.environ.get("RADAR_CITY", "kocaeli").strip().lower() or "kocaeli"
CFG = json.load(open(os.path.join(HERE, "cities", NAME + ".json"), encoding="utf-8"))

CITY = CFG["name"]                      # ekrandaki şehir adı, ör. "KOCAELİ"
BRAND = CFG["brand"]                    # ör. "KOCAELİ RADAR"
HANDLE = CFG["handle"]                  # ör. "@kocaeliradar41"
ACCENT = tuple(CFG.get("accent", [255, 204, 0]))
MAP = CFG["map"]
DEFAULT_FOCUS = CFG["default_focus"]
DIR = CFG.get("dir", "")                # çıktı kökü: "" (Kocaeli: v/, s/, c/) veya "beyoglu" (beyoglu/v/ ...)
DISTRICTS = CFG["districts"]            # kutlama/özel gün videolarındaki 12 çip
DISTRICTS_LABEL = CFG["districts_label"]  # ör. "12 İLÇE"
WHERE_Q = CFG["where_q"]                # kutlama sorusu, iki satır


def asset(fn):
    """Şehre özel varlık (tools/assets/<şehir>/fn) varsa onu, yoksa ortak tools/assets/fn'i döndürür."""
    p = os.path.join(HERE, "assets", NAME, fn)
    return p if os.path.exists(p) else os.path.join(HERE, "assets", fn)
