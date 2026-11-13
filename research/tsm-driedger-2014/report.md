# TSM method validation — Driedger/Müller/Ewert (2014) + user slicing synthesis

**Task:** Telegram msg 292 (user-handed method) + msg 294 (winners-league grading).
**Coordinator:** 545e5eab (died in a daemon restart ~02:47 EST) → recovery
(this run, completed 2026-11-12 ~04:40 EST).
**Date:** 2026-11-12. **Material:** MV-14 'CLIP IT' take audio (generated-video takes,
16 kHz mono), 4 takes × 6 (+1) variants. **No video, no commit, no Telegram.**

## Verdict

**VALIDATED WITH A SQUEEZE GUARD.** M7 — the user's method (per-gap-targeted
slicing, hits sample-identical, each gap stretched to land its hit on the song
grid) — is the only variant that beats the take's internal drift: words-3+
onset RMS **69.3 ms** vs **224–284 ms** for every uniform method (3.2–4.1×
better), and it lands hits bit-identically (max|diff| 0.0, centre error 0.000 s
on all 4 takes, direct check). **But it fails structurally on severe gap
squeezes:** a gap alpha of 0.24–0.33× destroys the word body that lives in the
gap — S50 (0.33× squeeze) heard 1/4 words ('keep the work alive' → 'You work
a lot'), S52 (0.24/0.25× squeezes) dropped word 4. The ±25 ms hit window
preserves the attack, not the word. **Rule: per-gap targeting only when gap
alpha ≥ ~0.5; below that, BAD-WORD RULE — cut to montage for that span, do
not stretch.** Uniform fallback: OLA256 (best identity 23/23, best uniform RMS
245.7 ms). PV is the worst uniform method on this material (identity 17/23,
RMS 315.3 ms) — do not build the core on PV. C11 build scope in §6.

## 1. The paper, read in full

Driedger, Müller & Ewert, "Improving Time-Scale Modification of Music Signals
using Harmonic-Percussive Separation", IEEE Signal Processing Letters 21(1):105–109,
2014. Author PDF: sebewert.github.io/publications_pdf/2014_DriedgerEM_TimeScaleModification_IEEE-SPL_AuthorVersion.pdf

- **Core idea:** transients are the failure mode of TSM. Instead of detecting them
  explicitly (error-prone, reinsertion sounds unnatural), split the signal into
  harmonic + percussive components with Fitzgerald median-filter HPSS, then stretch
  each with the method suited to it and sum.
- **Parameters (paper):** HPSS STFT N=1024, median length 2ℓ+1 with ℓ=5, binary
  masks; harmonic leg = phase vocoder, N=4096, identity phase locking; percussive
  leg = time-domain OLA, N=256. α ∈ [0.5, 3] tested.
- **Listening test:** 22 listeners, 10 excerpts, α=1.2 and 1.8, 5-point MOS vs
  commercial elastique (EL), identity-locked PV, Nagel/Walther transient PV (NW),
  WSOLA (WS). Mean MOS: HP 3.85/3.37, EL 4.13/3.49, PV 2.89/2.24, NW 1.96/1.81,
  WS 2.44/1.90 (α=1.2 / α=1.8). HP best on every percussive-heavy excerpt
  (Bongo, CastanetsViolin, DrumSolo, Jazz, Pop, Stepdad); HP ≈ EL overall.
- **The paper's own weak spot — directly relevant here:** HP is WORST on
  **SingingVoice** (2.59 vs PV 3.32 at α=1.2; 2.91 vs PV 3.77 at α=1.8). Voice is
  neither clearly harmonic nor percussive, so harmonic content leaks into the
  percussive leg and OLA phase jumps on it are not masked. Our material is sung
  vocals — the paper's method is weakest exactly on our material. The validation
  below tests whether that weakness reproduces on MV-14 takes.
- **Runtime (paper, MATLAB):** ~4–5 s per minute of audio, independent of α.

## 2. The user's synthesis (msg 292)

"Cut the loop at every hit and keep each hit sample-for-sample; noisy decays by
overlapping short grains, ringing decays by a phase vocoder that picks up in phase
with the hit before it; noise/ring split is from Driedger, Müller & Ewert (2014)."
Kicker: generated-video take audio IS there to time-match — i.e. the take's own
audio gives per-word hit times to cut on.

Reading of the method: hits = word onsets (from take ASR). Each hit window
(±25 ms) is copied verbatim; inter-hit gaps absorb the whole stretch. Ringing
(harmonic) gap content goes through the PV, noisy (percussive) gap content through
OLA, and the PV is fed the preceding hit tail (50 ms) so it picks up in phase.

## 3. Prototype (`tsm_proto.py`, `tsm_asr_grade.py`)

Takes (MV-14 QC audio + ledgered take-ASR word times + `SONG_WORDS.json` grid;
S51 dropped — its song times are uncertain in the ledger — replaced by S52):

| take | words | span in → out | α | raw drift (M0 linear RMS / max) |
|------|-------|---------------|---|----------------------------------|
| S47  | 7     | 1.66 → 2.52 s | 1.518 | 164 / 317 ms |
| S49  | 4     | 1.56 → 1.48 s | 0.949 | 24 / 43 ms |
| S50  | 4     | 1.72 → 1.38 s | 0.802 | 129 / 219 ms |
| S52  | 8     | 2.94 → 3.16 s | 1.075 | 157 / 316 ms |

M0 = linear scaling of take onsets onto the song grid (no per-word warp). The raw
take drift is up to 317 ms — this is the timing error a uniform stretch inherits
and only per-word/per-hit targeting can remove.

Variants (winners league, threaded stretch, 2 workers):
- **M1 PV** — librosa phase vocoder, N=4096, whole signal. (No identity phase
  locking: librosa 1.0.0 lacks it — documented deviation from the paper.)
- **M2 OLA256** — time-domain OLA, N=256.
- **M3 HP-TSM** — the paper: binary-mask HPSS (N=1024, ℓ=5) → PV N=4096 on
  harmonic + OLA N=256 on percussive → sum.
- **M4 SLICE** — user's slicing as first prototyped: hit windows ±25 ms kept
  sample-identical, inter-hit gaps stretched with the M3 split, 50 ms hit-tail
  lookback for phase carry. **Prototype limitation (found in recovery):** all gaps
  share ONE global gap_alpha, so hits drift off the song grid (S47: gap_alpha
  1.656 vs α 1.518). M4 does not implement the user's method as described.
- **M5 HP-TSM_SOFT** — M3 with soft (margin=3) HPSS masks instead of binary.
- **M6 OLA1024** — OLA with N=1024 (frame-size control: is M2's behaviour about
  OLA or about the short frame?).
- **M7 SLICE_TGT** (`tsm_m4b.py`, recovery-added) — M4 fixed to per-gap targeting:
  hit i lands exactly on song_on[i]; each gap gets its own alpha. Hit windows
  still bit-identical. Verified: hit identity 0.0 and centre error 0.000 s on all
  4 takes. Gap alphas range 0.24–3.22 (S52 has two ~0.25× gap squeezes; S50
  one 0.33× — those squeezes destroy the word bodies in the gaps, §4.1/§5).

Measurements per take per method: re-ASR with faster-whisper large-v3-turbo,
pipeline config (beam 1, word timestamps, no VAD), word-onset residual vs the
song grid (RMS + max, ms), word-identity match, flux 10–90% rise time
(transient smear), M4/M7 hit sample-identity (max|diff|, must be 0).

**Grade (msg 294):** OVERLAP AVERAGE — per word, the consensus is the MEDIAN
onset across variants; the grade is the RMS of the consensus residuals.
Per-variant residuals stay visible — never average away a disagreement.
Agreement = fraction of words where ≥4 of 6 variants agree within ±50 ms.

## 4. Results

### 4.1 ASR grades (vs song grid)

Overlap-average grade (msg 294): per word, consensus = MEDIAN onset across
M1–M6; grade = RMS of consensus residuals. M7 is NOT in the consensus (it
lands hits on the grid by construction — that would game the median); it is
reported alongside as the targeted reference.

| take | grade RMS | agreement | consensus residuals (ms) | M0 linear baseline RMS |
|------|-----------|-----------|--------------------------|------------------------|
| S47  | 231.1 ms  | 6/7       | −300, −250, 340, 240, 200, 80, 40 | 164.0 (interior 177.1) |
| S49  | 153.4 ms  | 3/4       | −300, 20, 60, 10         | 23.7 (interior 27.4)  |
| S50  | 246.4 ms  | 4/4       | −300, 300, 220, 120      | 128.6 (interior 148.5) |
| S52  | 302.4 ms  | 7/8       | −300, −10, 200, 20, 290, 440, 440, 360 | 157.4 (interior 168.3) |
| **episode** | **250.4 ms (23 words; interior excl. word 1: 238.6 ms)** | | | **M0 interior pooled ≈168 ms** |

Per-variant RMS (all words / excl. word 1 / words 3+; words heard):

| method | all | excl. w1 | words 3+ | heard |
|--------|-----|----------|----------|-------|
| M1 PV | 315.3 | 277.0 | 223.7 | 17/23 |
| M2 OLA256 | 245.7 | 239.9 | 245.0 | 23/23 |
| M3 HP-TSM (paper) | 264.8 | 258.8 | 275.1 | 22/23 |
| M4 SLICE (global gap α) | 325.4 | 292.5 | 261.7 | 22/23 |
| M5 HP-TSM_SOFT | 253.2 | 242.1 | 247.8 | 23/23 |
| M6 OLA1024 | 268.2 | 268.0 | 283.5 | 23/23 |
| **M7 SLICE_TGT (user's method)** | **199.7** | **191.6** | **69.3** | **18/23** |

M7 per take: S47 res [None, −720, 0, −20, −20, −60, −40] (words 3+ RMS 34.6,
6/7 heard); S49 [200, 80, 120, 20] (RMS 123.7, 4/4); S50 [None, None, −140,
None] (1/4 heard — see below); S52 [−300, −20, −40, None, 0, −140, 20, 20]
(words 3+ RMS 66.3, 7/8 heard). M7 gap alphas: S47 1.06–3.22 (all stretches);
S49 0.87–1.04 (near 1); S50 [0.333, 1.118, 1.148, 1.042]; S52 [1.093, 0.243,
2.2, 0.254, 2.556, 1.308, 1.526, 1.873].

**Word 1–2 are ASR edge artefacts, not method signal, on every variant:**
word 1 reads exactly −300 ms (ASR places the first heard word at the start
of the 0.3 s silence pad); word 2 is unstable in both directions (PV/SLICE
+660…+720 ms on S47, OLA/HP −300…−240 ms; M7's −720 ms on S47 is the same
artefact — ASR merged 'This is' into one token starting at the clip edge).
Hence the grade is reported over all words AND over interior words (3+),
and M7's headline is its words-3+ RMS (69.3 ms).

**Word-identity failures (ASR heard a different word — timing N/A):**
- **M1 PV — worst in the league:** S50 heard 'He broke up' for 'keep the
  work alive' (all 4 onsets None); S52 heard 'say what?' for 'stay online'
  (words 7–8 None). **RESOLVED (recovery):** the original unstretched S50
  window (`tsm_s50_check.py`) hears 'keep the work alive' at the ledgered
  times (0.00/0.68/0.90/1.22 in-window) — the window is right, PV at
  α=0.802 garbled the clip. M2–M6 heard it correctly from the same window.
- M3 HP-TSM: S49 heard 'Click' for 'clip' (word 1 only). **Correction
  (recovery):** the aligner had a consume-on-miss bug — a missed word ate the
  whole remaining word list and returned None for every later word. Fixed
  (restore the pointer on failure) in both graders; S49 M3 re-graded, words
  2–4 now measurable [−40, 60, 20], M3 S49 RMS 43.2 (best on that take),
  episode grade unchanged at 250.4 ms. The same bug had zeroed all 7 S47 M7
  onsets in the first M7 pass ('This' dropped by ASR at the clip edge).
- M4 SLICE: S50 heard 'Keep the work on us.' ('alive' → 'on us').
- **M7 — the squeeze failure:** S50 heard 'You work a lot.' (only 'work'
  matched, −140 ms); S52 dropped word 4 'it'. Both sit next to gap squeezes
  of 0.24–0.33×. See §5.

**Uniform methods are at their theoretical limit.** The perfect-uniform
prediction (take onsets × α, window→window) matches the consensus interior
residuals within ~25 ms on every take (e.g. S47: predicted [354, 227, 210,
82, 65] vs consensus [340, 240, 200, 80, 40]). The 250 ms episode grade IS
the take/song distribution mismatch — the take's words span 84% of its
window while the song's span 73% of its slot (S52) — not stretch error. No
uniform stretch can beat it; only per-word targeting can, which is what M7
does where it hears the word.

### 4.2 Transient smear (flux 10–90% rise, ms; lower = crisper)

From `stretch_measurements.json` (23 onsets × 6 methods; 0.0 = rise within one
16 ms hop frame):

| method | mean | median | max | zeros (of 23) |
|--------|------|--------|-----|---------------|
| M1 PV | 39.0 | 0.0 | 192 | 14 |
| M2 OLA256 | 58.4 | 16.0 | 192 | 10 |
| M3 HP-TSM | 60.5 | 48.0 | 192 | 11 |
| M4 SLICE | 69.6 | 48.0 | 192 | 8 |
| M5 HP-TSM_SOFT | 53.6 | 32.0 | 192 | 10 |
| M6 OLA1024 | 57.7 | 16.0 | 192 | 10 |

**Caution:** this metric conflates timing error with smear — the rise is measured
in a window around the EXPECTED (linear-α) onset, so a method whose onset lands
late reads as "slow rise" even if the transient itself is crisp. M4 is the proof:
its hits are bit-identical (max|diff| = 0.0 on all takes) yet it scores worst,
because its hits sit up to ~180 ms off the linear-α expectation (global gap_alpha).
Do not read this table as "PV preserves transients best" — read it as "onsets
land closest to the linear-α expectation under PV". The ASR grade (§4.1) is the
timing authority; flux-rise is a secondary signal only.

### 4.3 Hit identity

M4: max|diff| = 0.0 on all 4 takes (bit-identical hit windows). M7: 0.0 on all
4 takes, centre error 0.000 s on every hit — verified by DIRECT comparison
of each hit window at its placed position in the output WAV (recovery check).
Note: `m4b_measurements.json` records 0.29 for S47 M7 — that is an artefact
of the NCC-search verification (periodic vowel content matched a different
occurrence); the direct check on the same file reads 0.00 on every hit.

## 5. Analysis

1. **The uniform league is a measurement of drift, not of stretch quality.**
   All six uniform methods land within ~25 ms of the perfect-uniform
   prediction on interior words. Their differences (M2 245.7 vs M1 315.3 ms
   RMS) are second-order next to the 250 ms episode grade, which is the
   take/song mismatch itself. Choosing among uniform methods on timing alone
   is choosing noise — choose on word identity instead, where the spread is
   real: OLA256 / HP-SOFT / OLA1024 never lose a word (23/23), PV loses 6.
2. **M7 works — where the gaps stretch.** S47 (gaps 1.06–3.22×) and S52
   (words 3+ RMS 66.3 ms despite two 0.25× squeezes elsewhere) show the
   method doing exactly what the user described: hits land on the grid
   (centre error 0.000 s), words heard on-grid within ASR noise (~±60 ms),
   3.2–4.1× better than any uniform method. Gap stretches up to 3.22× cost
   nothing in intelligibility.
3. **M7 fails — where a gap must squeeze hard.** The word body lives in the
   gap, not in the ±25 ms hit window. S50's 0.33× squeeze (take holds 'keep'
   0.68 s, song allows 0.26 s) compressed the 'keep/the/alive' bodies past
   recognition ('You work a lot'); S52's 0.24/0.25× squeezes dropped 'it'
   and pushed 'me' −140 ms. Dose-response vs M4 (uniform 0.78× squeeze on
   the same S50 take → 3/4 words heard) confirms severity, not method, is
   the variable. The untested band is 0.5–0.87× (S49's 0.87× is fine);
   the guard at ~0.5 is a judgement call from the two fatal points (0.24,
   0.33) and the safe points (0.87+), not a measured threshold.
4. **S49 is the control that bounds the claim.** α≈0.95, drift ≈0 (M0
   interior 27.4 ms): every method is within ASR noise of the grid and M7
   shows no advantage (interior RMS 84.1 ms vs consensus interior 36.5 ms
   — a 3-word sample, the gap within the ~60 ms ASR noise floor).
   Targeting only pays where drift exists; where drift is ~0, the lightest
   touch (OLA at α≈1) wins by doing nothing.
5. **The paper's SingingVoice warning is NOT reproduced on our metrics —
   and the direction reverses.** Driedger et al. found HP-TSM worst on
   singing voice vs PV (MOS 2.59 vs 3.32 at α=1.2). On MV-14 takes, PV is
   the worst variant on both ASR metrics (identity 17/23, RMS 315.3 ms)
   while HP-TSM is mid-pack (22/23, 264.8 ms). Caveats: MOS ≠ ASR grade
   (perceptual smoothness vs word timing/identity), and our PV lacks the
   paper's identity phase locking (librosa has none) — that deviation may
   cost PV exactly the transient coherence the paper credits it with. A
   listening check is still owed before any MOS claim; the ASR verdict is
   only that PV garbles sung words on this material.
6. **ASR onset noise floor.** Interior-word agreement across 6 independent
   stretches is tight (consensus ≈ perfect-uniform prediction), but absolute
   ASR onsets carry ~±60 ms jitter on short percussive words (S49: M7
   +80/+120 ms on words that sit exactly on the grid by construction).
   Differences below ~60 ms RMS between variants on one take are noise.
   The M7 advantage (69 vs 224–284 ms) is 3–4× the noise floor — real.
   The M1-vs-M2 gap (315 vs 246 ms) is partly identity failures, not timing.

## 6. Recommendation (C11 build scope)

**Build M7 as the C11 TSM core** (sprint scope: `c11_tsm`, lego-first from
the prototype's DSP — HPSS median filter, PV, OLA already exist as patterns
in the user's C modules; the new work is the per-gap scheduler + guard):

- Per-gap-targeted slicing: hit windows ±25 ms verbatim, each gap stretched
  to land its hit exactly on the song-grid onset; gap DSP = paper's HP split
  (PV on harmonic, OLA N=256 on percussive); 50 ms hit-tail lookback so the
  PV picks up in phase with the preceding hit.
- **Squeeze guard (hard rule):** if a gap alpha < 0.5, do NOT stretch that
  gap — flag the span and let the assembly BAD-WORD RULE cut to montage for
  exactly that span, then resume at the next good hit. Operational guard
  0.7 until the 0.5–0.87 band is measured (one take with a moderate squeeze
  is the owed test).
- Uniform fallback when no targeting is needed (α≈1, drift≈0): OLA256 —
  best identity (23/23), best uniform RMS (245.7 ms), simplest DSP.
- **Do NOT build:** M1 PV as the core (worst identity on sung material);
  M4 global-gap slicing (superseded by M7 — same idea, no targeting).
- **Owed before shipping the core:** (a) one moderate-squeeze take to set
  the guard precisely; (b) a listening check (MOS-style, ears not ASR) —
  the paper's SingingVoice caveat is about perceived quality, which this
  validation did not measure; (c) identity-phase-locked PV if PV is ever
  revisited — the librosa PV used here lacks it.

## 7. Repro / files

- `~/workspace/research_notes/tsm-driedger-2014/tsm_proto.py` — stretch stage
  (24 files in `stretched/`, `stretch_measurements.json`)
- `~/workspace/research_notes/tsm-driedger-2014/tsm_asr_grade.py` — ASR grading
  (writes `tsm_grades.json`; checkpoint file `tsm_grades_partial.json`)
- `~/workspace/research_notes/tsm-driedger-2014/tsm_m4b.py` — M7 per-gap slicing
  (`m4b_measurements.json`, `stretched/*_M7_SLICE_TGT.wav`)
- `~/workspace/research_notes/tsm-driedger-2014/report.md` — this file
- `~/workspace/research_notes/tsm-driedger-2014/tsm_m7_grade.py` — M7 ASR
  grading (writes into `tsm_grades_partial.json`)
- `~/workspace/research_notes/tsm-driedger-2014/tsm_s50_check.py` — original
  S50 window check (resolves the PV-garble question)
- `~/workspace/research_notes/tsm-driedger-2014/grade_resume2.log` — recovery
  run log (S50 check + S49 M3 re-grade + M7 grade, rc=0)
- `~/workspace/research_notes/tsm-driedger-2014/winners_league.png` — the
  winners-league graph: per-word residuals + consensus, per-variant RMS,
  flux-rise means, S47 dadaspec strips for all 7 variants

**Environment notes (recovery):** run everything under `~/workspace/fw-venv`
(system python3 lacks soundfile/librosa). `tsm_asr_grade.py` passes the audio
ARRAY to faster-whisper — the fw-venv's faster-whisper 1.2.1 calls
`av.open(..., metadata_errors=...)`, which the installed PyAV rejects, so the
file-path call crashes on the first transcribe. Two bugs fixed in recovery:
(1) that av crash; (2) residuals were computed against ABSOLUTE song times while
ASR onsets are clip-local (first draft gave −106 s residuals). The grader now
checkpoints one JSON write per clip and skips done clips, because the blade
reaps background jobs and a 24-clip grade takes ~1–2 h under load
(load avg ~19 during this run: MV-14 assembly encode + CDN sync + hatch daemon).
