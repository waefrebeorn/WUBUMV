# Slopcannon toolset, SLERM-rebuilt on Muse tools

Stage reference for Engine v2. This is a rebuild, not a port.
Slopbot's toolset was studied for its *functions* — what each tool
is for, what it can and cannot do — and each function was rebuilt
from a tool Muse actually has. Nothing here copies Slopbot's UI,
credit system, branding, prompt format, or API shape, and nothing
here invents a Muse tool that does not exist. Where Muse has no
equivalent, the file says so, and the workflow routes around the
gap instead of pretending it closed.

Source of the functions being rebuilt:
`wubutv-network/musicvideo/slopcannon-learning/SLOPBOT_ANSWERS_2026-11-01.md`
(Q1–49 received; Q50–55 never arrived — still unknown, still not
invented). Unknowns from that file stay unknown here: model name,
tiers, frame rate, whether audio reaches the generation model,
rate limits, and backend approval locks. Do not fill them in.

## The one structural difference

Slopbot works through chat + a live project snapshot held by its
interface. Muse has no live project object and no endpoint for one.
WuBu's snapshot is therefore **the project record on disk, plus a
health report generated on demand from it**:

- Project record: `track.mp3`, `lyrics.txt`, `LYRIC_TIMELINE.md`,
  `ASSET_BOARD.md`, `MV_PREPRO_MV-<n>.md`, `POSE_CARDS.md`,
  vehicle files, `takes/`, `TAKE_HISTORY.md`,
  `VOLLEY_PROGRESS.md`, `CUTLIST.md`, `MUSIC_VIDEO_LEDGER.md`.
- Snapshot fields, rebuilt: a scene "has a playable take" means a
  QC-passed take row exists in `TAKE_HISTORY.md` with a file on
  disk and a matching md5 — not that a generation call returned.
  "Submission uncertain" means a file sits in `takes/` with no QC
  row, or a QC row points at a missing file. "Generation blockers"
  are: plan unapproved, a scene naming a bank row that does not
  exist, a failed gate still open, or the 6-video cap for this
  user message already spent.

A generation result is not a take in the project until it has been
renamed into `takes/`, fingerprinted, and logged. That is WuBu's
version of Slopbot's rule that a completed provider job can still
be unattached locally until recovered. Never claim a take exists
from a tool result alone.

## Muse tools actually investigated

Grouped by what they do in this engine, not by namespace name.
Only tools with a real job in the pipeline are listed as used;
the no-fit list at the end is part of the investigation, not an
oversight.

### Core state and measurement — the project memory
- `muse.exec` — shell work: ffmpeg trims and concatenations,
  ffprobe duration/frame checks, md5 fingerprints, `grep` searches
  over the project record, staged-file cleanup. This is the engine's
  hands for everything that is not generation.
- `muse.read` / `muse.write` / `muse.edit` — the project record
  itself. Every stage writes its gate result to a file before the
  next stage starts; chat history is never the memory.
