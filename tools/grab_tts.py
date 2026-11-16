"""Speko audio_synthesize sonuçlarındaki WAV dosyalarını toplar.

Speko sonucu büyük olduğu için oturumun tool-results klasörüne kaydedilir ve metninde
"saved to /…/mcp-Speko-blob-….wav" geçer. Bu betik son N synthesize sonucunu (eskiden yeniye)
bulur ve sırayla OUTDIR/<ad>.wav olarak kopyalar.

Kullanım: python3 tools/grab_tts.py OUTDIR ad1 ad2 ...   (adlar synthesize çağrı sırasıyla)

Ayrıca her sesin imzalı indirme bağlantısını (15 dk geçerli) OUTDIR/urls.json'a yazar ve ekrana basar.
Bu bağlantılar hemen mcp__Speko__audio_transcribe(audio_url=..., language="tr", word_timestamps=true)
ile kullanılır; dönen "words" listesi spec'teki ilgili sahnenin "words" alanına yapıştırılır
(news.py altyazıyı kelime kelime konuşmayla senkronlar).
"""
import glob, json, os, re, shutil, subprocess, sys

out, names = sys.argv[1], sys.argv[2:]
os.makedirs(out, exist_ok=True)
fs = sorted(glob.glob(os.path.expanduser("~/.claude/projects/*/*/tool-results/mcp-Speko-audio_synthesize-*.txt")) +
            glob.glob("/root/.claude/projects/*/*/tool-results/mcp-Speko-audio_synthesize-*.txt"),
            key=lambda p: int(re.search(r"audio_synthesize-(\d+)(?:-\w+)?\.txt$", p).group(1)))
fs = list(dict.fromkeys(fs))[-len(names):]
if len(fs) < len(names):
    sys.exit(f"Yalnızca {len(fs)} sonuç bulundu, {len(names)} gerekiyordu")
urls = {}
for n, f in zip(names, fs):
    parts = json.load(open(f)); t = parts[0]["text"]
    for p in parts[1:]:
        try:
            urls[n] = json.loads(p["text"])["url"]; break
        except Exception:
            pass
    m = re.search(r"saved to (\S+\.wav)", t)
    if not m:
        sys.exit(f"WAV yolu bulunamadı: {f}")
    dst = os.path.join(out, n + ".wav"); shutil.copy(m.group(1), dst)
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", dst], capture_output=True, text=True).stdout.strip()
    print(n, d, "sn")
json.dump(urls, open(os.path.join(out, "urls.json"), "w"), indent=1)
for n in names:
    print(f"URL {n}: {urls.get(n, '(yok)')}")
