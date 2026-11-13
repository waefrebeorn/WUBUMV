# Slopcannon QC — scored gates, triage, no silent passes

Stage 5 of Engine v2. QC is a separate pass with named gates, not
adjectives in a prompt. A failed gate is a reroll reason or a plan
rewrite, never a note. Every take gets a QC row before it can enter
the cut; no master assembles with a failed gate open.

## The gates

- G1 Character consistency: same character across first/mid/last
  appearance (face, hair, outfit, prop). Drift = fail. Compare stills,
  never memory: a take is not consistent because the last take was.
- G2 Zero unwanted on-screen text: any legible letter, number, word,
  glyph, or sign text in generated footage = fail, including a single
  glyph and including text on a structure the vehicle told to be
  blank. Blank panels are text-clean; lettered panels are not, even
  partial ("TOL" counts). Captions live only in the post layer, never
  in generated frames.
- G3 No licensed material: no licensed characters, plots, dialogue,
  logos, or real-person likeness for commercial use; no unconfirmed
  reference. Hard fail: block assembly until replaced or disclosed.
- G4 Performance-window (SINGING scenes only, see
  references/performance-window.md): frames at 2s/5s/8s; KEEP only if
  at least 2 of 3 samples show face-to-camera with the mouth visible
  AND at least 1 shows an open-mouth vocal passage. Diagnose before
  rerolling: FACING (never faces camera), DELIVERY (faces camera,
  mouth never opens), STAGING (action stacked on the vocal). Text and
  facing are separate gates: a take can pass one and fail the other.
- G5 Audio-sync placement: the take's trim points equal its true
  lyric window; cuts land on line/section boundaries; no drift
  checked only at the start — verify full-length alignment on the
  assembled master.
- G6 Banger check (on the plan, before assembly): hook in the first
  3 s, motif present at least 3 times, last chorus is the visual
  peak, no scene repeats the previous scene's shot type without a
  reason. A video passing G1–G5 but failing G6 goes back to PLAN,
  not to reroll lottery.

## Method rules

- Sample at 2s/5s/8s per take. When two reads disagree, widen the
  sample (1s/3s/4s/6s or 1 fps) instead of picking one read.
- A still of a face with an open mouth is checked against its
  speaking beat before being called a break. A closed-mouth passage
  is judged against the final true windows, not against a uniform
  grid: "between lines" and "not performing" look identical in one
  frame.
- Small objects are tested by thresholding the pixel difference and
  clustering the hits, never by averaging a whole region.
- A take that contains a sustained to-camera vocal passage followed
  by its designed post-line beat (turn, tear, place, step-back) passes
  G4 even if the beat occupies the back half of the take: judge the
  order (vocal first, beat after), not the beat's clock position.
- Nits are disclosed, never hidden and never promoted to fails:
  pocket-square hue variance, added accessories (tie, chain, bow
  tie), blank panels where the vehicle asked for none, handheld mic
  vs stand, framing widening after the vocal. A nit class that
  repeats across takes is logged once and referenced, not re-litigated.

## Triage (review fatigue is a failure mode)

- Score every take, then surface only the worst scenes + first,
  chorus, and last scenes for human-facing review. The rest
  auto-advance with their best take, logged.
- One review pass per volley, not per clip. A full song is 12–20
  scenes; reviewing every take of every volley is how standards
  collapse into approvals.

## Confidence tags on the QC report itself

- [confirmed]: measured (timing, md5, ffprobe, legible-text present/absent on sampled frames).
- [inferred]: model-judged (identity similarity, lip-sync plausibility, mouth-open reading).
- [assumed]: user claim (rights, lyric correctness where no alignment exists). A scene with only [assumed] on a rights or sync item cannot be marked ready.
