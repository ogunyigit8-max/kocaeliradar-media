"""Videoyu Instagram'in alabilecegi acik adrese koyar (Kocaeli Radar yontemi: depodaki v/ klasoru).
Kullanim: python3 tools/yayin.py bolumler/b02/b02.mp4
  -> senolsan/v/b02.mp4 olarak kopyalar, 4 gunden eski v/*.mp4 dosyalarini siler,
     commit + push eder, dosya acik adreste gorunene kadar bekler ve adresi yazar."""
import glob, os, shutil, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import istek, KOK
from gorsel import RAW


def git(*a):
    subprocess.run(["git", *a], check=True, cwd=KOK)


def main(yol):
    vdir = os.path.join(KOK, "v"); os.makedirs(vdir, exist_ok=True)
    ad = os.path.basename(yol)
    shutil.copyfile(yol, os.path.join(vdir, ad))
    for f in glob.glob(os.path.join(vdir, "*.mp4")):
        if time.time() - os.path.getmtime(f) > 4 * 86400 and os.path.basename(f) != ad:
            os.remove(f)
    git("add", "-A", "v")
    git("-c", "user.name=Sen Olsan", "-c", "user.email=noreply@anthropic.com", "commit", "-q", "-m", f"senolsan: {ad} yayina hazir")
    git("pull", "--rebase", "origin", "main")
    git("-c", "push.negotiate=true", "push", "origin", "HEAD:main")
    url = RAW + "v/" + ad
    for _ in range(30):
        try:
            if len(istek(url, ham=True, deneme=1)) > 100000:
                print(url)
                return url
        except Exception:
            pass
        time.sleep(10)
    sys.exit(f"Video acik adreste gorunmedi: {url}")


if __name__ == "__main__":
    main(sys.argv[1])