- `muse.memory_search` / `muse.memory_get` — cross-project memory
  (standing rules, past decisions, a character's history). Never a
  substitute for reading the current project's files.
- `muse.visual_grounding` — locate/count objects in a frame still
  when a QC question needs exact positions or counts (a sign panel,
  a second mic, a glyph). A plain look at a frame answers plain
  questions; grounding is for when position or count is the verdict.
- `muse.create_options` — bounded user choices as tappable replies:
  plan approval, treatment-replacement review, reroll-vs-retire.
  One widget per message, alongside written text, never alone.
- `muse.session_status`, `muse.db` — diagnostics only, never
  pipeline steps.

### Generation — the only render tools
- `media.generate_video` — fire. Takes the vehicle text verbatim
  as its prompt. No audio input is accepted, no lipSyncMode
  parameter exists, no model/tiers/fps are exposed — so sync is
  produced by performance-window staging plus window-first cuts,
  exactly as Engine v2 already states. Cap: at most 6 videos per
  volley, including videos made by handed-off agents. That
  cap is WuBu's budget unit; there is no credit wallet to quote
  against, so never quote credits and never promise a refund.
- `media.generate_image` — reference variants and stills: a new
  bank image, a pose anchor still, a cover frame. It chains edits
  through a media handle, not through source IDs, so a variant is
  a newly generated image saved as a new bank row (see below).
- `media.generate_icon` — square product artwork only. Not a music
  video tool; not used for takes, references, or the corner bug
  (the bug is added in assembly, not generated).

### Research and reference grammar
- `browser.search` / `browser.open` — asset search and pop-culture
  mechanics research: find the mechanic, read the source, translate
  it into a WuBu-native row on the asset board. Mechanics only,
  never copied lines, characters, plots, or logos.
- `browser.deep_research` — only when the user asks for a deep
  dive; ordinary asset search does not need it.
- `browser.browse` — live website work only (a requested visit,
  a publish step through a site). It is not a research tool and
  not a video-analysis tool.
- `social.search` — public-post grammar when a mechanic lives on
  social video (edit rhythm, caption style). Fallback, not a
  primary source; platform CLIs own WuBu's own posts.

### Delegation and review
- `subagent.spawn` / `subagent.list` / `subagent.send` /
  `subagent.close` / `subagent.resume` — parallel, self-contained
  work: triple-devil's-advocate research, per-volley QC sampling,
  timeline measurement checks. Delegated videos count against the
  same 6-per-message cap, and a subagent never fires a browser
  task or builds an artifact on its own.
- `widget.create_html_widget` / `widget.create_list_widget` /
  `widget.present` — optional review surfaces: a QC board, a plan
  review sheet. Optional means optional: a widget never replaces
  the project files, and a plan is not approved because a widget
  rendered.
- `artifact.*` — durable deliverables the user keeps (a written
  plan document, a report). The music video master itself is
  delivered as a chat attachment, never as an artifact link.

### Scheduling and continuity
- `cron.*` — the MV kickstands only: `mv-kickstand-watch`
  (read-only) and `mv-kickstand-nag` (nudges after 6h idle).
  Kickstand jobs never fire, reroll, or edit a project.
- `tracking.*` / `user_goal.*` — the music-video goal's timeline
  and tracked commitments. Bookkeeping, not generation.

### Connectors (found via connector docs, used only where they fit)
- Threads / Instagram / Facebook CLIs — publishing finished
  episodes and masters, per their own connector docs. Publishing
  is a separate, human-gated step; it is not part of firing or QC.
- Everything else found (Gmail, Calendar, Drive, Spotify, Plaid,
  Shopify, Duffel, Ticketmaster, and the rest) has no job in a
  music video pipeline and is not dragged in.

### No-fit tools — investigated, deliberately not used
Shopping, wallet/payments, travel/hotel/flight booking, maps,
device commands, ads, feed/idea publishing, trash, and
permissions management do not map to any Slopbot function and do
not gain one by being listed here. Forcing them in would be
copying the shape of a toolset without its function.

## Function-by-function rebuild

### Probe tools (Slopbot's only directly callable tools)

**search_project_references(query) → file search over the bank**
Muse has no project-reference search tool. The rebuild is:
`muse.exec` with `grep` over `ASSET_BOARD.md`, `POSE_CARDS.md`,
and the plan rows, plus `muse.read` of the matching rows.
Binding is enforced, not suggested: before any vehicle fires,
its bank IDs are grepped against the board. A vehicle naming a
row that does not exist is a generation blocker, not a warning.
Max 9 bank IDs per scene; one pose card per scene; a style row
sets look only and is never a person, prop, or place.

**analyze_reference_video(url, focus) → frames + grammar notes
(partial rebuild, honestly labeled)**
Muse has no watch-a-video tool. The rebuild is: `browser.open`
or `browser.search` for the public page's own description and
grammar discussion, plus — for a video WuBu already holds locally
— `muse.exec` ffmpeg frame extraction and `muse.visual_grounding`
on the stills for camera, lighting, and edit grammar. What is
lost: a single call that watches and summarizes a stream. What
is kept: the function, which is to steal a camera/edit mechanic
and translate it, never to copy footage, a likeness, or a line.
Do not claim a video was "watched" when only its page and
extracted frames were read.

**inspect_project_health(reason) → the health check procedure**
Run on demand, and by the kickstand watch, from the files:
1. List `takes/` on disk; list take rows in `TAKE_HISTORY.md`;
   report files without rows (unattached) and rows without files
   (broken) separately. A completed generation that never got
   renamed, fingerprinted, and logged is unattached, not lost
   and not in the project.
2. Check every active take has a QC row; every failed gate has a
   named reroll axis or a plan rewrite; the volley count against
   the 6-per-message cap; the plan's approval state.
3. Report blockers, unattached takes, and the next volley owed —
   in that order. This report is WuBu's recovery panel. There is
   no "open credits," "resume whisper," or "open support" action
   to call; a support question goes to the user as a decision,
   not to a panel.

### Proposal tools (Slopbot's structured proposals, applied or reviewed)

**update_treatment → edit the treatment section of the plan/bank**
A first treatment is written directly into the project record.
A *replacement* treatment stays a reviewed proposal: show the
diff (old lines vs new lines) and get the user's choice through
`muse.create_options` before applying it. This preserves
Slopbot's asymmetry (creation applies, replacement is reviewed)
without inventing an interface lock.

**revise_scene / revise_scenes → edit plan rows + vehicle files**
Edit the row in `MV_PREPRO_MV-<n>.md` and write a new vehicle
version. Never edit a fired take's history row to match a new
plan; history is append-only. A revision changes scene text,
reference IDs, or SINGING/CUTAWAY tag — never the song times,
which belong to the timeline. Retiming a scene is a recut
(rebuilt `CUTLIST.md` from `LYRIC_TIMELINE.md`), not a scene edit,
matching Slopbot's rule that the agent cannot split, merge, or
retime a scene in place.

**assign_scene_references → edit the plan row's bank IDs**
Validated the same way as search: every assigned ID must exist
on the board, max 9, one pose card. Assigning a reference to a
later scene never edits the original bank row.

**generate_reference_image (≤4 source IDs, replace/retire flags)
→ media.generate_image, variant-as-new-row**
Muse's image tool does not take source IDs; it takes a prompt
and optionally a media handle for chaining. The rebuild: write
the variant prompt from the bank rows it derives from, generate
it, save it as a NEW bank row, and mark the old row
DEMOTED or KILLED in `ASSET_BOARD.md` — never overwrite the old
image or its row. "Replace + retire atomically" becomes:
new row created, old row retired, plan rows pointing at the old
row are re-pointed explicitly, all in the same edit pass, so no
scene is left pointing at a retired row.

**remove_reference → retire, never delete**
Mark the row KILLED in `ASSET_BOARD.md` and remove it from
future plan rows. Files and history rows stay; a removed
reference is unusable for new scenes, not erased from old takes.

**update_scene_words → edit LYRIC_TIMELINE.md, user correction wins**
A correction to a line's words or times edits the timeline row
and is tagged by confidence ([confirmed] measured,
[inferred] estimated, [assumed] user claim). Caption lyrics may
be fixed in the subtitle track without re-rendering, and a
caption fix never edits the timeline's timing.

**set_caption_lyrics / set_captions → subtitle track in assembly**
Captions are built in post from the timeline's word times, in
the chosen style, as a subtitle track. They are never described
in a vehicle, never burned into generated footage, and a caption
change never triggers a re-render.

**trim_project_media → ffmpeg trim to the true window**
Trim only on an explicit plan decision (a hold coverage, a
pickup inside a section). The song is never trimmed, stretched,
or retimed; takes are trimmed to windows, never the reverse.

**fire_generation (sceneIds, cleanForModeration) → media.generate_video,
volley manifest first**
State the volley manifest before firing: scenes, takes owed,
what each reroll fixes. Fire each vehicle verbatim, at most 6
videos per volley including delegated agents. There is no
`cleanForModeration` flag in Muse; moderation is WuBu's own QC
gates (G1–G6) run after generation, and a take that fails them
is kept, flagged, and never chained from. After every volley,
update `VOLLEY_PROGRESS.md` + `TAKE_HISTORY.md` before anything
else fires.

**project_recovery_action → health check + named recoveries**
- refresh status = re-run the health check from disk.
- recut to words = rebuild `CUTLIST.md` from `LYRIC_TIMELINE.md`.
- recover unattached takes = rename, fingerprint, log, then QC.
- open credits / resume whisper / recheck analysis internals:
  no Muse equivalent. Do not invent one. A credit question is
  answered with the 6-per-message cap and the volley manifest;
  a word-timing question is answered by re-measuring the track
  with ffprobe and re-reading the timeline.

### Human gates (Slopbot's, rebuilt on Muse's gates)
- Rights acceptance → Stage 0 rights question, logged in the
  project record before any render spend. Unanswered = blocked.
- Media upload → the user sends the track in chat (intake);
  Muse never pulls a track from elsewhere on its own.
- Spend → plan approval by scene number before any render, plus
  the 6-per-message cap stated in every volley manifest. No
  credit balance exists to check, so the manifest is the quote.
- Take deletion → refused by design: takes are retired, never
  deleted. Deleting a take would destroy provenance.
- Publishing → chat attachment delivery + `#wubu-mv-6a90e1`
  announcement for masters; platform publishing through the
  Threads/Instagram connectors is a separate user decision, not
  an assembly step.

## Scene model, as rebuilt
The scene is still the smallest editable unit: one plan row, one
vehicle, one set of takes. A scene may contain internal beats,
but Muse's generated take is one clip — internal [Shot N] timing
is direction inside the vehicle, not a frame-exact edit, and the
cut in assembly is made at scene boundaries from the timeline.
Scene length follows the word window (5–15s renders in Slopbot's
terms; Muse takes are ~10s by the generation tool, trimmed to
the true window in assembly — short lines are pickups, never
stretched). Lyrics are never copied into a vehicle prompt: the
vehicle names its line and its staging, and the timeline supplies
the timing. Lip-sync mode is tri-state in the plan tag, not in a
tool parameter: SINGING (named on-screen vocalist, mouth
established before the first word, restrained head, steady
camera), CUTAWAY/action (no vocal burden), and offscreen/insert
(voice offscreen, no mouth to read). Judged as vocal readability
and start/end closure, explicitly not phoneme-accurate.

## What Muse adds that Slopbot did not expose
- Measured QC: ffprobe + md5 + frame sampling replace eye-only
  review for timing, identity, and text gates, while keeping the
  human triage pass (worst + first + chorus + last scenes).
- Parallel QC and research through subagents, with the cap
  counted across all of them.
- A review surface (widget/artifact) when the user wants to see
  a plan or QC board, without making the surface the record.
- Kickstand continuity: hourly read-only watch + 6h-idle nudge,
  so a waiting project is never silently dropped.

## Hard stops for this toolset
- No invented endpoint, API, MCP server, credit balance, model
  name, tier, or frame rate. If a number is not in the project
  record or a tool result, it is not stated.
- No take in the cut without a QC row; no master with a failed
  gate open; no third reroll of the same vehicle.
- No generated audio as soundtrack or timing source; no
  peak-tween, no time-stretch of the song, in any form.
- No licensed material, no copied prompts, workflow files, or
  gallery images; mechanics only, SLERM-transformed.
- No use of the user as a relay to another agent's toolset:
  WuBu asks its own tools and its own docs directly.
