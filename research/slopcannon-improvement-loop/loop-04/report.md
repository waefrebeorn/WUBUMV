# Slopcannon improvement loop 4 — report

**Date:** 2026-11-12 · **Coordinator:** a6fe92b4 · **Seed:** c11_vibrato FAILED FAST
(straight-tone chant) — the stall branch (user msg 252, msg 288, msg 313).
**Chain cap:** 3 hops, hop 2 crosses a category boundary. **Blind draw:** one, load-bearing (§8).
**Status:** research only. Code was run (two experiments + one probe, all measured),
no video generated, no commit, no Telegram write, no skill edit.

## Progress log (checkpoint lines)

- 2026-11-12 ~05:13 EST: loop 4 spawned (a6fe92b4). Read loop-03 report, vibrato
  sprint report, sprint-8 report in full.
- 2026-11-12 ~05:15 EST: disk inventory done. Ref: `c11_mir/hpss_mv14_ref.json`
  (12 segments, sung 1–10, bleed 11–12). Mix `c11_mir/mv14_16k.wav` on disk;
  stem 44k Demucs on disk; stem 16k regenerated via ffmpeg, md5
  `43d83ae22fc3424533c25a896942a455` — matches sprint 8's documented md5 exactly.
  venv (numpy 2.5.4 / scipy 1.17.1 / librosa 1.0.0) works.
- 2026-11-12 ~05:16 EST: snap files located. Stay-rule test uses sprint 8's
  validation-script definition: error indices are **1-based** (34, 56, 60, 112,
  162) into `snap_mix_mv14.json` (validate_bars2_6.py:159-161) — the sprint-8
  report's "0-based" prose conflicts with its own script; the script is
  authoritative. The 15-correct control set is not on disk; constructed here
  as words with |correction| ≤ 0.05 s, prob ≥ 0.9, on_peak (first 15 meeting
  the criteria, documented in the JSON).
- 2026-11-12 ~05:16 EST: TSM squeeze-guard check: the moderate-squeeze take
  (0.5–0.87 band) is STILL OWED — tsm-driedger-2014/SPRINT_SCOPE.md §63 lists
  it as owed work for c11_tsm. Loop 4 notes it; it does not do it.
