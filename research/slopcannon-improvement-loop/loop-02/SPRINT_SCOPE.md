# SPRINT SCOPE — c11_voice: C11 voicing gate (YIN + pYIN + CPP + HNR)

**Loop:** Slopcannon improvement loop 2, top-1 ranked entry (report.md §1).
**Parent:** spawn a build coordinator from this scope. Do NOT commit, do NOT write to Telegram, do NOT generate video.
**Why this sprint:** sprint 6 proved harmonic ≠ vocal — the HPSS boundary gate scored 12.5% vs an 80% bar (harmonic vocal-band power only 1.24× active-vs-silent; Demucs vocals RMS 192×). The pipeline has no genuine voicing feature, and three downstream improvements are blocked on one: the snapper's "stay if no in-span strong peak" rule, loop 1's unsung flag, and loop 1's mouth-open-vs-quiet gate (MAR × vocal RMS). This sprint builds the voicing feature they all consume.

## Goal

A single-file C11 tool, `detection-research/c11_voice/c11_voice.c` (libc + libm only, `gcc -std=c11 -O2 -Wall -Wextra`, zero warnings), that reads a 16 kHz mono WAV and emits a per-frame voicing analysis:

| Output per frame (10 ms hop) | Definition |
|---|---|
| `f0_hz` | YIN fundamental-frequency estimate (0 if unvoiced) |
| `voicing` | YIN voicing strength: 1 − CMNDF minimum (0..1) |
| `cpp_db` | Smoothed cepstral peak prominence (Hillenbrand & Houde 1996) |
| `hnr_db` | Boersma (1993) harmonics-to-noise ratio from the autocorrelation maximum |
| `voiced` | Binary decision: voiced iff (voicing ≥ 0.5 AND cpp ≥ calibrated threshold AND hnr ≥ calibrated threshold) — thresholds calibrated on MV-14, see Validation |
| `boundary` | Vocal-activity boundaries: voiced→unvoiced and unvoiced→voiced transitions, with times |

Also emit a `voice_curve.json` (per-frame arrays) and a `voice_bounds.json` (boundary list with times + confidence).

## Method — four classical algorithms, no weights

