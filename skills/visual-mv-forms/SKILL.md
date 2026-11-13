# Visual MV Forms — music videos are not just singing

Built 2026-11-06 from the user's order (~03:29 EST): *"music videos
are not just singing, they can be visuals and words flying on screen
next to the generated stuff and graphics — this is the way."*

This skill is the decision layer for every MV slot that is NOT a
mouth-sung take. Full detail lives in
`~/workspace/wubutv-network/musicvideo/visual-forms/VISUAL_FORMS_TAXONOMY.md`
(29 KB, per-form specs) and `KINETIC_TYPE_PLAYBOOK.md` — this file
condenses them to decision grade and points back. Governing rules for
sync, QC, and delivery remain the Slopcannon skill's
(`~/workspace/custom-skills/slopcannon/SKILL.md`); where anything here
seems to conflict with Slopcannon, Slopcannon governs.

## When to use

- Planning any MV section that is structural (pace floor hit),
  rap/bridge-fast (~1 s/line), instrumental, a hook/chant/mantra, a
  list/count lyric, a duet hand-off, or coverage over KEEP footage
  whose singer is wrong or off-camera.
- Choosing the sanctioned coverage for a slot instead of forcing
  another generation pull (Slopcannon structural-slot rule: once
  structural, the slot leaves the generation queue and gets an
  assembly treatment — this skill IS the treatment menu).
- Designing the type / graphics / accent layers of any MV, including
  over singing sections (Family A4 / Move 3 HIGHLIGHT is the default
  lyrical type treatment).

## Governing rules (inherited from Slopcannon — non-negotiable)

1. **Song is tempo gospel.** `track.mp3` untouched is the sole master
   audio and sole timing authority. Every cut, word, flash, and
   graphic lands on a measured song time — word onsets from
   `SONG_WORDS.json` / `LYRIC_TIMELINE.md`, beats from the measured
   beat grid. Nothing syncs to a take's generated audio.
2. **Text is an assembly layer, never generated.** Generated clips
   carry zero text/logos (Slopcannon gate G2). All words, titles,
   HUD, and graphics are placed in post (ASS / PNG overlays / code
   render). A form needing text inside the generated picture is
   disqualified; restage it so the text lives in post.
3. **One 16:9 master.** 1280×720 (or 1920×1080 plate), 24 fps. No
   9:16, no chat copy.
4. **Per-word warping does NOT apply to visual forms.** That law
   governs singing takes (with swing keyframes and bad-word montage
   cuts — Slopcannon WORD-SYNC). Visual forms are the sanctioned
   coverage where singing is impossible. A visual-form slot gets a QC
   row flagged **"not a mouth-sung slot"**, caption/graphic timing
   sourced from song times.
5. **Motion while words play.** No frozen frame during sung words —
   the graphic layer must itself move (drift/pulse counts only if
   pixels actually change) while words are sounding.
6. **Frame-audit loop.** Extract frames at word/beat onsets from the
   *rendered master*, verify, fix, re-render. QC on the master
   itself, never on the plan alone.
7. **Bad-word rule bridge:** when a singing take messes up a word,
   Slopcannon orders a fast cut to montage for exactly that span and
   back at the next good word. The montage material for those cuts
   comes from this skill's families (C1 first, then F/E plates).

## Stack architecture (organizing principle)

From the @Mnilax stack pattern (see MONDO_INDEX source notes): **one
dedicated tool per layer beats one monolithic generator.** The
generator is ONE layer (performance/world footage) — not the pipeline.
Type, graphics, effects, audio-reactive picture, assembly, and
optimization each get their own tool, with the song grid as the shared
contract. When a layer feels weak, fix that layer's tool — never just
write a bigger prompt to the generator.

## The 3-layer composition model

Every visual-form section is built and audited as three layers
(GRAPHICS_OVERLAY_NOTES.md):

1. **Picture layer** — generated takes (placed/warped per Slopcannon
   for singing; form footage for visual slots), or plates/stills.
2. **Type layer** — kinetic type from `tools/kinetic_ass.py`, one .ass
   per section, preset chosen per section energy (below).
3. **Graphic accent layer** — palette bar today; extends to shapes,
   counters, HUD ticks (ASS `\p1` drawing), particle bursts, and
   code-rendered scenes composited between layers 1 and 2.

