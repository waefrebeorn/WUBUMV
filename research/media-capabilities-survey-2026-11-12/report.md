# Media Capabilities Survey — how Muse's own image/video generation works, and what the outside world does with it

**Date:** 2026-11-12 ~03:20–03:45 EST
**Order:** Telegram msg 300 (2026-11-12 03:14 EST) — "focus on your capabilities like making images and video and how those work and online research any flags, usages, or muse agent sauce for yourself / improving the slopcannon and slerming is the way"
**Coordinator:** 2e9226ba (research only — no purchases, posts, commits, or Telegram writes)
**Scope:** Muse's own media tools (`media.generate_image` / `media.generate_video` / `media.generate_icon`), measured against the Slopcannon pipeline; plus Kevin Bacon online research on video-generation flags, prompting, and agent workflows.
**Read in full:** `video-api-mastery/SKILL.md`, `visual-mv-forms/SKILL.md`, `slopcannon/SKILL.md` (stages 0–7 + v5/v6 lessons), `~/docs/media.md`, `video-api-lab/VIDEO_API_AUDIT.md` + `IMAGE_REF_PLAYBOOK.md` + `TEST_LOG.md`, `slopcannon-learning/03-prompting.md`, self-tools survey §1a.

## 0. The one thing that did NOT happen (read this first)

**No probe videos were generated.** The `media.generate_video` tool contract carries a hard rule: *"When your task came from another agent, check that the task says how many videos you may make. If it does not, make none and say so in your result."* My brief authorized "small probes… few generations" but stated no number. I made **zero** videos and zero probe images, and I am saying so here as the tool requires.

The probes are NOT lost work: §2 specifies all five video probes + one image probe exactly (prompts, entry order, pass criteria, measurement procedure), ready to fire mechanically the moment the parent states a number (suggested: **5 videos + 1 image**). The rest of this report — the capability map, the measurement verification, and the online research — is complete and does not depend on the probes.

## 1. Capability map — what the tools actually are

### 1a. Tool schemas (read from the live catalog, 2026-11-12)

| Capability | What the schema says | Status vs video-api-mastery |
|---|---|---|
| `media.generate_video` | Ordered `{kind, value}` entries (text / local still-image path). Optional `name`, `output_dir`, `resume_from_snapshot_id`. **Max 6 videos per user message, successful calls only**; videos made by handed-off agents count toward the same 6; a task from another agent must state how many videos it may make or zero are made. No video-to-video input. **The prompt is handed to a specialized video subagent that "expands a short prompt into full video detail on its own"** — the vehicle text is NOT what the model sees verbatim; it is a seed for an expanding subagent. Results may include citations. | Extends the audit: the 6-cap, the expansion behavior, and the stated-number rule were not in the skill. |
| `media.generate_image` | Same entry structure; optional `resume_from_snapshot_id`, `output_format`, `style_preset` (only when a skill names one — none does for us). **Max 4 calls per response.** Prompt also expanded by a subagent ("expands short prompts into full detail itself"). Identity-reference labeling rules (profile photo / upload labels) are built in. | Extends the audit: 4-call cap, resume for images, expansion behavior. |
| `media.generate_icon` | **New capability, not in any skill yet.** Square icon artwork, fixed art direction (centered simple symbol, high contrast, no text unless requested), `surface` tailors it (space / podcast / discovery_pool / app / generic). One icon per call, ~1 min. Refine via `resume_from_snapshot_id` — **except surface=space icons, which return no snapshot_id and cannot be refined.** Use `media_handle` + `generate_image` when the result should stop being an icon. | Unused here. Plausible use: space/show artwork. Low priority. |
| Audio/TTS/podcast | NOT media functions — run through skills + the `tts` CLI. Rollout-gated. | Confirmed by docs/media.md. |
| Playback | **Cannot watch video or listen to audio playback.** Frames + transcription are the workarounds. | Already the standing QC doctrine. |
| Image search / reverse search | `image-search` skill exists for public image search. **Cannot reverse-search an image or identify people in photos.** | Already known. |

