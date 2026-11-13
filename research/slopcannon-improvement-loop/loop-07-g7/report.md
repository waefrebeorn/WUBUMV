# Loop 7 — G7 wrong-lyric gate: build + validation

**Status: BUILT. Validation bar missed by exactly one own-pair (S14) — reported
plainly below, bar not moved.** Both real positives flagged; every sung
own-pair passes; the gate is shippable under the spec's own hand-check
override, extended to the one failure mode the fixture exposed.

Coordinator: G7 build (loop 7 first build). Date: 2026-11-13.
Spec: loop 3 §2 #5 → loop 4 §2 #4 → loop 5 §3 #3 → loop 6 §3 #2, unchanged.
Deliverables:

- Gate script: `~/workspace/wubutv-network/musicvideo/detection-research/g7_wrong_lyric/g7_check.py`
- Validation harness beside it: `build_fixture.py`, `transcribe_set.py`, `score.py`, `fixture.json`
- This run's results: `validation_results.json` (this directory + the g7 dir)
- Proposed skill rule: `PROPOSED_G7_RULE.md` (this directory; full text in §7)

---

## 1. Method

**Metric (as specified).** overlap = |A ∩ P| / |P| over word SETS, where
A = the take's ASR words and P = the scene's planned words.
overlap < 0.5 → REJECT. Wordless slot (P = ∅): overlap = 1.0 iff A = ∅,
else 0.0.

