# SPRINT_SCOPE.md — c11_casa (Slopcannon improvement loop 4, top-1)

**Sprint:** c11_casa — CASA correlogram + harmonic grouping + ideal binary mask
experiment (loop 4 top-1; loop 3 report §2 #2, loop 4 report §2 #1).
**Parent:** loop 4 report. **Goal:** decide whether a classical auditory-scene-analysis
front end can segregate the voice from MV-14's dense mix — the only remaining
principled route after vibrato (straight-tone chant), formants (mix spectrum
dominates) and spectral entropy (no separation on either track) all failed.
**Held bar — ≥80% of vocal-activity boundaries within ±0.5 s** (the bar sprint 8
failed; do NOT lower it). **Do NOT re-run sprint 8's calibration. Do NOT touch
c11_voice's code except to lego in its autocorrelation / YIN machinery.**

## 1. Problem

Sprint 8 proved YIN/pYIN + CPP + HNR medians do not separate sung from
instrumental on MV-14's dense mix (8/24 mix, 14/24 stem best of 150 combos).
Loop 3's vibrato failed fast (the chant is straight-tone: sung 2.55c vs
instrumental 3.32c). Loop 4's formant experiment failed (formant-motion medians
overlap, wrong direction at order 14; parameter-unstable at order 18) and its
birdsong-entropy decision failed (vocal-band entropy sung 0.9072 vs instrumental
0.9129, IQRs overlap; wrong direction on the full band and on the stem). The
stall's shape is now fully mapped: **every feature computed on the mixture
inherits the accompaniment's dominance.** The next sensor must *segregate* the
scene rather than measure the mixture. That is CASA.

## 2. Background (verified, cite in the sprint report)

- Bregman, Auditory Scene Analysis (1990): grouping principles — continuity in
  pitch/timbre, harmonic relations, common amplitude/frequency modulation,
  onset/offset synchrony.
- Licklider (1951): the correlogram — short-time autocorrelation per frequency
  channel; a 3-D function (channel × lag × time) in which components sharing
  common AM/FM are revealed.
- Slaney & Lyon (1990; Duda & Lyon, Asilomar): "components sharing common AM/FM
  are revealed" by the correlogram; "common amplitude modulation groups
  components into sound sources." The expensive residue to AVOID is Lyon's full
  cochlear model (cascade filterbank + AGC — the 1990 paper itself notes it is
  expensive to simulate on conventional hardware); the feasible residue is a
  correlogram on STFT magnitudes.
- Wang & Brown CASA + Shao et al. 2010 (Computer Speech and Language 24):
  two-stage monaural CASA estimating the **ideal binary mask** (retain a T–F
  unit iff the target is stronger than the interference in it). Stage 1
  segregates voiced portions by harmonicity via multipitch tracking and
  unvoiced portions by onset/offset analysis; stage 2 groups T–F units across
  time by speaker characteristics.

## 3. Inputs (all exist, all on disk)

- MV-14 mix + Demucs stem: `detection-research/c11_mir/separation_mv14/`
  (stem exists) + `c11_mir/mv14_16k.wav` (mix, 16 kHz).
- STFT: c11_mir's, validated corr 1.000000 vs librosa — lego it in.
- Autocorrelation / YIN machinery: c11_voice's — lego it in, do not rewrite.
  (pYIN's multi-threshold trough candidates are the seed for multipitch.)
- Boundary-scoring harness + ref segments: sprint 8's harness (same 12-segment
  Demucs-RMS-VAD ref, same ±0.5 s window). Carry sprint 8's own caveat: a
  perfect gate tops out at 20/24 because ref segments 11–12 are wordless-outro
  Demucs bleed.
- Song word times / ref vocal-activity segments: MV-14 `SONG_WORDS.json` +
  sprint 8's ref.

## 4. Build steps

1. **Experiment FIRST (before any gate code):** build the correlogram on the
   mix STFT magnitudes — per-channel autocorrelation over lags covering the
   vocal F0 range. **The experiment's question:** during sung spans, does the
   correlogram show a dominant peak at the voice's F0 lag that is absent (or
   subordinate to the accompaniment's lag) during instrumental spans? Plot the
   voice-lag peak strength across the track with the ref segments shaded.
   **If the voice-lag peak does not separate sung from instrumental spans on
   ≥80% of the ref segments, STOP, report FAIL FAST with the plot, do not
   build the gate.** A null result here is a result: it kills the CASA route
   and the vocal-activity gap has no classical sensor left — Demucs stays the
   segmenter and the c11_sep runner becomes the only separation work.
