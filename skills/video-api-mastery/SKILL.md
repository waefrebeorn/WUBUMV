# Video API Mastery — what WuBu's generator actually does, measured

Built 2026-11-06 from the video-api lab battery: 2 generated reference
images + 3 generated videos, every claim frame-probed (colour-probe
pixel fractions + pixel MAE against the refs; cross-image controls
≈ 111 MAE). Evidence of record:
`~/workspace/wubutv-network/musicvideo/video-api-lab/VIDEO_API_AUDIT.md`,
`IMAGE_REF_PLAYBOOK.md`, `TEST_LOG.md` (same dir; harness `measure.py`
kept alongside). Where this skill and a lab file disagree, the lab
file wins — it is the measurement, this is the distillation.

This skill governs HOW the generator behaves. It does not govern what
ships: sync, QC gates, edit rules, and hard stops live in the
Slopcannon skill (`~/workspace/custom-skills/slopcannon/SKILL.md`),
which is governing wherever the two overlap.

## When to use

- Before any `media.generate_video` / `media.generate_image` call that
  carries an image entry, a duration or aspect requirement, or more
  than one image.
- When planning character consistency across takes or scenes.
- When someone (a plan, a worker, a past note) claims the generator
  "animates the image", "starts exactly on this frame", "chains from
  the last take", or "will be silent" — check the claim here first.
- Pair with Slopcannon stage 4 (Fire) for singing vehicles; pair with
  the visual-mv-forms skill when the slot is not a singing take.

## The one law of image refs

> **An image input is a strong conditioner, not a frame source.**
> The output is always a fresh generation. Composition, character
> design, props, and style carry over measurably (pixel MAE 43–52
> against the conditioning ref vs ≈111 cross-control), but no output
> frame is ever pixel-identical to a ref (MAE never near 0), and
> exact hues can drift. Plan for "same scene, re-rendered"; verify
> every take with the usual QC gates; never promise frame-exactness.

## Measured capability table

All rows measured 2026-11-06 unless marked as tool-contract facts.

| Capability | Measured behavior | Evidence |
|---|---|---|
| Inputs | Ordered list of `{kind: text}` and `{kind: image}` entries (image = local still-image path); optional `name`, `output_dir`, `resume_from_snapshot_id`. Interleaving text/image is expressive and carries meaning. | Tool contract; audit §1; V-01/V-03 orderings |
| Numeric parameters | **None.** No duration, aspect, fps, or seed fields exist. Duration and aspect are steered in prompt text — and work (below). | Audit §1, §4 |
| Audio input | **Does not exist.** No audio entry kind, no audio file parameter, no word-timing or lip-sync parameter. | Audit §1 |
| Video input | **Not supported** (no video-to-video). | Audit §1 |
| Duration | "exactly 5 seconds" in text → **5.000 s** exactly. No duration text → **10.000 s** default. Only 5 s and 10 s are measured points. | V-01; V-02/V-03 |
| Aspect | Text beats image: "vertical 9:16 portrait" over a 3:2 landscape ref → **720×1280**. No aspect text + no image → **1280×720 (16:9)** default. No aspect text + images attached → output **adopts the images' aspect** (3:2 → 1152×768). All outputs 24 fps h264. | V-01; V-02; V-03 |
| Output audio | Always synthesized AAC, always present. Quoted speech is synthesized verbatim (V-01: the exact line, whisper p=0.994). With NO audio instruction the outcome is a lottery: invented spoken line + louder bed (V-02, mean −19.8 dB) vs near-quiet ambient (V-03, mean −32.4 dB). Never silence by default; never predictable. | Audit §5 |
| Volume limits | At most **6 videos per user message**, including videos made by handed-off agents; the cap is a batching limit, never an interaction gate (Slopcannon stage 4). ~10 s is the default clip length, not a ceiling on what text can request — but only 5 s/10 s are measured. | Tool contract; audit §4 |
| Failures in battery | None: 5/5 calls (2 images, 3 videos) succeeded first try, no refusals, no retries. Prompt lengths were short (45–80 words of video text) — long-prompt behavior is **untested**. | Audit §7 |

## Image-ref doctrine

