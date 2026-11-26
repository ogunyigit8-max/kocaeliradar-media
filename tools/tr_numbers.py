"""TTS öncesi Türkçe metin normalleştirme: rakamları BÜTÜN sayı olarak yazıya çevirir.

Neden: TTS bazen "100"ü "bir sıfır sıfır" diye tek tek okuyor. Bu betik
"D-100" -> "Deyüz", "1000" -> "bin", "71,60 TL" -> "yetmiş bir lira altmış kuruş",
"%109" -> "yüzde yüz dokuz", "17.30" -> "on yedi otuz" yapar.

Kullanım (her seslendirme cümlesi için, audio_synthesize'dan ÖNCE):
    python3 tools/tr_numbers.py "Gebze'de D-100'de kaza: 19 yaralı"
    -> Gebze'de D yüz'de kaza: on dokuz yaralı
Altyazı (narr) metninde rakamlar kalır; yalnızca TTS metni çevrilir.

Ses seçimi (ay adı telaffuzu sese göre değişir): --ses emre|aylin
    python3 tools/tr_numbers.py --ses aylin "26 Kasım"
Verilmezse RADAR_CITY'ye göre state/voice.json (veya <şehir>/state/voice.json) "next" sesi kullanılır
(görevler seslendirme sırasında "next" sesiyle konuşur, next'i video bitince günceller).
"Kasım": Emre'de "Kâsım" (kullanıcı 25.11.2026 örnek 2), Aylin'de olduğu gibi "Kasım"
(kullanıcı 26.11.2026: Aylin'de Kâsım yanlış okunuyordu, örnek 1 seçildi).
"""
import re
import sys

BIR = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
ON = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
BUYUK = [(10**12, "trilyon"), (10**9, "milyar"), (10**6, "milyon"), (1000, "bin")]


def _uc(n):
    """0-999"""
    y, r = divmod(n, 100)
    o, b = divmod(r, 10)
    s = []
    if y:
        s.append(("" if y == 1 else BIR[y] + " ") + "yüz")
    if o:
        s.append(ON[o])
    if b:
        s.append(BIR[b])
    return " ".join(s)


def sayi(n):
    """Tam sayıyı Türkçe yazıya çevirir: 1000 -> bin, 2026 -> iki bin yirmi altı."""
    n = int(n)
    if n == 0:
        return "sıfır"
    if n < 0:
        return "eksi " + sayi(-n)
    parts = []
    for v, ad in BUYUK:
        if n >= v:
            k, n = divmod(n, v)
            parts.append(ad if (v == 1000 and k == 1) else _uc(k) + " " + ad)
    if n:
        parts.append(_uc(n))
    return " ".join(parts)


HARF = {"A": "a", "B": "be", "C": "ce", "Ç": "çe", "D": "de", "E": "e", "F": "fe", "G": "ge", "H": "he",
        "I": "ı", "İ": "i", "J": "je", "K": "ke", "L": "le", "M": "me", "N": "ne", "O": "o", "Ö": "ö",
        "P": "pe", "R": "re", "S": "se", "Ş": "şe", "T": "te", "U": "u", "Ü": "ü", "V": "ve", "Y": "ye", "Z": "ze"}


def _kod(k):
    """Yol kodu harflerini Türkçe okunuşla yaz: D -> de, TEM -> TEM (3 harf kısaltma olduğu gibi)."""
    return " ".join(HARF.get(c, c) for c in k) if len(k) <= 2 else k


def _yol(m):
    """D-100 -> "Deyüz" (tek kelime; ayrı yazınca TTS harften sonra duraksıyor), TEM-2 -> "TEM iki"."""
    k, n = m.group(1), sayi(int(m.group(2)))
    if len(k) == 1 and k in HARF:
        return HARF[k].capitalize() + n
    return _kod(k) + " " + n


def _int(s):
    return int(s.replace(".", ""))


