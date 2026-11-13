# Slopcannon improvement loop 5 — report

**Date:** 2026-11-12 · **Coordinator:** 07caec17 · **Seed:** CASA failed fast —
the adoption branch (user msg 252, msg 288, msg 313).
**Chain cap:** 3 hops, hop 2 crosses a category boundary. **Blind draw:** one, load-bearing (§12).
**Status:** research only. Code was run (vibrato re-measurement ×2, R8
pre-check, MDX verification, snapper-flux test ×2 flavours, all measured),
no video generated, no commit, no Telegram write, no skill edit.

## Progress log (checkpoint lines)

- 2026-11-12 ~05:36 EST: loop 5 spawned (07caec17). Read loop-04 report,
  CASA sprint report, wubuwizard report in full.
- 2026-11-12 ~05:38 EST: disk inventory done. Ref: `c11_mir/hpss_mv14_ref.json`
  (12 segments, sung 1–10, bleed 11–12). Mix `c11_mir/mv14_16k.wav` on disk;
  stem 16k `/tmp/mv14_stem_16k.wav` md5 `43d83ae22fc3424533c25a896942a455` —
  matches loop 4's documented md5 exactly. CASA `step1_curves.npz` (tau_ref,
  trusted, stem_r_max, stem_tau_raw) on disk. MDX runner + model + full-track
  stems on disk (`wubuwizard-cpu-sep/`). venv (numpy / scipy / librosa) works.
- 2026-11-12 ~05:40 EST: vibrato re-measurement v1 ran off integer tau_ref —
  114c smoothed / 189c raw, bleed HIGHER than sung. First diagnosis
  (integer-lag staircase) recorded, then FALSIFIED by v2 (§1).
- 2026-11-12 ~05:44 EST: vibrato re-measurement v2 ran — sub-sample parabolic
  peak interpolation, same numbers as v1; FM control recovers 21.79c for a
  true 35.36c, straight control 0.0c. Stability diagnostic: 4.6% of sung
  frames locally stable; stable-frame depth 17.82c. Decision: STANDS (§1).
- 2026-11-12 ~05:47 EST: R8 pre-check ran — FAIL on all three conditions
  (SNR −4.55 dB, Type-1 4.6%, HNR 1.69 dB). No boundary scoring (§4).
- 2026-11-12 ~05:47 EST: MDX adoption verification ran — full-track corr
  0.9676 vs wubuwizard claim 0.9675; 17 segments; active/silent 248.8× (§0).
- 2026-11-12 ~05:48 EST: blind draw — snapper vocal-flux curve (§12).
  Flux test ran on BOTH flavours — FAIL on all three statistics (§5).
- 2026-11-12 ~05:50 EST: MV-13 probe check — no MV-13 snapper output exists
  anywhere in ~/workspace; probe UNRUN (§6). TSM check — moderate-squeeze
  take STILL OWED (§7). c11_sep scope written (loop-05/SPRINT_SCOPE.md).
  Report complete.

## 0. The adoption decision (thread 1) — ADOPT MDX-Net ONNX as-is NOW

**Decision: adopt MDX-Net ONNX as-is now as the pipeline's segmenter, and
scope c11_sep as the sprint that makes it cheap.** The alternative (scope
c11_sep first, adopt later) is rejected: the pipeline needs a working
segmenter now, and MDX already works; c11_sep's validation target IS the
MDX port.

**Verified here (independent re-check of the wubuwizard report's headline
numbers, so this decision rests on measurements made in this loop):**

| Measure | This loop | Wubuwizard claim |
|---|---|---|
| Full-track corr MDX vs Demucs vocals | **0.9676** | 0.9675 |
| RMS-envelope corr | 0.9694 | 0.9750 |
| RMS-VAD segments | **17** | 17 |
| Active/silent, MDX | 248.8× | 201× |
| Active/silent, Demucs | 203.7× | 702× |

