# lyrics — hybrid lyric extraction + kinetic rebuild pipeline

The pipeline that re-extracted lyrics + per-word times from the audio
itself for MV-2/3/4/5/6 (Nov 2026), after the user's verdict that the
delivered captions were wrong. **The audio decides, never the old lyric
sheet.**

## The tested hybrid (standing method)

1. **Backbone:** faster-whisper `large-v3-turbo`, int8, cpu_threads=2,
   pinned `"en"`, `condition_on_previous_text=False`, beam 1,
   repetition_penalty 1.1, **no VAD** (speech VAD is fatal on chant
   singing — it deletes sung phrases as silence).
2. **Dense spans:** separated vocals (MDX stem via wubuwizard/c11_sep)
   only where the mix loops or the backbone garbles.
3. **Text authority:** the Suno lyric video (MV-3 finding: the turbo
   backbone alone is unusable on chant tracks — `no_repeat_ngram_size=3`
   suppresses real repeats, 535w vs 729w base).
4. **Time authority:** base-model anchors + turbo where base garbles;
   stem-envelope silence exposes base hallucinations.

## Findings that change the defaults

- `no_repeat_ngram=3` COLLAPSES legitimate hook repeats — use `0` for
  stem/mantra slices (MV-3) and on pop hooks too (MV-5: P1 454w, whole
  hook lines deleted). Suppression OFF hallucinates echo-loops on
  repetitive tails — P1's silence is more credible than P2's
  continuation on tails.
- **Stem onsets run 0.3–1.1 s EARLIER than mix passes** on lead-under-hook
  lines (MV-5: 24 corrections) — the lead enters under the hook's tail.
- P1 word-END times inherit segment ends (cap line ends at last word
  start + 0.5 s); P1 first-word times after a gap can be ~1 s early.
- `{\r}` in a karaoke highlight resets `\fs` to the style default —
  reset ONLY the colour. Measure bold widths with PIL, never
  `len*fs*0.52` (under-measures bold ~10%). Gate frame selection =
  `ceil(t×24)`, not round.

## Files

- `scripts/` — the MV-2 canonical script set (transcribe backbone +
  stems, grid build, .ass build, diff, gates) plus MV-5's
  `stem_envelope.py` / `transcribe_stem.py` (the stem-onset method).
  These are per-project adaptations — paths at the top of each script
  point at the project they were written for; adapt before reuse.
- `notes/` — `LYRICS_REDO_NOTES_MV-*.md` (the full redo records,
  incl. every wrong-word diff) + the extraction research notes.
- `lyrics-extraction-report.md` — the original CPU extraction survey.

## Environment

faster-whisper 1.2.1, `av==18.1.0` pinned (av decode must slice
resampled frames to `o.samples` and use
`av.audio.resampler.AudioResampler`, not `stream.resampler`).
Whisper hallucinates on near-silent audio — never caption a span the
stem envelope says is silent.