### 1b. Measured behavior (lab, 2026-11-06 — re-verified this survey, §3)

- Image input = **strong conditioner, not a frame source.** Frame 0 MAE 43.17 vs ref (cross-control ~111); character identity carries strongest; composition carries when aspect matches; prop singularity comes from the image; **exact hue does NOT reliably carry** (magenta → purple).
- **Duration and aspect obey plain text exactly:** "exactly 5 seconds" → 5.000s; no duration text → 10.000s default. "vertical 9:16 portrait" over a 3:2 ref → 720×1280. No aspect text + images → output adopts the images' aspect (3:2 → 1152×768). No aspect text + no image → 1280×720 default. All 24fps h264.
- **Two-image journey:** start-anchor → ~0.5s morph at 0.5–1.0s → invented middle scene → ~9s in the destination world. End anchor is the least exact (MAE 51.85 vs start 43.17).
- **Audio is always synthesized, never supplied.** Quoted speech is synthesized verbatim. With no audio instruction the outcome is a lottery (invented line at −19.8 dB vs near-silence at −32.4 dB). Always muted in assembly.
- **No numeric parameters exist** (no duration/aspect/fps/seed fields). No lip-sync parameter, no audio input, no video input.
- Lab budget: 5/5 calls succeeded first try, no refusals. Prompt lengths 45–80 words — **long-prompt behavior untested** (and Slopcannon vehicles run ~440–455 words, §4).

### 1c. Docs vs measurement — two conflicts, measurement wins both

1. `~/docs/media.md` says *"Each clip is about ten seconds long and that is not controllable."* **False on this tool:** the lab measured "exactly 5 seconds" → 5.000s. Text steering controls duration; the docs understate the tool.
2. `~/docs/media.md` says *"no preflight signal… Attempt it; the tool result is the only signal."* True — and it means the daily video budget (429) is discovered only by hitting it. There is no way to check budget before firing.

### 1d. What the outside API reveals about the same backend (useapi.net Muse API walkthrough, 2026-10-12)

- One POST = one image or one 10s video with spoken dialogue; **every file Muse makes is an asset id the next job takes as an input** (no re-upload) — the API-level version of `snapshot_id` / `media_handle` chaining.
- **Up to 9 images go into one image job** (`image_1`..`image_9`), prompt names them ("the woman from image_2…"). The agent tool's input-image limit is untested beyond 2 (video) — probe P2 tests 3.
- **Aspect phrasing matters:** "Cinematic 16:9 landscape photo" came back 3:2 (1920×1280); writing it as **"in exactly 16:9 aspect ratio"** fixed it. Our vehicles write "16:9" loosely — see ranked #4.
- **Error taxonomy:** `503` = worker glitched, nothing made, **retry the same prompt**; `403` = content refusal, change the prompt. A 503 costs nothing.
- **Costs (free plan, weekly allowance):** video 2–3% per clip (~30–50 videos/week), image 0–1%, uploads free. Video jobs took 68–138s each. **The binding constraint for us is the platform daily budget (429), not the weekly allowance.**
- **Narrated Short pattern:** script as JSON → three scenes at once → poll → join in one chat → fixed voice via TTS as `audio_1`. A format idea, not a pipeline change.
- Muse availability (Oct 30, 2026): US, Canada, Japan, Singapore. "Meta can switch off video for an account it sees used from elsewhere."

## 2. The probe pack — fully specified, ready to fire (blocked on a stated number)

Each probe is one call. Total: **5 videos + 1 image.** Parent must state the number (e.g. "you may make 5 videos") before any agent runs them.

**P0 (image, prerequisite for P2): refC.** `media.generate_image`, prompt: "Flat bold cartoon illustration, thick outlines, solid colours: a brass robot dog with a silver bell on its collar trots through a fern-filled forest clearing at dusk, fireflies, deep green and amber palette, 1920x1280." Output dir: `video-api-lab/refs/`, name `refC`. Measure: read it back (ref-poisoning check), record md5 + snapshot_id.

