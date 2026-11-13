# SPRINT_SCOPE.md — MDX_STEMACT (Slopcannon improvement loop 6, top-1)

**Sprint:** MDX_STEMACT — validate the MDX stem-activity curve as the pipeline's
voice-activity sensor.
**Parent:** loop 5 report §3 #2 + §8.2 (seed item 2); loop 6 report §3 (top-1).
**Goal:** prove — or kill — the stem-activity curve as the sensor that unblocks
three things at once: the snapper stay-rule patch, the mouth-open-vs-quiet gate
(loop 1 #3), and CCA AV-sync (loop 2 #3, loop 6 drawn entry). It is the ONLY
in-span stay-rule candidate left (c11_voice curve, vibrato depth, spectral
entropy, vocal-flux both flavours all dead — loop 5 §5). If it fails its own
bar, loop 7 records plainly that the stay-rule patch has no sensor at all.

## Held bars (from loop 5, unchanged — do NOT lower any bar)

**Bar A — boundaries.** The stem-activity curve's RMS-VAD boundaries reproduce
the Demucs stem-activity boundaries within **±0.5 s** on the 12 ref segments
(`c11_mir/hpss_mv14_ref.json`). Span-start metric as in c11_sep stage 4
(ref spans overlap-merged; each matched to its earliest-start overlapping pred
piece). Report max |dStart| per stem; dEnd is diagnostic (split/extension).

**Bar B — separation.** The **25 ms RMS envelope** separates sung from
instrumental with **non-overlapping IQRs** — on ALL THREE stems (c11, ONNX MDX,
Demucs). Report medians + IQRs per stem per class; the sprint-6 median-ratio
statistic (active/silent ≥100×) is reported alongside as a secondary, not the bar.

**Bar C — stay-rule application (pre-stated).** Stem-envelope-at-snapped-position
separates the **5 known snap errors** (1-based idx 34, 56, 60, 112, 162 into
`c11_mir/snap_mix_mv14.json`) from the **15 correct controls** (loop-4 rule:
|correction| ≤ 0.05 s, prob ≥ 0.9, on_peak, first 15): Mann-Whitney one-sided
p < 0.05 AND errors median < correct median. Diagnostic (NOT a bar): distance
from the snapped position to the nearest stem-envelope rising edge, errors vs
controls — if Bar C fails, this diagnostic says whether the rising edge is the
better statistic for loop 7.

**Verdict logic (pre-stated).** A+B pass and C passes → sensor VALIDATED for all
three uses; loop 7 calibrates the stay-rule patch + mouth-open gate + CCA on it.
A+B pass and C fails → sensor valid as a voice-activity curve (mouth-open + CCA
may calibrate on it), stay-rule use FAILS — the stay-rule patch has no sensor.
A or B fails → sensor FAILS; loop 7 records it and the stay-rule/mouth-open/CCA
chain stays blocked on a sensor that does not exist.

## Why this sprint now (loop-6 findings it builds on)

- c11_sep PASSED all 4 bars (committed a2b435bd): the production stem exists
  (corr 0.9675 vs Demucs, max |dStart| 0.21 s vs the HPSS ref, 242.7×,
  840.4 s). The stem is cheap enough to be a pipeline step, not a batch job.
- Loop 6 ran the sprint-5-specified stem-snap comparison and it FAILED: the
  stem snap does not reproduce the mix snap (median |diff| 0.032–0.048 s vs the
  16 ms bar; agreement 69–73/212; controls agree 3–4/15) and does not fix the
  5 errors (idx 56 goes 0.0 → −0.304 s). BUT the stem snaps are self-consistent
  (Demucs vs c11 median |diff| 0.0, agree 144–156/212): the stem has its OWN
  onset lattice, stable across separators, which DIFFERS from the mix lattice.
  Implication for Bar C: mix-snap positions are substantially
  accompaniment-locked, so envelope-at-snapped-position is a real test, not a
  formality — if it separates, the stay-rule has its evidence; if it does not,
  the rising-edge diagnostic is the next statistic, not a re-test of this one.
- Loop 6's CCA audio-side check PASSED its premise: the stem envelope peaks at
  **3.125 Hz** on sung spans (frac 18–20% of 0.5–10 Hz power) vs 1.25 Hz on gaps
  — the syllable-rate structure CCA needs is in the stem envelope. (The CCA
  visual side failed on one take: frame-diff in a mouth box is swamped by
  camera push — the visual feature must be mouth openness, and CCA stays
  sequenced after R2 + that feature. This sprint does not build CCA.)

## Inputs (all exist, all on disk)

- Stems (MV-14, 161.6 s): `detection-research/c11_sep/c11_vocals.wav` (C11),
  `~/workspace/wubuwizard-cpu-sep/mdx_vocals_full.wav` (ONNX MDX, adopted),
  `detection-research/c11_mir/separation_mv14/mv14_44k_(Vocals)_htdemucs.wav`
  (Demucs reference). 16 kHz mono versions in
  `research_notes/slopcannon-improvement-loop/loop-06/` (`mv14_c11stem16k.wav`,
  `mv14_mdxstem16k.wav`, `mv14_stem16k.wav`).
- Refs: `c11_mir/hpss_mv14_ref.json` (12 segments; sung 1–10, bleed 11–12),
  `c11_mir/make_ref_segments.py` (RMS-VAD recipe — use VERBATIM: median 25 ms
  RMS envelope, threshold, merge bar 1.0 s), `c11_mir/snap_mix_mv14.json` +
  `snap_vocal_mv14.json` (errors + controls live here).
- Calibration: `c11_sep/validate_fulltrack.py` + `stage4_fulltrack_validation.json`
  (reproduces loop-5's numbers on the ORT vocals: corr 0.9675, dStart 0.21,
  ratio 242.7) — calibrate your validator against it FIRST, before running it
  on the c11 stem. Do NOT re-run c11_sep. Do NOT re-run sprint 8's calibration.

## Method

1. Calibrate: run your RMS-VAD + envelope statistics on the ONNX MDX stem and
   reproduce loop 5's numbers (17 segments, max |dStart| 0.21 s, 248.8×) within
   rounding. If you cannot reproduce them, stop and report — do not proceed on
   an uncalibrated validator (loop-4 lesson).
2. Bars A+B on all three stems, same recipe, same masks. Report per-stem.
3. Bar C on the c11 stem (production stem) + the ONNX stem (adopted segmenter);
   report both, judge on the c11 stem.
4. Deliver the reusable artifact: the stem-activity curve per track (curve file
   + the RMS-VAD recipe as a script in `mdx_stemact/`) so loop 7 calibrates
   gates on it without re-deriving it.
5. Generalization leg (MV-11, if it fits — do NOT block the MV-14 verdict on
   it): Demucs stem on disk at
   `MV-11_water-hit-my-balls/analysis/tests/separation/track_44k_vocals_htdemucs.wav`;
   no MDX/c11 stem exists — produce one with the c11_sep runner
   (`detection-research/c11_sep/sep_main`, ~840 s, resilient dump mode,
   checkpoint per chunk) and test Bar A stem-to-stem (c11 boundaries within
   ±0.5 s of Demucs boundaries, no HPSS ref needed). If the leg does not fit
   in this sprint, record it as owed, with the reason.

## What this sprint does NOT do

- No gate build (stay-rule patch, mouth-open calibration, CCA are loop-7 work
  once this passes — they calibrate on the artifact this sprint delivers).
- No RMVPE vibrato arbiter (loop 5 #5, separate measurement), no G7/R5 builds,
  no c11_sep rerun, no TSM work (c11_tsm is a parallel sprint — do not duplicate).
- No Demucs model run (torch is broken in this venv; the Demucs stem on disk
  is the reference).

## Files (to be written by the sprint)

- `detection-research/SPRINT_2026-11-12_MDX_STEMACT.md` — sprint report, each
  bar PASS/FAIL stated plainly with numbers from the JSON on disk.
- `detection-research/mdx_stemact/` — validation JSON + scripts + curve
  artifacts + run logs.
- `DETECTION_FINDERS.md` run entry.
- No commit (parent owns commits). No video generation, no Telegram.

## Constraints

- BLADE REALITY: the VM reboots roughly every ~2 h — checkpoint per unit of
  work (curve + JSON after each stem). The validation compute is minutes per
  stem; the only long job is the optional MV-11 c11_sep run, which MUST use
  the resilient dump mode.
- HEARTBEAT: append one line `<task> <UTC ISO> <one-line status>` to
  `~/workspace/goals/wubu-music-videos-from-suno-tracks/hidden_files/heartbeats/mdx-stemact.beat`
  every ~5 min while running.
- Never hand-copy a number — read it from the JSON (loop-5 lesson: a
  transcription error was caught in-loop because the JSON was authoritative).
