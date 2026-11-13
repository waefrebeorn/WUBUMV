# Slopcannon performance-window lipsync (WuBu rebuild)

Source: user-supplied sauce (boneGPT posts + slop.cc Director's Wiki), audited
2026-11-01 against WuBu's tools and proven on MV-2's redo volley 1 (5 KEEP /
1 text-REJECT). The wiki pages confirm the core in softer form; the
non-negotiable framing and the SFX mechanism rest on bone's posts/direction
notes as supplied, not on wiki text. Read this before writing any SINGING
vehicle and before QC-ing any SINGING take.

## The window

A line's window runs from its first word to its last word. During the window
the singer must be on screen, facing camera (or 3/4), medium close-up or
closer, mouth fully visible and unobstructed. This pipeline's media tool
passes NO audio to the generator (text-to-video only), so framing IS the
sync: there is no audio-conditioned mouth to fall back on.

## Staging rules (hard gate for SINGING vehicles)

- The vehicle names its line. The singer is written as
  `THE VOICE (facing camera; static, medium close-up)` during the line.
- Order of events: choreography, gesture, reveal, pull-back, march, weave,
  and every other big action go BEFORE the first word or AFTER the last
  word, never stacked on the vocal. T2V models front-load the first action
  described, so the action-first sentence order is the mechanism, not a
  preference. MV-2 S18 proves the working order; S07 t1 proves the failure.
- Delivery wording (shared, verbatim where it repeats): the singer "sings
  the line clearly to camera with open, articulated mouth shapes, jaw
  relaxed on held notes, mouth returning to rest only after the last word."
  Never whisper, mumble, or deadpan closed mouth across a line.
- Restrained head movement and a steady camera during the vocal. Facing and
  motion go in parentheses after the name.
- One singer, one readable event per shot. Profile, hands, blur, and fast
  head turns hurt REVIEW: use them intentionally (a declared CUTAWAY beat),
  never by accident.
- Declare who visibly performs. Every prepro scene is tagged SINGING or
  CUTAWAY at plan time. A CUTAWAY scene carries no vocal burden and is never
  promised sync: mouth closed or turned away, face in profile or wide.
  Spend face time on chorus hooks, held notes, and emotional close-ups;
  cut away on fast runs, dense choruses, and hard lyrics (coverage budget).

## Judging a take (majority of samples, 2s/5s/8s)

- KEEP if at least 2 of 3 samples show face-to-camera with the mouth visible
  AND at least 1 sample shows an open-mouth vocal passage. Widen the sample
  when reads disagree instead of picking one read.
- A still of a face with an open mouth is checked against its speaking beat
  before being called a break. Frames alone cannot tell "between lines"
  from "not performing": judge closed-mouth passages against the final
  true windows in LYRIC_TIMELINE.md.
- Diagnose before rerolling, one named axis: FACING (never faces camera),
  DELIVERY (faces camera, mouth never opens), or STAGING (action stacked on
  the vocal). Never reroll a facing failure with a delivery fix.
- Phonemes are not visemes: judge held vowels and line-start/end closures,
  never letter-by-letter mouth shapes. Flat-cartoon mouths need FEWER
  visemes, not more: broad, clean shapes pass; a blurry or over-detailed
  mouth fails. Judge shape clarity, not realism.

## Killed or downgraded on transfer (do not write these into vehicles)

- KILLED: "model lip-syncs to the supplied audio chunk" (no audio input
  exists here); "correct auto lyrics / lipSyncMode: required" (no such
  parameter; the transferable remainder is that the lyric timeline itself
  must be true); "loud SFX steals mouth sync" as a generation claim
  (generated audio is dropped in assembly; kept only as an edit note).
- DOWNGRADED: "entire window, non-negotiable" to a sustained passage by
  majority (the model does not hold framing 10 s); "1-2 singers max" to
  readability; "check a clear consonant" to mouth-open + facing.
- DEAD, do not reuse: the cheap peak-tween assembly stage (ordinal RMS
  peak pairing + clamp/rescale). It produced fake alignment on MV-2 v1 and
  was rejected by the user. Assembly is window-first section-timing only
  (see references/assemble.md).

## Honest limit (state it at delivery, never soften it)

This maximizes the PLAUSIBILITY of mouth motion against the Suno master.
It does not produce phoneme-accurate lipsync: this pipeline has no
audio-conditioned generation. Real sync would need audio-driven generation
(if the media tool ever accepts audio input) or a mouth-repaint pass
(MuseTalk/LatentSync test on one flat-cartoon take — needs user approval
for GPU/cloud spend, not built).
