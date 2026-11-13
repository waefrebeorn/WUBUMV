# mdx_stemact — MDX stem-activity curve (voice-activity sensor)

Sprint 2026-11-12. **Verdict: Bar A + Bar B PASS, Bar C FAILS — the
stem-activity curve is VALID as a voice-activity curve; its STAY-RULE
use FAILS. The stay-rule patch has no sensor.**

## Bars

| Bar | Result |
|---|---|
| A — RMS-VAD boundaries vs Demucs | max \|dStart\| **0.21 s** on all three stems — PASS |
| B — sung vs instrumental envelope separation | 25 ms RMS envelope IQRs non-overlapping on all three stems; sung q25 0.0207 vs instrumental q75 0.00084 (MDX/c11) — 16–25× headroom — PASS |
| C — envelope-at-snapped-position separates 5 snap errors from 15 controls | errors median 0.04909 vs controls 0.07016, MW U=29/75, **p=0.2486** — FAIL |

Diagnostics also dead: rising-edge p=0.37, normalised-envelope p=0.78.
Do NOT re-test them.

## What it is good for

`stem_activity_curve.py` produces a per-stem voice-activity curve
(25 ms RMS envelope of the separated vocal stem). The c11 stem
reproduces the MDX curve to 5 decimal places. The curve MAY calibrate a
mouth-open-vs-quiet gate and CCA AV-sync — with the CCA visual feature
being mouth OPENNESS (lip distance), never frame-diff (loop 6 §3: the
frame-diff signal was the camera push, not the mouth).

## MV-11 generalisation leg: FAIL

Bar A stem-to-stem max |dStart| **1.71 s** (bar 0.5) — Demucs-stem
brass bleed crossing the 0.1×p99 VAD threshold. The c11 stem is the
cleaner stem (ratio 139.6× vs Demucs 70.1×). See `mv11/` for the
per-segment scores (`mv11_score.json`).

## Run

```sh
python3 stem_activity_curve.py   # build the curve from a vocal stem
python3 validate_stemact.py      # bars A/B/C against the JSONs here
```

Stems are NOT in this repo (audio stays on the HF media dataset).
Validation: `mdx_stemact_validation.json`, `bar_c.json`,
`stem_*_validation.json`, `stem_activity_*_segments.json`.
Full report: `../../research/detection-research/SPRINT_2026-11-12_MDX_STEMACT.md`.

## Metric bug banked

The span-start `match_boundaries` metric silently SKIPS unmatched
spans — it must count them as failures. Any gate trusting a boundary
to ±0.5 s on a new track needs a bleed-aware VAD threshold test first.