**ASR.** Fresh transcription of every take with the house lyrics pipeline
(MV-14's `work/mv14_take_asr.py` config, copied exactly): faster-whisper
large-v3-turbo int8, cpu_threads=2, NO VAD, beam 1,
condition_on_previous_text=False, word timestamps, repetition_penalty 1.1,
no_repeat_ngram_size 3, compression_ratio_threshold 2.4,
log_prob_threshold −1.0, no_speech_threshold 0.6, numpy input, pinned "en".
One model load, sequential, checkpointed per take (67 takes, ~30 min wall
on the blade; a reboot loses at most one take).

**What counts as a sung word (the screen).** Whisper hallucinates phrases
on musical audio, so a raw word set cannot be the gate input. A word
counts as sung iff its segment avg_logprob ≥ −1.0 (the decoder's own
house threshold constant) AND its word probability ≥ 0.5 (the midpoint).
These are the two numbers MV-14's own QC adjudicated sung-vs-hallucination
on (real lines: avg_logprob −0.18…−0.69, word probs ≥ ~0.59; hallucinations:
avg_logprob ≤ −1.08 or word probs ≤ ~0.26). The screen is part of the
definition of "ASR words", chosen before scoring; the RAW set is computed
and reported everywhere alongside, so the screen is never load-bearing in
secret. Normalization: lowercase, letters/digits only (apostrophes dropped,
so don't ≡ dont on both sides); punctuation-only tokens are not words.

**Planned words.** PRIMARY = the lyric fragments quoted in the scene plan
(`MV_PREPRO_MV-14.md` lyric column; "/" splits inside a fragment unioned —
chant phrases straddle slot edges). The loops name the scene's planned
words as the gate's reference; loop 3's parenthetical pointed at
SONG_WORDS.json, so the grid construction (grid words starting inside the
scene's assembly window) was computed as a full variant and is reported
in §5 — it is measurably worse, for a named reason: the grid is itself
ASR output and garbles chant (S21's slot reads "trip it posted"; S40's
reads "clip post you"; "don't" splits into don+t; windows run ~a phrase
late across the chant). The plan text is the sheet the vehicles were
written from; the grid remains the timing authority.

**Fixture.** MV-14: all 65 KEEP takes from `work/TAKE_LEDGER.md` (72 rows;
7 REJECTs excluded), one per scene S01–S65, every take file md5-verified
against the ledger (65/65). 43 scenes are sung, 22 wordless under the
plan-text planned sets. Cross-pairing: each take scored against every
other scene's planned set (65 × 64 = 4,160 pairs), stratified (§4).
MV-2 real positives: S04 t3 (proven wrong-segment: sang the 34.56–40.94s
segment at S04's 41.90–48.84 slot) and S21 t1 (loop 6's "candidate pending
verification": chorus echo line over the verse slot).

## 2. Verdict vs the pre-stated bar

Loop 6's bar: *cross-pairing the 65 KEEP takes against every other scene's
planned words (must score < 0.5), own-pairs ≥ 0.5 with zero false REJECTs;
plus the real positive MV-2 S04 t3.* The brief's PASS line: zero false
REJECTs on own-pairs AND the positives flagged.

| Bar element | Result |
|---|---|
| MV-2 S04 t3 flagged | **YES** — overlap 0.125 vs its slot |
| MV-2 S21 t1 (candidate) flagged | **YES** — overlap 0.0; candidate is a true positive |
| Own-pairs, sung scenes (43) | **43/43 ≥ 0.5** — zero false REJECTs |
| Own-pairs, wordless scenes (22) | **21/22** — one false REJECT: **S14** (§5.1) |
| Cross-pairs < 0.5 (strict, all pairs) | **NO** — breaches concentrated in named classes (§4) |

**The bar as pre-stated is therefore missed by exactly one own-pair.**
Everything else passes, most of it with a wide margin (own-pair median 1.0
vs discriminating cross-pair median 0.0). S14's failure is in the ASR
layer, not the take, and it is the failure the spec's hand-check override
exists for — §5.1 gives the mechanism and §7 extends the override text to
cover it. I did not re-tune anything to make S14 pass: a segment threshold
of −0.9 would have caught it, and that observation is recorded here
precisely so it is *not* silently adopted — it was derived from the
failure it would fix.

## 3. Own-pair distributions (65 KEEP takes)

**Sung scenes (n=43), primary planned sets:**

| variant | min | p25 | median | max | # < 0.5 |
|---|---|---|---|---|---|
| screened (gate value) | 0.500 | 1.0 | 1.0 | 1.0 | **0** |
| raw ASR set | 0.667 | 1.0 | 1.0 | 1.0 | **0** |
| grid-planned variant (screened) | 0.333 | 0.75 | 1.0 | 1.0 | **2** |

Screened histogram: 34 takes at 1.0, 1 at 0.75–1.0, 8 at 0.5–0.75, none
below 0.5. The eight at 0.5–0.75, by name and cause:

- **S16 t2, S19 t2, S35 t1, S38 t2, S50 t1, S55 t2 — 0.667 each.** The
  chant-straddle scenes: their planned sets include the "post it"
  fragment the plan assigns to the scene, but the take sings only its own
  phrase (assembly put "post it" in the previous take). Structural, not
  error — the takes sing exactly what the delivered master uses.
- **S46 t1 — 0.500 screened / 0.667 raw.** ASR "if you wanna help me"
  against planned "if you want to help me": the colloquial "wanna" is the
  homophone-class miss the override names. The take sits exactly ON the
  threshold — it passes, with no margin.
- **S49 t1 — 0.500 screened / 1.0 raw.** The take sings "clip it, post
  it"; the screen dropped "clip" (low word probability on that token)
  while "post" survived. The screen cost real resolution here.
- **S07 t1 — 0.833 screened / 1.0 raw** (just above the band): screen
  dropped the soft first word "built" (the project's own QC recorded it
  at p=0.413).

Read together: on sung material the screen is not needed (raw min 0.667)
and slightly costly at the floor (two takes land on exactly 0.5 because
of it). Its value is entirely on wordless takes (§5.2). The gate keeps
the screened value as primary because that is where false REJECTs would
do damage — but the floor margin on sung takes is thinner than the raw
numbers, and both are printed by the tool on every run.

**Wordless scenes (n=22), primary planned sets (all ∅):**
screened: 21 at 1.0, **1 at 0.0 (S14)**. Raw: 15 at 1.0, 7 at 0.0
(S01, S05, S14, S24, S33, S57, S63 — §5.2).

## 4. Cross-pairing (4,160 pairs)

Strata are classified on the two scenes' planned sets, priority order:
identical → near-identical (Jaccard ≥ 0.5) → subset (one strictly
contains the other) → discriminating. Pairs against wordless scenes
(planned ∅) are undefined and excluded (1,408).

| stratum | n | median | max | # ≥ 0.5 | reading |
|---|---|---|---|---|---|
| quarantine_identical | 72 | 1.0 | 1.0 | 72 | identical chorus lines — high by construction; the spec's quarantine |
| near_identical | 28 | 1.0 | 1.0 | 28 | sibling lines (Jaccard ≥ 0.5) — high by the song's design |
| subset | 960 | 0.0 | 1.0 | 1 | chant granularity; separates except 1 (below) |
| **discriminating** | **1,692** | **0.0** | 1.0 | **127** | the bar's real test: 92.5% score < 0.5 |

The 127 discriminating breaches decompose into three named classes —
there are no others:

1. **Two-word planned sets + the shared word "it" (108 pairs at exactly
   0.5; 114 of the 127 breaches are against 2-word sets).** The hook
   micro-slots {clip, it} and {it, post}: any take whose sung line
   contains "it" ("built it…", "put it up", "find… it") scores exactly
   0.5. With |P| = 2 the metric has one-step resolution; 0.5 is its
   smallest nonzero value. These are not wrong-segment confusions — no
   take's ASR resembles the hook line beyond the function word.
2. **Chant-phrase containment (17 pairs at 1.0).** Takes that sing the
   full chant phrase "clip it, post it" (S15, S18 t2, S34, S37, S49,
   S54) scored against the 2-word sub-slots {clip, it} / {it, post}
   (incl. S40, whose planned set is {it, post}), and S52's take — which
   sings the hook plus "help me stay online" — against every hook
   sub-slot and against S51's {clip, it, post}. The sub-slots are
   fragments of the very phrase these takes sing; no word-set metric
   can separate a phrase from its own fragments. Same family as the
   subset stratum's single breach (S22's take vs S40's {it, post}).
3. **Shared-vocabulary line families (13 pairs at 0.5–0.667, |P| ≥ 3).**
   Distinct lines that genuinely share ≥ half their word sets:
   "I don't need a parade/pitch" vs "I need somebody steady" ({i, need},
   0.5); S22's "don't overthink the cut" vs the "keep the work alive"
   scenes ({it, post, the}, 0.5); "just find the moment and put it up"
   vs "built it from the ground up" ({it, the, up}, 0.5); the bridge
   pair S44 ↔ S45 ("I'm tired of explaining it" / "tired of spelling it
   out" share {it, of, tired}, 0.6 both ways); S46 vs S52 ({help, me},
   0.5). This is the metric's honest resolution limit on a
   small-vocabulary chant track.

The near-identical stratum behaves as the spec anticipates — sibling
lines score high against each other (S10 ↔ S11 "parade/pitch" at 0.8:
the one differing word IS the separation, visible in the score but not
below threshold — G7 alone cannot catch a parade/pitch swap; S51's full
chant phrase {clip, it, post} draws 0.667–1.0 from every hook take).
The proposed rule (§7) therefore adds a distinctive-word rider for
sibling scenes instead of pretending the base metric covers them.

**Where the real separation sits.** For slots whose planned set has
≥ 3 words and does not belong to a shared-vocabulary family, separation
is effectively clean: discriminating median 0.0, and every breach ≥ 0.5
in the whole matrix belongs to one of the classes above. The 0.5
threshold is not the problem; vocabulary granularity is. The gate's
validated domain: wrong-SEGMENT takes (a different line) on slots with
≥ 3 planned words — which is exactly the failure it was built for
(MV-2 S04 t3 class). It is not validated — and should not be trusted —
as the sole check on 2-word hook slots or one-word-apart sibling lines;
those ride on the quarantine + rider + ear.

## 5. Failure cases by name

### 5.1 S14 t1 — the one false REJECT (wordless own-pair)

S14 is a wordless gap pocket: empty night desk, clip pulsing, no person
on screen (ledger-verified; the project's ASR heard "Let's go." at
avg_logprob −1.089 and adjudicated it a hallucination). The fresh
transcription in this run hears **"We'll be right back."** — a
*confident* hallucination: segment avg_logprob −0.959 (passes the −1.0
screen constant by 0.041), word probs be 0.757 / right 0.752 /
back 0.995; only "we'll" (0.114) is screened out, leaving
{back, be, right} ≠ ∅ → overlap 0.0 → REJECT on a take with no singer.

Two measurements make the mechanism plain. (a) The same audio produced
a *different* hallucination under the project's stored run — decoder
variance on musical audio is large; the phrase it invents is not stable.
(b) The invented phrase is the song's own phantom tag — the song grid
contains the same "We'll be right back" at 153.5s, which the MV-14 plan
flags as an unverified ASR blip, not a lyric. Whisper reaches for the
same phrase on MV-14's music wherever it has nothing to transcribe.
No round-constant screen on segment logprob/word prob separates this
from a real quiet line (real sung segments reach −0.69; S14 sits at
−0.959; anything between is a judgement call, and −0.9 would be tuning
to this fixture). The escape is the one the spec already designs: a
hand-check override, here on a wordless take verifiable by eye (no
singer in frame) and ear/RMS in seconds. §7's rule text extends the
override to this case explicitly, with the REJECT left standing in the
gate output and the override logged in the ledger.

### 5.2 The raw-set wordless failures (why the screen exists)

Without the screen, 7 of 22 wordless takes false-REJECT. The raw ASR
texts are a catalogue of whisper-on-music invention: S01 "so",
S05 "All right.", S24 "I'm sorry.", S33 "I'll see you next time.",
S57 "Music", S63 "Oh", S14 (§5.1). The screen (segment avg_logprob
≥ −1.0 AND word prob ≥ 0.5) cleans 6 of the 7; S33's five-word sign-off
phrase is the most fluent of them and still fails both constants.
Reported so the screen's contribution is measured, not assumed:
screened wordless failures 1/22 vs raw 7/22.

### 5.3 Planned-set construction failures (grid variant)

Under the grid construction of planned words, own-pairs fail 6 times
(vs 1 under plan-text): S21 (0.333 — grid garbles the slot to
"trip it posted" while the take sings "Clip it!"), S40 (0.333 — grid
"clip post you" for the "post it" slot), S17 (grid assigns chant-bleed
"trip" to a wordless vault shot), S33 and S63 (grid assigns boundary /
phantom-tag words to wordless scenes), S14 (§5.1 under both). Any
future project wiring G7 to grid-derived planned words instead of the
scene plan will manufacture false REJECTs. The rule text (§7) fixes
the plan as the text authority on this evidence.

### 5.4 The positives, verified as content (not noise)

- **MV-2 S04 t3**: overlap vs its own slot **0.125** → REJECT. Against
  the segment it actually sang (34.56–40.94s grid words) the same ASR
  scores **0.667** — ASR text: "The fast lanes, the rich ones fly on by
  / while the rest of us crawl watching money flash by." The gate fires
  because the take sings real words from the wrong place, and the
  control direction proves it reads content.
- **MV-2 S21 t1**: overlap **0.0** → REJECT. ASR: "Toll roads are done"
  (the chorus hook, "done" ≈ "dumb" mishear) over the verse slot
  ("the road gets meaner every single time…"). Loop 6 left this as
  "candidate pending verification" — it is a true positive.

## 6. What the gate does and does not catch (honest scope)

Catches, validated: wrong-segment takes (different lyric line than the
slot) — the MV-2 S04 t3 / S21 t1 failure class, and by the cross-pair
matrix any take whose sung line belongs to another scene with a
non-sibling planned set. Catches invented-word takes on sung slots
(the MV-3 S13/S39 failure that motivated the gate: invented words share
no vocabulary with the planned set — the same measurement, though no
MV-3 take was in this fixture). Does NOT catch, by construction:
one-word-apart sibling swaps (parade/pitch class — rider + ear),
2-word hook-slot assignments among chant takes (quarantine class),
timing/sync errors of any kind (other gates' job), or a take singing
the right words in the wrong *order* (set metric is order-blind —
the LCS/timing gates own order).

## 7. Proposed rule text

Full text in `PROPOSED_G7_RULE.md` (this directory), written for the
parent to apply to SKILL.md. It restates the loops' gate (metric,
threshold, homophone + near-identical-chorus overrides, identical-chorus
quarantine, standing cross-pair fixture, assembly boundary check) with
two loop-7 riders the evidence supports: the **distinctive-word rider**
for sibling scenes (Jaccard ≥ 0.5), and the **wordless-slot
hallucination override** (S14 precedent). It also fixes two operational
points the validation decided: planned words come from the scene plan,
not the grid (§5.3), and the ASR word set is the confidence-screened set
with the raw set always printed beside it (§5.2).

## 8. Reproduce

```
cd detection-research/g7_wrong_lyric
python3 build_fixture.py                 # rebuild fixture.json (md5-verified)
~/workspace/tools/lyrics-venv/bin/python transcribe_set.py   # checkpointed ASR
~/workspace/tools/lyrics-venv/bin/python score.py            # -> validation_results.json
~/workspace/tools/lyrics-venv/bin/python g7_check.py --audio <take.mp4> --planned "clip it post it"
```

Transcription wall time for the full fixture: ~30 min on the blade
(1.5 shared CPUs). Per-take gate checks after model load: ~15–40 s.
