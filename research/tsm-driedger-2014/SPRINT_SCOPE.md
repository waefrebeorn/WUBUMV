# SPRINT SCOPE — c11_tsm (C11 per-gap-targeted time-stretch core)

**Source:** TSM method validation, 2026-11-12 — `~/workspace/research_notes/tsm-driedger-2014/report.md`
(parent-verified in full ~04:44 EST). User method: Telegram msg 292 (Driedger/Müller/Ewert
2014 + user slicing synthesis). Grading: msg 294 winners league (overlap average).

## Verdict the build inherits

**VALIDATED WITH A SQUEEZE GUARD.** M7 (per-gap-targeted slicing) is the only variant
that beats the take's internal drift: words-3+ onset RMS **69.3 ms** vs **224–284 ms**
for every uniform method (3.2–4.1× better), hits bit-identical (max|diff| 0.0,
centre error 0.000 s on all 4 takes). **But it fails structurally on severe gap
squeezes:** gap alpha 0.24–0.33× destroys the word body in the gap — S50 (0.33×)
heard 1/4 words, S52 (0.24/0.25×) dropped word 4. Uniform fallback: OLA256
(best identity 23/23, best uniform RMS 245.7 ms). PV is the worst uniform method
on sung material (identity 17/23, RMS 315.3 ms) — do not build the core on PV.

## What to build

- **Per-gap-targeted slicing (M7 as the C11 core), lego-first** from the prototype's
  DSP — HPSS median filter, PV, OLA already exist as patterns in the user's C
  modules; the new work is the per-gap scheduler + guard.
- Hit windows ±25 ms copied verbatim; each gap stretched to land its hit exactly
  on the song-grid onset; gap DSP = the paper's HP split (PV on harmonic,
  OLA N=256 on percussive); 50 ms hit-tail lookback so the PV picks up in phase
  with the preceding hit.
- **Squeeze guard (HARD RULE):** if a gap alpha < 0.5, do NOT stretch that gap —
  flag the span and let the assembly BAD-WORD RULE cut to montage for exactly
  that span, then resume at the next good hit. **Operational guard 0.7** until
  the 0.5–0.87 band is measured (one take with a moderate squeeze is the owed
  test — the untested band is 0.5–0.87×; S49's 0.87× is fine, 0.24/0.33× are
  fatal, so 0.5 is a judgement call, not a measured threshold).
- **Uniform fallback** when no targeting is needed (α≈1, drift≈0): OLA256.

## Do NOT build

- M1 PV as the core (worst identity on sung material).
- M4 global-gap slicing (superseded by M7 — same idea, no targeting).

## Validation bars (must pass, from the validation's own numbers)

1. **Hit identity:** max|diff| 0.0 and centre error 0.000 s on every hit, all test
   takes (direct comparison of each hit window at its placed position).
2. **Timing:** words-3+ onset RMS ≤ 100 ms on the validation takes (M7 measured
   69.3 ms; uniform methods 224–284 ms — the build must stay in M7's band,
   not the uniform band).
3. **Identity:** ≥ 18/23 words heard on the validation set with the guard active
   (M7 measured 18/23; the 5 misses are all guard-zone squeezes that must now
   flag instead of garble).
4. **Guard:** every gap with alpha < 0.5 is flagged (not stretched); the moderate-
   squeeze take (owed test) sets the guard precisely between 0.5 and 0.87.
5. **Fallback:** OLA256 path reproduces the prototype's identity (23/23) on the
   validation takes.
6. **Parity:** C11 output vs the Python prototype (tsm_proto.py / tsm_m4b.py)
   on the same takes — per-gap alphas and hit placements identical; stretched
   audio corr ≥ 0.99 vs the prototype's M7 output.
7. **Runtime:** faster than the Python prototype on the blade (1.5 shared CPUs,
   6 GB); target < 10 s per take-scale stretch (the prototype's grade run took
   ~1–2 h for 24 clips under load — the C11 core must not be the bottleneck).

## Owed before shipping the core

(a) One moderate-squeeze take to set the guard precisely (0.5–0.87 band).
(b) A listening check (MOS-style, ears not ASR) — the paper's SingingVoice
    caveat is about perceived quality, which the validation did not measure.
(c) Identity-phase-locked PV if PV is ever revisited — the librosa PV used in
    the validation lacks it.

## Inputs on disk

- `~/workspace/research_notes/tsm-driedger-2014/` — report.md (full method +
  results + analysis), tsm_proto.py, tsm_m4b.py (M7), tsm_asr_grade.py,
  tsm_grades.json, tsm_grades_partial.json (M7 grades), m4b_measurements.json
  (gap alphas, hit identity), stretch_measurements.json, stretched/ (24 files),
  winners_league.png.
- Validation takes: MV-14 S47/S49/S50/S52 (take audio + ledgered ASR word times
  + `SONG_WORDS.json` grid). S51 dropped (song times uncertain in the ledger).
- LEGO sources: the user's C modules (lego-harvest-scratch: wubuwizard, wubuos,
  www) — HPSS median filter, PV, OLA patterns; c11_mir FFT (sprint 4, corr
  1.000000 vs librosa); c11_voice (sprint 8, FAILED — do not reuse its voicing
  gate as a boundary source; the gate is unusable, bar 5).

## Deliverables

- `detection-research/SPRINT_2026-11-12_C11_TSM.md` — build report with the
  7 bars above, each PASS/FAIL stated plainly. Do NOT lower a bar if it fails.
- Code under `detection-research/c11_tsm/` (C11, libc+libm only, zero warnings,
  ASan-clean) + validation scripts + JSON outputs.
- DETECTION_FINDERS.md run entry.
- No commit, no Telegram, no video generation — parent owns the commit and
  the delivery. Never commit binaries, wavs, or the stretched/ outputs.
