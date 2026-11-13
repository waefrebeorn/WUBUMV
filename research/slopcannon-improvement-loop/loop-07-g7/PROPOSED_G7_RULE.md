# PROPOSED — G7 wrong-lyric gate rule (loop 7, for parent to apply to SKILL.md)

Drafted from loop 3 §2 #5 / loop 4 §2 #4 / loop 5 §3 #3 / loop 6 §3 #2 and the
loop-7 validation (see report.md in this directory). Do not apply verbatim
without the parent's read — the two riders marked (loop-7) are new wording
the validation evidence supports; everything else restates the loops' text.

---

**G7 — WRONG-LYRIC GATE (QC, per take, before KEEP).** A take is gated on
*what it sings*, not only how it looks or moves. Run take ASR (house lyrics
pipeline config: faster-whisper large-v3-turbo int8, cpu_threads=2, NO VAD,
beam 1, condition_on_previous_text=False, repetition_penalty 1.1,
no_repeat_ngram_size 3) and compute the **word-set overlap**
|A ∩ P| / |P| between the take's ASR words A and the scene's planned words P.

- **Planned words P** = the scene plan's lyric fragment for the slot
  (the sheet line the vehicle asked the take to sing). The song word grid
  is the *timing* authority, NOT the text authority — grid ASR garbles
  chant (loop-7 evidence: MV-14 grid reads S21's slot as "trip it posted"
  and S40's as "clip post you"; both would false-REJECT clean KEEP takes).
- **ASR words A ("sung words")** = words with word-probability ≥ 0.5 in
  segments with avg_logprob ≥ −1.0. Whisper hallucinates phrases on
  musical audio; the raw word set is reported alongside, never hidden.
- **overlap < 0.5 → REJECT.** A wordless slot (P empty) passes iff A is
  also empty; singing words into a wordless slot is the same failure.
- **Tool:** `detection-research/g7_wrong_lyric/g7_check.py`
  (`--audio take.mp4 --planned "…"`, or `--planned-file` / `--grid --window`).
  It prints both screened and raw overlaps; the screened overlap is the
  gate value.

**Hand-check overrides (log the override + reason in the take ledger):**
- *Homophones / ASR mishears* — "told" for "toll", "wanna" for "want to",
  "done" for "dumb": if the ear confirms the take sings the planned line,
  override. (Loop-7: MV-14 S46 sits exactly at 0.5 on "wanna" alone.)
- *Near-identical choruses* — when another scene's planned set has
  Jaccard ≥ 0.5 with this scene's, a cross-match against that scene is
  expected and is NOT evidence against the take (provenance quarantine
  for identical chorus lines: the same line sung in C1 and C2 must not
  false-REJECT). (loop-7) *Distinctive-word rider:* for such sibling
  scenes, the take must contain at least one word of its own scene's
  set difference (e.g. "parade" vs "pitch") when that difference is
  non-empty — G7 alone cannot catch a swap between one-word-apart lines.
- (loop-7) *Wordless-slot hallucination* — a REJECT on a wordless slot
  may be overridden when the take is verified wordless by eye/RMS (no
  singer on screen, near-silent audio): whisper invents confident
  phrases on music (MV-14 S14 precedent: "We'll be right back." at
  avg_logprob −0.959 on an empty-desk shot). The override is logged;
  the REJECT stands in the gate output.

**Standing fixture.** Every volley's takes are cross-paired against the
project's other scenes' planned words at QC time (harness pattern:
`build_fixture.py` + `score.py` beside the gate script). A take whose
overlap vs a *different* scene's planned words exceeds its overlap vs
its own scene's is flagged WRONG-SEGMENT for hand-check even if both
scores pass 0.5. Assembly boundary check (carried from loop 3,
unvalidated in loop 7): re-check the last 0.5 s + first 0.5 s across
each cut against the neighbouring slots' words.
