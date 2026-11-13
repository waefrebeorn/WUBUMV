# SPRINT_SCOPE.md — c11_vibrato (Slopcannon improvement loop 3, top-1)

**Sprint:** c11_vibrato — vibrato-signature vocal-activity sensor.
**Parent:** loop 3 report §2 #1. **Goal:** a vocal-activity curve for the MV-14 mix that reaches the
**held bar — ≥80% of vocal-activity boundaries within ±0.5 s** (the bar sprint 8 failed; do NOT lower it).
**Do NOT re-run sprint 8's calibration. Do NOT touch c11_voice's code except to lego in its pYIN.**

## 1. Problem

Sprint 8 (c11_voice) proved YIN/pYIN + CPP + HNR medians do not separate sung from instrumental on
MV-14's dense mix (boundaries 8/24 mix, 14/24 stem best of 150 combos; medians within 0.04 dB; recall
~0.52–0.55). The mix's periodicity is dominated by the accompaniment. The one thing sprint 8 proved
works ON THE MIX is the pYIN F0 track itself (corr 1.0000 vs librosa, gross error 0.00%). This sprint
does not detect the voice's pitch — it detects its *wobble*: the 5–7 Hz periodic modulation of F0
(vibrato) that a sung vowel carries and the accompaniment does not.

## 2. Background (verified, cite in the sprint report)

- Sundberg: vibrato = F0 undulation at 5–7 Hz, extent ~±1 semitone (~50–100 cents each side).
- Nix et al. 2016 (n=75 vocal majors): mean vibrato rates 5.0–5.16 Hz across five vowels, SD ~0.6–0.7 Hz;
  extent 50–120 cents peak-to-peak; <20 cents = straight tone, >150 cents = excessive; <4 Hz = wobble,
  >7 Hz = bleat.
- Titze reflex-resonance model: vibrato rate largely outside conscious control (physiological signature).
- Vibrato MASKS small random perturbations (jitter/shimmer) — the sung vowel's perturbation readings
  are dominated by its vibrato. That is why vibrato is the sensor and jitter/shimmer is not.
- MV-14 is a *chant* track — chant may be straight-tone. **The sprint's first measurement decides
  whether the sprint continues** (see §4, step 1).

## 3. Inputs (all exist, all on disk)

- MV-14 mix + Demucs stem: `detection-research/c11_mir/separation_mv14/` (stem exists).
- pYIN F0 track on the mix: c11_voice's pYIN — lego it in, do not rewrite. (Sprint 8 bar 1, mix leg:
  corr 1.0000, gross 0.00% — the validated starting point.)
- Boundary-scoring harness + ref segments: sprint 8's harness (same ref, same ±0.5 s window). Carry
  sprint 8's own caveat: a perfect gate tops out at 20/24 because ref segments 11–12 are wordless-outro
  Demucs bleed.
- Song word times / ref vocal-activity segments: MV-14 `SONG_WORDS.json` + sprint 8's ref.

## 4. Build steps

1. **Day-1 falsifier (BEFORE any gate code):** compute the mix F0 track (lego'd pYIN) and the
   vibrato-band modulation depth (detrend → bandpass 4–8 Hz → RMS in cents) per frame. Plot depth
   across the track. **If the depth is flat everywhere (no 5–7 Hz modulation in the sung spans),
   the chant is straight-tone — STOP, report FAIL FAST with the plot, do not build the gate.**
   A null result here is a result: it kills the entry and routes loop 4 to CASA.
2. **Modulation-depth curve:** detrend the F0 contour (remove slow pitch drift), bandpass 4–8 Hz,
   modulation depth = RMS of the bandpassed contour in cents, per frame (hop ~10 ms). Smooth
   (~100 ms) → vocal-activity curve.
3. **Threshold + boundaries:** threshold the depth curve (calibrate the threshold on MV-14: sung-span
   median vs instrumental-span median — report both, with IQRs); hysteresis (on/off thresholds) to
   avoid chatter; emit boundaries.
4. **Synth-LFO confound check:** measure modulation depth on the instrumental-only spans. If any
   instrumental span shows 5–7 Hz modulation above the sung median, the feature is contaminated —
   report it, do not claim the bar.
5. **Vibrato-absence check (the detector must be able to say "not here"):** on a known straight-tone
   or instrumental span, the curve must report *absent* (depth below threshold), not hallucinate
   modulation. A detector that cannot say "not here" cannot be trusted when it says "here."
6. **Boundary scoring:** same harness, same ref, same ±0.5 s window as sprint 8. Report boundaries
   within ±0.5 s as a fraction of 24 (and of 20, excluding the bleed segments — report both numbers,
   do not hide the denominator).

## 5. Validation bars (all must pass; the bar is held, not lowered)

- **Bar A (separation):** median vibrato-band modulation depth on sung spans > median on instrumental
  spans, with non-overlapping interquartile ranges — on the MIX F0 track (the stem test is trivial
  and does not count).
- **Bar B (boundaries):** ≥80% of vocal-activity boundaries within ±0.5 s of the Demucs ref
  (≥16/20 on the clean ref; report the /24 number alongside).
- **Bar C (no contamination):** no instrumental-only span exceeds the sung median depth (synth-LFO check).
- **Bar D (absence):** straight-tone/instrumental spans report below threshold (no hallucinated vibrato).
- **Bar E (honest scope):** if step 1 fails fast, the sprint reports FAIL FAST with the depth plot
  and stops — that is a pass of the sprint's *method* and a fail of the *entry*. Do not build a gate
  on a flat curve.

## 6. Deliverables

- `c11_vibrato/` code (C11, lego'd pYIN + new modulation-depth pass) + Makefile + README.
- `c11_vibrato_validation.json` — depth medians/IQRs (sung vs instrumental, mix), boundary scores
  (/24 and /20), confound-check numbers, absence-check numbers.
- `SPRINT_2026-11-12_C11_VIBRATO.md` — report: method, numbers, the day-1 plot (or the fail-fast
  plot), what it replaces/enables (mouth-open-vs-quiet gate calibration + CCA on the vibrato curve +
  snapper stay-rule evidence — only if Bar B passes).
- Commit: code + Makefile + README + validation JSON + report. Do NOT commit binaries, wavs, stems,
  or curve JSONs over ~100 KB. Never `git add -A`; explicit globs; `git diff --cached` before commit.

## 7. Constraints (standing)

- Blade: 1.5 shared CPUs / 6 GB RAM, no GPU. The modulation pass must run in seconds on MV-14.
- No video generation. No Telegram write. No skill edit (draft proposed edits only).
- Do not re-run sprint 8's calibration; reuse its harness and ref.
- Do not lower the bar. If Bar B fails, report the failure with the numbers — a failed sprint with
  honest numbers is worth more than a lowered bar.
- Heartbeat: append `<task> <UTC ISO> <one-line status>` to
  `~/workspace/goals/wubu-music-videos-from-suno-tracks/hidden_files/heartbeats/` every ~5 min
  (file `c11-vibrato.beat`, or the loop-3 file if the parent directs).

## 8. Queue after this sprint

- If Bar B passes: mouth-open-vs-quiet gate calibration + CCA AV-sync on the vibrato curve (loop 1 #3
  + loop 2 #3, both owed); snapper stay-rule patch using vibrato depth as in-span evidence.
- If step 1 fails fast: loop 4 runs the formant experiment + birdsong-entropy decision in parallel
  and scopes the CASA correlogram experiment as the next sprint.