**P1 (video — resume chaining, THE test, playbook §7 exact).** `resume_from_snapshot_id = f8e32fdc-b667-4381-a632-243edb4d596f:844s3x` (V-03, pier ending). Single text entry: "The cat turns and walks back toward the camera, waving the brass key, lighthouse still behind it. Exactly 10 seconds, 16:9." No image resent. Measure: ffprobe duration/dims; extract frame 0; `measure.py` navy probe; MAE vs V-03 t9.7 frame. **PASS = frame 0 continues the pier (navy >50%, lighthouse visible, magenta ~0%) with no image resent.** FAIL = room/magenta return, or a fresh unrelated scene. Settles whether snapshot chaining can carry a scene across volleys.

**P2 (video — 3 images in one call).** Entries in order: text "This video starts at the first image, passes through the second image, and ends at the third image." → refA → text "The teal robot cat stands up from the rug, carrying the giant brass key, and the room transforms into the pier scene in the second image:" → refB → text "The cat walks the pier under the full moon and the scene becomes the forest clearing in the third image:" → refC → text "The brass robot dog trots through the fern-filled forest clearing at dusk among fireflies, still carrying the giant brass key. Flat bold cartoon illustration throughout. Exactly 10 seconds, 16:9." Measure: colour timeline (magenta / navy / green-amber) at 0/1/2.5/5/7.5/9.7s. **Question: does it visit all three worlds, or collapse to two?**

**P3 (video — style-only transfer).** Entries: image refA → text "A brass robot dog with a silver bell trots through a fern-filled forest clearing at dusk among fireflies, in the flat bold cartoon style of the reference image, thick outlines, solid colours. The dog is the only animal in the scene. Exactly 10 seconds, 16:9." Measure: frame 0/mid/late visual read + probes. **Question: does the cat leak in? Does the style carry to an unrelated subject?**

**P4 (video — duration other than 5/10s).** Text only: "A teal robot cat sits on a wooden pier at night under a full moon, slowly raising a giant brass key, flat bold cartoon illustration. Exactly 7 seconds, 16:9." Measure: ffprobe duration. **Question: does "exactly 7 seconds" return 7.000s, or snap to 5/10?**

**P5 (video — image-after-text ordering, single image).** Replicate V-01 exactly but text-first: text "Animate this scene, exactly 5 seconds, vertical 9:16 portrait orientation. The teal robot cat raises the giant brass key and says 'The key is mine!'" → image refA. Measure: frame-0 MAE vs refA. **Question: does ordering move the 82.51 MAE V-01 got image-first?**

## 3. Measurement-pipeline verification (done this survey, no generation)

Re-ran the lab harness on the existing files. **The audit numbers reproduce exactly:**
- ffprobe: V-01 720×1280 5.000s · V-02 1280×720 10.000s · V-03 1152×768 10.000s — identical to TEST_LOG.md.
- `measure.py` on V-03 frames: t0 magenta **24.38%**, teal 15.68%, green 6.37% — identical to the audit; t9.7 navy **68.56%** — identical. The probe harness is deterministic; the audit is verified, not just trusted.

## 4. The vehicle-length finding (the single biggest tension)