### What carries, in strength order
1. **Character identity carries strongest.** Species, colour, ears,
   scarf, chest light, signature prop persisted across a complete
   scene change (room → pier) in V-03 — and even *overrode drift in
   the second ref* (the image model had given RefB disc ears; the
   video came back with cat ears, leaning on the stronger/first ref).
2. **Composition and layout** carry when output aspect matches ref
   aspect: V-03 frame 0 was a near-replica of RefA (MAE 43.17; colour
   probes within ~2 points on every channel).
3. **Prop singularity** comes from the image, not the words: text-only
   V-02 multiplied "one giant key" into key-rings and a small key;
   image-conditioned takes kept exactly one.
4. **Exact hue does NOT reliably carry.** RefA's magenta walls
   (26.28% probe) came back purple in V-01 (magenta probe 0.11%,
   purple bucket 13.2%). Identity and layout held; colour values
   drifted. Never QC-pass or QC-fail a take on hue alone without
   checking whether the drift class is this one.
5. **Text alone cannot reproduce a reference scene.** The same words
   with no image produced a different, busier room and a different
   cat face (V-02). Words describe a concept; an image pins a design.

### The recipes (full versions: IMAGE_REF_PLAYBOOK.md §i–vi)
- **First-frame lock:** framing text → image → action text. Lands a
  near-replica open **only if the ref is at the target aspect**; a
  conflicting aspect demand forces a recomposition (V-01: MAE 82.51,
  zoomed, re-posed). The lock holds ~0.5 s before motion/transformation
  begins (V-03 probes: signature intact at 0.5 s, dissolving by
  0.75 s) — a hook frame and a clean cut point, not a held tableau.
- **Character anchor:** the character's clearest full-design image
  goes **first**; still restate the invariant traits in every text
  entry. One strong anchor image early beats trait lists.
- **Two-image journey:** interleave framing text → image 1 →
  transition text naming image 2 → image 2 → arrival text. Measured
  shape: **start-anchor → ~0.5 s morph at 0.5–1.0 s → an invented
  middle scene in neither ref → ~9 of 10 s in the second image's
  world**, landing on a recomposed version of image 2 (MAE 51.85 —
  the end anchor is the *least* exact in the chain). Use for
  location-change / transformation / travel bridges. NOT a storyboard
  of equal beats and NOT a crossfade: for timed panels, generate one
  clip per panel and cut in assembly.
- **End-frame / target-frame:** the target picture goes **last**,
  introduced by destination language ("ends at the second image").
  Expect a recomposed landing (the lighthouse gained a house; the cat
  re-centred). If the exact frame must appear verbatim, lay the still
  in during editing — the generator will not reproduce it.
- **Generate-the-ref-first pipeline (the standard WuBu route):**
  (1) design the ref for measurability — bold shapes, one signature
  prop, distinctive palette — via `media.generate_image` into the
  project dir; log md5 + snapshot_id. (2) **Read the ref back before
  using it** — RefB itself arrived with drifted ears; a bad ref
  poisons every downstream take. Re-generate or accept-and-note.
  (3) Feed it to video ordered per the recipe above; text carries
  duration, aspect, action, any quoted speech. (4) Probe the output
  (ffprobe + frame 0/mid/late extraction + probe/MAE comparison)
  before the take enters a volley. (5) Mute generated audio in
  assembly — always (Slopcannon: generated audio is never a
  soundtrack or timing source).

### Always state aspect in text
For the one-16:9-master rule this is mandatory, not hygiene: an
unstated aspect **follows the attached images** (3:2 in V-03), and a
ref at the wrong aspect also degrades the first-frame lock. Generate
or choose refs at master aspect, and still write the aspect line on
every call.

### Anchor-still-per-character playbook (2026-09-26, still governing)
This doctrine is the measured confirmation of the consistency
playbook adopted 2026-09-26 (`~/workspace/wubutv-network/CONSISTENCY_RESEARCH.md`):
lock identity first with a reference image, then animate — extract a
canonical anchor still per character from an accepted piece and pass
it on every new generation, keep the full text description alongside
it, chain snapshots for direct sequels, and keep detail-tile QC. The
2026-09-26 A/B (text-only vs reference frame, same character, new
setting) found cross-clip identity clearly favored the image
reference; the 2026-11-06 lab measured *why and how much* (MAE 43–52
vs ≈111) and added the limits: recognizably the same character, never
pixel-identical; per-take face/prop QC remains necessary.

