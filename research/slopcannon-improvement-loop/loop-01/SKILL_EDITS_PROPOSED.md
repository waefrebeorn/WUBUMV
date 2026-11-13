# Slopcannon SKILL.md — proposed edits, Loop 01 (2026-11-11)

DRAFTS ONLY — not applied. The parent verifies and applies. Each edit quotes the current SKILL.md text it replaces (verified by reading `~/workspace/custom-skills/slopcannon/SKILL.md` 2026-11-11 ~23:50 EST) and gives the replacement. Evidence + validation for each: `report.md` §4.

## §1 — Intake: forced-align the known lyric sheet (fixes P1a + P2)

**Current text** (WORD-SYNC, MEASURE BOTH SIDES):

> - MEASURE BOTH SIDES: the song's word times come from LYRIC_TIMELINE.md /
> SONG_WORDS.json (measured, never the sheet where performance differs).
> Each take's sung word times come from transcribing the take's own
> generated audio with word timestamps.

**Replace with:**

> - MEASURE BOTH SIDES: the song's word times come from LYRIC_TIMELINE.md /
> SONG_WORDS.json (measured, never the sheet where performance differs).
> They are produced by FORCED ALIGNMENT of the KNOWN lyric sheet against
> the Demucs vocal stem — never by trusting a transcriber's interpolated
> word times (Whisper's own word times run ~150 ms early and drift by
> hundreds of ms; forced alignment places boundaries at ~20 ms — Chu et
> al. 2026; Carpio 2026: "far more accurate than transcribing, because
> nothing has to be guessed"). Blade path: whisper.cpp experimental word
> timing (`-ml 1`) or Parakeet TDT as the transcriber, plus the C11
> snapper (`snap` mode) as the alignment refiner, with the stay-rule
> patch (a word with no in-span strong peak stays where the aligner
> put it — never snaps onto the previous word or a drum hit). Each
> SONG_WORDS.json entry carries `confidence` and an `unsung` flag: a
> word the aligner cannot place in the vocal stem is UNSUNG — it gets
> no lipsync scene (cover/text treatment instead), never a scene built
> on a hallucinated time. Repeated lyrics are aligned with a MONOTONIC
> FORWARD walk — each occurrence aligns after the previous one, never
> glued to the first occurrence. Each take's sung word times come from
> transcribing the take's own generated audio with word timestamps,
> snapped the same way.

## §2 — Anticipatory visual anchors (fixes P1b)

**Current text** (V4 CORRECTION):

> Anchors are VISIBLE MOUTH EVENTS in the take, not the take's audio
> words: audio-word warping preserves the mouth lag (~0.5–1s inside
> some takes) that the mouth-lag caution below warns about.

**Replace with:**

> Anchors are VISIBLE MOUTH EVENTS in the take, not the take's audio
> words. A visible mouth gesture LEADS its acoustic word by ~0.10–
> 0.15 s (anticipatory coarticulation: the viseme is seen before the
> phone is heard — Bregler & Konig: visual leads acoustic by ~120 ms
> on average; Terry et al.; Lulaci et al. 2024: lip-rounding cues
> usable from 15 ms into the onset). So the visual anchor for a word
> sits ~0.12 s BEFORE its forced-aligned acoustic onset — word-class
> dependent (plosive-initial words lead more: the closure is silent;
> vowel-initial words lead less). A take whose mouth opens exactly at
> the acoustic onset reads as LATE, not on. Audio-word warping that
> ignores the lead preserves a systematic ~0.12 s error on every word.

**Current text** (SWING KEYFRAMES, caution):

> Caution (earned 2026-11-02): take audio words are HINTS — they can
> lead the visible mouth by up to ~1s inside a take; if the master
> gate shows a consistent mouth lag for a scene, shift that scene's
> keyframes by the measured mouth offset.

**Replace with:**

> Caution (earned 2026-11-02, refined 2026-11-11): take audio words are
> HINTS — they can lead the visible mouth by up to ~1s inside a take.
> That lag has two parts: (a) the systematic viseme lead (~0.12 s,
> §2 above — apply it at anchor time, always); (b) the residual
> per-take mouth offset, measured from the take's own mouth-state reads
> (MAR curve vs forced-aligned onsets). If the master gate shows a
> consistent residual mouth lag for a scene, shift that scene's
> keyframes by the measured residual offset. Never use the old ~1 s
> blanket as a tolerance — it is ~4–8× looser than perception and
> symmetric where perception is asymmetric (see §3).

## §3 — Asymmetric sync tolerance + mouth-open-vs-quiet gate (fixes P3)

**Current text** (stage 5 QC, gate definitions):

> Read references/qc.md. Every take is scored against named gates
> (G1 character consistency, G2 zero unwanted on-screen text, G3 no
> licensed material, G4 performance-window for SINGING scenes, G5
> audio-sync placement, G6 banger check on the plan) with pass/flag/fail
> per scene and confidence tags.

**Append to the G5 definition (new paragraph after the gate list):**

> G5 ASYMMETRIC TOLERANCE (2026-11-11, loop 1): sync tolerance is
> asymmetric — audio LEADING the picture is detected at ~+45 ms,
> audio LAGGING at ~−125 ms (ITU-R BT.1359); the McGurk window runs
> 30 ms audio lead to 170 ms audio lag, weakening at 60 ms lead /
> 240 ms lag. The master gate's mouth-state read at line/hook onsets
> is judged on that window: a mouth opening up to ~0.12 s AFTER the
> word onset is inside tolerance; a mouth opening 0.05 s BEFORE the
> word onset is already a fail. Generated mouths get LESS tolerance
> than real ones (Shahin et al. 2017: tolerance grows with the
> spectrotemporal fidelity of the mouth) — never looser.
> G5b MOUTH-OPEN-VS-QUIET (2026-11-11, loop 1): for every singing
> take, compute the mouth-open fraction during song-silent spans
> (MAR curve × vocal RMS envelope over the take's own ASR word gaps).
> A mouth open during quiet is a number, not an eye-read (Carpio
> 2026: "the jaw was open during 35% of the quiet moments" → a
> fixable sentence). Flag for eye review above the threshold calibrated
> on the project's KEEP takes (same method as the M6 calibration:
> threshold from the KEEP distribution, never a guess). If the gate
> does not separate rejected from accepted masters on the calibration
> pair (MV-8 v2 vs v3), it stays an eye-review flag, never a gate.

**Current text** (V4 CORRECTION, master gate):

> The master gate READS MOUTH STATE at every line onset AND every
> hook onset (open / transitional-open / closed, at onset and +0.15s);
> any hook onset closed is a GATE FAIL.

**Replace the parenthetical with:**

> The master gate READS MOUTH STATE at every line onset AND every
> hook onset (open / transitional-open / closed, at onset −0.12s,
> onset, and +0.15s — the −0.12s read catches the anticipatory
> viseme; a mouth that is still closed at onset −0.12s but open at
> onset is on time, not late); any hook onset closed at onset +0.15s
> is a GATE FAIL. The onset read is judged on the asymmetric window
> in G5 above.

## §4 — Piecewise beat grid (fixes P4)

**Current text** (SWING KEYFRAMES):

> Compare against the
> BEAT MIX: measure the song's beat grid (tempo, beat times,
> downbeats) and use it as the hint layer — montage cuts land ON
> beats, return cuts land ON word onsets, accents land on stressed
> words.