- 2026-11-12 ~05:17 EST: entropy experiment ran — FAIL on both bands, both
  tracks (see §2 #2). Stay-rule test: entropy cannot serve as in-span evidence.
- 2026-11-12 ~05:19 EST: formant experiment ran — FAIL (see §2 #1). Controls
  validate both pipelines (synthetic vowel vs gliding brass 8.7×; tone/noise/
  harmonic-stack entropy 0.20/0.98/0.49). One control bug found and fixed
  mid-run (noise-burst window measured silence; corrected to the burst window,
  H 0.98 — the JSON carries the corrected values).
- 2026-11-12 ~05:21 EST: break-the-sync probe RUN (not just specified) — PASS
  (see §3). Loop 3 mislabeled the phrase: "Fourth law" is MV-13's hook, not
  MV-14's; MV-14's real repeats are "Clip it, post it" (×3). Probe run on the
  real repeats.
- 2026-11-12 ~05:23 EST: blind draw — jitter/shimmer (§8). CASA scope written
  (loop-04/SPRINT_SCOPE.md). Report complete.

## 0. The stall, restated (what loop 4 routes around)

Sprint 8 failed the voicing gate structurally (8/24 mix, 14/24 stem best of 150
combos vs the ≥80% bar; medians within 0.04 dB; recall ~0.52–0.55). Loop 3
ranked vibrato top-1; the c11_vibrato sprint failed fast — the chant is
straight-tone (sung 2.55c vs instrumental 3.32c; stem voice itself 2.68c).
Loop 4 ran the stall branch loop 3 seeded: the formant experiment and the
birdsong-entropy decision, in parallel. **Both failed — and both failed on the
stem too, which is the decisive detail.** The stall is no longer "the mix is
too dense for this feature"; it is "the chant voice itself carries no
separable signature in any of the three classical voice features tried"
(vibrato, formant stability, spectral entropy). What remains is the one
family that does not ask the mixture for a voice signature at all: separation
first (CASA), or adoption-as-is (MDX-Net ONNX). The bar is HELD, not lowered.
Do not re-run any of these experiments' calibrations.

## 1. Hop chain (audit data)

- **Seed:** vibrato fail-fast — MV-14's chant is straight-tone; the voice
  carries no 5–7 Hz modulation to detect.
- **Hop 1 (the other half of the voice shelf, measured this loop):** formant /
  LPC tracking (loop 3 #6) + birdsong spectral entropy (loop 3 #9, sprint 8
  rec #2). Both run as experiments with stated bars, on mix and stem, with
  synthetic controls. Both fail — see §2.
- **Hop 2 (CATEGORY CROSS — measure the mixture → segregate the scene):**
  CASA correlogram + harmonic grouping + ideal binary mask (loop 3 #2), scoped
  as the next sprint in loop-04/SPRINT_SCOPE.md. The cross was made in loop 3;
  loop 4 executes it as the sprint scope because the hop-1 experiments left
  nothing else standing.
- **Hop 3 (back to the MV):** G7 wrong-lyric gate (small build, no audio
  feature — the highest-certainty deliverable left) + R5 flow interpolation
  (assembly rescue, routes around the gap) + the break-the-sync probe, RUN
  this loop instead of specified (§3) + the snapper stay-rule verdict
  (still no in-span evidence signal — §2 #2).

Chain cap reached. No DONE node re-searched. No BAN_LIST endpoint banked.

## 2. Ranked entries

### #1 — CASA: correlogram + harmonic grouping + the ideal binary mask (TOP-1 — sprint scoped in SPRINT_SCOPE.md)

**What it is.** Loop 3 §2 #2, carried verbatim in scope: stop asking "is the
voice present in this frame" and *segregate the scene* — STFT magnitudes →
per-channel autocorrelation (correlogram) → harmonic grouping by common F0 →
ideal binary mask → boundaries off the voice stream's mask. The scope is in
loop-04/SPRINT_SCOPE.md with the experiment-first bar held: the voice-lag peak
must separate sung from instrumental spans on ≥80% of the ref segments before
any gate build; multipitch confusion rate reported as its own finding; absence
check on the wordless outro + intro.

**Why it is top-1 now.** It is the only entry left whose failure mode is not
already measured. Vibrato, formants, entropy, CPP/HNR, and YIN-voicing have
all failed on MV-14 — four of them on the stem too, which rules out "the mix
is hiding it" as the explanation. CASA is the only classical family that
unmixes instead of measuring the mixture. Its hard part is honest and stated
in the scope (multipitch tracking: voice + bass/brass at once), and its
fail-fast step is built in (step 1 kills the sprint in a day if the voice-lag
peak does not separate).

**What it replaces / enables.** Replaces Demucs as the segmenter *if* it ever
reaches the bar — the pipeline's heaviest dependency (Demucs 894 s/track;
MDX-Net ONNX 1,592 s). Enables: the mouth-open-vs-quiet gate calibration
(loop 1 #3) + CCA AV-sync (loop 2 #3) on the CASA curve, and the snapper
stay-rule patch using the CASA voice-stream activity as in-span evidence —
all three currently blocked on a sensor that passes the held bar.

### #2 — Birdsong spectral entropy: MEASURED, FAIL (loop 3 #9 — the decision is made)

**What it was.** Sprint 8's rec #2, loop 3 #9: spectral entropy as a note-vs-
noise feature — a sustained sung vowel is low-entropy (peaky spectrum);
drums/noise are high-entropy; brass sits in between. Bar: entropy (mix)
separates sung from instrumental with non-overlapping IQRs; sung < instrumental,
Mann-Whitney p<0.01. It was also the next candidate for the snapper stay-rule
evidence after vibrato died.

**What was measured.** STFT 1024-sample frame / 10 ms hop / Hann, centred
(sprint 8's framing). Entropy H = −Σ p log₂ p / log₂ N, two bands (full 0–8 kHz;
vocal 300–4000 Hz), RMS gate (frames < 1% of max frame RMS excluded; coverage
sung 1.00 / instr 0.99 on the mix). Synthetic controls validate the pipeline:
pure tone H 0.196, white noise 0.978, harmonic stack (f0 220 Hz) 0.489, noise
burst 0.978 — the measurement works; the material does not separate.

| Measure | Mix vocal band | Mix full band | Stem vocal band |
|---|---|---|---|
| Sung median [IQR] | **0.9072 [0.8803, 0.9291]** | 0.8863 [0.8475, 0.917] | 0.8863 [0.8475, 0.917] |
| Instrumental median [IQR] | 0.9129 [0.8901, 0.9317] | **0.8461 [0.7959, 0.8813]** | 0.8461 [0.7959, 0.8813] |
| Mann-Whitney p (sung < instr) | 1.8e-10 | 1.0 | 1.0 |

The vocal band is *statistically* significant (p=1.8e-10) on a 0.006 effect
size with IQRs overlapping almost completely — a large-n artifact, useless
as a separator. The full band is the WRONG DIRECTION (sung entropy higher
than instrumental). Per-segment medians sit 0.87–0.92 across all 10 sung
segments — no segment approaches a low-entropy regime. **And the stem fails
the same way** (vocal band sung 0.8863 > instr 0.8461): the isolated voice
is more entropic than the stem's residual bleed. The hypothesis fails at the
root — a chant voice with consonants, rhythmic delivery, and room is not a
sustained vowel, even isolated.

**Stay-rule verdict (the second question the experiment had to answer):**
entropy at the snapped position — errors median 0.9179 vs correct 0.9038,
ranges overlapping fully (errors 0.847–0.933, correct 0.843–0.945). Span-min
(tonal dip inside the ASR span) — errors 0.8392 dip LOWER than correct 0.8558,
the wrong direction for a veto. **Entropy cannot serve as the snapper
stay-rule in-span evidence.** The stay-rule patch still has no peak-evidence
signal. The remaining candidates are the snapper's own vocal-flux curve
(sprint 8's recommendation) or CASA's voice-stream activity if #1 passes.

**Verdict: FAIL. Do not scope a sprint. Do not re-run.**

### #3 — Formant / LPC tracking: MEASURED, FAIL (loop 3 #6 — the decision is made)

**What it was.** Loop 3 #6: formants are the vocal tract's resonances — a sung
vowel holds stable F1/F2 across its duration; instrumental spectra move
differently. The discriminative idea is formant *stability* (low frame-to-
frame F1/F2 variance) during a sustained vowel. It needs no pitch tracking —
LPC is a filter computation — which is why it survived the stall's root cause
(the voicing decision) on paper.

**What was measured.** 25 ms Hamming window / 10 ms hop / pre-emphasis 0.97,
16 kHz. LPC via autocorrelation + Levinson-Durbin; formants from LPC
polynomial roots (bandwidth < 400 Hz, 200–4000 Hz); F1/F2 = two lowest.
Feature M = |ΔF1| + |ΔF2| per hop, smoothed ~100 ms. Primary LPC order 14;
order 18 as a sensitivity check. Synthetic controls validate the pipeline:
fixed-formant vowel M=38.34 vs gliding-formant brass M=332.34 (8.7×) —
the measurement separates stable from gliding formants when they exist.
White noise yields no formants (correct).

| Measure | Mix order 14 | Mix order 18 | Stem order 14 |
|---|---|---|---|
| M sung median [IQR] | **386.83 [100.08, 791.22]** | 465.08 [168.73, 820.22] | **377.83 [101.30, 752.76]** |
| M instr median [IQR] | 290.95 [127.14, 754.83] | 626.42 [349.68, 1027.21] | 103.83 [66.98, 312.36] |
| Mann-Whitney p (sung < instr) | 0.52 | 1.0e-37 | 1.0 |
| Frac sung below instr median | 0.4423 | 0.6315 | 0.2574 |
| Coverage (sung / instr) | 0.293 / 0.190 | 0.671 / 0.524 | 0.577 / 0.138 |

Order 14 (primary): wrong direction, p=0.52, IQRs overlap — no separation at
all. Order 18: right direction with a significant p-value, but IQRs still
overlap heavily and only 63% of sung frames sit below the instrumental
median — and it *contradicts* order 14's direction on the same track, which
is itself evidence the feature is unstable to a free parameter, not a robust
sensor. **And the stem fails the same way** (order 14 sung 377.83 vs instr
103.83, wrong direction, p=1.0): the isolated voice's formants move more
than the residual bleed's spuriously stable poles. The F1/F2 *values* do not
separate either (mix F1 sung 931.92 vs instr 952.33; F2 2517.71 vs 2502.45 —
the mixture's formants are the mixture's). Per-segment M medians range
93.9–570.33 across sung segments — the feature varies more between segments
than between classes. Coverage is low on the mix at order 14 (29% of sung
frames yield F1+F2 at all): the dense mix often has no clean formant pair.

**Verdict: FAIL. Do not scope a sprint. Do not re-run.** Formants join
vibrato as a dead sensor for MV-14's chant — and the parameter instability
(order 14 vs 18 disagreeing in direction) is recorded as a warning for any
future formant work on dense mixes.

### #4 — G7 wrong-lyric gate (small build — the highest-certainty deliverable left)

**What it is.** Loop 3 §2 #5, unchanged: a take singing the wrong part of the
song has no gate. Word-set overlap between the take's ASR words and the
scene's planned words: overlap < 0.5 → REJECT, with a hand-check override for
homophones and near-identical choruses (provenance quarantine for identical
choruses). Validation bar (unchanged): construct positives by cross-pairing
the 65 KEEP takes against every other scene's planned words (must score
< 0.5), own-pairs must score ≥ 0.5 with **zero false REJECTs**; plus the real
positive MV-2 S04 t3 (proven: t3 sang 30–40 s lyrics at 43–48 s; t4 covers
the window, LCS 15/19) and the S21 candidate pending verification.

**Why it ranks #2 now.** It needs no audio feature, no sensor, and no
separation — the only entry in the loop whose inputs already exist and whose
bar can pass this week. It is the first QC check that reads *what* the take
sings rather than how it looks or moves. The cross-pairing fixture becomes
standing QC: every future volley's takes get cross-paired automatically, so a
wrong-segment take cannot ship silently again (MV-2 proves it happens;
MV-14's ledger cannot distinguish "doesn't happen" from "nobody caught it").

**Status:** not built in this loop (research only). Scoped as a small build —
QC script + ledger rule, not a sprint.

### #5 — R5 flow interpolation for BAD-WORD spans (build — routes around the gap)

**What it is.** Loop 3 §2 #4, unchanged: symmetric-flow MCFI (Raket et al.
2012) — synthesize the missing motion between the good frames on either side
of a bad word instead of cutting to montage. C11 Farneback exists (sprint 7,
validated vs cv2); the build is the warp/blend/hole-fill pipeline plus the
symmetric-flow estimation pass. Bar (unchanged): delete a 0.3–0.5 s span from
a KEEP take, interpolate it back — M6 in KEEP range + eye can't tell +
interpolated mouths must not read as a different word — and at least as clean
as ffmpeg `minterpolate` mci on the same span.

**Why it ranks here.** It is unaffected by the vocal-activity gap: it routes
around the gap's consequence in assembly instead of through it. It does not
need a sensor. If it passes, the BAD-WORD RULE gains an "interpolate first,
cut second" branch for short spans — which is the only repair path for the
takes whose only defect is one bad word.

**Status:** not built in this loop. Scoped as a build, on its own bar.

### #6 — R8 jitter/shimmer: the blind-drawn entry (TEST, not a rescue)

**What it is.** Loop 3 §2 #3's second half — jitter (cycle-to-cycle period
variability) and shimmer (cycle-to-cycle amplitude variability). The
hypothesis: the sung voice's cycle irregularity differs from the
accompaniment's — brass is very regular, drums are aperiodic, the voice sits
between with *structured* irregularity. Loop 3 drew "voice break degree";
loop 4 drew "jitter/shimmer" (§8) — the draw splits R8 across the two loops,
and this entry is the jitter/shimmer half with its own bar.

**Why it stays a test.** The validity pre-check must pass before any boundary
scoring: jitter/shimmer computed on MV-14's mix must satisfy Titze's
conditions (Type 1 periodicity, SNR > 30 dB) on the sung spans. It almost
certainly fails on this material — and now more likely than in loop 3, for a
reason loop 4 measured: the chant is straight-tone (vibrato dead) and its
formants move (formant experiment dead), which means the voice on this track
has no stable periodic structure for a perturbation measure to grip. The
measurement is a day, not a sprint, and a failed pre-check is a result:
it closes the last leg of the voice-quality shelf.

**Validation bar (held).** Pre-check first (Titze conditions on sung spans);
only if it passes, boundaries ≥80% within ±0.5 s. If the pre-check fails,
report the failure with the numbers — do not proceed to boundary scoring on
an invalid measure.

### Also carried (not ranked — status notes)

- **c11_sep separation runner:** already scoped (wubuwizard report §6, bar
  <894 s, stem corr ≥0.95, boundaries ±0.5 s, active/silent ≥100×). If CASA
  fails fast, this becomes the only separation work: make Demucs/MDX cheap
  rather than replacing it. Not re-scoped here.
- **Mouth-open-vs-quiet gate (loop 1 #3) + CCA AV-sync (loop 2 #3):** still
  blocked. Both wait on the first sensor that passes the held bar — now
  CASA (#1) or nothing classical. Neither is unblocked by this loop.
- **Snapper stay-rule patch:** still unbuildable. Three candidate in-span
  signals are now dead on MV-14 (c11_voice curve, vibrato depth, spectral
  entropy). Remaining candidates: the snapper's own vocal-flux curve, or
  CASA's voice-stream activity if #1 passes.
- **TSM squeeze-guard band measurement:** STILL OWED. The moderate-squeeze
  take (0.5–0.87 band) has not landed; tsm-driedger-2014/SPRINT_SCOPE.md §63
  lists it as owed work for c11_tsm. Loop 4 checked; it does not do it.
- **wubu_synth residue (loop 3 #8):** unchanged — a `c11_scaffold` template
  library is a build, scoped only if a sprint's scaffolding is ever written
  twice the same way. Never from wubu_synth as-is.
- **Slopcore vehicle-template changes (loop 3 #7):** unchanged — proposed
  skill edits (kinds system, {END} footer, macro-managed identity, pilot
  pattern), parent applies. No skill edited this loop.

## 3. The per-loop break-the-sync probe (loop 4) — RUN, PASS

**The repeated-chorus collapse probe, run this loop.** Loop 3 specified it;
loop 4 ran it on MV-14's snapper output (`snap_mix_mv14.json`, 212 words)
against the song words (`SONG_WORDS.json`).

**Correction to loop 3's probe statement:** loop 3 said "MV-14's C2/C3
'Fourth law' chant runs to FOUR repeats." That is wrong on the material —
"Fourth law" is **MV-13's** hook, not MV-14's. MV-14's actual repeated phrase
is **"Clip it, post it"** — three occurrences (C2 ×2 + Final ×1). The probe
was run on MV-14's real repeats, which is the correct reading of its intent
(the snapper is MV-14's timing authority; the question is whether its times
advance through repeats or collapse onto repeat 1).

| Repeat | Song idx | ASR starts | Snapped starts | Corrections |
|---|---|---|---|---|
| 1 (C2) | 115 | 77.78, 78.54, 78.94, 79.26 | 77.856, 78.528, 78.992, 79.328 | +0.076, −0.012, +0.052, +0.068 |
| 2 (C2) | 123 | 83.32, 83.76, 84.08, 84.48 | 83.248, 83.76, 84.08, 84.416 | −0.072, 0.0, 0.0, −0.064 |
| 3 (Final) | 173 | 112.16, 112.68, 113.0, 113.4 | 112.16, 112.688, 113.136, 113.488 | 0.0, +0.008, +0.136, +0.088 |

**Result: PASS.** Word times advance through all three repeats (max
|correction| 0.136 s, within the ±0.1 s anchor tolerance modulo the snapper's
own ±0.14 s spread on these words). No snapped time lands within ±0.1 s of
an earlier repeat's ASR time. Global check across all 212 words: **0 collapse
hits** — no snapped word lands on an earlier identical word's time. The
snapper does not glue repeats. The monotonic-forward-walk fix (loop 1 #1) is
not needed on this evidence; the timing authority stands on repeats.

**Follow-up (not run here):** MV-13's "Fourth law" ×4 repeats remain an unrun
probe for MV-13's snapper data — different track, different snapper output.
Loop 5 may run it if MV-13's snapper run is located.

## 4. Loop-5 seed

1. **CASA experiment first.** The c11_casa sprint runs the experiment-first
   bar (voice-lag peak separation on ≥80% of ref segments). If it passes,
   the full gate is built on the same held bar — and the mouth-open-vs-quiet
   gate, CCA AV-sync, and snapper stay-rule patch all unblock on the CASA
   curve, in that order.
2. **If CASA fails fast:** the vocal-activity gap has no classical sensor
   left. Loop 5 takes the adoption branch: MDX-Net ONNX adopt-as-is as the
   segmenter (wubuwizard run 14, already proven) + the c11_sep runner as the
   only separation work. The sensor search stops; the pipeline accepts a
   neural separator and spends its effort making it cheap.
3. **R8 jitter/shimmer test runs either way** (a day of measurement, validity
   pre-check first) — it closes the voice-quality shelf regardless of CASA's
   outcome.
4. **G7 + R5 proceed on their own bars** regardless of CASA: G7's
   cross-pairing fixture becomes standing QC; R5's interpolation results feed
   the BAD-WORD RULE ("interpolate first, cut second" for 0.3–0.5 s spans).
5. **TSM squeeze-guard band measurement** is still owed — loop 5 checks again
   whether the moderate-squeeze take landed.
6. **MV-13 "Fourth law" ×4 repeat probe** — run against MV-13's snapper data
   if it is located.

## 5. Proposed skill edits (draft only — parent applies, no skill edited this loop)

1. **Vehicle template (carried from loop 3 #7, unchanged):** kinds system
   (lips / motion / insert), the {END} prohibition footer on every vehicle,
   macro-managed identity, pilot pattern. Source: slopcore PROMPTS.md, measured.
2. **BAD-WORD RULE (conditional on R5 passing):** "interpolate first, cut
   second" branch for 0.3–0.5 s spans — only after the M6 + eye + mouth tests pass.
3. **QC gates:** add G7 (word-set overlap < 0.5 → REJECT, cross-pairing
   positives as the fixture, homophone hand-check override) once §2 #4's
   validation passes.
4. **Snapper stay-rule (conditional):** CASA voice-stream activity as the
   in-span peak-evidence signal — only once CASA passes its bar. Vibrato
   depth and spectral entropy are both dead as candidates; do not list them.

## 6. Honest scope

- **Code was run:** two experiments (entropy, formant) + one probe
  (repeated-chorus collapse), all measured on MV-14's mix and Demucs stem,
  with synthetic controls. Every number in this report is in
  `loop4_validation.json`, reproduced from `entropy_experiment.json` and
  `formant_experiment.json` (scripts in loop-04/, inputs on disk, unchanged).
- **Two experiments failed — and failed on the stem too.** That is the
  loop's main finding: the stall is not mix-dominance, it is the chant voice
  itself carrying no separable signature in these features.
- **One control bug found and fixed mid-run:** the entropy noise-burst
  control initially measured the silent tail (H 0.00); corrected to the burst
  window (H 0.978). The JSON carries the corrected values; the original
  wrong value is recorded here, not hidden.
- **One index-definition conflict found and resolved:** sprint 8's report
  calls the 5 snap errors "0-based indices in snap_mix_l2.json" while its
  own validation script uses 1-based indices into snap_mix_mv14.json. The
  script is authoritative; the stay-rule test used 1-based indices into
  snap_mix_mv14.json. The 15-correct control set is not on disk; it was
  constructed here (|correction| ≤ 0.05 s, prob ≥ 0.9, on_peak, first 15)
  and the rule is recorded in the JSON.
- **One probe-statement correction:** loop 3's "Fourth law" phrase belongs
  to MV-13, not MV-14; the probe ran on MV-14's real repeats ("Clip it,
  post it").
- **Web-verified claims:** formant/LPC method (Praat formant tracker;
  VoiceSauce; Vienna Talk singing-voice toolbox); spectral entropy as a
  note-vs-noise feature (birdsong syllable-splitting literature, loop 2 #2);
  CASA (Bregman 1990; Licklider 1951; Slaney & Lyon 1990; Shao et al. 2010);
  MCFI (Raket et al. 2012); jitter/shimmer validity (Titze 1995; Deliyski
  2005; Patel et al. 2018 — carried from loop 3). Full citations in
  SOURCES.md entries 56+ (loop 3's file; loop 4 adds no new source file —
  see the gap note in §6 of loop 3, still open: no shared SOURCES.md exists).
- **Measured on disk (reproducible):** entropy — mix vocal sung 0.9072 vs
  instr 0.9129, full-band wrong direction, stem same failure; formant — mix
  order-14 M sung 386.83 vs instr 290.95 (wrong direction), order-18
  parameter-unstable, stem same failure; probe — 0 collapse hits, 212 words.
- **What this loop did NOT do:** no re-run of sprint 8's calibration; no
  lowering of the 80% bar; no gate built from a failed experiment; no video
  generation; no commit; no Telegram write; no skill edit.

## 7. Top 5 (for the parent's report)

1. **CASA correlogram + ideal binary mask** — the only principled route left;
   experiment-first scope written (loop-04/SPRINT_SCOPE.md). If the voice-lag
   peak does not separate on ≥80% of ref segments, the classical sensor search
   is over.
2. **G7 wrong-lyric gate (small build)** — word-set overlap < 0.5 → REJECT;
   real positive MV-2 S04 t3 + cross-pairing fixture; zero false REJECTs on
   own-pairs. Highest-certainty deliverable in the loop.
3. **R5 flow interpolation (build)** — symmetric-flow MCFI; Farneback exists;
   routes around the vocal-activity gap in assembly. Bar: M6 in KEEP range +
   eye can't tell + mouths don't read as another word.
4. **R8 jitter/shimmer (blind draw, test)** — validity pre-check first
   (Titze Type-1 / SNR > 30 dB); expected to fail on the straight-tone
   chant, measured either way. Closes the voice-quality shelf.
5. **c11_sep separation runner (already scoped)** — the fallback if CASA
   fails: make Demucs/MDX cheap (<894 s) rather than replacing it.

## 8. Blind draw (method audit)

Drawn with `secrets.choice` from a 12-item candidate pool of loop-4 ideas:
`correlogram peak, formant stability, entropy dip, voice-break degree,
jitter/shimmer, symmetric flow, kinds system, macro identity, pilot pattern,
cross-pairing, squeeze guard band, mouth-open gate`.
**Draw: "jitter/shimmer"** (first draw accepted, no discard). Checked: 0
whole-word occurrences of any pool phrase in
`~/workspace/wubutv-network/ideas/BAN_LIST.md` (3,185 lines); not among
banked form ideas (COMPASS, VESSEL, CRADLE SHOT, SATELLITE ORBIT, HARBOR,
RIVER, FEATHER).
**Deviation, stated plainly:** loop 3 drew "voice break degree" and loop 4
drew "jitter/shimmer" — the two halves of the same R8 entry, split across
two loops' draws. The draw is load-bearing in the method's sense: it forced
the jitter/shimmer half into a full entry (§2 #6) with its own validation bar
instead of letting it dissolve into voice-break degree as an afterthought.
The pool reuses items from loop 3's pool (correlogram, formant stability,
entropy dip, voice-break degree, symmetric flow, kinds system, macro identity,
pilot pattern, cross-pairing, squeeze guard band, mouth-open gate) because
those are still the live candidates; the draw is fresh per loop.
