# Media Probe Results — P0–P5 (2026-11-12)

**Date:** 2026-11-12 ~03:40–04:00 EST
**Order:** parent-stated budget — **exactly 5 videos + 1 image** (media tool contract: task from another agent must state the number). Budget used: **5/5 videos, 1/1 image. No 429, no refusals, no retries.**
**Spec:** `research_notes/media-capabilities-survey-2026-11-12/report.md` §2 (prompts, entry order, pass criteria). Lab: `video-api-lab/` — refs `refA.webp` / `refB.webp` / `refC.webp`, videos `p1.mp4`–`p5.mp4`, frames `p*_*.png`, harness `measure.py` (colour probes, tol 60) + 160×90 MAE.
**Method note:** one frame per ffmpeg invocation (separate `-ss` calls, distinct md5s verified) — the multi-input frame-extraction trap (frame 0 for every output) was avoided throughout.

## Scoreboard

| Probe | Question | Verdict |
|---|---|---|
| P0 refC | Third ref: clean, separable, no poisoning? | **PASS** |
| P1 resume | Does `resume_from_snapshot_id` carry the scene? | **PASS — chaining works** |
| P2 3-image | Does it visit all three worlds or collapse to two? | **PASS — three worlds, clean handoff** |
| P3 style-only | Does style carry to an unrelated subject? Does the cat leak? | **PASS — style carries, no leak past f0** |
| P4 7 seconds | Does "exactly 7 seconds" return 7.000s or snap? | **FAIL as asked — snaps to 10.000s** |
| P5 text-first | Does image-after-text ordering move the V-01 82.51 MAE? | **PASS with an ordering effect — MAE 77.23, hue held** |

## P0 — refC (image)