def _ondalik(tam, kesir):
    """71,60 -> yetmiş bir virgül altmış ; 3,5 -> üç virgül beş"""
    kesir = kesir.rstrip("0") or "0"
    if kesir.startswith("0") and kesir != "0":
        return sayi(_int(tam)) + " virgül " + " ".join(sayi(int(c)) for c in kesir)
    return sayi(_int(tam)) + (" virgül " + sayi(int(kesir)) if kesir != "0" else "")


NUM = r"\d{1,3}(?:\.\d{3})+|\d+"  # 1.250.000 veya 1250


def _aktif_ses():
    import json, os
    city = os.environ.get("RADAR_CITY", "").strip()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yol = os.path.join(root, city, "state", "voice.json") if city and city != "kocaeli" else os.path.join(root, "state", "voice.json")
    try:
        return json.load(open(yol)).get("next", "emre")
    except Exception:
        return "emre"


def tts_text(s, ses=None):
    ses = (ses or _aktif_ses()).lower()
    # para: 71,60 TL / 4.780 TL / 50 lira
    def para(m):
        tam, kesir = m.group(1), m.group(2)
        out = sayi(_int(tam)) + " lira"
        if kesir and int(kesir.ljust(2, "0")[:2]):
            out += " " + sayi(int(kesir.ljust(2, "0")[:2])) + " kuruş"
        return out
    s = re.sub(rf"({NUM})(?:,(\d{{1,2}}))?\s*(?:TL|₺|lira)\b", para, s)
    # yüzde: %109 / % 4,5 / yüzde 20
    s = re.sub(rf"%\s*({NUM})(?:,(\d+))?", lambda m: "yüzde " + (_ondalik(m.group(1), m.group(2)) if m.group(2) else sayi(_int(m.group(1)))), s)
    # saat: 17.30 / 17:30 (yalnızca 0-23 . 00-59)
    s = re.sub(r"\b([01]?\d|2[0-3])[.:]([0-5]\d)\b(?!\d)", lambda m: sayi(int(m.group(1))) + (" " + sayi(int(m.group(2))) if int(m.group(2)) else ""), s)
    # yol/hat kodu: D-100, O-4, E-5, TEM-?  -> "D yüz"
    s = re.sub(r"\b([A-ZÇĞİÖŞÜ]{1,3})-(\d+)(?:['’](?=\w))?", _yol, s)
    # aralık: 21-50 -> yirmi bir ile elli
    s = re.sub(rf"\b({NUM})\s*[-–]\s*({NUM})\b", lambda m: sayi(_int(m.group(1))) + " ile " + sayi(_int(m.group(2))), s)
    # ondalık: 3,5
    s = re.sub(r"\b(\d+),(\d+)\b", lambda m: _ondalik(m.group(1), m.group(2)), s)
    # binlik ayraçlı ve düz tam sayılar (ek korunur: 100'de -> yüz'de)
    s = re.sub(rf"\b({NUM})\b(?:['’](?=\w))?", lambda m: sayi(_int(m.group(1))), s)
    # ay adı telaffuzu (kullanıcı 25.11.2026: "Kasım" yapay okunuyordu; Emre örnek 2 seçildi): Kasım -> Kâsım
    # Aylin'de düz "Kasım" doğru okunuyor (kullanıcı 26.11.2026, örnek 1); yalnızca büyük harf yazım düzeltilir
    if ses == "aylin":
        s = re.sub(r"\bKASIM\b", "Kasım", s)
    else:
        s = re.sub(r"\bKasım(?=\b|['’])", "Kâsım", s)
        s = re.sub(r"\bKASIM\b", "Kâsım", s)
        s = re.sub(r"\bkasım(?=\b|['’])", "kâsım", s)
    # birimler
    s = re.sub(r"\bkm\b", "kilometre", s)
    s = re.sub(r"\bkg/m²|\bkg/m2\b|\bkg\b", "kilogram", s)
    s = re.sub(r"\bm²|\bm2\b", "metrekare", s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()


if __name__ == "__main__":
    args = sys.argv[1:]
    ses = None
    if len(args) >= 2 and args[0] == "--ses":
        ses, args = args[1], args[2:]
    print(tts_text(" ".join(args) if args else sys.stdin.read(), ses))
