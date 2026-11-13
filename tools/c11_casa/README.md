# c11_casa — CASA voice-segregation probe (sprint, FAIL FAST)

Sprint 2026-11-12. **Verdict: FAIL FAST — step 1 fails on both bars
with the correct voice-lag seed. No gate build.**

The question: does the voice-lag peak in a per-frame autocorrelation
(correlogram) separate sung from instrumental spans? It does not — on
either bar, with a correct seed.

| Bar | Requirement | Result |
|---|---|---|
| A — voice-lag peak on sung spans | ≥ 18/22 | **0/22 FAIL** |
| E — multipitch confusion (octave-aware) | ≤ 0.20 | **0.5606 FAIL** |

## Why it matters

This was the last classical family left after sprint 8 (voicing gate),
vibrato, formants, and spectral entropy all failed: segregate the scene
instead of measuring the mixture. With CASA dead, **the classical sensor
search is over**. Loop 5 took the adoption branch (MDX-Net ONNX as-is +
c11_sep). Do not re-run this experiment expecting a different answer
unless a new signal class is proposed.

## Seed audit (the finding that outlived the sprint)

The v1 run seeded the **bass**, not the voice — mix pYIN pins at the
50 Hz floor on 81% of voiced frames; stem pYIN pins at the 800 Hz
ceiling on 63%. **Neither saved pYIN track is a voice-F0 track.** Any
future F0-based measurement must source F0 from the stem autocorrelation
reference in the report §2 (per-segment median F0 144–267 Hz), or from
RMVPE — never from raw pYIN on the mix.

## Run

```sh
python3 step1_experiment.py     # v1 (withdrawn — wrong seed, kept for the audit trail)
python3 step1_experiment_v2.py  # v2, correct stem-derived seed
python3 step1_plot.py           # plot (step1_plot.svg)
```

Validation: `c11_casa_validation.json`, `step1_experiment.json`,
`step1_experiment_v1_seedmix.json`.
Full report: `../../research/detection-research/SPRINT_2026-11-12_C11_CASA.md`.
