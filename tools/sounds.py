"""Hikâye sesleri (tamamen sentetik, telifsiz). numpy ile üretilir, scipy varsa filtre kalitesi artar."""
import numpy as np, wave

SR = 44100

def _lp(x, fc):
    try:
        from scipy.signal import butter, sosfilt
        return sosfilt(butter(2, fc, btype="low", fs=SR, output="sos"), x)
    except Exception:
        a = 1 - np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
        for i in range(len(x)): s += a * (x[i] - s); y[i] = s
        return y

def _hp(x, fc): return x - _lp(x, fc)

def _bp(x, lo, hi): return _lp(_hp(x, lo), hi)

def _env(n, a=0.4, r=0.8):
    t = np.arange(n) / SR; T = n / SR
    return np.clip(t / a, 0, 1) * np.clip((T - t) / r, 0, 1)

def rain(T, heavy=False, thunder=False, seed=1):
    n = int(SR * T); rng = np.random.default_rng(seed)
    base = _bp(rng.normal(0, 1, n), 400, 6000) * (0.5 if heavy else 0.32)
    hiss = _hp(rng.normal(0, 1, n), 5000) * 0.08
    drops = np.zeros(n)
    for _ in range(int(T * (90 if heavy else 45))):
        p = rng.integers(0, n - 2000); L = rng.integers(200, 900)
        f = rng.uniform(1500, 5000); t = np.arange(L) / SR
        drops[p:p + L] += np.sin(2 * np.pi * f * t * (1 - t * 8)) * np.exp(-t * rng.uniform(80, 200)) * rng.uniform(0.05, 0.25)
    x = base + hiss + drops
    x *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.17 * np.arange(n) / SR)
    if thunder:
        p = int(SR * min(2.0, T * 0.3)); L = min(n - p, int(SR * 3.5)); t = np.arange(L) / SR
        rum = _lp(rng.normal(0, 1, L), 120) * (np.exp(-t * 1.2) * (1 - np.exp(-t * 20))) * 3.5
        x[p:p + L] += rum
    return x * _env(n, 0.8, 1.0)

def wind(T, seed=2):
    n = int(SR * T); rng = np.random.default_rng(seed)
    x = _bp(rng.normal(0, 1, n), 200, 1200)
    mod = 0.55 + 0.45 * np.sin(2 * np.pi * 0.11 * np.arange(n) / SR + 1.3) * np.sin(2 * np.pi * 0.05 * np.arange(n) / SR)
    pad = sum(np.sin(2 * np.pi * f * np.arange(n) / SR) for f in (220, 277.2, 329.6)) * 0.025
    return (x * 0.25 * mod + pad) * _env(n, 1.0, 1.2)

def market(T, mood=0, seed=3):
    """Borsa havası: açılış zili + saat tıkırtısı + hafif nabız + yükseliş/düşüşe göre tonlanan akor.
    mood: +1 yükseliş, -1 düşüş, 0 nötr"""
    n = int(SR * T); t = np.arange(n) / SR; rng = np.random.default_rng(seed)
    x = np.zeros(n)
    # açılış zili (çan)
    L = int(SR * 2.5); tt = np.arange(L) / SR
    bell = sum(a * np.sin(2 * np.pi * f * tt) * np.exp(-tt * d) for f, a, d in ((880, .5, 2.2), (1760, .25, 3), (2637, .15, 4), (1318.5, .2, 2.8)))
    x[:L] += bell * 0.5
    # saat tıkırtısı (borsa ekranı)
    for k in range(int(T * 2)):
        p = int(SR * (0.6 + k * 0.5)); Lc = 600
        if p + Lc >= n: break
        c = _hp(rng.normal(0, 1, Lc), 3000) * np.exp(-np.arange(Lc) / SR * 400)
        x[p:p + Lc] += c * (0.18 if k % 2 == 0 else 0.10)
    # nabız (bas)
    for k in range(int(T / 0.5)):
        p = int(SR * (0.6 + k * 0.5)); Lb = int(SR * 0.3)
        if p + Lb >= n: break
        tb = np.arange(Lb) / SR; f = 55 + 40 * np.exp(-tb * 30)
        x[p:p + Lb] += np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tb * 10) * (0.35 if k % 2 == 0 else 0.2)
    # akor
    ch = (261.6, 329.6, 392.0, 523.3) if mood > 0 else (220.0, 261.6, 329.6, 440.0) if mood < 0 else (246.9, 311.1, 370.0, 493.9)
    pad = sum(np.sin(2 * np.pi * f * t + i) for i, f in enumerate(ch)) * 0.035 * np.clip((t - 0.8) / 1.5, 0, 1)
    x += pad
    # dijital "data" blipleri
    for k in range(int(T * 1.5)):
        p = rng.integers(int(SR * 1), n - 3000); Lp = 1500; tp = np.arange(Lp) / SR
        x[p:p + Lp] += np.sin(2 * np.pi * rng.choice([1046.5, 1318.5, 1568.0]) * tp) * np.exp(-tp * 60) * 0.06
    return x * _env(n, 0.05, 1.2)

def save(x, path, gain_db=-16):
    x = x / (np.abs(x).max() + 1e-9) * 0.9
    st = np.stack([x, x], 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