**Replace with:**

> Compare against the
> BEAT MIX: measure the song's beat grid (tempo, beat times,
> downbeats) and use it as the hint layer — montage cuts land ON
> beats, return cuts land ON word onsets, accents land on stressed
> words. The grid is PIECEWISE, not global: `beat_grid.json` records
> per-section phase + swing + a departure list (where the song leaves
> the grid). A single global phase is the loose part — the C11 DP
> tracker and librosa agree with each other (median 0.035 s) far
> better than either agrees with a rigid global grid, and tempo
> autocorrelation is a plateau, not a peak (sprint 3, MV-14). The
> swing-keyframe hint layer reads the section's phase.

## §5 — Kinetic type: measure, don't estimate (fixes P5)

**Add to the kinetic-type rules (stage 6 assembly / kinetic layer — insert after the caption/kinetic paragraph):**

> KINETIC WIDTH IS MEASURED, NEVER ESTIMATED (2026-11-11, loop 1):
> kinetic line widths come from real glyph advances (fontTools), never
> from a `char_w` estimate — the estimate under-reads real widths by
> 6–15% and overflowed the frame on MV-13 v1 (L04, L46). The per-line
> fs-scaling cap (1100 px) stays as belt-and-braces. A rebuilt kinetic
> layer asserts 0 overflow on the burned frames at full-res read
> before delivery.