Assembly order: place picture → generate type .ass from
SONG_WORDS.json with the section's preset map → burn → onset-frame
audit → fix → re-render → gate the master as usual.

## The 9 families (decision-grade)

Difficulty: 1 = scriptable today · 2 = half-day reusable build ·
3 = new tooling/craft per use. Full specs: taxonomy file.

- **A — Kinetic typography (words AS the picture).** A1 full-screen
  lyric type over a plate · A2 word-fly beside footage (onset = the
  move's *landing*; start 150–300 ms early) · A3 moving typographic
  poster (intros, titles, hook branding) · A4 karaoke-highlight
  promoted to design (full line stays; only the highlight moves).
  Producer: post ASS via `kinetic_ass.py`. Difficulty 1–2.
- **B — Audio-reactive visualizers.** B1 waveform/spectrum/frequency
  bars rendered by ffmpeg (`showwaves`/`showspectrum`/`showfreqs`/
  `showcqt`) from `track.mp3` itself — sync is intrinsic. B2
  beat-reactive graphic accents keyed to a *measured* beat map
  (accent peak ON the beat frame). Difficulty 1–2. (Compression note:
  `showwaves mode=cline` runs ≈6.6 Mbps at 720p — prefer `mode=line`,
  thin strips, or CRF 28; see H/optimization.)
- **C — Montage & collage.** C1 beat-matched montage (proven: MV-5 v3
  bridge — cuts on the beat/word frame, 1–2 f early is the pro feel;
  exact frame counts `round(span*24)`) · C2 collage/mixed-media
  composite (forgives style drift a clean cut exposes) · C3
  split-screen & PiP (solves duet hand-offs the generator can't do
  mid-clip; panel emphasis swaps on the singer-change frame).
  Difficulty 1–3.
- **D — Graphic systems.** D1 shapes/diagrams that *act* (a counter
  hits 7 ON the word "seven", never after) · D2 HUD/UI overlays in
  post (viewfinder, ON AIR, name straps, the `~ WuBu ~` bug is this
  family). Producer: ASS `\p1` + type, PNG overlays. Difficulty 1–2.
- **E — Stills in motion.** E1 stop-motion/paper-cutout (stepped
  8–12 fps judder built in POST — never ask the video model for
  stop-motion, it will smooth it; steps quantize to the beat grid) ·
  E2 abstract/loopable plates (the bed under A/B/D) · E3 animated
  cover/poster plate (first frame rhymes with last — banger test).
  Difficulty 1–3.
- **F — Performance without singing.** F1 dance/movement (the move's
  *hit* lands on the beat) · F2 environment journey (camera through
  worlds; chain clips in post, transitions on section boundaries) ·
  F3 object/product hero shots (motif object performs; its action
  completes ON the word that names it). Producer: the generator,
  staged for energy not lip-sync. Difficulty 1–2. Image-input note:
  for how a supplied still actually behaves in OUR generator
  (conditioner, not literal frame 0), the video-api-mastery skill
  governs — external platforms' first/last-frame pinning is
  documented there as NOT verified on WuBu's tool.
- **G — CODE-RENDERED GRAPHICS ★ (deterministic, frame-exact).**
  G1 code-rendered motion scenes (a render function of time,
  `renderAt(t)`: cards, posters, HUD worlds, diagram/count scenes) ·
  G2 code kinetic type (GSAP-class springs/overshoot/stagger ASS
  cannot express) · G3 code 3D accents (the same motif object every
  return — a model file doesn't drift). Beat-locking is arithmetic,
  not luck; a fix is a code edit + re-render. Weakness is the mirror
  of the generator's: it renders design, not life. The banger MV
  mixes both. **PROOF GATE (binding): no plan may promise a Family G
  scene until its renderer has passed a 10-second proof render on
  this VM, frame-audited; until then plan an ASS/PNG fallback
  (Families A/D) that ships if the proof fails.** Feasibility as
  checked 2026-11-06: ffmpeg 8.1.2 ✅, `kinetic_ass.py` + proof ✅,
  faster-whisper ✅ in-house, Node v24 present ✅ (plausible, not
  installed); **Blender 4.5.15 LTS MEASURED 2026-11-06** (installed
  `~/workspace/tools/blender/`): Cycles CPU PROVEN (palette still
  21.3 s @640×360/16spp; 24f keyframed anim ~23.5 s/frame → 1.000 s
  mp4) — short 3D accents, turntables and storyboard stills are
  viable, 720p ≈ 1–2 min/frame so no long 3D sequences; EEVEE
  BLOCKED (no libEGL on this VM); Grease Pencil API present but GP
  rendering unverified (same GL abort). Full record:
  `visual-forms/BLENDER_FEASIBILITY.md`. Remotion / HyperFrames /
  GSAP / Three.js / ComfyUI ⚠️ UNVERIFIED on this VM.
  Difficulty 3 today.
- **H — Effects, procedural & background layers** (plugs, not
  standalone forms). H1 dedicated particle-effects layer (burst apex
  ON the beat; never prompt "add sparkles" into footage) · H2
  procedural texture/noise backgrounds (palette-exact, identical
  across sections — ffmpeg sources available today) · H3 purposeful
  background crowd motion (crowd state changes on beats) · H4
  **optimization as a named final step** — CRF/preset per content
  type, size sanity, md5 + ffprobe of the delivered file; happens
  AFTER the gate passes, and any re-encode that changes frame count
  or duration voids the gate. Difficulty 1–3.
- **I — Countdown / listicle.** A simple steady base carried by a
  graphics layer: persistent overlay character/bug + progress counter
  ("4/10") + consistent per-item framing. The counter increments ON
  the word/beat naming the next item, never between items. Native
  fit for list-shaped WuBu lore (THE COUNT, the roster, the channel
  grid). Difficulty 1 (ASS/PNG) – 3 (code cards).

**Two form-adjacent additions (2026-11-13, taste research)** — not
new families; seam devices that sharpen the families above:
- **THE POSE-CUT** (nu_vogue_art — pose-as-cut). At each 10 s
  boundary the subject strikes a new held editorial pose while the
  world changes around the pose; the cut hides in the pose change,
  and continuity is carried by the body, not the set. Pairs with
  F (performance) and C (montage); the pose is written into the
  vehicle as a silhouette sentence (see the Slopcannon LOOK BLOCK).
- **LIGHT-SHIFT SECTION CHANGE** (SoundBoost). One set held across
  sections; the section change is carried by light and colour, not
  location — e.g. 42 scenes in ONE house, blue present / golden
  memory. The plan's section colour map names the shift per section
  (verse cool, chorus warm, bridge colour-shift); pairs with any
  family where a set change would spend budget the light can carry.

## Slot → form decision table

| Slot situation | First choice | Fallback |
|---|---|---|
| Line too fast to generate sung (pace floor) | A1/A4 type over E2 plate, or C1 montage | A2 over F1 |
| Rap/bridge alternation ~1 s/line | C1 montage (proven MV-5 v3) | A4 over C1 |
| Instrumental / intro / outro | B1 visualizer, F2 journey, E3 cover plate | D2 HUD frame |
| Hook = chant / mantra / counted list | A1 SLAM type, D1 counter, F3 hero object | G1 code scene |
| Chorus escalation | F1 dance + B2 beat accents | C1 montage, wider |
| Verse listing places/things | F2 journey + A2 word-fly | C2 collage |
| Duet hand-off | C3 split-screen | C1 alternating montage |
| Lore/system lyric (count, roster, viewer) | D1/D2 graphics + type | G1/G3 code render |
| List / countdown lyric or segment | I1 countdown (counter + overlay) | D1 + A1 |
| Chorus punctuation / magic / celebration | H1 particle layer over F1/C1 | B2 beat accents |
| Plate under type, style must not drift | H2 procedural background | E2 generated plate |
| Lived-in world behind hero shot | H3 crowd layer | F2 journey plate |
| Whole track, no cast | F2 + A1/A2 (journey + type) | B1 full visualizer cut |
| Hero type moment (title, peak chorus) | G2 code type (if proof gate passed) | A1 ASS SLAM/CASCADE |

## The 5 kinetic house moves (numbers, not adjectives)

Implemented in `visual-forms/tools/kinetic_ass.py` (stdlib python3;
input = SONG_WORDS.json-shaped words + preset → .ass for ffmpeg burn).
**Stagger is never a constant — it is the song's word-onset grid.**
ASS has two time units: karaoke tags = centiseconds, animation tags =
milliseconds — mixing them runs animation 10× off. Burn ASS in, never
soft-mux (platforms strip styling). Palette: BONE #F4EEDC primary ·
CADMIUM #FFC61E active · INK #141414 outline · accents cycle
CADMIUM→VERMILION #E23A1B→COBALT #1B3FD1→FOREST #1E4D33 (max 2
primaries + bone + ink per frame). Font: one display family, bold
(proof: Noto Sans Bold 54 pt at 720p, INK outline 4).

1. **SLAM** (hook hits, downbeats): word alone, centered lower-third;
   scale 300%→100% over **150 ms (≈3.6 f)** — alpha punch 0–60 ms,
   settle 60–150 ms; out-fade 90 ms. Starts AT the onset (the arrival
   IS the hit); holds to next onset. ≤1 full SLAM per line.
2. **CASCADE** (fast/rap passages): line builds word by word; each
   word `\move`s **420 px** into its slot from alternating L/R over
   **200 ms (≈4.8 f)**, 60 ms fade head, starting AT its onset; words
   hold cumulatively to line end.
3. **HIGHLIGHT** (lyrical default; the only legal form at very fast
   word rates): full line dim (~60% alpha BONE) for its whole span
   (end clamped to the *next* line's onset); active word pops CADMIUM
   at **112%→100% over 90 ms (≈2.2 f)**, starting 2 frames before its
   onset. (Playbook Move 3 spec; the tool's docstring reads 118% —
   the frame-audited playbook number governs.)
4. **STACK** (lists, building lines): one word per row, scale
   **40%→100% + fade over 130 ms (≈3.1 f)** from onset; row pitch
   **67.5 px** (1.25 × 54 pt); final word CADMIUM, the rest BONE.
5. **ACCENT BAR + beat punctuation**: `\p1` bar **7 px** tall, width =
   line width (min 120 px), slides in **260 px over 220 ms (≈5.3 f)**
   from the line's first onset; colour cycles per line. Extensions in
   the same grammar: beat flash ≤15% alpha for exactly 2 frames
   (never >3 flashes/sec), wipe landing on the section downbeat,
   counter tick exactly ON the naming word. Gotcha: never put
   `\pos(0,0)` on a `\p1` event that also has `\move` — they fight
   and the bar renders at frame top (audit fix #1).

**Honest motion ceiling:** libass `\t` is a power curve, not a spring
— no true overshoot/elastic physics in ASS. SLAM's settle is a
two-segment fake of a back-out. For real springs, escalate to Family
G2 code render (proof gate applies); in ASS specs, write the intent
("spring, damping 12") so the code port is mechanical.

**Proof on disk:** `visual-forms/proof/kinetic_proof_16x9.mp4`
(10.0 s, 1280×720, 24 fps, md5 `570e4ffdca5077c31feb546483326eed`) —
all presets frame-audited at word onsets over real MV-5 footage; the
audit caught and fixed two real bugs (bar at frame top; HIGHLIGHT
line-bleed/slot drift). Details: `GRAPHICS_OVERLAY_NOTES.md`.

## QC for visual-form slots (every slot, no exceptions)
- QC row exists, flagged "not a mouth-sung slot" where no mouth is
  claimed.
- Word/beat placement measured on the master: onset frames show the
  word/graphic landed (not off by >2 frames).
- Motion check: no frozen run ≥24 frames while words play.
- Legibility: full line readable ≥1 beat before exit; contrast checked
  on extracted frames over the actual footage, not assumed.
- No generated text anywhere: every visible word traces to the
  post/code layer.

## Pointers
- Full taxonomy (per-form specs, sync rules, feasibility table):
  `visual-forms/VISUAL_FORMS_TAXONOMY.md`
- Kinetic craft (tool choice, GSAP vocabulary → ASS mapping, fonts):
  `visual-forms/KINETIC_TYPE_PLAYBOOK.md`
- Tool + proof + overlay notes: `visual-forms/tools/kinetic_ass.py`,
  `visual-forms/proof/`, `visual-forms/GRAPHICS_OVERLAY_NOTES.md`
- Generator behavior for F-family footage: skill `video-api-mastery`
- Storyboard/animatic production flow + motion rules (one motion per
  shot, stranger test): `visual-forms/SOURCE_renproton_motion_design_studio.md`
- Critic loop (contact-sheet QC, worst-3 fixes, 8+ bar), state lists /
  morphing container, springs on one clock:
  `visual-forms/SOURCE_nicc0_film_crew_stack.md`
- Index of everything: `~/workspace/wubutv-network/musicvideo/MONDO_INDEX.md`