- **Prompt (verbatim):** "Flat bold cartoon illustration, thick outlines, solid colours: a brass robot dog with a silver bell on its collar trots through a fern-filled forest clearing at dusk, fireflies, deep green and amber palette, 1920x1280."
- **File:** `refs/media-generation-refc-0-81828223-6a39-4a8c-8ac0-adb475c5b79f.webp`, 590,098 B; working copy `refs/refC.webp`, **md5 `ddd785ca4448394a9f3ed75b360c9bef`**, 1920×1280. **snapshot_id `c579d32a-d476-4ad3-b14e-b8e9ee11a81e:ptlb72`.**
- **Probes:** dark-green buckets dominate (#202020 18.5%, #204020 14.9%); navy 12.53 (dusk sky), yellow 3.13 (fireflies/amber), orange 3.95; **magenta 0.0, teal 0.0, green-floor 0.0** — cleanly separable from refA (magenta 26.28) and refB (navy 55.46).
- **Visual read-back:** all specified elements present — brass robot dog, silver bell on collar, fern-filled clearing, dusk, fireflies, deep green + amber palette, flat bold cartoon, thick outlines. No text, no cat, no room/pier bleed. **No ref poisoning.**
- **Verdict: PASS.**

## P1 — resume chaining (THE test)

- **Call:** `resume_from_snapshot_id = f8e32fdc-b667-4381-a632-243edb4d596f:844s3x` (V-03 pier ending), single text entry: "The cat turns and walks back toward the camera, waving the brass key, lighthouse still behind it. Exactly 10 seconds, 16:9." No image resent.
- **File:** `videos/media-generation-p1-resume-pier-0-945656fd-89d0-4272-a533-527c46956cea.mp4`, 5,617,997 B; working copy `videos/p1.mp4`, **md5 `07548bc7649ad7ef67cbd04014cebd84`**, 1280×720, 24fps, **10.000s**. Returned **snapshot_id `f8e32fdc-b667-4381-a632-243edb4d596f:u5loz9`** — same base id as V-03, new suffix (the context carried, it did not start a fresh chain).
- **Probes:** f0 navy **62.17%** (>50% bar), magenta **0.0%**; mid navy 63.24%, magenta 0.0%; late navy 51.93%, teal 16.52% (cat larger in frame as it approaches), magenta 0.0%.
- **MAE:** p1_f0 vs v03_t9.7 **45.24** (same band as V-03's own anchors: start 43.17, end 51.85); vs refB **35.45**; vs refA cross-control **107.99**; p1_late vs v03_t9.7 47.77.
- **Visual read:** f0 = the pier at night, full moon, red/white lighthouse behind right, teal robot cat centre holding the giant brass key. Late frame = cat much larger, walking toward camera, key raised/waving, lighthouse still behind. One drift note: f0 ears read disc/mouse-like (RefB's drift); by late frame the ears are pointed cat ears again — the stronger identity re-asserted itself.
- **Verdict: PASS.** Resume chaining carries the scene with no image resent. The fixed-seed substitute exists. **Slopcannon: keep resume in the skill as the continuation mechanism; the two-image last-frame chain stays as the fallback for fresh starts (resume needs a prior snapshot).**

## P2 — 3 images in one call

- **Entries (in order):** text "This video starts at the first image, passes through the second image, and ends at the third image." → refA → text "The teal robot cat stands up from the rug, carrying the giant brass key, and the room transforms into the pier scene in the second image:" → refB → text "The cat walks the pier under the full moon and the scene becomes the forest clearing in the third image:" → refC → text "The brass robot dog trots through the fern-filled forest clearing at dusk among fireflies, still carrying the giant brass key. Flat bold cartoon illustration throughout. Exactly 10 seconds, 16:9."
- **File:** `videos/media-generation-p2-three-images-0-e286d723-846d-4810-881b-f05e84cd6bda.mp4`, 6,669,991 B; working copy `videos/p2.mp4`, **md5 `e6ef7c3b7d8e6c85e6e498f1ac872946`**, **1152×768 (3:2)**, 24fps, **10.000s**. **snapshot_id `75233a48-5b19-4000-8387-625029bd6fa6:ogho2w`.**
- **Aspect note:** output came back 3:2 (the images' aspect) **despite the "16:9" text** in the last entry. Bare "16:9" did not override the images' aspect — corroborates the survey's ranked #4 (useapi: loose "16:9" returned 3:2 once; exact phrasing "in exactly 16:9 aspect ratio" fixed it). All three refs are 3:2, so no aspect conflict was created; the finding is that bare aspect text loses to attached images.
- **Colour timeline (magenta / navy):** t0 **24.41 / 6.36** (room) · t1 **24.99 / 5.75** (room — holds past 1.0s, later morph than V-03's 0.5–1.0s window) · t2.5 **0.0 / 66.18** (pier) · t5 **0.0 / 59.96** (pier) · t7.5 **0.0 / 9.9**, yellow 2.17, orange 4.63 (forest) · t9.7 **0.0 / 8.29**, yellow 3.02, orange 5.84 (forest).
- **Visual read:** t2.5 = pier, full moon, lighthouse right, teal cat walking the pier carrying the key. t7.5 = forest clearing, ferns, fireflies — the **brass dog** (silver bell, collar) carrying the giant brass key in its mouth. t9.7 = same dog still trotting with the key. **The subject changed at the world boundary (cat → dog) exactly as the text said; no cat leaked into the forest, no dog leaked into the pier.**
- **Timing shape:** room ~0–1.5s, pier ~1.5–6s, forest ~6–10s. More even than V-03's two-image shape (start ~1s, invented middle, destination ~9s) — the middle world gets the long stretch, the destination gets the last ~3.5–4s. Three images do NOT collapse to two, and the destination does NOT dominate the way V-03's did.
- **Verdict: PASS.** 3-image calls work and distribute time across all three worlds with clean subject handoffs. **Slopcannon: three-world journeys are viable for travel/transformation bridges; budget ~1.5s / ~4.5s / ~4s per world, not equal thirds, and never expect the destination to hold 9s.**

## P3 — style-only transfer

- **Entries:** image refA → text "A brass robot dog with a silver bell trots through a fern-filled forest clearing at dusk among fireflies, in the flat bold cartoon style of the reference image, thick outlines, solid colours. The dog is the only animal in the scene. Exactly 10 seconds, 16:9."
- **File:** `videos/media-generation-p3-style-transfer-0-3706b1e2-008e-4df2-aa09-aaf9dbb20fd7.mp4`, 7,608,696 B; working copy `videos/p3.mp4`, **md5 `874e5c1bb42cf76f73a145727eb5bad3`**, 1280×720, 24fps, **10.000s**. **snapshot_id `d9a3b899-0f2e-4141-892c-ae5e0978c1df:41afp9`.**
- **Probes:** f0 magenta 32.36%, teal 12.9% (the room anchor); mid navy 81.52%, everything else ~0; late navy 78.36%. **Probe caveat:** the navy bucket catches the dark blue-purple dusk forest, not just pier-night — navy% alone cannot distinguish pier from dusk-forest. The visual read is authoritative here.
- **Visual read:** f0 = refA's room, teal cat sitting on the rug with the key — the image input locked frame 0 to the ref (first-frame lock, ~0.5s, as the playbook documents). Mid = fern-filled forest at dusk, fireflies — a **copper robot dog with silver bell and red collar**, trotting. Late = same dog from behind, walking deeper into the forest. **No cat anywhere past the f0 anchor morph.** The dog's design differs from refC (copper-orange, pipes/gears, no key) — the STYLE transferred, the specific refC design did not (no refC image was attached, so this is expected: style from refA + text-described dog).
- **Verdict: PASS.** Style carries to an unrelated subject; the ref's subject does not leak past the opening anchor. **Slopcannon: style refs are safe for new-subject takes — expect frame 0 to be the ref itself, and the new scene to start after the ~0.5s morph.**

## P4 — "exactly 7 seconds"

- **Call:** text only — "A teal robot cat sits on a wooden pier at night under a full moon, slowly raising a giant brass key, flat bold cartoon illustration. Exactly 7 seconds, 16:9."
- **File:** `videos/media-generation-p4-seven-seconds-0-f924bdea-c1c2-48a2-ab19-15a7fff9bf83.mp4`, 3,891,848 B; working copy `videos/p4.mp4`, **md5 `fb1a9ff1eb4784a6092ebd5dbbb14ace`**, 1280×720, 24fps, **duration 10.000000s, 240 frames**.
- **Result:** "Exactly 7 seconds" returned **10.000s**. The clip itself is well-formed (mid frame: pier at night, full moon, teal cat sitting, raising the brass key) — only the duration missed.
- **Verdict: FAIL as asked — durations are quantized to {5, 10}.** 5s works (V-01, P5), 10s is the default, 7s snaps to 10s. **Slopcannon: never request a non-{5,10} duration; plan takes in 5s or 10s only, and cut in assembly for anything else.** (Untested: 15s, 20s, other values — the quantization may be {5,10} exactly, or a coarser grid; one more probe would settle it, but it is outside this pack's budget.)

## P5 — image-after-text ordering

- **Call:** replicate V-01 exactly but text-first — text "Animate this scene, exactly 5 seconds, vertical 9:16 portrait orientation. The teal robot cat raises the giant brass key and says 'The key is mine!'" → image refA.
- **File:** `videos/media-generation-p5-text-first-0-e2a1de40-09ee-48ad-85db-db954e0010c1.mp4`, 2,031,398 B; working copy `videos/p5.mp4`, **md5 `e4317ffa73dcba014c51b03dd85a2cbd`**, 720×1280 (9:16), 24fps, **5.000s**. **snapshot_id `3f5bc91a-f900-4233-b2bf-ef6b3207a6ae:y6myfz`.**
- **MAE:** p5_f0 vs refA **77.23** vs V-01 image-first **82.51** (−5.28, −6.4%). p5_f0 vs v01_f0 54.51 (the two portrait re-renders resemble each other more than either resembles the ref); vs refB cross-control 101.24.
- **Probes (f0):** magenta **20.31%** vs V-01 f0's **0.11%**; teal 15.68%, green 8.59%, yellow 2.91%, orange 4.44%.
- **Visual read:** portrait recomposition of refA (same class as V-01: zoomed, re-posed, cat larger, rug bigger) — but the **magenta walls HELD** this time, where V-01's went purple. Star lamp, checkered floor, key, scarf all present.
- **Audio (extra check, V-01's speech bundle):** "The key is mine" 0.00–4.10s, avg_logprob −0.25 (large-v3-turbo, lyrics venv) — the quoted line synthesized verbatim text-first, same as V-01 image-first. Mean −20.7 dB, max −0.4 dB.
- **Verdict: PASS with a real ordering effect.** The MAE move is small (−5.28, within fresh-generation noise), but the hue-fidelity move is large: text-first kept the magenta walls (20.31% probe) where image-first lost them to purple (0.11%). **Slopcannon: when hue matters under an aspect conflict, put the text FIRST — the text anchors the palette before the image is seen. Ordering is not cosmetic.**

## What each result means for the Slopcannon

1. **Resume chaining: KEEP.** P1 proves `resume_from_snapshot_id` carries the scene (navy 62.2% f0, MAE 45.24 vs the resumed ending, no image resent). It is the fixed-seed substitute — cheaper and less drift-prone than re-sending last frames as images. The continuity method gains a no-resend chain; the two-image last-frame chain stays the fallback for fresh starts (resume needs a prior snapshot). The video-api-mastery skill's fenced item #1 is now MEASURED, not untested.
2. **Three-image journeys: VIABLE.** P2 visits all three worlds with clean subject handoffs and no collapse. Budget ~1.5s / ~4.5s / ~4s per world; the destination does not dominate. Use for travel/transformation bridges with a subject change per world.
3. **Style refs: SAFE.** P3 shows style carries to an unrelated subject with no leak past the f0 anchor. Frame 0 will be the ref itself — plan the morph into the shot.
4. **Durations: {5, 10} only.** P4 proves 7s snaps to 10s. Never request other durations; cut in assembly.
5. **Ordering: text-first when hue matters.** P5 shows a small MAE move but a large hue-fidelity move (magenta held 20.31% vs 0.11%). The first-frame-lock recipe should lead with text when the ref's palette must survive an aspect conflict.
6. **Aspect phrasing: bare "16:9" loses to images.** P2 returned 3:2 despite "16:9" in the text — corroborates the survey's ranked #4. Use "in exactly 16:9 aspect ratio" (the exact form) whenever images are attached.

## Single biggest Slopcannon implication

**Resume chaining works — the continuity method now has a no-resend chain.** P1 is the pack's decisive result: a snapshot id alone, with one short text entry, continued V-03's pier ending into a new 10s clip (frame 0 MAE 45.24 vs the resumed ending, navy 62.2%, magenta 0.0%, lighthouse present, cat walking toward camera waving the key). Every volley that chains scenes can now do it without re-sending last frames as images — less drift, less prompt weight, and the snapshot id is the chain. The second-biggest is the ordering finding: text-first preserves hue under aspect conflict, which is a one-line recipe change in the first-frame lock.

## Honest limits

- **n=1 per probe.** Every result is a single draw; the model is stochastic and the prompt-expansion subagent sits between the text and the model. P1's pass is strong (multiple independent measures agree: probes + MAE + visual), P4's snap is structural (a duration grid, not a draw), P5's MAE move is small enough to be noise — only the hue move is large.
- **The probe harness measures colour + MAE, not motion.** Motion quality (does the dog actually trot? does the cat actually walk?) was judged by eye on 2–3 frames per probe, not by a motion metric.
- **P2's aspect finding is confounded:** all three refs are 3:2, so "bare 16:9 loses to images" is consistent with both "images win" and "3:2 refs win" — the exact-phrasing test (ranked #4) still needs its own call.
- **P4 leaves the duration grid partly open:** {5, 10} are measured; 15s/20s/other values are not. The grid may be exactly {5,10} or coarser/finer — one more probe would settle it, outside this pack's budget.
- **No audio was measured on P1–P4** (P5's speech check only). Generated audio is muted in assembly regardless.
- **Daily video budget (429) never hit** — all 5 videos + 1 image succeeded first try, no refusals.

## File inventory (lab dir, working copies)

| File | md5 | Size | Notes |
|---|---|---|---|
| refs/refC.webp | ddd785ca4448394a9f3ed75b360c9bef | 590,098 B | 1920×1280, snapshot c579d32a…:ptlb72 |
| videos/p1.mp4 | 07548bc7649ad7ef67cbd04014cebd84 | 5,617,997 B | 1280×720, 10.000s, snapshot f8e32fdc…:u5loz9 |
| videos/p2.mp4 | e6ef7c3b7d8e6c85e6e498f1ac872946 | 6,669,991 B | 1152×768, 10.000s, snapshot 75233a48…:ogho2w |
| videos/p3.mp4 | 874e5c1bb42cf76f73a145727eb5bad3 | 7,608,696 B | 1280×720, 10.000s, snapshot d9a3b899…:41afp9 |
| videos/p4.mp4 | fb1a9ff1eb4784a6092ebd5dbbb14ace | 3,891,848 B | 1280×720, 10.000s (240f), snapshot 1929b6a1…:wgt63k |
| videos/p5.mp4 | e4317ffa73dcba014c51b03dd85a2cbd | 2,031,398 B | 720×1280, 5.000s, snapshot 3f5bc91a…:y6myfz |

Frames: `frames/p1_f0.png` (14906cdd…), `p1_mid.png` (77d6c360…), `p1_late.png` (8cbccbb4…), `p2_t0.png` (767c368e…), `p2_t1.png` (f926aa3e…), `p2_t2p5.png` (45287654…), `p2_t5.png` (e1c9b057…), `p2_t7p5.png` (5a3bec9a…), `p2_t9p7.png` (63980341…), `p3_f0.png` (8535f577…), `p3_mid.png` (bede0dcb…), `p3_late.png` (dceb1fda…), `p4_mid.png` (4db23f73…), `p5_f0.png` (00f4c59e…).

## Recovery verification (2026-11-12 ~04:16 EST)

The original probe coordinator died (daemon restart) after completing all probes; a recovery coordinator resumed from disk. Verified, no re-fires (budget already 5/5 videos + 1/1 image, fully used): all five video md5s + refC md5 re-checked and match this file exactly; ffprobe re-run on p1–p5 confirms dims/durations (p1 1280×720 10.000s · p2 1152×768 10.000s · p3 1280×720 10.000s · p4 1280×720 10.000s — the 7s snap, confirmed · p5 720×1280 5.000s); frame md5s spot-checked (p1_f0, p5_f0, p2_t9p7) match TEST_LOG.md. TEST_LOG.md independently documents the same P0–P5 results. Deliverable complete as written; nothing further owed.