**Measured:** MV-14 vehicles run **439–455 words** (10 lines; e.g. S49 439 words, S47 455 words). The lab's test prompts were **45–80 words**. External guidance, everywhere, says short:
- slop.cc wiki (`slopcannon-learning/03-prompting.md`, the engine's own research base): "One readable event: Start with the subject and a visible verb" · "concentrate the motion prompt on what changes from that frame" (with an established starting frame) · "Avoid style adjectives that compete with the central action" · "Begin with one shot and one main event" · "Separate inputs: A starting image, a character reference, and a style reference serve different purposes. Label those roles in your production notes."
- Runway Gen-4 official guide (via UMAtechnology): "The Gen-4 model thrives on prompt simplicity" · "extensively repeating details already visible in the input image can reduce motion or produce unexpected results."
- Muse Video guide (getmusehelp.com): "One or two sentences is enough — long paragraphs do not help" · prompt formula **subject + action + place + camera + sound** · "small edits beat rewriting the whole prompt."
- AICraft: "Re-describing every visual detail can invite the video model to reinterpret the frame" · "protect the uploaded frame before it asks for movement… one camera move, one dominant subject action" + a prohibition block.
- Larund: "Once the frames fix the look, the prompt only needs to describe the path… Do not re-describe the subject in detail; contradictions between prompt and image invite the model to redraw."

**The gap:** Slopcannon vehicles bundle every role into one 440-word text — identity restatement + setting + hue locks + wordmark + camera + action + SFX + anti-text — and the video subagent then **expands that further** before the model sees it. The engine's own research base says to separate the roles and concentrate the text on what changes. The vehicles drifted long; the research never moved. This is not a guess about the model — it is a documented contradiction between Slopcannon's practice and its own sources, corroborated by every external guide found.

## 5. Online research — chains and lilypads

**Chain A — what flags do other tools expose that Muse's doesn't (gap analysis).**
- Runway Gen-4 (help.runwayml.com): input image **required**; first frame = input image; text "almost entirely focused on describing the desired motion"; **fixed seed**; 5/10s; 1000-char text limit; 24fps; **motion brush** (paint motion onto up to 5 regions); resolutions incl. 21:9; upscale to 4K post-generation.
- Runway API models (useapi.net): `veo-3.1` 4/6/8s **start + end frames**; `kling-3.0-pro` 5/10/15s **start + end**; `seedance-2` 4–15s start + end; `seedance-2-5` up to 30s with 50 references; `wan-3.0` up to 30s with image/video/audio references. **Sora 2 shut down Sept 24, 2026** — do not plan around it.
- Veo 3: 8s, **native audio** (SFX + spoken dialogue), Flow for chaining shots. Sora: Remix / Storyboard / Re-cut / Loop; 20s at 1080p (Pro).
- **Lilypads banked:** Runway Gen-4 prompting guide (motion-first text, fixed seed, motion brush) · Kling 3.0 start+end frames · Seedance 2.5 long-form (30s, 50 refs) · Veo 3 Flow chaining.

**Chain B — image-to-video prompting technique.**
- Larund (start/end frames): keyframes = control; "with only a start frame, the model controls the ending"; **keep the world identical between frames, change only what the shot is about** — otherwise "the model blends them into a warped morph"; "the bigger the difference… the more likely it is to cheat with a dissolve"; prompt only the path once frames fix the look; lens tokens (`&35mm`, `&low-angle`) pin the shot.
- AICraft: frame lock → subject lock → one camera move → one dominant action → secondary motion → **prohibition block** ("no morphing, duplicate objects, new text, camera shake"). **"Use the shortest duration that completes the shot's editorial job"** — longer generations drift more. Continuity between shots: record screen direction, camera height, lens, light direction, subject orientation, prop position.
- Agentbrisk 2026 guide: video prompts have 3 layers (action/change, camera behavior, …); **camera direction often matters more than action description**; seed reuse per tool (Sora seeds; Runway first-frame > seed matching; Kling character reference mode).
- **Lilypads banked:** Larund keyframe discipline · AICraft prohibition-block structure · Agentbrisk camera-first prompting.

**Chain C — Muse agent sauce (the same backend, from the outside).**
- useapi.net Muse API walkthrough (2026-10-12, read in full, §1d): asset-id chaining, 9-image jobs, aspect phrasing, 503/403 taxonomy, narrated-Short pattern. **The most directly applicable outside source found.**
- muse-video.app user guide: **"the editor does not expose a separate last-frame input for this model"** — Muse Video has NO last-frame input; our two-image interleaving is the only end-frame path, and it is implicit. References mode with `@` mentions (face from one image, outfit from another) — the agent tool has no equivalent naming; the workaround is describing the split in text (untested). Character references: portrait for face, full-body for clothing. Storyboards: break a clip into beats, name framing/action/sound per beat. Long-form: repeat character/lighting/location cues, join in editor.
- LumienAI (Oct 30, 2026): Muse launched Japan late Oct 2026; image up to 4 variations/request, conversational fine-tuning; video ~10s, scene stitching, auto background music; goal-setting + scheduled execution.
- **Lilypads banked:** useapi.net Muse API walkthrough (full) · muse-video.app user guide (References/@-mentions, no last-frame input).

**Chain D — the slop scene (what the music-video makers do now).**
- **obie/slopcore** (github.com/obie/slopcore): Claude Code skill + toolkit — Midjourney stills, Seedance clips, **every lyric drawn in code on the beat**. "Queso": 3:49, 93 shots, ~11 hours agent time, $309 Seedance. Pipeline: song analysis (beat grid + word times, confirm by ear) → storyboard (one shot per lyric line) → **prompt book + pilot (every clip prompt written by hand, then three test clips)**. Method follows anabology's BLISS/CLODYSSEY packages. **Lilypad: the repo's `PROMPTS.md` (101 clip prompts) is the prompt book to study for vehicle-writing style.**
- **NOVALYX "Slop Aipocalypse"** (novalyxcash.com, 3-min MV): Suno v4.5, Nano Banana Pro stills 2K/4K, Veo 3.1 Fast, Google Flow for face clips. "The canon lives in words, because an image model keeps no memory between prompts" — text canon for identity (same as our vehicle trait restatement). **14 sung windows, each with a start frame + a Veo prompt that times the mouth to the words.** "The character does not sign, there is no mimic of the lyrics in the video, sad about that" — **lip-sync is the scene-wide unsolved problem, same as ours.** Veo refused the first face start frame (content filter) — face clips via Flow.
- slop.cc news (Sep 2026): field guide to camera moves/light/styles (Sep 29); **"start from your own footage — upload a video and restyle it scene by scene"** (Sep 27) — video-to-video restyle, a gap: Muse's tool takes no video input.
- anchorterminal slopcore history: scene started Sept 2026 (Suno v6 + Opus 5.5); donaldjewkes single-prompt MV; anabology "ESCAPE VELOCITY"; Claudia open character (Oct 8) with making-of notes, MCP server, agent skill; SlopHits chart 144 → 620 videos/week by Oct 27.
- createmotion (donaldjewkes pattern): one long production prompt + ~20 visual references in a folder; agent reads every reference first; Magnific MCP with `account_balance` + `simulate_cost` before batches.
- **Lilypads banked:** obie/slopcore PROMPTS.md · NOVALYX start-frame-per-sung-window · slop.cc video-restyle (gap) · anabology BLISS/CLODYSSEY packages.

## 6. The four missing flags (and the Slopcannon workaround for each)

| Missing flag | What others have | What Muse's tool has instead | Slopcannon workaround today |
|---|---|---|---|
| Fixed seed | Runway, Sora, Kling (seed reuse = same character/world across clips) | Nothing — no seed field | **Snapshot resume (untested, P1)** + last-frame chaining (continuity method) |
| Negative prompt | Kling, Runway, most tools (separate field) | Nothing — prohibitions must live in the text | Prohibition block in vehicle text (ranked #3) |
| Last-frame / end-frame input | Kling 3.0 Pro, Veo 3.1 (explicit end frame) | **Nothing exposed** (muse-video.app: "does not expose a separate last-frame input") | Two-image interleaving (measured: 90% in destination world, front-loaded morph) |
| Video input / restyle | Sora (video in), slop.cc (restyle your footage) | Nothing — "video-to-video input is not supported" | None. A take can only be regenerated, never restyled. |

## 7. Ranked adoption list (top 5)

### #1 — Short motion-focused vehicles (A/B test against the 440-word vehicle)
- **Finding:** §4. Vehicles are ~6–10× longer than the tested range and than every guide recommends; the engine's own research base says motion-only text over an established frame.
- **Slopcannon change:** vehicle template v2 — the IMAGE carries appearance (bank/hue/wordmark stay as production notes + the ref itself); the TEXT carries motion only (one event, one camera move, one action, SFX note, prohibition block). A/B it on the next volley: same scene, long vs short vehicle; judge on QC gates + motion + identity drift, not vibes.
- **Blocker:** none — a template change + one volley. Needs the parent's go-ahead on the template rewrite (loop 1's skill-edit path).

### #2 — Run the resume-chaining probe (P1)
- **Finding:** `resume_from_snapshot_id` is the only continuation mechanism the tool offers, and it is the direct substitute for the fixed seed every other tool has. Untested since the lab (budget).
- **Slopcannon change:** if it carries the scene, the continuity method gains a no-resend chain (cheaper, less drift than re-sending last frames as images); if it doesn't, the two-image last-frame chain stays the method and resume is struck from the skill.
- **Blocker:** parent must state the video number (5 videos + 1 image for the full pack, or 1 video for P1 alone).

### #3 — Prohibition blocks as a standard vehicle footer
- **Finding:** AICraft's structure (frame lock → subject lock → one camera move → one action → prohibition block) maps directly onto the two failure modes that keep recurring: burned-in subtitles (G2, five failures) and prop multiplication (V-02's several keys).
- **Slopcannon change:** add a standard prohibitions line to every vehicle: "No on-screen text, no subtitles, no captions, no morphing, no duplicate props, no camera shake." The anti-text clause already exists; this generalizes it into a tested structure and covers the non-text failure modes too.
- **Blocker:** none — template addition.

