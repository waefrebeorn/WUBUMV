#!/usr/bin/env python3
"""Hand-check harness for the c11_mir word-time snapper (sprint 5).

Mirrors the C front end in numpy (periodic Hann 1024/256, centred frames,
16 kHz mono) and prints, for a stratified sample of MV-14 words, the
vocal-band energy + vocal/mix flux traces around the ASR start — WITHOUT
the snapped value, so the onset pick is blind. Run, pick onsets by eye
from the traces, then compare against /tmp/snap_vocal.json.
"""
import json, random
import numpy as np
from scipy.io import wavfile

WAV = "/home/hatch/workspace/wubutv-network/musicvideo/detection-research/c11_mir/mv14_16k.wav"
WORDS = "/home/hatch/workspace/wubutv-network/musicvideo/MV-14_clip-it/analysis/SONG_WORDS.json"
SNAP = "/tmp/snap_vocal.json"   # used ONLY for sample selection, never printed
FRAME, HOP, SR = 1024, 256, 16000
HOP_S = HOP / SR
LO, HI = 300.0, 3400.0

sr, pcm = wavfile.read(WAV)
x = pcm.astype(np.float64) / 32768.0
n = len(x)
nframes = 1 + (n + HOP - 1) // HOP
while nframes > 1 and (nframes - 1) * HOP > n + FRAME // 2:
    nframes -= 1
win = 0.5 * (1 - np.cos(2 * np.pi * np.arange(FRAME) / FRAME))  # periodic Hann
# centred STFT magnitude, same as C stft_mag
spec = np.zeros((nframes, FRAME // 2 + 1))
for fi in range(nframes):
    c = fi * HOP
    seg = np.zeros(FRAME)
    lo, hi = c - FRAME // 2, c + FRAME // 2
    s0, s1 = max(lo, 0), min(hi, n)
    seg[s0 - lo:s1 - lo] = x[s0:s1]
    spec[fi] = np.abs(np.fft.rfft(seg * win))
nbins = FRAME // 2 + 1
flo = int(np.ceil(LO / SR * FRAME)); fhi = int(np.floor(HI / SR * FRAME))
band = spec[:, flo:fhi + 1]
energy = (band ** 2).sum(axis=1); energy /= energy.max()
d = np.diff(band, axis=0, prepend=np.zeros((1, band.shape[1])))
vflux = np.maximum(d, 0).sum(axis=1); vflux /= vflux.max()
# sanity: mirror flux vs the C tool's dumped vocal flux
cflux = np.loadtxt("/tmp/flux_vocal.txt")
print("mirror vocal-flux corr vs C dump: %.6f  max|diff|: %.6f"
      % (np.corrcoef(vflux, cflux)[0, 1], np.abs(vflux - cflux).max()))
mflux = np.loadtxt("/tmp/flux_mix.txt")

words = json.load(open(WORDS))["words"]
snap = json.load(open(SNAP))["words"]
assert len(words) == len(snap) == 212

# --- stratified sample (selection uses snap stats; traces never show snapped) ---
by_corr = sorted(range(212), key=lambda i: -abs(snap[i]["correction_s"]))[:8]
gap_out = [i for i in range(212) if snap[i]["gap_asr"] and not snap[i]["gap_snapped"]][:8]
rnd = random.Random(11)
rest = [i for i in range(212) if i not in set(by_corr) | set(gap_out)]
rand8 = rnd.sample(rest, 8)
sample = sorted(set(by_corr) | set(gap_out) | set(rand8))
print("sample size:", len(sample), "| large-corr:", by_corr, "| gap-out:", gap_out, "| random:", sorted(rand8))

def spark(vals):
    """41-char decile sparkline: ' ' for <0.05, 0-9 otherwise."""
    out = []
    for v in vals:
        if v < 0.05: out.append(" ")
        else: out.append(str(min(9, int(v * 10))))
    return "".join(out)

HALF = 20  # +-20 frames = +-0.32 s
print()
print("Legend: E=vocal-band energy 0-9 (blank<0.05) | V=vocal flux | M=mix flux")
print("        | marks the ASR start frame (centre). Offsets are frames (16 ms).")
for i in sample:
    w = words[i]; s = snap[i]
    f0 = int(round(w["start"] / HOP_S))
    lo_f, hi_f = f0 - HALF, f0 + HALF
    e = energy[lo_f:hi_f + 1]; v = vflux[lo_f:hi_f + 1]; m = mflux[lo_f:hi_f + 1]
    print("#%03d %-12s asr=%7.3f prob=%.2f gap_asr=%s |corr|=%.3f"
          % (i, w["word"], w["start"], w.get("prob", 0), s["gap_asr"], abs(s["correction_s"])))
    print("   E " + spark(e))
    print("   V " + spark(v))
    print("   M " + spark(m))
    print("   " + " " * HALF + "|")