The headline corr reproduces to 0.0001. The envelope-corr gap (0.9694 vs
0.9750) is windowing: 25 ms non-overlapping windows at 16k here vs the
report's windowing — same order, not a failure. The active/silent gaps are
mask-dependent, as the wubuwizard report §4 already states ("same order,
mask-dependent"): mine uses 25 ms RMS envelopes at 16k with ref-mask medians;
both mine and theirs clear the ≥100× bar by 2× or more. **Quality verdict:
MDX replaces Demucs for the segmentation job.**

**Speed: 1,592 s vs Demucs' 894 s (1.78× slower) — accepted, for two
reasons.** First, torch Demucs is BROKEN in the current venv (the
torchvision `operator torchvision::nns does not exist` clash the wubuwizard
sprint reproduced) — MDX is currently the only WORKING separator on the
blade, so "stay on Demucs" is not an available option. Second, the speed gap
is c11_sep's job, not a reason to delay adoption: the C11 runner's bar is
<894 s with stem corr ≥0.95, boundaries ±0.5 s, active/silent ≥100×
(wubuwizard §6, carried into loop-05/SPRINT_SCOPE.md). The model is 95% of
chunk time; the front-end is noise. Speed lives or dies on the model kernel.

**What adoption unblocks immediately.** The MDX vocal stem is a voice-activity
curve the pipeline already owns: RMS-VAD on the MDX stem gives the sung/
instrumental boundaries the classical sensors never delivered (§3 #2). The
mouth-open-vs-quiet gate (loop 1 #3) and CCA AV-sync (loop 2 #3) calibrate
on the MDX stem curve instead of a classical sensor. The snapper stay-rule
patch gets its in-span evidence from MDX stem activity — the only candidate
left after §5 (§3 #2). None of these need c11_sep to finish first; they need
the MDX stem, which exists now.

## 1. The vibrato re-measurement decision (thread 2) — STANDS, basis corrected

**Decision: the straight-tone verdict STANDS as the operative verdict, but
its evidential basis is corrected.** The original numbers (mix 2.55c, stem
2.68c) are measurements of pinned pYIN contours and are withdrawn as
evidence — not as arithmetic, as measurements of a voice that cannot move.
The re-measurement on the correct F0 source does not show vibrato either,
but for a different, structural reason: the F0 contour is too unstable for
a vibrato measurement to be defined on 95% of the sung material, and the
4–8 Hz band energy peaks at 3 Hz (drift, not vibrato). **Vibrato does NOT
re-enter as a sensor candidate.** The loop-6 seed does not change on this
account; the definitive arbiter (RMVPE on the MDX stem) is ranked §3 #5.

### What was measured

The CASA stem-autocorrelation reference (tau_ref, median F0 238.8 Hz,
phrase-dependent 144–267 Hz) is the correct F0 source on this material.
Two legs, same falsifier method verbatim (0.51 s detrend, 4–8 Hz Butterworth,
0.5 s sliding RMS):

**v1 — integer tau_ref.** Smoothed sung median **114.06c**, raw 189.38c —
with bleed (252.32c) and outro (208.04c) HIGHER than sung. A measurement
that reads deepest where there is no voice is measuring instability, not
vibrato. First diagnosis recorded: the integer-lag staircase (1 sample at
tau=67 is 3.6 Hz ≈ 26 cents) injects step noise into the band.

**v2 — sub-sample parabolic peak interpolation (the diagnosis tested).**
Recomputed the stem autocorrelation with CASA's exact framing and extracted
the top peak in [27, 200] with parabolic interpolation (~0.1-sample
precision). Result: smoothed **114.31c**, raw 189.26c — THE SAME NUMBERS as
v1 to within 0.3c. **The quantization hypothesis is FALSIFIED.** The 114c
is tracker instability (harmonic jumps + phrase pitch steps), not
quantization. Recording the falsified diagnosis, not hiding it.

**Controls (same pipeline):** synthetic 6 Hz ±50c FM tone recovers
**21.79c** for a true 35.36c RMS (attenuation 0.616 — the 11-frame median
smooth + falsifier smoothing); straight tone recovers **0.0c**. The method
CAN see vibrato when it is there. The stem's 114c is five times the FM
control's recovered depth — it is not vibrato, it is something much bigger
than vibrato in the contour.

**PSD (the positive evidence against vibrato):** sung power 2–4 Hz
139,671 vs 4–8 Hz 58,334 (2.4×) — peak at **3.0 Hz**, the band edge. A
true 5–7 Hz vibrato concentrates power in 4–8 Hz with a peak at 5–7 Hz.
The energy is slow drift and phrase steps leaking into the band.

**Stability diagnostic (why the measurement is ill-defined):** only
**4.6%** of trusted sung frames are locally stable (tau within ±2 samples
of its 51-frame trend over ±0.25 s); instrumental 0.0%. On the stable
frames, depth is **17.82c** [11.15, 25.03] (n=495) vs 122.41c on unstable
sung frames. But the stability mask is biased by construction: a ±50c
vibrato moves tau by ±2 samples — exactly the stability threshold — so the
mask EXCLUDES the frames where vibrato would show. The 17.82c is a lower
bound on a 4.6% selected subset; attenuation-corrected (≈29c) it sits above
the 20c boundary, uncorrected at it. **The measurement cannot resolve
straight-tone vs vibrato on this contour.** What it resolves is the sensor
question: as a sensor, vibrato depth fails on the correct source too (sung
114c vs instrumental 71c, IQRs [48, 196] vs [28, 142] overlapping, bleed
highest — the feature responds to instability, which is highest where there
is no voice).

**The mix leg has no valid F0 source** (mix pYIN tracks the bass at the
50 Hz floor) and is NOT re-measured. The stem IS the isolated voice: if
the isolated voice carried vibrato, the stem leg would show it. It shows
instability instead.

## 2. Hop chain (audit data)

- **Seed:** adoption branch — MDX-Net ONNX as-is + c11_sep (loop 4 §4.2).
- **Hop 1 (same category, separation):** the MDX stem itself as a sensor —
  stem activity (RMS-VAD on the MDX vocal stem) as the voice-activity curve
  that unblocks the blocked gates. The stem is already the segmenter's
  output; reading activity off it costs nothing.
- **Hop 2 (CATEGORY CROSS — audio separation → visual/QC gates):** the
  stem-activity curve drives gates that live in the VIDEO domain:
  mouth-open-vs-quiet (loop 1 #3) and CCA AV-sync (loop 2 #3) calibrate on
  the MDX stem curve instead of a classical sensor. The cross is from
  "separate the audio" to "read the mouths off the separated audio".
- **Hop 3 (back to the MV):** G7 + R5 proceed on their own bars (no sensor
  needed) + the skill edits (kinds system, {END} footer, macro identity,
  pilot pattern) + the TSM guard check.

Chain cap reached. No DONE node re-searched. No BAN_LIST endpoint banked.

## 3. Ranked entries

### #1 — c11_sep separation runner (TOP-1 — sprint scoped in SPRINT_SCOPE.md)

**What it is.** The wubuwizard §6 scope, carried forward with the loop-5
adoption decision baked in: a C11 MDX-Net/Demucs runner that separates a
track faster than torch Demucs' 894 s on the blade, torch-free, validated
against the MDX-Net ONNX port (stem corr ≥0.95 vs the Demucs stem, RMS-VAD
boundaries within ±0.5 s of `hpss_mv14_ref.json`, active/silent ≥100×).
Lego-first: WuBuRVC `wubu_audioio.c` (WAV IO, as-is), `wubu_fft.c` +
`wubu_stft.c` (extend to complex-out + ISTFT, **fix the padding: reflect,
not zeros** — the wubuwizard trap), wubuwizard kernel dispatch +
thread pool, quantized matmul (int8 GEMM for the U-Net convolutions),
WuBuRVC weight-extraction pattern (`.onnx` → flat `WUBU` binary), parity
method from `wubu_rvc_parity.c`. Write from scratch: the MDX-Net U-Net
forward in C11 + the UVR chunking/overlap-add driver (`mdx_onnx_cpu.py`
is the executable spec).

**Why it is top-1 now.** Adoption is decided (§0); the only open question
is speed, and c11_sep is the only route that plausibly beats 894 s (the
model kernel, not the front-end, is 95% of chunk time). If the C11 forward
can't beat ORT's ~32 s/chunk, the sprint reports that with the numbers and
the ONNX port stays the torch-free fallback — the scope's fail-fast is
honest, not hopeful. Target: int8 path at 2–4× realtime (<650 s).

**What it replaces / enables.** Replaces ORT as the separation runtime
(and torch Demucs wherever it still runs). Enables: the MDX stem-activity
sensor at production speed (the stem-activity curve in §3 #2 is currently
a 1,592 s batch job — c11_sep makes it a pipeline step), and the
mouth-open/CCA/stay-rule calibrations on a cheaply-produced stem.

### #2 — MDX stem activity as the stay-rule / gate sensor

**What it is.** RMS-VAD on the MDX vocal stem — the same recipe that
produced the 17 MDX segments (wubuwizard §4): median 25 ms-window RMS
envelope, threshold, merge bar 1.0 s. The stem activity curve is the
voice-activity sensor the classical search never found, obtained by
separation instead of measurement. Validation bar: the MDX stem-activity
curve reproduces the Demucs stem-activity boundaries within ±0.5 s on the
12 ref segments (the wubuwizard run already shows all 12 ref STARTS within
0.21 s; the 5 mismatches are splits at real phrase gaps, not boundary
errors) AND separates sung from instrumental with non-overlapping IQRs on
the 25 ms RMS envelope (active/silent 248.8× measured here).

**Why it ranks #2 now.** It is the ONLY in-span candidate left for the
snapper stay-rule patch: c11_voice curve dead, vibrato depth dead,
spectral entropy dead, vocal-flux dead (§5). It also unblocks the
mouth-open-vs-quiet gate and CCA AV-sync, which have waited on a sensor
since loop 1. It costs no new experiment — the stem exists, the recipe
exists, the validation target exists.

**What it replaces / enables.** Replaces the classical sensor in all three
blocked gates. Enables: the snapper stay-rule patch (in-span peak evidence
= MDX stem activity inside the snapped span), the mouth-open gate
calibration, CCA AV-sync. If the stem-activity curve fails its own bar
(boundaries ±0.5 s), the stay-rule patch has no sensor at all, and loop 6
records that plainly.

### #3 — G7 wrong-lyric gate (small build — the highest-certainty deliverable left)

**What it is.** Loop 3 §2 #5 / loop 4 §2 #4, unchanged: a take singing the
wrong part of the song has no gate. Word-set overlap between the take's
ASR words and the scene's planned words: overlap < 0.5 → REJECT, with a
hand-check override for homophones and near-identical choruses
(provenance quarantine for identical choruses). Validation bar
(unchanged): construct positives by cross-pairing the 65 KEEP takes
against every other scene's planned words (must score < 0.5), own-pairs
must score ≥ 0.5 with **zero false REJECTs**; plus the real positive MV-2
S04 t3 (proven: t3 sang 30–40 s lyrics at 43–48 s; t4 covers the window,
LCS 15/19) and the S21 candidate pending verification.

**Why it ranks here.** It needs no audio feature, no sensor, and no
separation — the only entry whose inputs already exist and whose bar can
pass this week. It is the first QC check that reads *what* the take sings
rather than how it looks or moves. The cross-pairing fixture becomes
standing QC: every future volley's takes get cross-paired automatically.

**Status:** not built in this loop (research only). Scoped as a small build
— QC script + ledger rule, not a sprint.

### #4 — R5 flow interpolation for BAD-WORD spans (build — routes around the gap)

**What it is.** Loop 3 §2 #4 / loop 4 §2 #5, unchanged: symmetric-flow MCFI
(Raket et al. 2012) — synthesize the missing motion between the good
frames on either side of a bad word instead of cutting to montage. C11
Farneback exists (sprint 7, validated vs cv2); the build is the
warp/blend/hole-fill pipeline plus the symmetric-flow estimation pass.
Bar (unchanged): delete a 0.3–0.5 s span from a KEEP take, interpolate it
back — M6 in KEEP range + eye can't tell + interpolated mouths must not
read as a different word — and at least as clean as ffmpeg `minterpolate`
mci on the same span.

**Why it ranks here.** It is unaffected by the vocal-activity gap: it
routes around the gap's consequence in assembly instead of through it. It
does not need a sensor. If it passes, the BAD-WORD RULE gains an
"interpolate first, cut second" branch for short spans — the only repair
path for takes whose only defect is one bad word.

**Status:** not built in this loop. Scoped as a build, on its own bar.

### #5 — RMVPE pitch tracker on the MDX stem: the definitive vibrato arbiter

**What it is.** WuBuRVC's RMVPE pitch tracker (C11 port matches PyTorch
corr 0.9999 / 0.19 Hz mean diff — already built and parity-verified) run
on the MDX vocal stem, then the c11_vibrato falsifier method run on the
RMVPE track. RMVPE is a neural pitch tracker: it does not pin at
boundaries the way pYIN's Viterbi does, and it does not jump harmonics
the way raw autocorrelation does. It is the one F0 source on this material
that is neither pinned nor jumpy — the definitive arbiter of whether the
chant is straight-tone.

**Why it ranks here.** §1 leaves the straight-tone question structurally
open: pYIN is pinned, autocorr is jumpy, and the stable-frame estimate
sits at the boundary on a biased subset. The question matters because a
real vibrato signature would re-enter as a sensor candidate — but only a
clean F0 track can answer it, and RMVPE is the only clean F0 tracker
already built. Bar: same falsifier method, same 20c boundary; the RMVPE
track must show a 5–7 Hz PSD peak AND a sung median depth ≥20c with
non-overlapping IQRs vs instrumental for the verdict to fall — otherwise
the straight-tone verdict is confirmed on a clean source and the question
closes for good.

**Status:** not run in this loop (research only). Scoped as a measurement,
not a sprint — one RMVPE run + the falsifier method, a day at most.

### Also carried (not ranked — status notes)

- **Mouth-open-vs-quiet gate (loop 1 #3) + CCA AV-sync (loop 2 #3):** still
  blocked on a sensor — but the sensor is now named: the MDX stem-activity
  curve (§3 #2). They calibrate on it, in that order, once §3 #2 passes
  its bar.
- **Snapper stay-rule patch:** still unbuildable on a classical signal.
  Four candidate in-span signals are now dead on MV-14 (c11_voice curve,
  vibrato depth, spectral entropy, vocal-flux both flavours). Remaining
  candidate: MDX stem activity (§3 #2).
- **TSM squeeze-guard band measurement:** STILL OWED (§7).
- **wubu_synth residue (loop 3 #8):** unchanged — a `c11_scaffold` template
  library is a build, scoped only if a sprint's scaffolding is ever written
  twice the same way. Never from wubu_synth as-is.
- **Slopcore vehicle-template changes (loop 3 #7):** unchanged — proposed
  skill edits (kinds system, {END} footer, macro-managed identity, pilot
  pattern), parent applies. No skill edited this loop.
- **Voice-break degree (R8 second half):** CLOSED with jitter/shimmer (§4)
  — same pulse train, same Titze conditions, same failure.

## 4. R8 jitter/shimmer: the blind-drawn entry (TEST, not a rescue) — FAIL AT PRE-CHECK

**What it was.** Loop 3 §2 #3's second half (loop 4 drew it, §8) — jitter
(cycle-to-cycle period variability) and shimmer (cycle-to-cycle amplitude
variability). The hypothesis: the sung voice's cycle irregularity differs
from the accompaniment's — brass is very regular, drums are aperiodic, the
voice sits between with *structured* irregularity. Loop 3 drew "voice
break degree"; loop 4 drew "jitter/shimmer" — the two halves of the same
R8 entry, split across two loops' draws. This loop runs the test.

**Validity pre-check (loop 3 bar, held — must pass before any boundary
scoring):** jitter/shimmer computed on MV-14's mix must satisfy Titze's
conditions (Type 1 periodicity, SNR > 30 dB) on the sung spans.

**What was measured (all three conditions fail):**

| Condition | Bar | Measured | Pass? |
|---|---|---|---|
| Mix SNR, median across sung spans | > 30 dB | **−4.55 dB** (per-span −3.12 to −9.33 dB) | NO |
| Type-1 periodicity, stable fraction of sung frames | ≥ 50% | **4.64%** | NO |
| HNR (autocorr-based), median on trusted sung frames | > 30 dB | **1.69 dB** [−1.51, 5.79] | NO |

The mix SNR is negative on EVERY sung span — the accompaniment carries
more power than the voice in every sung span (voice is 21–33% of mix power
per span; segs 9–10 just 10–11%). The voice is not 30 dB above anything;
it is 4.55 dB BELOW the accompaniment. The Type-1 fraction (4.64%) is the
same stability number as §1's diagnostic — the voice's period is stable on
fewer than 1 in 20 sung frames. HNR 1.69 dB is 28 dB short of the bar.

**Verdict: FAIL AT PRE-CHECK. No boundary scoring.** Per the held bar, the
entry stops here. Voice-break degree closes with it: it needs the same
pulse train and the same Titze conditions, and the pulse train does not
exist on a signal that is 4.6% periodic. **The voice-quality shelf is
closed:** vibrato (no 5–7 Hz peak, no stable carrier), jitter/shimmer
(pre-check fails on all three conditions), voice-break degree (same
failure), CPP/HNR (sprint 8, medians do not separate). Nothing on the
voice-quality shelf survives on MV-14.

## 5. The blind-drawn entry: snapper vocal-flux curve — MEASURED, FAIL

**What it is.** The loop-5 blind draw (§12) selected the snapper's own
vocal-flux curve — the last untested stay-rule candidate. The snapper's
flux is spectral flux (half-wave rectified positive magnitude differences,
normalised to max 1) from the c11_mir STFT front end; the `vocal` flavour
restricts to 300–3400 Hz (suppresses kick/hat), the `mix` flavour is
full-band. The stay-rule question: does the flux curve have a peak inside
the snapped span for correct snaps but not for the 5 snap errors (1-based
indices 34, 56, 60, 112, 162)?

**What was measured (both flavours, three statistics each):**

| Statistic | Errors median [IQR] | Correct median [IQR] | MW p (errors < correct) |
|---|---|---|---|
| Mix flux, max in ASR span | 0.4622 [0.372, 0.644] | 0.4723 [0.400, 0.543] | 0.63 |
| Mix flux, max in snapped span | 0.4622 [0.372, 0.644] | 0.4723 [0.400, 0.543] | 0.63 |
| Mix flux at snapped position | 0.2892 [0.222, 0.353] | 0.3153 [0.266, 0.393] | — |
| Vocal flux, max in ASR span | 0.5043 [0.324, 0.668] | 0.4714 [0.414, 0.567] | 0.50 |
| Vocal flux, max in snapped span | 0.5160 [0.324, 0.668] | 0.4714 [0.414, 0.567] | 0.50 |
| Vocal flux at snapped position | 0.2704 [0.185, 0.293] | 0.2945 [0.182, 0.375] | — |

The vocal-flux curve was recomputed from the mix STFT (300–3400 Hz bins
20–217); the replication was validated first — my mix-flux recomputation
correlates **1.0000** with the on-disk `flux.txt`, so the vocal numbers are
trustworthy. (Note: the on-disk `flux.txt` and the snap run that produced
`snap_mix_mv14.json` used the MIX flavour, not the vocal default — the
vocal curve had never been computed before this loop.)

**Verdict: FAIL.** No statistic separates on either flavour. The mechanism
is structural: the snapper snaps TO flux peaks, so error snaps sit near
peaks too — the errors are small displacements (0.05–0.14 s) to nearby
peaks, not off-peak. The snapped-span max EQUALS the ASR-span max (same
peak caught in both windows). Flux measures change, and the change is
present at both the true and the displaced positions. The vocal flavour is
if anything worse (errors 0.5043 HIGHER than correct 0.4714).

**Consequence.** The stay-rule patch has no classical in-span candidate
left. Dead: c11_voice curve, vibrato depth, spectral entropy, vocal-flux
(both flavours). Remaining: MDX stem activity (§3 #2) — the only one left.

## 6. The per-loop break-the-sync probe (loop 5) — UNRUN, snapper data absent

**The MV-13 "Fourth law" ×4 repeat probe, not run.** Loop 4 corrected loop
3's mislabel ("Fourth law" is MV-13's hook, not MV-14's) and ran the MV-14
probe (PASS, 0 collapse hits). The MV-13 half needs MV-13's snapper
output — snapped times vs ASR times for the "Fourth law" repeats.

**Searched:** all of `~/workspace` for `snap*13*` / `*mv13*` word-time
files. The only MV-13 word-time file on disk is the Whisper ASR output,
`MV-13_movin-on-newton/analysis/SONG_WORDS.json` (394 words, start/end/
prob — ASR times, no snapped times). No `snap_mix_mv13.json` or
equivalent exists. The probe question (does the snapper glue repeats?) is
unanswerable without the snapper's output: the ASR times alone have no
snapped times to compare against.

**Follow-up (loop 6):** run the MV-13 snapper (sprint 5 tool,
`SPRINT_2026-11-11_C11_SNAPPER.md`), then run this probe on its output.
The "Fourth law" repeats are confirmed present in the MV-13 lyrics (the
hook runs to four-plus repeats in the back half), so the material is
waiting, not missing.

## 7. TSM squeeze-guard check — STILL OWED

Checked `tsm-driedger-2014/stretched/`: it holds only the S47/S49/S50/S52
validation takes (M1–M7 methods). No moderate-squeeze take (gap alpha
0.5–0.87) has landed. The scope §63 (a) item — one moderate-squeeze take
to set the guard precisely between 0.5 and 0.87 — is still open. Loop 5
notes it; it does not do it. Loop 6 checks again.

## 8. Loop-6 seed

1. **c11_sep sprint runs** (scope in loop-05/SPRINT_SCOPE.md). Bar: <894 s,
   stem corr ≥0.95, boundaries ±0.5 s, active/silent ≥100×.
2. **MDX stem-activity sensor validation** (§3 #2): the stem-activity curve
   reproduces Demucs stem-activity boundaries within ±0.5 s AND separates
   sung from instrumental with non-overlapping IQRs. If it passes, the
   mouth-open gate, CCA AV-sync, and snapper stay-rule patch calibrate on
   it, in that order.
3. **RMVPE-on-MDX-stem vibrato arbiter** (§3 #5): the definitive
   straight-tone answer on a clean F0 track. If it falls, vibrato re-enters
   as a sensor candidate and the loop-7 seed changes; if it stands, the
   question closes for good.
4. **G7 + R5 builds proceed on their own bars** regardless of c11_sep.
5. **MV-13 snapper run → Fourth-law probe** (§6): the unrun probe needs
   snapper output first.
6. **TSM squeeze-guard check again** (§7): the moderate-squeeze take is
   still owed.

## 9. Proposed skill edits (draft only — parent applies, no skill edited this loop)

1. **Vehicle template (carried from loop 3 #7, unchanged):** kinds system
   (lips / motion / insert), the {END} prohibition footer on every vehicle,
   macro-managed identity, pilot pattern. Source: slopcore PROMPTS.md, measured.
2. **BAD-WORD RULE (conditional on R5 passing):** "interpolate first, cut
   second" branch for 0.3–0.5 s spans — only after the M6 + eye + mouth tests pass.
3. **QC gates:** add G7 (word-set overlap < 0.5 → REJECT, cross-pairing
   positives as the fixture, homophone hand-check override) once §3 #3's
   validation passes.
4. **Snapper stay-rule (conditional):** MDX stem activity as the in-span
   peak-evidence signal — only once §3 #2 passes its bar. Vibrato depth,
   spectral entropy, and vocal-flux (both flavours) are all dead as
   candidates; do not list them.
5. **F0-source rule (new, from §1):** never use a saved pYIN track's f0_hz
   as "the voice's F0" without a pinning audit (fraction of voiced frames
   at fmin/fmax). Sprint 8's saved tracks are NOT voice-F0 tracks (mix 81%
   pinned at 50 Hz, stem 63% pinned at 800 Hz). The stem-autocorrelation
   reference (median F0 238.8 Hz) is the correct voice-F0 source on this
   material until RMVPE-on-stem (§3 #5) replaces it.

## 10. Honest scope

- **Code was run:** vibrato re-measurement v1 (integer lag) + v2
  (sub-sample parabolic peak) + controls + stability diagnostic; R8
  pre-check (three conditions); MDX adoption verification (corr +
  envelope corr + segments + active/silent); snapper-flux test on both
  flavours (three statistics each). Every number in this report is in
  `loop5_validation.json`, reproduced from `vibrato_remeasure.json`,
  `vibrato_remeasure_v2.json`, `r8_precheck_mdx_verify.json`,
  `snapper_flux_test.json`, `snapper_vocal_flux_test.json` (scripts in
  loop-05/, inputs on disk, unchanged).
- **One misdiagnosis caught and corrected in-loop:** v1's 114c was first
  attributed to integer-lag quantization; v2 falsified that (sub-sample
  gives the same numbers). The 114c is tracker instability. The falsified
  diagnosis is recorded here, not hidden.
- **One transcription error caught and corrected:** the first draft of
  `loop5_validation.json` carried HNR IQR [0.92, 2.60] from memory; the
  script output is [−1.51, 5.79]. Fixed from the script output before the
  report was written. (Parent's registry lesson, applied to my own files:
  never hand-copy a number — read it from the JSON.)
- **Two experiments failed, one probe unrun:** vibrato re-measurement
  (no 5–7 Hz peak, no stable carrier — verdict STANDS on corrected
  grounds), R8 pre-check (fails on all three conditions), snapper
  vocal-flux (fails on both flavours). MV-13 probe unrun (no snapper data).
- **Web-verified claims:** vibrato straight-tone boundary 20c (Nix et al.
  2016, carried); jitter/shimmer validity (Titze 1995; Deliyski 2005;
  Patel et al. 2018 — carried from loop 3); CASA (Bregman 1990; Licklider
  1951; Slaney & Lyon 1990; Shao et al. 2010 — carried from loop 4); MCFI
  (Raket et al. 2012 — carried). Full citations in SOURCES.md entries 56+
  (loop 3's file; loop 5 adds no new source file — see the gap note in §10
  of loop 3, still open: no shared SOURCES.md exists).
- **Measured on disk (reproducible):** MDX corr 0.9676; vibrato
  re-measurement 114.31c smoothed / 189.26c raw, PSD peak 3.0 Hz, stable
  fraction 4.6%, stable-frame depth 17.82c; R8 SNR −4.55 dB / Type-1 4.6% /
  HNR 1.69 dB; vocal-flux errors 0.5043 vs correct 0.4714 (p=0.50).
- **What this loop did NOT do:** no re-run of sprint 8's calibration; no
  lowering of any bar; no gate built from a failed experiment; no video
  generation; no commit; no Telegram write; no skill edit.

## 11. Top 5 (for the parent's report)

1. **c11_sep separation runner** — adoption decided; the sprint that makes
   MDX cheap. Scope written (loop-05/SPRINT_SCOPE.md). Bar <894 s, stem
   corr ≥0.95, boundaries ±0.5 s, active/silent ≥100×.
2. **MDX stem activity as the stay-rule / gate sensor** — the only in-span
   candidate left; RMS-VAD on the MDX stem, validated against the Demucs
   stem curve. Unblocks mouth-open, CCA, stay-rule.
3. **G7 wrong-lyric gate (small build)** — word-set overlap < 0.5 →
   REJECT; real positive MV-2 S04 t3 + cross-pairing fixture; zero false
   REJECTs on own-pairs. Highest-certainty deliverable in the loop.
4. **R5 flow interpolation (build)** — symmetric-flow MCFI; Farneback
   exists; routes around the vocal-activity gap in assembly. Bar: M6 in
   KEEP range + eye can't tell + mouths don't read as another word.
5. **RMVPE on the MDX stem: the definitive vibrato arbiter** — the one
   clean F0 tracker already built; settles straight-tone for good. Bar:
   5–7 Hz PSD peak AND sung median depth ≥20c with non-overlapping IQRs,
   or the question closes.

## 12. Blind draw (method audit)

Drawn with `secrets.choice` from a 12-item candidate pool of loop-5 ideas:
`MDX-Net stem activity as stay-rule sensor, snapper vocal-flux curve, G7
wrong-lyric gate, R5 flow interpolation, TSM squeeze-guard band
measurement, mouth-open-vs-quiet gate on MDX stem activity, CCA AV-sync on
MDX stem activity, kinds system (vehicle template), macro-managed identity,
pilot pattern, {END} prohibition footer, wubu_synth c11_scaffold residue`.
**Draw: "snapper vocal-flux curve"** (first draw accepted, no discard).
Checked: 0 whole-word occurrences of any pool phrase in
`~/workspace/wubutv-network/ideas/BAN_LIST.md` (3,185 lines); not among
banked form ideas (COMPASS, VESSEL, CRADLE SHOT, SATELLITE ORBIT, HARBOR,
RIVER, FEATHER).
**Deviation, stated plainly:** the pool excludes the three assigned threads
(adoption/c11_sep, vibrato re-measurement, R8 jitter/shimmer) — unlike
loops 3–4, whose pools included the drawn item's own thread, loop 5's
threads were assigned by the brief before the draw, so the pool was built
from the remaining live candidates only. The draw is load-bearing in the
method's sense: it forced the snapper vocal-flux curve into a full measured
entry (§5) with its own bar instead of letting it sit as an unexamined
"remaining candidate" — and the measurement killed it, which sharpens the
loop-6 seed (MDX stem activity is now the only candidate left).
