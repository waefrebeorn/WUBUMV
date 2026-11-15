# Generated Panels + Reference Workflows — research report

**Date:** 2026-11-15 · **Order:** Telegram msg 432 (user): "learning how to make better generated panels and reference workflows, documenting and backing up all workflows."
**Feeds:** Slopcannon MV builds + WuBuTV station shows. **Companion docs (ours, governing):** `~/workspace/custom-skills/video-api-mastery/SKILL.md` (measured generator behaviour), Slopcannon skill CONTINUITY METHOD (per-project reference stack), niceaunties lilypad study (STILL-FIRST SLOT, `research/lilypads/niceaunties-20261115/`).

**Evidence key.** **EVIDENCED** = measured on our own tool, in vendor docs, or corroborated by multiple independent practitioner sources. **LEAD-LEVEL** = single-source practitioner/marketing claim — usable as a hypothesis, never as a load-bearing step. Where field practice and our own measurements conflict, **our measurement wins** and the conflict is flagged in §3.

---

## 1. What the field does

### 1.1 Storyboard panels: one key image per shot, hero frame first

The converged 2026 pipeline is script → key images → animation, and the storyboard stage is treated as non-optional ("skipping the storyboard is the most expensive mistake" — Ramon Gomes' Nov 2026 workflow guide, EVIDENCED as consensus across sources below). The working pattern:

- **One key image per scene/shot**, generated starting with the main character; that image is kept and becomes the reference for all the others (Gomes). At animation time the prompt describes **only the motion** — the picture already carries the world.
- **Hero-frame lock (daisychain.tools animatic workflow, EVIDENCED as practice):** write a shot list where a **style line and a character line go into every prompt verbatim**; generate shot 1 and iterate until one frame is right; that hero frame is then the reference image for every other shot. Their hard-won warning: *"Consistency drifts by shot 5. Re-use the hero frame as the reference every time, not the previous shot, or the character slowly mutates."* (This is about board/still generation across non-adjacent shots — see §3 for how it coexists with our take-chaining law.)
- **Dedicated storyboard tools** (Drawstory, mstudio.ai, ImagineArt's Storyboard node) automate script→panel breakdown with character locks, single-panel regeneration, and animatic export (EVIDENCED these products exist and work this way; their marketing stats — "52% cheaper, 48% faster approvals", "57% of creators report drift" — are LEAD-LEVEL vendor numbers, not findings).

### 1.2 Contact-sheet / panel-grid prompting: decide in a grid, build at full size

A distinct, newer pattern: generate **many frames in ONE image** as a grid, choose, then rebuild the winner.

- **8frame's ShotGrid workflow (EVIDENCED, detailed practitioner write-up):** a 3×3 "contact sheet" of nine frames of the same scene/story in one 4K image. Two sheet types: a **story sheet** (nine different beats of one sequence — test order and coverage) and an **option sheet** (nine versions of one shot — pick the best framing before animating). A shared style/character paragraph across all nine panel descriptions is what makes the grid read as one film. Takes 1–10 reference images (character sheet, location, product, mood frame), and the prompt must say what each reference is *for*.
- **The catch, stated by the source itself:** each panel is one ninth of the sheet, so a cropped panel is a fraction of the resolution — **the chosen frame is rebuilt at full size, in the film's aspect, from the crop before it becomes a start frame.** The sheet is a decision tool ("you are choosing, not finishing"), never a fireable asset.
- **Midjourney practice points the other way for control (EVIDENCED, readray/MJ storyboard guides):** one-shot grids give limited control over each panel's action; the reliable route is **individual panels, assembled and annotated in an external tool**. MJ also "understands the sheet concept" — character-design sheets and expression sheets with multiple poses/expressions of one character in a single wide image are a long-standing MJ idiom.
- **Prompt-shared grid generators** (Nano Banana-family "3×3 cinematic storyboard contact sheet" prompts, EVIDENCED as circulating practice): one input image → nine shots across focal lengths (wide / full-body / knees-up rows) with strict same-subject/same-clothing/same-lighting constraints written into the prompt.

### 1.3 Character sheets and turnarounds: remove ambiguity, then LOCK

The character reference sheet is the field's core consistency asset (Kapwing guide; EZ Character; invideo production write-up — EVIDENCED consensus):

- **Contents:** primary full-body image; front, three-quarter, profile, back views; neutral + expressive facial close-ups; close-ups of easily-confused details (scars, accessories, wordmarks). "A good reference sheet is not necessarily the most attractive one. Its main job is to remove ambiguity."
- **Angle-anchoring:** every angle is generated **anchored to the one master image** ("the character is rotated, not reinterpreted") — re-prompting each view from text is what causes drift (EZ Character's 8-angle compass turnaround: front, both three-quarters, both profiles, both back three-quarters, back).
- **invideo's production rules (EVIDENCED, from a shipped 70-second short):** four angles + face close-up + mid-angle close-up, generated at high resolution, **hands empty** (held props drift between angles — generate each prop as its own separate reference; one production used 11 reference images for 4 characters + 1 prop). Generate ~4 sheet variations, **formally lock the best one before any video generation begins** (~5 attempts, LEAD-LEVEL cost figure ~$9.78/character). Attach the locked sheet to every video generation. If a continuity error appears in a shot, **fix it in the sheet panel, not the shot** — the corrected sheet propagates to everything downstream.
- **Coverage principle (invideo):** "video models reproduce only what the sheet actually shows" — an angle or detail not in the sheet will be invented at fire time.
- **State variants:** if a character's appearance changes across the story (costume change, accumulated props), build a **distinct sheet per state/beat**, not one sheet plus hope (invideo; Ciaro Pro's wardrobe-states practice agrees).

### 1.4 Start/end frame pairs: the field's endpoint control — with one construction rule

First/last-frame generation is now standard across the field's tools (EVIDENCED, vendor docs via topai.one / dreamdrive.ai / aipromptgeneer.com surveys, checked Oct–Nov 2026): Veo 3.1 "Frames to Video", Kling 4.0 Keyframes (start/end + up to 10 keyframes at any position), Luma Ray3.2 Multi-Keyframe (up to 16 keyframes per clip), Seedance 2.5, Pika Pikaframes. On those tools the end frame is a genuine endpoint the model interpolates toward.

The construction rule that matters for us (EVIDENCED, dreamdrive.ai): **make the end frame by editing a copy of the start frame** (instruction editors — Flux Kontext / Gemini image edit), not by generating a second frame from scratch. Change one thing, keep the rest; keep the same lens and light; one clear movement per clip; for a bigger journey, chain clips using the end frame of one as the start of the next.

### 1.5 Reference bibles and show kits: an archive, not a prompt

For series work the field has converged on **documents + locked asset sets**, explicitly *not* model memory (EVIDENCED across hardeststories, Maosika, Ciaro Pro, ScreenWeaver):

- **Visual bible (hardeststories):** a short approved rule set — lighting logic, palette, contrast, texture, camera language, recurring design elements — written **before** generation expands. Separate permanent style choices from shot-specific instructions. **Compare every generation against the project reference, not just the previous clip.**
- **Continuity bible (Maosika, AI short-drama production):** a structured archive — character identities, stable traits, *current state* (wounds, disguises, status changes), relationships, open/resolved threads, appearance schedule — updated after each batch and retrieved before the next. Their look-dev stage produces three things before a single clip: **character sheets for every named role, empty scene plates for every recurring location, and a prop catalog extracted from the script's own wording**. Per-shot reference maps are assembled in a fixed order: **scene plate → props in this shot → character sheets**.
- **Show kit (ScreenWeaver, series production):** lock once — reference sheets, pinned descriptions, palette, model + settings; **freeze every asset the moment an episode ships**. Four distinct drifts need four distinct checks: asset drift (side-by-side across shipped episodes), canon drift (canon log read before outlining), **model drift** (same sheet + same prompt, different face after an endpoint update → run a bridge test on archive shots before committing an episode), taste drift (locked grade preset + one reference frame per environment).
- **Character bible (Ciaro Pro):** canonical record per character (stable ID, silhouette, palette, signature objects), versioned approved assets, wardrobe/appearance states with the episode where each starts, an episode continuity brief, and edit review against the bible.

### 1.6 LoRA and trained-identity routes: the ceiling above reference images

- **Reference image alone has a measured ceiling (Wan 2.2 LoRA guide — one practitioner's 40+ trained LoRAs, LEAD-LEVEL numbers, EVIDENCED direction):** I2V reference-only consistency is "medium — face holds 2–3 seconds, then drifts." Rule of thumb from the same source: **train a LoRA when the same character must survive more than ~3 clips or clips longer than ~5 s.**
- **The dataset is the product (EVIDENCED consensus across Wan guide, Stable Yogi/Krea, BFL docs, adtestbench survey):** 15 images minimum, **25–40 recommended**; **at least 5 angles** (front, both three-quarters, profile, back); vary everything except the identity — and **caption the clothes/background so they don't fuse into the identity** (the classic failure: same green top in all 40 dataset images → the LoRA learns the top as part of the face). One good image can be expanded into a ~40-image dataset by generating varied angles/places/light from it.
- **In-context LoRA — the reference SHEET as a single conditioning input (EVIDENCED, Lightricks LTX-2.3):** the "Ingredients" IC-LoRA takes **one composite reference sheet** (characters + props + location in a single image at a specified size) and carries those elements into the generated clip. The field is productising exactly the artefact this report specifies in §4: a composed panel that carries a whole shot's cast/prop/place into generation.
- Hosted shortcuts exist (Higgsfield Soul ID: 20+ photos, minutes to train; OpenArt custom character: 4–100 images; Krea built-in LoRA training) — LEAD-LEVEL for our purposes: none of them run on WuBu's generator (see §2).

### 1.7 Still-first at scale (banked, ours)

The niceaunties study (banked 2026-11-15) is the field's existence proof at hundreds-of-pieces scale: 25–30 prompts per finished video spent **in stills**, the still gated by eye as a finished frame, then animated with behaviour-only prompts; accidents harvested at the still stage; every still filed into a reusable library that seeds later work (STILL-FIRST SLOT recipe). It agrees with §1.1's motion-only animation prompts and §1.3's lock-before-video discipline, from an independent, shipped body of work.

---

## 2. What OUR tools actually do with references (measured — this section outranks §1)

From `video-api-mastery` (lab battery 2026-11-06, frame-probed) and the Slopcannon CONTINUITY METHOD (incl. probe P1, 2026-11-13):

1. **An image input is a strong conditioner, never a frame source.** Output is always a fresh generation. Composition/identity/props/style carry measurably (pixel MAE 43–52 vs ≈111 cross-control); **no output frame is ever pixel-identical to a ref**; exact hues can drift (magenta walls → purple, identity and layout intact).
2. **Carry strength order:** character identity strongest (survives a complete scene change, and overrode drift in a second ref) → composition/layout (when aspects match) → prop singularity (image conditioning kept exactly one key; text-only multiplied it) → exact hue (unreliable).
3. **There are no numeric parameters and no dedicated slots.** No duration/aspect/fps/seed fields (duration + aspect are steered in text — and work: "exactly 5 seconds" → 5.000 s; default 10 s; aspect text beats image aspect). **No first-frame/last-frame slots, no LoRA input, no character-reference slot.** Images are an ordered list interleaved with text, and the ordering carries meaning.
4. **Two images = a journey, not an interpolation.** Measured shape: start-anchor → ~0.5 s hold → morph at 0.5–1.0 s → **an invented middle scene in neither ref** → ~9 of 10 s in the second image's world, landing on a **recomposed** version of image 2 (end-anchor MAE 51.85 — the least exact element in the chain). The first-frame lock itself holds ~0.5 s before motion begins.
5. **Resume chaining is measured and works:** `resume_from_snapshot_id` continued a scene with no image resent (frame-0 MAE 45.24 vs the resumed ending) — first-choice chain for continuations; the two-image last-frame chain is the fallback for fresh starts.
6. **≤2 images per call is the measured envelope.** 3+ images: untested. Style-only transfer: untested, and conditioning appears whole-image, so subject leakage is expected. Single-image text/image ordering variants, long prompts, photoreal/human identity refs: untested.
7. **Unstated aspect follows the attached images** (3:2 refs → 3:2-ish output). For the one-16:9-master rule, refs must be generated at master aspect **and** aspect must still be stated in text on every call.
8. **Ref poisoning is real:** a drifted ref (the lab's RefB arrived with wrong ears) propagates into takes or gets silently "corrected" toward the stronger ref. **Every ref is read back before use** — this is already pipeline law; §4 makes it a panel gate.
9. **No audio input exists; generated audio is always synthesized and always muted in assembly.** Panels never carry audio responsibility.

### Conflicts: field claim vs our measurement — ours wins

| # | Field claim | Our measured reality | Working rule |
|---|---|---|---|
| C1 | "Give the model a start frame and an end frame; it interpolates between them" (Kling/Veo/Luma behaviour) | Our two-image call front-loads a morph, invents a middle, spends ~90% of the clip in image 2's world, and recomposes the landing | An end panel is a **destination conditioner**, never an endpoint. For timed beats: **one clip per panel, cut in assembly**. Never promise a take lands *on* a panel |
| C2 | "When a character has a reference image, the prompt must not re-describe their appearance" (Maosika) | Our playbook measured the opposite: one strong anchor image early **plus** invariant traits restated in every text entry | Restate the invariant traits in text on every call, anchor image first |
| C3 | "Always reference the hero frame, never the previous shot, or the character mutates" (daisychain, about still/board generation) | Our CONTINUITY law chains take N+1 from take N's last frame (and resume), measured MAE ~45–52 at the joint | Both, scoped: **chain for joints** between consecutive takes of one scene; **re-anchor to the locked character panel at every scene start** so drift cannot compound across a whole video. Never chain across a scene break for identity — chain across it only for world/frame continuity when the plan says so |
| C4 | "Train a LoRA for any character in >3 clips" (Wan/field practice) | Our generator has no LoRA route at all | The LoRA's job is done by the **locked panel set + trait restatement**. The LoRA *dataset* discipline (§1.6: 25–40 varied images, ≥5 angles, vary everything but identity) still applies — as the coverage spec for the panels themselves (§4), because our conditioner can only carry what a panel shows |
| C5 | "Attach the whole character sheet / reference set to every generation" (invideo, Seedance-style multi-ref) | Our measured envelope is ≤2 images per call; 3+ is untested | Panels are chosen **per call** (max 2, ordered by recipe), never dumped in as a set. The sheet's job is done at panel-build time; at fire time the vehicle names the 1–2 panels it uses |

---

## 3. (Reserved — conflicts are tabulated in §2 above.)

---

## 4. THE PANEL WORKFLOW SPEC (the deliverable)

This spec **upgrades** the existing Slopcannon reference stack (REFERENCE_STACK.md + `work/stills/stack/`, one start/end pair per scene, written before volley 1) — it does not replace it. It adds panel *types* with distinct jobs, a lock discipline, a naming/storage convention, and panel-level QC. It also generalises the banked STILL-FIRST SLOT recipe from hero slots to a typed system.

### 4.1 Panel types

| Panel | What it is | How it's built | Fire-time use (our recipes) | Panel QC gate |
|---|---|---|---|---|
| **CHAR — character sheet** | One character, locked identity: hero front/¾ full-body + face close-up; extended set adds profile + back. Hands empty; NO held props | Generate hero still from the LOOK block; read back; generate angle variants **anchored to the hero** (image-ref), never re-prompted from text alone. ~4 variations of the hero, lock 1 | **Image 1** in the character-anchor recipe for every take featuring the character; re-anchor at every scene start (rule C3). Traits still restated in text (rule C2) | Identity read-back vs LOOK block (species/face/wardrobe/signature prop/wordmark — `~ WuBu ~` exact where it applies); all angles recognisably the same character; drift in any angle = that angle is REJECT, hero re-anchors |
| **PROP — prop panel** | One signature prop alone, clean background, hero angle (+1 alternate) | Generated solo — never cropped out of a group shot | Singularity enforcement: text-only generation multiplies props (measured); the PROP panel is image 2 (or interleaved) when a take must contain exactly one of the prop | Exactly one prop in frame; scale cues readable; no character hands/body attached |
| **WORLD — scene plate** | The location EMPTY of characters: layout, lighting direction, palette, recurring set elements | Generated from the scene brief; for recurring locations, built once and versioned (show kit, §4.4) | Destination image in a two-image journey (arrival into the world); fresh-first-frame source for cuts that need a new start in a known world; background conditioner behind a CHAR anchor | No characters/figures in frame; lighting direction matches the project's bible line; palette within the locked palette; aspect 16:9 |
| **PEAK — peak-frame panel** | The slot's frame-0 = peak image as a finished still: subject, event, scale gag, the one impossible thing, all legible in one glance | STILL-FIRST SLOT: written as a still brief, generated, gated by eye **before** any video spend; accidents harvested here (re-brief around a better accident) | The take's start-anchor image; the video prompt then carries motion only (what moves, how fast, what stays locked) | One-glance legibility test (event readable with no caption); composition decided (not "a nice picture of the subject"); cast correct; 16:9. A PEAK that fails is re-rolled at image cost, never patched at video cost |
| **TRANS — transition pair** | Start panel + end panel for a two-image journey; the end panel is **edited from the start panel** (one thing changed), same lens/light | Build start (usually a PEAK or WORLD); derive end by image-edit/regeneration anchored on the start, changing exactly the destination element | Two-image journey recipe: framing text → image 1 → transition text naming image 2 → image 2 → arrival text. Landing is recomposed (C1) — assembly cuts on the landing, never holds it | Delta check: exactly the intended change differs; lens/light/palette identical; both panels 16:9; the pair is logged as a pair (never split across scenes) |
| **SHEET — contact/option grid** | 3×3 (or 2×2) grid in ONE image: story sheet (beats of a sequence) or option sheet (versions of one shot) | One generation with a shared style/character paragraph + numbered panel descriptions; refs named by role in the prompt | **Decision tool only.** The winning cell is rebuilt full-size at 16:9 as a PEAK/WORLD/CHAR panel, then fired. A SHEET is never attached to a video call (grid artefacts + fraction resolution) | Grid reads as one film (same character/light across cells); winner marked in REFERENCE_STACK.md with cell coordinates; rebuild verified against the cell before the rebuild is locked |
| **STYLE — style frame** | One frame whose job is palette/texture/grade only | Generated or extracted from an approved KEEP take | **Use with the C-leakage warning:** our conditioning is whole-image, so a STYLE frame's subject will leak. Preferred route: bake style into CHAR/WORLD/PEAK panels and carry style in the bible's text lines. STYLE panels are for experiments, not load-bearing slots | Marked EXPERIMENTAL in the stack; never the sole conditioner of a hero take |

### 4.2 Build order (per project, at plan time — before volley 1)

1. **Bible lines first** (already in the plan/LOOK block): palette, lighting logic, camera language, cast LOOK blocks. Panels are generated *against* these lines.
2. **CHAR panels** for every named cast member (hero + face close-up minimum; profile/back when the plan has turns, exits, or over-shoulder shots). Lock them.
3. **WORLD plates** for every recurring location (once per location, not per scene).
4. **PROP panels** for every signature prop that must stay singular.
5. **PEAK panel per scene slot** (still-first gate), **TRANS pairs** wherever the plan calls a journey/portal/arrival.
6. **SHEETs on demand** — when a slot's framing is genuinely undecided, run an option sheet instead of burning video re-fires on framing.
7. Every panel logged in REFERENCE_STACK.md (§4.3) with status before any vehicle may name it. **Only LOCKED panels may be named in a vehicle.**

Coverage rule (from §1.6/C4): the CHAR set must cover the angles and states the plan actually uses — ≥ the views the shots need, wardrobe states as separate CHAR variants, each variant its own locked panel set. If a shot needs an angle no panel shows, the model will invent it; build the panel first.

### 4.3 Naming + storage convention

- Location (unchanged from Slopcannon): `work/stills/stack/` inside the project dir; index `REFERENCE_STACK.md` at project root.
- File names: `PNL-<TYPE>-<ID>[-<variant>].png`
  - `PNL-CHAR-UNC-hero.png`, `PNL-CHAR-UNC-face.png`, `PNL-CHAR-UNC-profile.png`, `PNL-CHAR-GIRL-blue-dress-hero.png` (wardrobe state in the variant slot)
  - `PNL-WORLD-kitchen.png`, `PNL-WORLD-boardwalk.png`
  - `PNL-PROP-brasskey.png`
  - `PNL-PEAK-S07.png`, `PNL-TRANS-S07-a.png` / `PNL-TRANS-S07-b.png`
  - `PNL-SHEET-S03-options.png` (winner recorded in the index, not the filename)
- REFERENCE_STACK.md row per panel: `file · type · md5 · snapshot_id (if any) · status (DRAFT/LOCKED/REJECT) · built-from (text / anchored-to PNL-…) · used-by (vehicle/scene list) · QC note`. md5 + snapshot logging follows the existing generate-the-ref-first pipeline law.
- REJECT panels stay on disk (marked REJECT) — the reject pile is evidence and, per still-first practice, a spare-parts library for later slots; it is never deleted mid-project and never named in a vehicle.

### 4.4 Station extension (WuBuTV shows)

For recurring-cast shows, the stack lifts one level: a **show kit** at the show's project root — CHAR panels + WORLD plates + bible lines locked once, **frozen when an episode ships** (ScreenWeaver), inherited by every episode, with per-episode panels (PEAK/TRANS/SHEET) built in the episode's own `work/stills/stack/`. Model-drift bridge test: after any generator change, re-fire three archived panels' anchor takes and compare before committing an episode. Canon/state changes (new wardrobe state, new recurring location) are new panel versions in the kit, logged with the episode where the change begins — never silent replacements.

### 4.5 Panel QC checklist (every panel, before LOCKED)

1. **Read-back done** — the panel was actually viewed after generation (ref-poisoning law). No panel locks sight-unseen.
2. **Identity/detail check** — vs the LOOK block / bible lines: face, wardrobe, signature prop, wordmark exactness where applicable. Hue drift alone is not a fail (measured drift class); identity/layout drift is.
3. **Aspect** — 16:9 (1280×720 or a clean multiple). A panel at any other aspect degrades the first-frame lock and hijacks output aspect.
4. **Type-specific gate** — per the table in §4.1 (hands empty on CHAR, empty room on WORLD, one-glance read on PEAK, single-delta on TRANS, one-film read on SHEET).
5. **Singularity & count** — one character per CHAR panel, one prop per PROP panel; no multiplied objects, no extra figures at frame edges.
6. **Status written** — LOCKED only after 1–5 pass; the stack row is updated in the same step, not later.

### 4.6 Fire-time rules (unchanged laws, restated for panels)

- Max **2 images per call**, ordered per recipe (framing text → image → action/transition text → image 2 → arrival text). Panel choice per call is deliberate; the stack is a library, not a dump (C5).
- Aspect stated in text on every call, even with 16:9 panels attached.
- Duration stated in text ("exactly 5 seconds" / 10 s default are the measured points).
- Chain joints: resume first, last-frame chain fallback; re-anchor identity to the locked CHAR panel at scene starts (C3).
- Probe every take (ffprobe + frame 0/mid/late + MAE/probe vs its panels) before it enters a volley — a take that drifts from its PEAK/CHAR panels is a QC conversation at take cost, not at master cost.

---

## 5. Sources

**Ours (governing):** `~/workspace/custom-skills/video-api-mastery/SKILL.md` + lab evidence `~/workspace/wubutv-network/musicvideo/video-api-lab/` (VIDEO_API_AUDIT.md, IMAGE_REF_PLAYBOOK.md, TEST_LOG.md); Slopcannon SKILL.md CONTINUITY METHOD + probe P1 (2026-11-13); niceaunties lilypad study, `~/workspace/research_notes/lilypads/niceaunties-20261115/report.md` (also mirrored in this repo).

**Field (accessed 2026-11-15):**
- Ramon Gomes, "How to make videos with AI: step by step and tools" (Nov 2026) — https://ramongomessilva.com.br/blog/how-to-make-videos-with-ai
- daisychain.tools, Drop 006: "Storyboard to animatic, with a scratch voiceover, in an afternoon" — https://www.daisychain.tools/drops/006
- mstudio.ai, "Script to Storyboard AI" — https://mstudio.ai/blog/storyboarding/script-to-storyboard-ai-2026 (vendor stats treated as lead-level)
- Kapwing, "How to Create a Character Reference Sheet With AI" — https://www.kapwing.com/resources/how-to-create-a-character-reference-sheet-with-ai/
- EZ Character, "Character Turnaround Sheet" — https://ezcharacter.com/turnaround-sheet
- invideo, "Multi-Angle Character Turnaround Sheet for AI Video" — https://invideo.io/faq/how-do-you-create-a-multi-angle-character-turnaround/
- 8frame, "AI Contact Sheet Storyboard: Nine Frames in One Image, Then Pick, Crop, Animate" — https://www.8frame.co/blog/shotgrid-contact-sheet-workflow
- ImagineArt docs, "Storyboard" node — https://docs.imagine.art/storyboard
- readray.ai, "Can you make storyboards in Midjourney?" — https://readray.ai/en/notes/ai-midjourney-20251111/midjourney-create-storyboards-ai-images
- topai.one, "First and Last Frame AI Video Guide (2026)" — https://topai.one/image-video/first-last-frame-ai-video/
- dreamdrive.ai, "Start and End Frames in AI Video: Which Platforms Support What" — https://www.dreamdrive.ai/learn/cross-platform/start-and-end-frames-which-ai-video-platforms/
- aipromptgeneer.com, "First Frame and Last Frame in AI Video" — https://aipromptgeneer.com/craft/first-frame-last-frame/
- hardeststories.com, "How to Keep Lighting, Color and Visual Style Consistent Across AI Clips" — https://hardeststories.com/keep-ai-video-style-consistent/
- Maosika, "AI Video Consistency Explained" — https://www.maosika.com/blog/ai-video-consistency-guide-2
- Ciaro Pro, "How to Use Reference Images for Consistent AI Video" — https://ciaro.pro/answers/reference-images-consistent-ai-video
- ScreenWeaver, "AI Series Production: A Consistent World Across Episodes" — https://www.screenweaver.ai/blog/ai-series-production-consistency
- wan27.org, "Wan 2.2 LoRA Training Guide" (single-practitioner; numbers lead-level) — https://wan27.org/blog/wan-2-2-lora-training-guide
- crepal.ai, "How to Use IC-LoRA in LTX 2.3: Identity-Consistent Video" (Ingredients reference-sheet IC-LoRA) — https://crepal.ai/blog/aivideo/ltx-2-3-ic-lora-guide/
- Stable Yogi, "Character LoRA from one image: Krea 2 and AI Toolkit" — https://stableyogi.com/blog/character-lora-from-one-image-krea-2
- adtestbench.com, "AI influencer LoRA: train one on your character, step by step" — https://adtestbench.com/guides/ai-influencer-lora/