### #4 — Standardize the aspect line to "in exactly 16:9 aspect ratio"
- **Finding:** useapi measured loose "16:9" returning 3:2 once; the exact phrasing fixed it. The lab measured exact compliance with "exactly 5 seconds" / "vertical 9:16 portrait" phrasing — the pattern is that exactness in the phrasing is what the text steering obeys.
- **Slopcannon change:** every vehicle carries the aspect line in the exact form "in exactly 16:9 aspect ratio (landscape)" instead of a bare "16:9".
- **Blocker:** none — one-line template change.

### #5 — Study obie/slopcore's prompt book + NOVALYX's start-frame-per-sung-window
- **Finding:** the slopcore repo's `PROMPTS.md` (101 Seedance prompts, hand-written, pilot-tested in threes) is the closest outside prompt book to our vehicles — and NOVALYX runs one start frame per sung window with a mouth-timing prompt, the same shape as our singing vehicles.
- **Slopcannon change:** read the prompt book, extract the vehicle-writing patterns (prompt length? motion focus? prohibition usage?), and fold the best ones into the vehicle template. Also: the "three test clips" pilot pattern is our chorus-hook test, already a gate — confirm it matches.
- **Blocker:** none — a reading task for loop 3 or the next research coordinator.

## 8. Single biggest Slopcannon change