## Audio doctrine
- There is no way to supply audio, words, timings, or a lip-sync
  target to this generator. Anything claiming otherwise is wrong
  about this tool.
- Quoted speech in text IS synthesized verbatim (V-01) — and is still
  dropped in MV assembly, always. It is never a timing source.
- Unprompted audio is a lottery (invented dialogue vs near-silence
  under identical no-instruction conditions). Never plan a take
  around its generated audio, in either direction: do not count on
  speech, do not count on quiet.

## Failure modes (measured or directly implied)
- **Hue drift under conditioning** — magenta → purple while layout
  and identity held (V-01). Expect it; don't chase it with rerolls
  unless the hue itself is a gate (e.g. wordmark colour — Slopcannon
  QC governs).
- **Recomposition under aspect conflict** — demanding 9:16 against a
  3:2 ref rebuilt the scene (zoom, added tail, redrawn feet, smaller
  re-posed key). Match ref aspect to target aspect instead.
- **Prop multiplication in text-only mode** — "one giant key" became
  several (V-02). If a prop must be singular, condition with an image.
- **Invented speech / unpredictable levels** — see Audio doctrine.
- **End-anchor softness** — the destination frame is recomposed more
  than the start frame (MAE 51.85 vs 43.17). Cut on the landing in
  assembly rather than expecting a hold.
- **Ref poisoning** — drift generated INTO a ref (RefB's ears)
  propagates or gets silently "corrected" toward the stronger ref;
  either way, read refs back before use (pipeline step 2).

## UNTESTED — fenced, unproven, do not build workflow on these
Everything in this section is schema-plausible or externally
documented but **not measured on WuBu's tool**. A plan may name one
of these only as an experiment with a fallback, never as a load-bearing
step.

1. **`resume_from_snapshot_id` chaining.** Every call returns a
   snapshot_id and the schema says it "continues the same video
   context… instead of resending that result's local_path" — but the
   lab's 3-video cap was exhausted before a resume call could run, so
   whether context, character, or scene actually carries is UNKNOWN.
   **The exact one-call test (playbook §7, ready to fire under a
   future budget):** call `media.generate_video` with
   `resume_from_snapshot_id = f8e32fdc-b667-4381-a632-243edb4d596f:844s3x`
   (V-03, the pier ending) and a single text entry: "The cat turns
   and walks back toward the camera, waving the brass key, lighthouse
   still behind it." Then probe: does frame 0 continue the pier scene
   (navy signature ~68%, lighthouse present) with no image resent?
   Until that call runs, resume behavior is unproven.
2. **Style-only transfer.** Style demonstrably carried along with
   everything else in V-01/V-03, but no test isolated style (a style
   exemplar of an *unrelated* subject). Conditioning appears to be
   whole-image, so expect subject leakage. One-call follow-up: attach
   an unrelated-subject style ref, write the new subject explicitly,
   probe for leakage (playbook §iii).
3. **More than 2 images in one call.** Untested entirely. The
   2-image behavior (front-loaded morph, destination-dominant) gives
   no license to extrapolate to 3+.
4. **Also untested** (audit §8): image-after-text vs image-before-text
   ordering for a *single* image (V-01 was image-first); long prompts;
   photoreal subjects; human identity refs; negative prompts; any
   duration other than 5 s / 10 s. Each is a one-call follow-up on the
   lab's probe harness.

## Evidence pointers
- Full audit (claims + numbers): `video-api-lab/VIDEO_API_AUDIT.md`
- Recipes in full: `video-api-lab/IMAGE_REF_PLAYBOOK.md`
- Every call logged (prompts, md5s, snapshot IDs, frame md5s):
  `video-api-lab/TEST_LOG.md`
- Probe harness: `video-api-lab/measure.py`; refs/videos/frames kept
  in the lab dir.
- Index of everything: `~/workspace/wubutv-network/musicvideo/MONDO_INDEX.md`
