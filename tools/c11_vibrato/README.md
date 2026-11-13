# c11_vibrato — vibrato depth measurement (sprint, FAIL FAST)

Sprint 2026-11-12. **Verdict: FAIL FAST as delivered — Bar E fails; the
chant is straight-tone on the delivered measurement.**

Method: pYIN F0 track → cents contour → 4–8 Hz Butterworth bandpass →
modulation depth = RMS of bandpassed cents. Controls validate the
pipeline (synthetic 6 Hz wobble recovered at 35.16c vs 35.36 expected;
synthetic 3 Hz wobble correctly rejected at 0.30c).

## What the numbers were

| Bar | Result |
|---|---|
| A — median depth sung vs instrumental, mix F0 | Sung 2.55c [0.27, 6.66] vs instr 3.32c [0.45, 10.36] — IQRs overlap, wrong direction — **FAIL** |
| E — separation | fails |

## Correction (loop 5, 2026-11-12 — read before trusting the verdict)

The depth numbers are measurements of **pinned pYIN contours**: the mix
track pins at the 50 Hz floor on 81% of voiced frames, the stem pins at
the 800 Hz ceiling on 63%. A contour pinned at a constant boundary has
~0 modulation depth *by construction*. Loop 5 re-measured on the correct
source: depth 114c, PSD peak 3.0 Hz (drift, no 5–7 Hz vibrato peak) —
**AMBIGUOUS** by the pre-stated rule. "Straight-tone STANDS" is operative
only because the sensor fails on the correct source too.

**Definitive arbiter: RMVPE on the MDX stem** (not built yet). Do not
re-run this sprint's measurement as a vibrato gate.

## Run

```sh
python3 day1_controls.py     # controls
python3 day1_falsifier.py    # falsifier + validation JSON
python3 day1_plot.py         # plot (day1_falsifier_plot.svg)
```

Validation: `c11_vibrato_validation.json`, `day1_falsifier.json`.
Full report: `../../research/detection-research/SPRINT_2026-11-12_C11_VIBRATO.md`.
