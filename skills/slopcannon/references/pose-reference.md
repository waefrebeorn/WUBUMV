# Slopcannon pose reference

WuBu's own pose system, SLERM-built from the public pose-workflow pattern:
a reference gallery supplies body geometry, a depth map supplies layering,
and a multi-reference composite supplies identity + outfit + pose in one
recipe. Rebuilt here for WuBuTV's text-driven video tool — no ComfyUI, no
copied gallery images, no copied prompts.

## What we took (and what we did not)

- From the pose galleries (ai-pose-gallery-zh and the POSE-DB-02 depth
  gallery): the WORKFLOW, not the assets. A pose is a searchable unit with a
  viewpoint (front / three-quarter / side / back / top). A recipe has three
  slots: face, outfit, pose. A depth reference is a layering statement: what
  sits near, mid, and far. That is all we took.
- From Stable Diffusion tutorial workflow writing: the conditioning pattern —
  reference-driven generation beats prompt-only generation for consistency,
  and a repeated verbatim block beats a paraphrased one. Same lesson WuBu's
  own 2026-09-26 consistency research already proved: lock identity first
  with a reference image, then animate; repeat the full description verbatim.
- NOT taken: the galleries' images (copyright of their original author, and
  their repo carries no usable license grant — browse them by URL only, never
  copy an image into a WuBu project), their prompt text, their UI, their
  plugin code, or their model choices. WuBu pose cards are original text.

## Hard exclusions

- SFW poses only: standard full-body and upper-body poses. NEVER the
  galleries' adult categories (their sexy / couple / 18+ sets) — never
  browse them for a project, never describe them, never attach them to a
  WuBu character.
- Poses are body geometry, never identity. Never attach a pose to a real
  person's face or body, and never use a pose reference to reproduce a
  real person.
- One character per scene keeps its own pose card. A pose card never
  introduces a second person.

## The pose card

Write `POSE_CARDS.md` in the project folder during Direction, before any
firing. One card per SIGNATURE pose (a pose reused across scenes), and every
scene in `MV_PREPRO` assigned to exactly one card plus a one-line variation.

A card carries, in this order:

1. Name (e.g. P-CROON) and viewpoint (front / three-quarter / side / back / top).
2. Stance: feet, hips, weight distribution.
3. Torso: lean, turn, tension.
4. Arms and hands: exact hand positions, prop contact (mic, ticket, glass).
5. Head and gaze: chin angle, eye direction, expression (deadpan, wince, wink).
6. Depth layering (the depth-map translation, in words): near / mid / far —
   what is closest to camera, where the character stands, what sits behind.
7. Motion inside the 10 seconds: start pose → end pose (one change only).

## The vehicle anatomy (3-slot recipe)

Every scene vehicle is built in this order, each block verbatim wherever it
repeats: [identity block] + [outfit block] + [pose block] + [setting] +
[camera move] + [beat]. Identity and outfit never change mid-project; only
the pose block changes, and only to a card from `POSE_CARDS.md`.

## Anchor stills

The first accepted take of a signature pose yields its anchor: the take's
first frame, filed in the project folder as `anchors/<POSE>.jpg`. Later
scenes using that pose name the anchor in their vehicle ("same stance as
anchor P-CROON"). Consistency means recognizably the same character in the
same stance, never pixel-identical frames — that limit is honest and stands.

## QC on poses

A scene fails pose QC if: the character's pose does not match its card
(wrong hands, wrong gaze, wrong stance); a second person appears; the pose
reads as an adult-category pose; or the depth layering puts the character
behind a prop that hides the face or the motif object. Reroll on the pose
axis only, one named correction, per the firing rules.