2. **Multipitch tracking (the hard part, stated honestly):** two periodic
   sources at once (voice + bass/brass). Seed the voice F0 from pYIN's
   trough candidates (sprint 8's validated mix track, corr 1.0000) and the
   accompaniment F0 from the correlogram's second peak. Decide which F0 is
   the voice's by harmonic-grouping continuity (Bregman: the voice's F0
   track is continuous across a phrase; the accompaniment's jumps with the
   chord). Report the multipitch confusion rate on the ref segments — if the
   voice/accompaniment F0s cannot be told apart on ≥80% of sung frames, the
   experiment fails at this step, not at the mask.
3. **Harmonic grouping + ideal binary mask:** group T–F units whose
   periodicity matches the voice F0 into the voice stream; emit the binary
   mask; boundaries from the mask's voice-stream activity (same RMS-VAD
   post-processing rules as sprint 8: merge gaps < 1.0 s, drop < 0.5 s, pad
   0.3 s).
4. **Absence check (the detector must be able to say "not here"):** on the
   wordless outro (≥128.20 s) and the intro (0.00–14.14), the voice-stream
   mask must read absent, not hallucinate a voice from the accompaniment's
   periodicity. A detector that cannot say "not here" cannot be trusted
   when it says "here."
5. **Boundary scoring:** same harness, same ref, same ±0.5 s window as
   sprint 8. Report boundaries within ±0.5 s as a fraction of 24 (and of 20,
   excluding the bleed segments — report both numbers, do not hide the
   denominator).

## 5. Validation bars (all must pass; the bar is held, not lowered)

- **Bar A (experiment):** the voice-lag peak separates sung from
  instrumental spans on ≥80% of the ref segments (16/20 clean ref; report
  the /24 number alongside). Fail-fast step: if step 1 fails, the sprint
  reports FAIL FAST with the correlogram plot and stops — that is a pass of
  the sprint's *method* and a fail of the *entry*. Do not build a gate on a
  flat peak.
- **Bar B (boundaries, only if A passes):** ≥80% of vocal-activity
  boundaries within ±0.5 s of the Demucs ref (≥16/20 on the clean ref;
  report the /24 number alongside).
- **Bar C (no contamination):** the voice-stream mask's activity during
  instrumental-only spans stays below the sung-span median (the
  accompaniment's periodicity must not leak into the voice stream).
- **Bar D (absence):** wordless outro + intro read absent (voice-stream
  activity below threshold), no hallucinated voice.
- **Bar E (honest scope):** if the multipitch step cannot tell the voice
  F0 from the accompaniment F0 on ≥80% of sung frames, report the confusion
  rate and stop — that is the experiment's finding, not a reason to tune
  thresholds until it passes.

## 6. Deliverables

- `c11_casa/` code (C11, lego'd STFT + autocorrelation/YIN + pYIN candidates)
  + Makefile + README.
- `c11_casa_validation.json` — voice-lag peak separation per ref segment,
  multipitch confusion rate, boundary scores (/24 and /20), absence-check
  numbers.
- `SPRINT_2026-11-12_C11_CASA.md` — report: method, numbers, the
  correlogram plot (or the fail-fast plot), what it replaces/enables (the
  mouth-open-vs-quiet gate calibration + CCA on the CASA curve + snapper
  stay-rule evidence — only if Bar B passes).
- Commit: code + Makefile + README + validation JSON + report. Do NOT commit
  binaries, wavs, stems, or curve JSONs over ~100 KB. Never `git add -A`;
  explicit globs; `git diff --cached` before commit.

## 7. Constraints (standing)

- Blade: 1.5 shared CPUs / 6 GB RAM, no GPU. The correlogram must run in
  minutes on MV-14, not hours.
- No video generation. No Telegram write. No skill edit (draft proposed edits
  only).
- Do not re-run sprint 8's calibration; reuse its harness and ref.
- Do not lower the bar. If Bar A fails, report the failure with the numbers —
  a failed sprint with honest numbers is worth more than a lowered bar.
- Heartbeat: append `<task> <UTC ISO> <one-line status>` to
  `~/workspace/goals/wubu-music-videos-from-suno-tracks/hidden_files/heartbeats/`
  every ~5 min (file `c11-casa.beat`, or the loop-4 file if the parent directs).

## 8. Queue after this sprint

- If Bar B passes: mouth-open-vs-quiet gate calibration + CCA AV-sync on the
  CASA curve (loop 1 #3 + loop 2 #3, both owed); snapper stay-rule patch using
  the CASA voice-stream activity as in-span evidence.
- If step 1 fails fast: the vocal-activity gap has no classical sensor left.
  Demucs stays the segmenter; the c11_sep runner (already scoped, bar <894 s)
  becomes the only separation work, and the sensor search moves to
  adoption-as-is (MDX-Net ONNX) rather than classical cores. Loop 5 takes
  the adoption branch.
- Either way: the G7 wrong-lyric gate (small build, no audio feature) and the
  R5 flow-interpolation build proceed on their own bars — neither is gated
  on CASA.