**Rewrite the vehicle template around §4: image carries appearance, text carries motion.** The 440-word vehicle contradicts the engine's own prompting research and every external guide found; the short-vehicle A/B test is the cheapest experiment with the largest upside — if short vehicles hold identity as well as long ones (the image does that work anyway), every volley gets simpler vehicles, fewer re-descriptions for the model to trip over, and a direct attack on the subtitle/prop failure modes via the prohibition block. The template rewrite is loop 1's skill-edit path; the A/B test is one volley.

## 9. Honest limits

- **No probes ran** (§0) — P1–P5 are specified, not measured. Resume chaining, 3-image calls, style-only transfer, 7s duration, and image-after-text ordering are all still unproven on this tool.
- **The lab is n=1 per condition** (2026-11-06); the audit's qualitative gaps are large, but exact numbers are single draws. My re-verification (§3) confirms the harness is deterministic, not that the model is.
- **The video subagent expands prompts** — vehicle wording is a seed, not the literal model input. Any claim about "what the model was told" must account for the expansion layer, which is itself unmeasured.
- **Online claims are as-reported** (Runway docs, useapi.net, guides). Where a claim matters for a Slopcannon change, the ranked items cite the primary source; the lilypads are banked for follow-up reading, not verified by testing here.
- **Daily video budget (429) is the binding constraint**, not the weekly allowance. Probes compete with volleys for the same budget — schedule them when no volley is owed.
- `media.generate_icon` is untested here; the space-artwork use is a guess, not a measured fit.