1. **YIN** (de Cheveigné & Kawahara, JASA 111(4):1917–30, 2002; DOI 10.1121/1.1458024). Steps: (1) autocorrelation via FFT; (2) cumulative-mean-normalized difference function; (3) absolute threshold 0.1, first minimum below threshold; (4) parabolic interpolation of the minimum; (5) best local estimate; (6) octave-error handling per the paper. Search range 50–800 Hz (singing; no upper-frequency limit is YIN's advantage — do not cap at speech range). Validate against `librosa.pyin` on the same audio.
2. **pYIN shell** (Mauch & Dixon, ICASSP 2014): run YIN at multiple thresholds, keep candidate F0s with probabilities from the paper's Beta prior, smooth with a Viterbi pass over time. Reuse the snapper's DP/Viterbi machinery from `c11_mir` — do not write a third Viterbi. pYIN is the *smoothing* layer; YIN is the estimator. If time is short, ship YIN + a median-filtered F0 track first, pYIN second — say which shipped.
3. **CPP** (Hillenbrand et al. 1994; Hillenbrand & Houde 1996): cepstrum (FFT → log magnitude → IFFT), find the cepstral peak in the quefrency range corresponding to 50–800 Hz, prominence = peak − regression line through the cepstrum, in dB; smooth over ~5 frames (CPPS). Do NOT import a clinic's cutoff (Praat 14.45 dB sustained /a/, 9.33 dB running speech) — calibrate on MV-14 (see Validation).
4. **HNR** (Boersma, IFA Proceedings 17, 1993, pp. 97–110): HNR = 10·log10(r(τmax)/(1−r(τmax))), where r is the normalized autocorrelation and τmax the pitch lag from YIN. Parabolic interpolation of the autocorrelation peak (the paper's accuracy claim rests on it); correct the autocorrelation for the window (divide by the window's autocorrelation, as in the paper / soundgen's getHNR). Hanning window, 6 glottal cycles per the efficient-variant finding (mean HNR error < 0.42 dB).

## LEGO (reuse, do not rewrite)

- **FFT / STFT / mel / window functions:** from `detection-research/c11_mir/c11_mir.c` — lego in the functions, do not re-derive. Note sprint 4's two validation-caught fixes (librosa ref=1.0 for MFCC dB; periodic Hann, not symmetric) — the lego'd code already carries them.
- **Viterbi / DP:** from the snapper (`snap` mode in c11_mir.c) — same transition structure, different cost (YIN candidate probability instead of onset-flux cost).
- **JSON emission:** slermes libjson vendored in `c11_mir/json.c` + `json.h` (byte-identical + 2-line build fix, sprint 5) — reuse verbatim.
- **16 kHz WAV input:** `detection-research/c11_mir/mv14_16k.wav` already exists as the canonical resample; the tool reads WAV (16-bit PCM mono) and the coordinator documents the exact resample command for other tracks.
- **No new dependencies.** No torch, no librosa at runtime, no weights files. Validation-only Python may use librosa/pyin (detection-research/venv has numpy/scipy; pyin needs librosa — install into the throwaway venv only if missing, document it, do not commit the venv).

## Inputs (on disk now)

- `detection-research/c11_mir/mv14_16k.wav` — MV-14 track, 161.6 s, 16 kHz mono.
- `detection-research/c11_mir/separation_mv14/mv14_44k_(Vocals)_htdemucs.wav` — Demucs vocal stem (sprint 6 output; NEVER commit; use as the validation reference for sung spans).
- `detection-research/c11_mir/snap_vocal_mv14.json` + `snap_mix_mv14.json` — snapper outputs (212 words) for cross-checks.
- MV-14 section map (report.md §4): Intro 0.00 / V1 14.14 / C1 36.44 / V2 55.90 / C2 77.78 / Bridge 98.50 / Final 112.16 / Outro 128.20.
- Sprint 6 reference: `detection-research/c11_mir/hpss_mv14.json` + `.validation.json` (boundary ground truth the HPSS gate failed against — reuse the same boundary list so the scores are comparable).

## Validation — the bar is written to be failed honestly

Run every check below and report the numbers; a FAIL on any starred item is a failed sprint, not a footnote.

1. **YIN vs librosa.pyin (MV-14 mix + vocal stem):** F0 correlation ≥ 0.99 on voiced frames; gross error (frames where |F0_c11 − F0_pyin| / F0_pyin > 20%) ≤ 2%. (Paper baseline: YIN gross error 1.03% on laryngograph speech.)
2. **★ Vocal-activity boundaries vs hand-checked MV-14 boundaries:** ≥80% of sung-span boundaries (starts AND ends, scored separately like sprint 6) within ±0.5 s of hand-marked boundaries. Hand-marking: the coordinator marks sung-span starts/ends by ear on the Demucs vocal stem for at least the 12 reference segments sprint 6 used (reuse `make_ref_segments.py`'s segment list if it exists; else mark 12 segments fresh and commit the list). This is the loop-1 seed bar and the number that decides whether Demucs stops being the segmenter for boundary work.
3. **★ Beat HPSS:** vocal-activity boundaries from this gate must beat HPSS's 12.5% starts / 8.3% ends on the *same* segment list. Report both numbers side by side.
4. **CPP/HNR separation:** median CPP on sung spans ≥ median CPP on instrumental spans + 3 dB; same direction for HNR (median sung HNR ≥ instrumental + 3 dB). If CPP separates but HNR does not (or vice versa), report which carries the decision and why — do not average away a disagreement.
5. **Snapper cross-check:** the voicing curve's "no voicing in span" flag must fire on all 5 of the snapper's known early-snap errors (sprint 5 report: words snapped early onto previous-word/drum peaks when the word has no in-span strong peak). If it fires on <5, the stay-rule patch cannot be built on this curve — say so.
6. **Unsung-flag sanity:** run the voicing curve under 3 lyric-sheet lines known to be unsung-or-ambiguous on MV-14 (coordinator picks from the intake; document which). The curve must read unvoiced under at least 2 of 3 — else the unsung flag (loop 1's #1) has no sensor.
7. **Performance:** full MV-14 track (161.6 s) in < 10 s wall on this blade (1.5 shared CPUs); peak memory < 200 MB. Report the measured numbers.
8. **Build hygiene (sprint 4/5/6/7 standard):** clean rebuild, zero warnings under `-Wall -Wextra`; binary byte-identical across two consecutive builds; `--selftest` mode with a synthetic signal (pure sine + noise burst) that must recover the sine's F0 within 1% and mark the noise burst unvoiced; no ASan/UBSan findings on the self-test + one full MV-14 run.

## Deliverables

- `detection-research/c11_voice/c11_voice.c` (+ Makefile, README.md) — single-file C11, libc + libm only.
- `detection-research/c11_voice/c11_voice_validation.json` — all validation numbers above, machine-readable.
- `detection-research/c11_voice/voice_mv14.json` + `voice_bounds_mv14.json` — outputs on MV-14 (mix + vocal stem; two runs, both files).
- `detection-research/SPRINT_2026-11-12_C11_VOICE.md` — report: method, LEGO notes, validation table (pass/fail per bar), honest limits, what it unblocks (snapper stay-rule patch, unsung flag, MAR gate — each named with its next step).
- `DETECTION_FINDERS.md` run entry (next run number; follow the run-13 format).
- **Do NOT commit** the binary, any `.wav` outputs, or the Demucs stem. Commit only the `.c`, Makefile, README, report, validation JSON, and DETECTION_FINDERS.md entry.

## Sequencing notes for the parent

- This sprint unblocks three queued follow-ups: (a) sprint 5's snapper stay-rule patch (voicing curve = the in-span evidence); (b) sprint 5's stem-flux blind check (run the voicing gate on the stem, compare against mix); (c) loop 1's improvement #3 validation (MAR × vocal RMS gate — needs this curve).
- The next sprint after this one (loop 2's #3, CCA sync) needs a face box (#5 Viola-Jones) — sequence c11_frames → Viola-Jones → CCA, or prototype CCA's audio side first.
- If validation bar 2 fails (<80% within ±0.5 s): do NOT lower the bar. Report which measure (YIN voicing / CPP / HNR) carries the error, whether the failure is threshold calibration (fixable) or structural (like HPSS — the measure does not separate vocals on a dense mix), and recommend the next candidate (MDX-Net ONNX adopt-as-is, or the birdsong entropy feature from loop 2's #2) with evidence.
