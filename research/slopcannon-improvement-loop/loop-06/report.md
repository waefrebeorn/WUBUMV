# Slopcannon improvement loop 6 — report

**Date:** 2026-11-12 · **Coordinator:** session 35b1f020-8991-48b9-b862-063215ab6a8d
**Seed:** c11_sep PASS all 4 bars (loop 5 top-1, committed a2b435bd) — the adoption
branch, continued. **Chain cap:** 3 hops, hop 2 crosses a category boundary.
**Blind draw:** one, load-bearing (§11).
**Status:** research + three in-loop experiments run + top-1 sprint spawned,
verified in full, and DONE (see §1). No video generated, no commit, no Telegram
write, no skill edit.

## Progress log (checkpoint lines)

- 2026-11-12 ~09:47 EST: loop 6 spawned. Read loop-05 report, loop5_validation.json,
  c11_sep scope + sprint report in full.
- 2026-11-12 ~09:50 EST: c11_sep landing verified on disk from
  `stage4_fulltrack_validation.json` (corr 0.9675, max |dStart| 0.21 s, 242.7×,
  840.4 s) — not from the report's prose (§0).
- 2026-11-12 ~09:55 EST: disk inventory done. Stems on disk: c11
  (`c11_sep/c11_vocals.wav`), ONNX MDX (`wubuwizard-cpu-sep/mdx_vocals_full.wav`),
  Demucs (`c11_mir/separation_mv14/mv14_44k_(Vocals)_htdemucs.wav`); MV-11 Demucs
  stem also on disk (`MV-11.../analysis/tests/separation/`). No MV-13 snapper
  output existed; MV-13 16k wav did not exist. TSM scope read (c11_tsm is the
  parent's parallel sprint — not duplicated here).
- 2026-11-12 ~09:57 EST: Kevin Bacon hop 1 (web) — singing-voice detection
  literature: separation-preprocessing + temporal smoothing (Zhang et al. LRCN),
  attribute-based vocal-section segmentation (Sundaram & Narayanan 2006),
  VAD-via-separation (Doukas et al. 1997), singing-robust SAD (Grundhuber 2025).
  Hop 2 (web) — DTW forced alignment: production pattern is MDX-Net separation
  ahead of CTC alignment constrained by DTW; landmark-DTW (Sharma & Li 2019,
  −47.5% word-boundary error). No new slermable core beats RMS-VAD on the stem.
- 2026-11-12 ~10:00 EST: MV-13 snapper run (both flavours, 394 words) +
  Fourth-law probe RUN — PASS with one adjacent double-bark artifact (§2).
- 2026-11-12 ~10:02 EST: stem-snap comparison RUN (sprint-5-specified FIRST
  follow-up, never run) — FAILS the spec agreement test; the stem lattice
  finding (§4). MV-13 probe + stem-snap scripts in loop-06/.
- 2026-11-12 ~10:05 EST: blind draw — CCA AV-sync on MDX stem activity (§11).
  Leg A (audio side) RUN — premise HOLDS (sung envelope peaks 3.125 Hz). Leg B
  (one-take visual prototype, MV-13 S25 t2) RUN — FAIL, mechanism diagnosed (§5).
- 2026-11-12 ~10:10 EST: TSM squeeze-guard check — moderate-squeeze take STILL
  OWED; c11_tsm owns it (its scope bar 4) (§6).
- 2026-11-12 ~10:12 EST: MDX_STEMACT sprint scoped (loop-06/SPRINT_SCOPE.md) and
  coordinator spawned (§1).
- 2026-11-12 ~11:12 EST: MDX_STEMACT sprint COMPLETE (coordinator 9b01b8aa).
  Report `detection-research/SPRINT_2026-11-12_MDX_STEMACT.md` + `mdx_stemact/`.
  Parent-verified in full this loop: every headline number recomputed from the
  JSONs on disk (Bar C MW U=29.0 p=0.2486 recomputed with scipy; Bar B medians/
  IQRs/ratios read from the per-stem JSONs; MV-11 leg rechecked span by span).
  Verdict: A+B PASS, C FAIL (§1). Report complete.

## 0. The c11_sep landing (what loop 6 inherited — verified on disk)

c11_sep is DONE, PASS all 4 bars, parent-verified in full, committed a2b435bd.
Loop 6 re-read the numbers from `c11_sep/stage4_fulltrack_validation.json`
itself, not from the sprint report's prose:

| Bar | Measured (JSON) | Bar |
|---|---|---|
| Stem corr vs Demucs (mono) | **0.9675** (L 0.9686, R 0.9670) | ≥0.95 |
| RMS-VAD boundaries, max \|dStart\| | **0.21 s** (max \|dEnd\| 0.82 s, diagnostic) | ±0.5 s |
| Active/silent RMS ratio | **242.7×** (Demucs 191.0× same mask/method) | ≥100× |
| Runtime, clean single run | **840.4 s** (model 795.3 s, STFT 6.3 s) | <894 s |

Target <650 s NOT met — the int8 quantized-matmul path is the next speed lever
(scoped, not built; loop 6 ranks it §3 #5). STFT parity 1.526e-05 / ISTFT
1.272e-08; chunk-0 parity 24/24; driver smoke 1 int16 LSB. The production stem
exists and is the sprint's input. What adoption changed (loop 5's decision,
now banked): separation is a pipeline step, not a batch job, and the stem is a
first-class artifact the gates can calibrate on — which is exactly what this
loop's top-1 sprint tests.

Note (MEMORY.md correction, same morning): the "structural EDQUOT / effectively
full volume" diagnosis was WRONG — /tmp is a 512M tmpfs and the fallocate
failures measured /tmp, not the home volume. Real state after the user's
clean-house order (msg 325): 43G avail; the sync's 61G worktree copy still
does not fit (lean rework still needed or phase-2 frees 18G+). Loop 6's files
are small (wavs + JSONs, ~40 MB); nothing in this loop depends on the CDN sync.

## 1. Hop chain (audit data)

- **Seed:** adoption branch, continued — c11_sep PASS (see §0); the stem is now
  a cheap pipeline artifact.
- **Hop 1 (same category, separation → sensor):** the MDX stem-activity curve as
  the voice-activity sensor — the top-1 sprint (§3 #1). The stem is already the
  segmenter's output; reading activity off it costs nothing, and loop 5's
  adoption decision made it the only stay-rule candidate left.
- **Hop 2 (CATEGORY CROSS — audio separation → visual/QC gates):** the
  stem-activity curve drives gates that live in the VIDEO domain:
  mouth-open-vs-quiet (loop 1 #3) and CCA AV-sync (loop 2 #3, loop 6 drawn
  entry §5) calibrate on the MDX stem curve instead of a classical sensor. The
  cross is from "separate the audio" to "read the mouths off the separated
  audio". It also pulls in the face-box dependency (Viola-Jones R2): the visual
  half of CCA needs a mouth region, and loop 6 §5 shows the visual feature must
  be mouth openness, not frame-diff.
- **Hop 3 (back to the MV):** G7 + R5 proceed on their own bars (no sensor
  needed) + the skill edits + the snapper's error model reframed by §4 (the
  mix-snap anchors are accompaniment-locked — the stay-rule statistic must be
  stem evidence, not mix evidence).

Chain cap reached. No DONE node re-searched. No BAN_LIST endpoint banked.

## 2. The per-loop break-the-sync probe (loop 6) — RUN, PASS

**The MV-13 "Fourth law" ×4 repeat probe, run this loop** (loop 5 §6 follow-up:
run the MV-13 snapper first, then the probe). Loop 6 ran the snapper on MV-13
(`c11_mir snap`, both flavours, 394 words — `snap_mix_mv13.json`,
`snap_vocal_mv13.json`): mix 335/394 moved, vocal 343/394 moved, median
|corr| 0.060 / 0.056 s, on-peak 359 / 378. MV-13 16k wav made from track.mp4
(185.6 s) for the run; no MV-13 snapper output existed before this loop.

Method (loop 4's, verbatim): "Fourth law" bigram occurrences, hook clusters
(≥3 occurrences after 90 s), ASR vs snapped starts + corrections; global check:
no snapped word lands within ±0.1 s of an earlier identical word's ASR time.

| Cluster (back half) | ASR starts | Snapped starts (vocal) | Corrections |
|---|---|---|---|
| 117.74–126.72 | 117.74, 122.70, 124.10, 125.40, 126.72 | 117.776, 122.768, 124.304, 125.360, 126.704 | +0.036, +0.068, +0.204, −0.040, −0.016 |
| 132.44–141.40 | 132.44, 138.28, 139.36, 141.40 | 132.432, 138.240, 139.360, 141.360 | −0.008, −0.040, 0.0, −0.040 |
| 157.72–176.64 | 157.72, 162.74, 164.12, 165.18, 166.38, 167.14, 172.50, 176.64 | 157.760, 162.768, 164.112, … 167.136, 172.528, 176.496 | +0.040, +0.028, −0.008, …, −0.004, +0.028, −0.144 |

**Result: PASS on the probe's question — 0 chorus-repeat collapse hits.**
All 17 hook-cluster rows advance through repeats (max |corr| 0.204 s vocal).
One criterion hit on both flavours: idx 133 "What?" snapped 71.568 vs earlier
idx 132 "What?" ASR 71.48 — but these are ADJACENT double barks (ASR 71.48 and
71.70, 0.22 s apart), and BOTH snapped to the SAME flux peak (71.568: idx 132
+0.088, idx 133 −0.132). That is a same-peak double-bark assignment, not chorus
glue: the DP puts two words 0.22 s apart on one onset because they share one
flux peak. Documented as snapper behaviour (the second bark has no own anchor —
the stay-rule/TSM side should know), not a collapse. The monotonic-forward-walk
fix holds on MV-13 as on MV-14.

## 3. Ranked entries

### #1 — MDX stem-activity sensor validation (TOP-1 — sprint spawned, §1)

**What it is.** Loop 5 §3 #2, unchanged in bar, now scoped as the sprint
`MDX_STEMACT` (loop-06/SPRINT_SCOPE.md): RMS-VAD on the MDX vocal stem,
validated against the Demucs stem curve. Bars (held from loop 5): **A** —
boundaries ±0.5 s vs the Demucs stem-activity curve on the 12 ref segments;
**B** — non-overlapping IQRs sung vs instrumental on the 25 ms RMS envelope,
all three stems (c11, ONNX MDX, Demucs); **C** — stem-envelope-at-snapped-
position separates the 5 known snap errors from the 15 controls (MW one-sided
p < 0.05 AND errors median < correct median). Deliverable: the reusable
stem-activity curve artifact + recipe script, so loop 7 calibrates gates on it
without re-deriving it. Generalization leg: MV-11 (Demucs stem on disk; produce
a c11 stem with the c11_sep runner if it fits — do not block the MV-14 verdict
on it).

**Why it is top-1 now.** It is the ONLY stay-rule candidate left, and it
unblocks three things (stay-rule patch, mouth-open gate, CCA AV-sync). All
inputs exist; the validation is minutes of compute per stem; the verdict is
decisive either way (pass → loop 7 builds on it; fail → loop 7 records that the
stay-rule has no sensor). Loop 6's §4 finding sharpens Bar C: mix-snap
positions are accompaniment-locked, so envelope-at-snapped-position is a real
test — and the rising-edge distance is the stated diagnostic if it fails.

**Status:** coordinator 9b01b8aa COMPLETE 2026-11-12 ~11:12 EST. Report
`detection-research/SPRINT_2026-11-12_MDX_STEMACT.md` + `detection-research/mdx_stemact/`
(validation JSONs, `validate_stemact.py`, `stem_activity_curve.py`, curve
artifacts, MV-11 leg). **Parent-verified in full by this loop** — every headline
number recomputed from the JSONs on disk, not from the report's prose:
calibration reproduced loop 5 exactly (17 segs, dStart 0.21, ratio 248.91 vs
248.8); Bar C MW recomputed with scipy (U=29.0, p=0.2486 — exact match); Bar B
medians/IQRs/ratios read from the per-stem JSONs (exact match); MV-11 leg
rechecked span by span (7/11 within bar, 2 outside, 2 unmatched — exact match);
curve artifacts load (6464 frames MV-14, 6896 MV-11); DETECTION_FINDERS.md run
entry present (line 1765).

**Verdict: Bar A PASS (all three stems), Bar B PASS (all three stems), Bar C
FAIL.** Per the pre-stated logic: **the sensor is VALID as a voice-activity
curve — the mouth-open gate and CCA may calibrate on it — but the stay-rule use
FAILS. The stay-rule patch has no sensor.** All five in-span candidates tried
across loops 4–6 are now dead on MV-14 (c11_voice curve, vibrato depth,
spectral entropy, vocal-flux both flavours, stem-envelope-at-snapped-position).

| Bar | Measured (verified) |
|---|---|
| A — boundaries ±0.5 s vs Demucs | MDX max \|dStart\| **0.21 s**; c11 **0.21 s** (segments identical to MDX to the 10 ms grid); Demucs **0.00 s** (self-check) |
| B — non-overlapping IQRs, 25 ms RMS envelope | Sung q25 0.0207 / 0.0207 / 0.0267 vs instr q75 0.00084 / 0.00084 / 0.00163 (MDX / c11 / Demucs); ratios 248.9× / 248.9× / 200.5×; secondary all-12 ratios 242.7× / 242.7× / 191.0× |
| C — envelope-at-snapped, errors vs controls | c11 (judged; MDX identical): errors median 0.04909 vs controls 0.07016, MW U=29/75, **p = 0.2486** — worse than chance pairwise (37.5 expected) |

**Why Bar C fails (mechanism, same family as loop 5's flux failure).** The
snapper snaps TO peaks, and the stem envelope stays high across the small
displacements involved: the 5 errors are 0.048–0.144 s displacements to nearby
positions inside sung spans, where the voice is continuously active.
Envelope-at-a-point cannot tell a true onset from a position 0.05–0.14 s away
when the whole neighbourhood is loud. Bar B's decisive separation is
sung-vs-instrumental (span scale); Bar C asks for onset-vs-nearby-inside-a-sung-
span (sub-span scale), and at that scale the envelope has no contrast. The low
errors median is carried by one point (idx 56 'Help', env 0.0103, prob 0.013 —
its ASR is itself unreliable); idx 162 'If' sits ABOVE the controls' median
(0.0921); one control (idx 19 'you', env 0.0001) sits at essentially zero stem
envelope. The rising-edge diagnostic also fails (median |dist| 0.368 s vs
0.190 s, p = 0.37 — verified by recomputation); locally-normalised envelope is
worse (p = 0.78 — verified). Loop 7 should not re-test these two statistics on
MV-14 hoping for a different answer.

**MV-11 generalisation leg — COMPLETE, FAILS.** The c11 stem was produced via
`sep_main --dump-dir` (run 1 SIGTERM'd by a VM reboot at 26/40 chunks; resumed,
40/40 dumped, assembled). Bar A stem-to-stem: max |dStart| **1.71 s** (bar
0.5 s), stem corr **0.8466** (vs 0.9675 on MV-14); 7/11 Demucs spans within bar,
2 outside (0.63, 1.71 s), 2 unmatched by the metric. Mechanism verified on the
envelopes: Demucs-stem brass bleed crosses the VAD threshold — both stems agree
the true voice onset is ~71.5 s in the worst span while the Demucs segment
starts at 69.27 on bleed blips. The c11 stem is cleaner on this track (ratio
139.6× vs Demucs 70.1× — the Demucs stem itself is below the 100× bar on
MV-11). Consequence: **the MV-14 validation does not generalise to MV-11 at
±0.5 s.** Two loop-7 follow-ups, recorded not built: (1) gate calibrations
should use the c11 stem's own boundaries (the cleaner stem), and a bleed-aware
threshold (or higher thr_frac) is worth testing before any gate trusts a
boundary to ±0.5 s on a new track; (2) `match_boundaries` must count unmatched
spans as failures, not skip them — the metric understates disagreement whenever
a pred piece starts outside the 1.0 s window or in the previous span. The MV-14
verdict stands (its spans were all matched); the MV-11 leg bounds its
generality. One calibration subtlety banked: loop 5's 248.8× uses the sung-only
active mask; the all-12 variant is 242.7× — same statistic, different masks.

### #2 — G7 wrong-lyric gate (small build — the highest-certainty deliverable left)

**What it is.** Loop 3 §2 #5 / loop 4 §2 #4 / loop 5 §3 #3, unchanged:
word-set overlap between a take's ASR words and the scene's planned words,
overlap < 0.5 → REJECT, with a hand-check override for homophones and
near-identical choruses (provenance quarantine for identical choruses).
Validation bar (unchanged): cross-pairing the 65 KEEP takes against every other
scene's planned words (must score < 0.5), own-pairs ≥ 0.5 with zero false
REJECTs; plus the real positive MV-2 S04 t3 (proven: t3 sang 30–40 s lyrics at
43–48 s; t4 covers the window, LCS 15/19) and the S21 candidate pending
verification.

**Why it ranks here.** It needs no audio feature, no sensor, and no separation —
the only entry whose inputs already exist and whose bar can pass this week. It
is the first QC check that reads *what* the take sings rather than how it looks
or moves. The cross-pairing fixture becomes standing QC: every future volley's
takes get cross-paired automatically.

**Status:** not built in this loop (research only). Scoped as a small build —
QC script + ledger rule, not a sprint.

### #3 — R5 flow interpolation for BAD-WORD spans (build — routes around the gap)

**What it is.** Loop 3 §2 #4 / loop 4 §2 #5 / loop 5 §3 #4, unchanged:
symmetric-flow MCFI (Raket et al. 2012) — synthesize the missing motion between
the good frames on either side of a bad word instead of cutting to montage.
C11 Farneback exists (sprint 7, validated vs cv2); the build is the
warp/blend/hole-fill pipeline plus the symmetric-flow estimation pass. Bar
(unchanged): delete a 0.3–0.5 s span from a KEEP take, interpolate it back —
M6 in KEEP range + eye can't tell + interpolated mouths must not read as a
different word — and at least as clean as ffmpeg `minterpolate` mci on the
same span.

**Why it ranks here.** It is unaffected by the vocal-activity gap: it routes
around the gap's consequence in assembly instead of through it. It does not
need a sensor. If it passes, the BAD-WORD RULE gains an "interpolate first, cut
second" branch for short spans — the only repair path for takes whose only
defect is one bad word.

**Status:** not built in this loop. Scoped as a build, on its own bar.

### #4 — RMVPE pitch tracker on the MDX stem: the definitive vibrato arbiter

**What it is.** Loop 5 §3 #5, unchanged: WuBuRVC's RMVPE pitch tracker (C11
port matches PyTorch corr 0.9999 / 0.19 Hz mean diff — already built and
parity-verified) run on the MDX vocal stem, then the c11_vibrato falsifier
method run on the RMVPE track. RMVPE is a neural pitch tracker: it does not
pin at boundaries the way pYIN's Viterbi does, and it does not jump harmonics
the way raw autocorrelation does. It is the one F0 source on this material that
is neither pinned nor jumpy — the definitive arbiter of whether the chant is
straight-tone.

**Why it ranks here.** Loop 5 §1 leaves the straight-tone question structurally
open: pYIN is pinned, autocorr is jumpy, and the stable-frame estimate sits at
the boundary on a biased subset. The question matters because a real vibrato
signature would re-enter as a sensor candidate — but only a clean F0 track can
answer it, and RMVPE is the only clean F0 tracker already built. Bar: same
falsifier method, same 20c boundary; the RMVPE track must show a 5–7 Hz PSD
peak AND a sung median depth ≥20c with non-overlapping IQRs vs instrumental
for the verdict to fall — otherwise the straight-tone verdict is confirmed on a
clean source and the question closes for good.

**Status:** not run in this loop (research only). Scoped as a measurement, not a
sprint — one RMVPE run + the falsifier method, a day at most.

### #5 — c11_sep int8 speed lever (follow-up sprint — the 650 s target)

**What it is.** c11_sep §5 + §9: the 650 s target was NOT met (840.4 s clean
run). The gap is the 3x3 convs (im2col GEMM ~118 GFLOPS) and the 1x1 convs
(out^T GEMM ~63 GFLOPS). The next lever is the wubuwizard int8
quantized-matmul path (quantized_matmul.c / quantized_dot_generic.c, lego'd
already in the harvest) applied to the U-Net convolutions. Bar: same four
c11_sep bars (stem corr ≥0.95, boundaries ±0.5 s, active/silent ≥100×) PLUS
runtime <650 s on the blade. If int8 cannot hold the parity bars, the sprint
reports that with the numbers and 840.4 s stands as the production runtime.

**Why it ranks here.** 840.4 s already passes the <894 s bar, so this is
optimization, not unblocking — it ranks below the four items that unblock
gates. But it is the only remaining speed lever, and every pipeline use of the
stem pays 840 s until it lands.

**Status:** not built in this loop. Scoped as a follow-up sprint.

### Also carried (not ranked — status notes)

- **Mouth-open-vs-quiet gate (loop 1 #3) + CCA AV-sync (loop 2 #3):** still
  blocked on a sensor — but the sensor is now under validation (§3 #1). They
  calibrate on the stem-activity curve, in that order, once §3 #1 passes its
  bar. Loop 6 §5 adds a second gating fact: the CCA visual feature must be
  mouth openness, not frame-diff — and it needs the face box (R2).
- **Snapper stay-rule patch:** still unbuildable until §3 #1 passes Bar C.
  Loop 6 §4 reframes its error model: the mix-snap anchors are
  accompaniment-locked (the stem lattice differs from the mix lattice), so the
  stay-rule evidence must be stem evidence. The sprint-5 "stay if no in-span
  strong peak" rule (mix-flux) is unchanged as the patch shape; its evidence
  signal is what §3 #1 validates.
- **TSM squeeze-guard band measurement:** STILL OWED (§6) — c11_tsm owns it.
- **MSAF classical structure (R6), Viola-Jones face box (R2), Sakoe-Chiba DTW
  (R7), TransNetV2 classical shell, Thayer valence (R12):** unchanged, not
  built. R2 is now the gating dependency for CCA's visual half (§5); R7's
  design gained a citation this loop (Sharma & Li 2019 landmark-DTW, −47.5%
  word-boundary error) and a production corroboration (MDX-Net separation ahead
  of CTC alignment constrained by DTW). R6's bar still needs MSAF boundaries
  for loop 1 #4's piecewise-grid validation.
- **wubu_synth residue (loop 3 #8):** unchanged — a `c11_scaffold` template
  library is a build, scoped only if a sprint's scaffolding is ever written
  twice the same way. Never from wubu_synth as-is.
- **Slopcore vehicle-template changes (loop 3 #7):** unchanged — proposed
  skill edits (kinds system, {END} footer, macro-managed identity, pilot
  pattern), parent applies. No skill edited this loop.
- **Voice-quality shelf:** CLOSED (loop 5 §4) — unchanged. Nothing on it
  survives on MV-14, on the mix or the stem.
- **Stem-flux snapper:** CLOSED by §4 — the stem snap does not reproduce the
  mix snap and does not fix the errors. It is not a replacement snapper and not
  a stay-rule candidate. The lattice finding (stem lattice ≠ mix lattice) is
  banked as the reframing of the snapper's error model.

## 4. The stem-snap comparison (sprint-5-specified FIRST follow-up) — RUN, FAIL

**What it was.** Sprint 5's §"Stem validation" specified it exactly, and it was
never run (the stem was in flight when sprint 5 validated): run the snapper on
the 16k mono stem (`--flux mix` — "the stem IS the vocal channel, so mix flux
= stem flux"), compare `snapped_start` against `snap_vocal_mv14.json` (median
|diff|, agreement within 16 ms = 1 STFT frame), recompute gap counts on stem
energy at 0.01/0.02. The stem would also settle the hand-check disagreements —
a stem flux peak at the snapper's position vindicates it; silence there
convicts it. Loop 6 ran it on BOTH stems (Demucs + c11), BOTH flux flavours
(mix per spec + vocal variant) — four runs, all 212 words.

**What was measured (spec test — median |diff| vs the mix-vocal snap):**

| Stem snap | Median \|diff\| vs mix-vocal | Agree within 16 ms | Controls agree (15) |
|---|---|---|---|
| Demucs, mix flux (spec) | **0.032 s** | 70/212 (33%) | 4/15 |
| Demucs, vocal flux | 0.040 s | 73/212 (34%) | 4/15 |
| c11, mix flux (spec) | 0.048 s | 69/212 (33%) | 3/15 |
| c11, vocal flux | 0.048 s | 70/212 (33%) | 4/15 |

**The 5 known errors (1-based idx into snap_mix_mv14.json) — stem does not fix
them** (Demucs mix-flux run; vocal-flux run same pattern):

| Idx | Word | Mix corr | Stem corr | Reading |
|---|---|---|---|---|
| 34 | pitch | −0.120 | +0.104 | flips side |
| 56 | Help | 0.000 | −0.304 | moves a held word 0.3 s EARLY — worse |
| 60 | Trip | −0.088 | +0.072 | flips side |
| 112 | back | −0.048 | −0.048 | identical — no change |
| 162 | If | −0.144 | −0.128 | same direction, still large |

**Verdict: FAIL the spec agreement test.** The stem snap does not reproduce the
mix snap within 16 ms on any run, does not keep the 15 controls (3–4/15 agree),
and does not fix the 5 errors (3 of 5 move to yet other positions; one is
unchanged; one gets worse). The stem snap is NOT a drop-in replacement
snapper, and it does not vindicate the mix positions.

**The lattice finding (the durable part).** The stem snaps ARE self-consistent:
Demucs mix-flux vs vocal-flux median |diff| **0.0**, agree 142/212; Demucs vs
c11 (same flavour) median |diff| **0.0**, agree 144–156/212. The stem has its
OWN onset lattice, stable across separators and flux flavours, which DIFFERS
from the mix lattice (median 32–48 ms, agree ~33%). Neither lattice is validated
as "true" word onsets — the mix lattice is the pipeline's current timing
authority (sprint 5 hand-check + the accepted MV-14 assembly's word-sync), so
the stem lattice cannot replace it without its own validation. What the finding
does is reframe the snapper's error model: the mix-snap anchors are substantially
accompaniment-locked (drum/bass transients in the 300–3400 Hz band), not voice
onsets in the separated sense. That is why the stay-rule evidence must be stem
evidence (§3 #1 Bar C), and why a mix-flux "stay if no in-span strong peak"
rule can only ever be a patch, not a fix.

**Gap counts (sprint-5 spec: recompute on stem energy).** Snapper's own
`n_gap_asr`: mix 115 vs Demucs stem 126 vs c11 stem 120 — the stem has MORE
gap words (sparser onsets); `n_gap_snapped`: 64/74 mix vs 65/73 Demucs vs 63/80
c11. Absolute-silence check (25 ms RMS < 1%/2% of global max): 0/0 spans on mix
and Demucs stem, 0/3 on the c11 stem — the "gaps" are low-onset regions, not
silence, on all three.

## 5. The blind-drawn entry: CCA AV-sync on MDX stem activity — MEASURED

**What it is.** Loop 2 §2 #3, drawn from a 17-item pool (§11): CCA
(Hotelling 1936; Weenink's Praat implementation; Xie et al. 2012; Sargın et al.
2006; Pedersen et al. 2022) as the classical core of SyncNet's job — measure
whether mouth motion and audio agree (peak height = LSE-C) and by how much
(peak lag = LSE-D). Loop 2 sequenced it after the face box (R2) "or prototype
the audio side first against hand-marked mouth boxes". Loop 6 did both halves:
leg A (audio side) + leg B (one-take visual prototype, hand-marked box).

**Leg A — audio side: PREMISE HOLDS.** Pedersen's premise is that face motion
correlates with the acoustic envelope below 10 Hz, peaking at the 3–4 Hz
syllable rate. Loop 6 tested it on the stem envelope (25 ms RMS, Welch PSD per
segment, averaged): on MV-14 sung spans (ref 1–10), the envelope peaks at
**3.125 Hz** on ALL THREE stems (MDX frac 18.3%, Demucs 19.8%, c11 18.3% of
0.5–10 Hz power); on instrumental gaps it peaks at 1.25 Hz at ~175× lower
absolute power. c11 == MDX-ONNX to 7 significant figures (the C11 stem
reproduces the ONNX stem's envelope modulation exactly). The syllable-rate
structure CCA needs IS in the stem envelope. (One misdiagnosis caught and
corrected in-loop: the first PSD run concatenated detrended segments and peaked
at 1.25 Hz — the joins leaked low-frequency power. Per-segment Welch, averaged,
gives 3.125 Hz. The corrected method is what the JSON carries.)

**Leg B — one-take visual prototype: FAIL, mechanism diagnosed.** Take: MV-13
S25 t2 (mouth OPEN at both "What?!" barks, ledger-verified; close-up 0–2.5 s).
Hand-marked mouth box from frames f_06/f_11/f_20 (x 135–185, y 70–110 in
320×180 — the face is frontal and the mouth is clearly visible). Feature:
mouth-box mean abs frame-diff (24 pts @10 fps) vs the take's own audio envelope
(100 ms RMS bins). Pre-stated bar: peak |r| > 0.4 AND peak lag in the R3 range
(motion 0.5–1.4 s AFTER audio) AND peak |r| ≥ 2× the shuffled-control peak.

| Measure | Value |
|---|---|
| Mouth vs audio peak | lag **+1.3 s**, r **0.698** (r at lag 0: 0.326) |
| Whole-frame vs audio peak | lag +1.3 s, r **0.948** |
| Shuffled-control peak (0.5 s block shuffle) | lag +0.9 s, r **0.93** |

The first two conditions pass; the third fails decisively (0.698 < 2 × 0.93) —
**verdict FAIL.** The mechanism, read off the series: the motion series is a
step function (40–80 while the camera pushes in at t 0.05–1.15 s, then 2–20
after it settles) and the envelope is a single pulse (the "What?!" bark at
t ≈ 0.95–1.15 s, 0.20 vs a 0.02–0.05 floor). With ONE event in a 2.4 s window
the test has ~1 degree of freedom: any lag that aligns the two single features
gives high r, including the shuffled control (its big bark bin lands somewhere
and the peak-finder finds it). And the mouth opening itself is INVISIBLE in the
frame-diff series — the box motion at the bark (65.1 at t 0.95) is lower than
the push motion (79.8 at t 0.75). Worse, whole-frame motion correlates BETTER
(0.948) than mouth-box motion (0.698) at the same lag: the "signal" is the
camera push, not the mouth.

**Consequence.** CCA's visual feature must be mouth OPENNESS (lip distance /
MAR-like measure), invariant to camera push — not raw frame-diff in a box. And
it needs the face box (R2) to locate the mouth, and multi-event takes (longer
windows, many barks) so the correlation has degrees of freedom. The audio side
is viable (leg A); the visual side is not demonstrable on one take with this
feature. CCA stays sequenced after R2 + a mouth-openness feature. The +1.3 s
lag is consistent with the known R3 mouth-lag (0.5–1.4 s), but on this evidence
it is not distinguishable from the camera push + single-event alignment — it is
recorded as consistent, not as measured.

## 6. TSM squeeze-guard check — STILL OWED (c11_tsm owns it)

Checked `tsm-driedger-2014/stretched/`: 28 files, only the S47/S49/S50/S52
validation takes (M1–M7 methods). No moderate-squeeze take (gap alpha 0.5–0.87)
has landed. The c11_tsm sprint (parent-spawned in parallel, scope bar 4) owns
the guard measurement — loop 6 does not duplicate it. Loop 6 notes it; it does
not do it.

## 7. Loop-7 seed

1. **MDX_STEMACT sprint verdict — DONE (§3 #1): A+B PASS, C FAIL.** The sensor
   is VALID as a voice-activity curve; the stay-rule use FAILS. Loop 7
   calibrates the mouth-open gate + CCA on the delivered stem-activity curve
   (in that order), and records that the stay-rule patch has no sensor. The
   stay-rule stays unbuilt unless a NEW signal class is proposed (onset
   detector with sub-span resolution, or a different error set with more than
   5 errors) — do not re-test envelope-at-position or rising-edge distance on
   MV-14. The MV-11 leg bounds the validation: boundaries are
   separator-dependent where bleed crosses the VAD threshold; loop 7 uses the
   c11 stem's own boundaries and fixes `match_boundaries` to count unmatched
   spans as failures; a bleed-aware threshold test is owed before any gate
   trusts a boundary to ±0.5 s on a new track.
2. **G7 wrong-lyric gate** (§3 #2): the highest-certainty deliverable left;
   builds on its own bar regardless of the stemact verdict.
3. **R5 flow interpolation** (§3 #3): routes around the gap in assembly.
4. **RMVPE vibrato arbiter** (§3 #4): closes the straight-tone question for good.
5. **c11_sep int8 speed lever** (§3 #5): the 650 s target.
6. **MV-11 generalization leg** if the stemact sprint did not fit it: c11 stem
   for MV-11 + Bar A stem-to-stem.
7. **CCA visual half**: R2 face box + mouth-openness feature (loop 6 §5) before
   any CCA build is scoped.
8. **TSM squeeze-guard check again** (§6): the moderate-squeeze take is still owed.

## 8. Proposed skill edits (draft only — parent applies, no skill edited this loop)

1. **Vehicle template (carried from loop 3 #7, unchanged):** kinds system
   (lips / motion / insert), the {END} prohibition footer on every vehicle,
   macro-managed identity, pilot pattern. Source: slopcore PROMPTS.md, measured.
2. **BAD-WORD RULE (conditional on R5 passing):** "interpolate first, cut
   second" branch for 0.3–0.5 s spans — only after the M6 + eye + mouth tests pass.
3. **QC gates:** add G7 (word-set overlap < 0.5 → REJECT, cross-pairing
   positives as the fixture, homophone hand-check override) once §3 #2's
   validation passes.
4. **Snapper stay-rule (conditional):** MDX stem activity as the in-span
   peak-evidence signal — only once §3 #1 passes Bar C. If Bar C fails, the
   rising-edge distance is the next candidate statistic, not the
   envelope-at-position. Vibrato depth, spectral entropy, vocal-flux (both
   flavours), and stem-flux snap positions are all dead as candidates; do not
   list them.
5. **F0-source rule (carried from loop 5 #5, unchanged):** never use a saved
   pYIN track's f0_hz as "the voice's F0" without a pinning audit (fraction of
   voiced frames at fmin/fmax). Sprint 8's saved tracks are NOT voice-F0 tracks.
6. **Snapper error-model note (new, from §4):** mix-snap anchors are
   substantially accompaniment-locked — the stem lattice differs from the mix
   lattice (median 32–48 ms). A snap correction is evidence about the mix
   onset lattice, not about the voice onset. Do not use a mix-snap position as
   a voice-onset ground truth in any gate.
7. **CCA visual-feature rule (new, from §5):** mouth motion must be measured
   as mouth OPENNESS (lip distance), never as raw frame-diff in a mouth box —
   frame-diff under camera movement measures the camera, not the mouth.

## 9. Honest scope

- **Code was run:** MV-13 snapper (both flavours) + Fourth-law probe; stem-snap
  comparison (4 runs: 2 stems × 2 flavours) + lattice agreement + gap counts;
  CCA leg A (stem-envelope PSD, 3 stems) + leg B (one-take prototype, 25 frames,
  hand-marked box). Every number in this report is in `loop6_validation.json`,
  reproduced from `loop6_probe_stemsnap.json` and `cca_prototype.json` (scripts
  in loop-06/, inputs on disk, unchanged).
- **Two misdiagnoses caught and corrected in-loop:** (a) the CCA leg-A PSD first
  peaked at 1.25 Hz because concatenated segments leaked join power — per-segment
  Welch gives 3.125 Hz; (b) the CCA leg-B +1.3 s / r 0.698 peak looked like an
  R3-range hit until the shuffled control peaked at 0.93 — the bar's third
  condition exists for exactly this, and it caught it. Both falsified readings
  are recorded here, not hidden.
- **One transcription risk avoided:** the stem-snap error table reports the
  mix-flux corrections for the 5 errors from `snap_mix_mv14.json` (the file the
  indices address) and the vocal-flux corrections separately — the two files
  differ (idx 56: mix 0.000 vs vocal +0.128). The index-base conflict loop 4
  resolved (1-based into snap_mix_mv14.json) is respected throughout.
- **Two experiments failed, one probe passed, one sprint DONE and verified:**
  stem-snap comparison FAIL (spec agreement), CCA leg B FAIL (visual feature
  wrong); Fourth-law probe PASS; MDX_STEMACT A+B PASS / C FAIL (Bar C MW
  U=29.0 p=0.2486 recomputed with scipy in this loop), MV-11 leg FAIL
  (max |dStart| 1.71 s, corr 0.8466).
- **Web-verified claims:** singing-voice detection with separation preprocessing
  (Zhang et al. 2020, MDPI); attribute-based vocal-section segmentation
  (Sundaram & Narayanan, MMSP 2006, <10% error); VAD via source separation
  (Doukas, Naylor & Stathaki, Eurospeech 1997); singing-robust SAD (Grundhuber
  et al. 2025, AUC 0.919); landmark-DTW speech-to-singing alignment (Sharma &
  Li, Interspeech 2019, −47.5% word-boundary error); Sakoe-Chiba band (Sakoe &
  Chiba 1978 — carried); CCA temporal modulation filters (Pedersen et al. 2022 —
  carried from loop 2). Full citations in SOURCES.md entries — [GAP NOTE: no
  shared SOURCES.md exists; loop 3 §10's gap is still open. Loop 6 adds its
  citations here and in loop6_validation.json, not in a shared file.]
- **Measured on disk (reproducible):** MV-13 snapper (mix 335/394 moved, vocal
  343/394, median |corr| 0.060/0.056 s); Fourth-law probe (0 chorus-repeat
  collapse hits; 1 adjacent double-bark same-peak at 71.568); stem-snap (median
  |diff| 0.032–0.048 s, agree 69–73/212, controls 3–4/15; stem self-agreement
  median 0.0, 142–156/212); CCA leg A (sung peak 3.125 Hz, frac 18–20% vs gaps
  9.5–14.9%); CCA leg B (mouth r 0.698 @ +1.3 s, whole-frame 0.948, shuffled
  0.93 — FAIL).
- **What this loop did NOT do:** no re-run of any sprint calibration; no
  lowering of any bar; no gate built from a failed experiment; no video
  generation; no commit; no Telegram write; no skill edit; no TSM build
  (c11_tsm is the parent's parallel sprint).

## 10. Top 5 (for the parent's report)

1. **MDX stem-activity sensor — VALIDATED as a voice-activity curve, stay-rule
   use FAILED.** Bars A+B pass on all three stems (max |dStart| 0.21 s,
   non-overlapping IQRs, 248.9×); Bar C fails (p = 0.2486). Mouth-open gate +
   CCA may calibrate on the delivered curve; the stay-rule patch has no sensor.
   MV-11 leg fails (1.71 s) — boundaries are separator-dependent where bleed
   crosses the threshold.
2. **G7 wrong-lyric gate (small build)** — highest-certainty deliverable left.
3. **R5 flow interpolation (build)** — routes around the gap in assembly.
4. **RMVPE on the MDX stem: the definitive vibrato arbiter** — closes straight-tone.
5. **c11_sep int8 speed lever** — the 650 s target.

## 11. Blind draw (method audit)

Drawn with `secrets.choice` from a 17-item candidate pool of loop-6 ideas:
`G7 wrong-lyric gate, R5 flow interpolation, RMVPE vibrato arbiter,
Mouth-open-vs-quiet gate on MDX stem activity, CCA AV-sync on MDX stem
activity, MSAF classical structure (R6), Viola-Jones face box (R2), Sakoe-Chiba
DTW forced aligner (R7), TransNetV2 classical shell (inside-take shot
boundaries), Thayer valence (R12), c11_sep int8 speed lever, Attribute-based
vocal-section segmentation on the stem (Sundaram & Narayanan 2006), Kinds system
(vehicle template), Macro-managed identity, Pilot pattern, {END} prohibition
footer, wubu_synth c11_scaffold residue`.
**Draw: "CCA AV-sync on MDX stem activity"** (first draw accepted, no discard).
Checked: 0 whole-phrase occurrences of any pool item in
`~/workspace/wubutv-network/ideas/BAN_LIST.md`; not among banked form ideas
(COMPASS, VESSEL, CRADLE SHOT, SATELLITE ORBIT, HARBOR, RIVER, FEATHER).
**Deviation, stated plainly:** the pool excludes the assigned threads (top-1
sprint scoping, MV-13 probe, stem-snap comparison, TSM check) — following loop
5's deviation, not loops 3–4 (whose pools included the drawn item's own thread).
The draw is load-bearing in the method's sense: it forced CCA AV-sync into a
full measured entry (§5) with a pre-stated bar instead of letting it sit as an
unexamined "blocked on a sensor" line — and the measurement split it: the audio
side holds, the visual side fails on its feature, which sharpens the loop-7 seed
(R2 + mouth openness before any CCA build).
