# Slopcannon Engine v2 — song in, music video out

Rebuilt from square one 2026-11-01 from the aggregated research
(`wubutv-network/musicvideo/notes/SLOPCANNON_AGGREGATED_RESEARCH_2026-11-01.md`).
Learning library (fresh slop.cc scrapes, 2026-11-01):
`wubutv-network/musicvideo/slopcannon-learning/` — read file 08 there
before claiming any Slopcannon behavior for WuBu's tool.
Toolset (Slopbot's functions rebuilt on Muse tools, 2026-11-01):
`references/toolset.md` — read it before claiming a tool exists,
quoting a credit balance, or promising a recovery action Muse has
no equivalent for.
This version supersedes the patched v1 skill outright: the old cheap
peak-tween assembly stage is gone, the uniform scene grid is gone, and
every stage now has an exit gate. Nothing from v1's wording survives
except what re-earned its place here.

Built from scratch with WuBuTV tools. Never copy another workstation's
UI, credit system, branding, or prompt format. The public workflow shape
is song in and timed video out. Everything else here is WuBuTV native.

## The one rule above all stages

The song is the timing authority. The story, the cuts, and the captions
follow the song, never the other way around. The user's track is muxed
untouched as the sole master audio; generated audio is dropped, never a
soundtrack and never a timing source. "Untouched" means content and
timing — the CODEC is a delivery law: an MP4 master's audio stream is
AAC (48 kHz stereo, ~192k) with faststart, exactly like every shipped
MV master. NEVER stream-copy an MP3 track into an MP4: ffmpeg decodes
it fine (so a PCM-identity gate passes), but phone players render the
file silent — this exact bug shipped on MV-2 (2026-11-02) and again on
MV-6 (2026-11-06). The master gate must ffprobe the audio codec, not
just decode the audio.

The VIDEO encode is also a house format: libx264 preset medium,
**CRF 18**, yuv420p, 1280×720, 24 fps (x264 core 164 SEI options must
read crf=18.0). Every shipped master — MV-2 v6, MV-3 corrected, MV-4,
MV-5 v4 — is CRF 18. MV-6 first shipped at CRF 15 (5.06 Mbps, 150 MB)
and the user's phone would not load or play it (2026-11-06); the
CRF-18 re-encode (111 MB) is the shipped master. The delivery gate
reads the x264 SEI from the delivered file, not the encode command.

## Companion skills (the mondo set, 2026-11-06)

This engine governs every MV build. Two companion skills carry the
measured knowledge it leans on — read them where they apply:
`~/workspace/custom-skills/video-api-mastery/SKILL.md` (measured
behavior of the generator itself: image refs are strong conditioners,
never frame sources; character identity is the strongest carrier;
duration/aspect steer exactly by text; audio is always synthesized —
before any generation call using image refs, a specific duration or
aspect, or multiple images) and
`~/workspace/custom-skills/visual-mv-forms/SKILL.md` (visual-first
forms beyond singing — kinetic typography, visualizers, montage,
graphic systems, stills in motion, code-rendered graphics, countdown
forms — for structural slots, rap/bridge sections, instrumentals, and
hooks; kinetic type/graphics are an ASSEMBLY layer in post, never
generated in-clip text). One-page map of the whole set:
`wubutv-network/musicvideo/MONDO_INDEX.md`. Where a companion skill
and this engine disagree, this engine governs.

## WORD-SYNC (2026-11-04, user standard) — the whole game

Word sync is not a QC extra; it is the assembly itself. Every word on
screen is synced to the word in the song, by conversion math:

- MEASURE BOTH SIDES: the song's word times come from LYRIC_TIMELINE.md /
SONG_WORDS.json (measured, never the sheet where performance differs).
Each take's sung word times come from transcribing the take's own
generated audio with word timestamps. Slot alignment is not word
alignment: a take placed by its window while its words sit elsewhere
in that window is NOT synced, and never ships as sync.
- CONVERT, THEN PLACE: for every sung word, compute offset (take word
time minus song word time) and pace drift (first-word vs last-word
offset). Shift and warp the picture so the take's words land on the
song's words. Warp the picture, never the song.
- PER-WORD TIME WARPING IS THE METHOD (user law 2026-11-06): anchor
every word. Warp the interval between each pair of word anchors —
each take word is time-warped individually so it lands on its song
word — instead of relying on one uniform warp per scene or line.
SPEEDING UP is fine, including hard squeezes (disclose extremes in
the assembly notes). SLOWING DOWN is the capped direction: never
slow any interval past 2x slow (playback speed below 0.5x) — past
that the picture visibly degrades. A slot whose words cannot land
inside those bounds is structural: montage or cover, never a >2x
slow stretch. Gates re-run on the warped output.
- V4 CORRECTION (2026-11-06, earned on MV-5 v3's rejection — this
amends how the per-word law above is APPLIED): per-word data PLACES
phrases; it does not chop words. The warp actually applied is
PHRASE-LEVEL AND SMOOTH — one factor (or one linear ramp) per sung
phrase, never per-word setpts steps inside a phrase. Per-word
stepping lurches the playback speed at every word boundary and
reads on screen as jarring jumps even when every word "lands."
Anchors are VISIBLE MOUTH EVENTS in the take, not the take's audio
words: audio-word warping preserves the mouth lag (~0.5–1s inside
some takes) that the mouth-lag caution below warns about. Every
hook/refrain occurrence gets its OWN mouth-verified anchor — hooks
are the weakest anchors in the song (ASR may hear the hook word
zero times) and must never ride inferred or neighbouring anchors.
The master gate READS MOUTH STATE at every line onset AND every
hook onset (open / transitional-open / closed, at onset and +0.15s);
any hook onset closed is a GATE FAIL. Placement evidence (pixel-diff
frame matching) is NOT a sync gate: donor/cover frames sitting on an
onset pass placement while the singer's mouth is shut. If a phrase's
smooth warp cannot fit inside the caps, swap to another existing
KEEP take; if none fits, flag the slot STRUCTURAL and take the
least-bad smooth warp, disclosed. A hook that cannot land
open-mouthed at a phrase edge gets the sanctioned bad-word
treatment: beat-cut to montage for exactly that hook, back at the
next good anchor. Insert candidates chosen to fix an onset must be
verified from FULL-RES candidate strips — tile/contact scans of
take tails are unreliable and land inserts on calm frames.
Proven on MV-5 v4 (2026-11-06): hooks 6/30 open (v3) → 29/29
open-or-transitional; in-phrase judder steps 89 → 0.
- SWING KEYFRAMES + BAD-WORD MONTAGE CUTS (user law 2026-11-06):
the per-word warp is built from SWING KEYFRAMES measured off the
take's own generated audio. Transcribe every take per word; each
word's offset (take word start − song word start) and the drift to
the next word form the swing curve, and the keyframes sit on the
words themselves — warp interval by interval between keyframes so
the take's timing swings land on the song's. Compare against the
BEAT MIX: measure the song's beat grid (tempo, beat times,
downbeats) and use it as the hint layer — montage cuts land ON
beats, return cuts land ON word onsets, accents land on stressed
words. When a take MESSES UP a word (wrong word, missing word,
repeated word, or an interval that cannot land inside the warp
caps), that word span is BAD: never warp it into place, never
freeze it — FAST CUT on the nearest beat to montage/B-roll for
exactly that span, then cut BACK to the lipsync take (or the
alternate proper take for that line) at the next good word anchor.
A bad word is the sanctioned exception to sustained lyrical
cutting: out for the bad span only, back on the next good word.
Caution (earned 2026-11-02): take audio words are HINTS — they can
lead the visible mouth by up to ~1s inside a take; if the master
gate shows a consistent mouth lag for a scene, shift that scene's
keyframes by the measured mouth offset. Tooling: work/swing/
per project (beat_grid.json, swing_keyframes.py, SWING_METHOD.md).
- WARP, NEVER FREEZE: gaps are covered by bounded time-warp and by
moving picture. A still frame during words is a fail, not coverage.
Slow drift is motion; a repeated frame is a freeze.
- MONTAGE IS MATERIAL: where no take syncs, cutaway / B-roll /
reaction / dead footage edited to the music is legitimate picture —
edited together into a good music video, not a failure to hide. A
cover slot gets a QC row flagged "not a mouth-sung slot" with its
caption still keyed to song word times; the audience hears the word
while the picture looks elsewhere.
- GATE ON THE MASTER: before delivery, word-match-check the finished
master itself — sampled sung words across the song, mouth/cut/caption
against song word times. "Roughly occupying the window" no longer
ships. What ships is measured word placement, or disclosed cover.
This claims measured placement, not phoneme-accurate generation.
- SNAPPER ERROR MODEL (2026-11-13, loop 6 measured): mix-snap anchors
are accompaniment-locked, not voice onsets. A stem-snap on the same
words differs by a median 32–48 ms, agreeing within one 16 ms STFT
frame on only 69–73 of 212 words — the stem lattice is not the mix
lattice. Never use a mix-snap position as voice-onset ground truth;
a snapper position is an anchor, not a measurement of when the voice
starts.
- F0 SOURCE RULE (2026-11-13, loops 5–6): never use a saved pYIN
track's f0_hz as "the voice's F0" without a pinning audit. Sprint 8's
saved tracks are NOT voice-F0 tracks: the mix track is pinned at the
50 Hz floor on 81% of voiced frames, the stem track pinned at the
800 Hz ceiling on 63%. The correct source until RMVPE-on-stem
replaces it is stem autocorrelation (median F0 238.8 Hz on the
measured track). Any F0 claim from a pinned track is withdrawn, not
cited.
- MOUTH-OPENNESS RULE (2026-11-13, loop 6 CCA): the visual feature
for mouth motion is mouth OPENNESS (lip distance), never raw
frame-diff in a mouth box. Frame-diff in a mouth box correlated
with shuffled controls at r 0.93 — above the true mouth signal at
r 0.698 — so it cannot separate mouth motion from any other motion.
Any AV-sync or mouth-gate measurement built on frame-diff is invalid
until re-run on openness.
- SINGER-CUT DISCIPLINE (2026-11-13, taste research — the MV-5
verdict, "cat talking when she is"): inside a sung phrase, the ONLY
legal singer change is at a phrase boundary, and it is reached via
look → cut → reaction: the outgoing shot ends on a look, a breath,
or the other singer's reaction — never a hard cut from one open
mouth to another open mouth mid-phrase. A singer change mid-phrase,
or a cut to a closed or wrong mouth under a sung line, is a
MOUTH-LIE CUT — a named G6 GATE FAIL, not a disclosed nit. For
alternating lines (MV-5 bridge, GIRL-first), the plan writes the
listener's reaction as its own planned slot in the vehicle — the
listener's face is a planned shot, not assembly salvage.

## CONTINUITY METHOD (2026-11-10, user law — the MV-11 rejection rebuild)

MV-11 v1 passed every internal gate and was rejected on playback: "the same image and then some 4 seconds of splash gen." The failure was structural, not a bad take: every take opened on the same anchor still, held, burst, and stopped — stop-start flow. The method below replaces the anchor-still workflow on every build from now on. It is a generation method, not an assembly fix: continuity is made at fire time.

- LAST FRAME → FIRST FRAME CHAINING. Take N+1 is generated with take N's last frame as its first image reference (two-image call: first image = previous take's last frame, second image = the scene's own reference). Each take starts exactly where the last one ended. NEW FIRST FRAMES ARE ALLOWED for cuts: when a cut needs a fresh start (new angle, new setting, new scene), generate a new first frame for it — the rule exists to have MORE CONTINUITY, not to forbid new starts. A fresh first frame must still line up with the outgoing frame's world (same lighting, framing, and subject position) so the joint doesn't jump; a new start that breaks the world is a continuity fail, same as a broken chain. Never chain from a rejected take; a chain break (a rejected or unusable take) restarts the chain from the last good take's last frame.
- RESUME CHAINING (2026-11-13, probe P1 measured). `resume_from_snapshot_id` carries the scene into a new clip with no image resent: one short text entry on the prior clip's snapshot id continued the scene (frame-0 MAE 45.24 vs the resumed ending, same snapshot base id, new suffix). Resume is the first-choice chain for continuations; the two-image last-frame chain stays the fallback for fresh starts (resume needs a prior snapshot).
- AUTOGENERATED IMAGE-REFERENCE STACK, PER PROJECT. At plan time, generate the project's own reference stack: one start/end reference pair per scene, built from the project's own material (its style lock, its KEEP takes, its anchor stills) — never one anchor still reused across scenes. The stack is a project file (REFERENCE_STACK.md + work/stills/stack/), written before volley 1, and every vehicle names the stack frames it uses.
- TIME THE PROMPTS FROM THE MUSIC. Prompt timing comes from the measured track: beat grid, onset times, word times (LYRIC_TIMELINE.md / SONG_WORDS.json). Each prompt carries its motion beats keyed to the song's own events (brass stabs, word onsets, downbeats) — never a generic "then it moves."
- PLAN A FULL 10 SECONDS OF PROMPT. Every 10s take gets motion planned across the whole duration: what moves in seconds 0–3, 3–7, 7–10, keyed to the song. A prompt that only describes an opening image and hopes for the rest is not a vehicle. Empty motion (a held frame with nothing moving) is cut at assembly — the take's usable span is its in-motion span.
- EDIT USING IN-MOTION SHOTS. Assembly cuts land only on frames already in motion (measured frame-diff above the scene's live baseline at the cut frame). Cuts never land on a still, a hold, or an anchor-still head: trim every take's anchor-still head before it enters the cut. A cut that lands on a still is a QC fail.
- STOP-START FLOW IS A QC FAIL. A take that reads still → burst → still, or a master that reads stop-start across joints, fails G6 even if every word lands. Continuity is checked at the joints: the last frame of take N and the first frame of take N+1 must match in framing, lighting, and subject position (frame-diff + eye read) before the joint ships.

## The project record (the engine's memory)

Chat history is never the project memory. Each project lives under
`~/workspace/wubutv-network/musicvideo/<slug>/` and its state is a set of
files, not a transcript. Every stage reads the record and writes its own
gate result before the next stage starts:

- `track.mp3` (+ `track.mp4` if supplied) — the delivered master, fingerprinted (md5), never overwritten or re-encoded.
- `lyrics.txt` — verbatim, the text of record.
- `LYRIC_TIMELINE.md` — measured section boundaries + per-line start/end times (see references/timeline.md).
- `ASSET_BOARD.md` — per-section search context + KEPT/DEMOTED/KILLED rows (see references/asset-search.md).
- `MV_PREPRO_MV-<n>.md` — the plan: one machine-readable row per scene (see references/direct.md).
- `POSE_CARDS.md` — one pose card per signature pose (see references/pose-reference.md).
- Vehicle files `mv<n>_s<kk>_vehicle[_v<n>].txt` — the full prompt per scene, written before firing.
- `takes/mv<n>_s<kk>_t<t>.mp4` — every take kept, including rejected takes, with md5.
- `TAKE_HISTORY.md` + `VOLLEY_PROGRESS.md` — fired scenes, active takes, flagged scenes with their reroll axis, scenes still to fire.
- `CUTLIST.md` — active take per scene + trim points.
- `MUSIC_VIDEO_LEDGER.md` — masters + provenance manifest (scene/take/QC/rights per master).

Name a project `MV-<n> "<Title>"`. Music videos take their own numbers
and never take bumper, episode, or commercial numbers.

## The eight stages (in order, each gated)

### 0. Receipt (intake)
Read references/intake.md. Copy the track, record its md5, log the
receipt, keep the lyrics verbatim, measure duration with ffprobe. Ask
the rights question once: does the user own or hold licence for this
track, and are the characters original? Log the answer in the project
record. Never send a track back for a timing miss. Defaults unless the
user overrides per track: full song, WuBuTV cast performing in the
world of the song. FORMAT RULE (user, 2026-11-05 01:31 EST, standing):
ONE 16:9 master only — no 9:16 reel, no chat copy. Fast and best.

### 1. Timeline (measure, never guess)
Read references/timeline.md. Build LYRIC_TIMELINE.md from the delivered
track before any scene is planned: section boundaries, per-line times,
confidence tags ([confirmed] measured, [inferred] section label or
bracket estimate, [assumed] user claim). GATE: no plan may be drafted
from a uniform grid or from timings measured against a different master.
If the track is re-delivered, the timeline is re-measured; the old grid
is void.

### 2. Bank (lock the look before spending a frame)
Read references/asset-search.md and references/pose-reference.md. Build
ASSET_BOARD.md (one row per scene: archetype, motif, pop-culture
mechanic + its WuBu-native SLERM translation, first/last/new/transition
slots, KEPT/DEMOTED/KILLED) and POSE_CARDS.md. Identity is selected
from the bank per scene, never re-described in prose. Story changes
become variants assigned only to later scenes, never edits to the
original. SFW poses only; never copy a gallery image, prompt, or
workflow file. GATE: no vehicle may name a character, outfit, prop, or
place that has no bank row.

### 3. Plan (the contract)
Read references/direct.md. Write MV_PREPRO from the timeline: one row
per scene in song order with number, song in/out, lyric lines covered,
SINGING or CUTAWAY tag, setting, characters + bank references, one
beat, one camera move, motif callback, transition. The plan must pass the banger test as a gate
(2026-11-13, taste research — this replaces the old "hook in the
first 0.5–3 s" wording). FRAME 0 IS THE PEAK IMAGE: carry element +
a motion event + an open mouth if the intro is sung — no leader, no
establishing still, no cloned pre-word frames. The FIRST CUT lands
at ≤2.5 s, on the first downbeat or first word onset, whichever is
first. The intro passes a MUTED 3-SECOND TEST at QC: motion visible,
carry element visible, mouth open if sung. A plan whose S01 vehicle
describes a settle, a zoom-in, or "the scene opens" fails this gate.
The plan carries a PER-SECTION ENERGY ARC in cuts/minute, measured
at plan time: verse 12–20, pre-chorus ramp 20→40, chorus 40–66,
bridge 15–25 (a texture break — location, colour, speed, or one
unbroken take; never just more of the same faster), outro 10–15.
The FINAL CHORUS is the densest section (≥1.5× verse density) and
holds the visual peak. Never cut on every beat for a whole section —
vary on-beat/off-beat; hold a shot across bars to build tension,
then snap back. The plan NAMES, per section, the tension (what
tightens) and the release (what lets go); a section with no named
tension/release is an unplanned section. One repeatable motif
returning at least 3 times, bridge contrast, final frame rhyming
with the first. Short lines (~2–3 s) are pickups inside longer
sections, never stretched to a full scene; long holds get an explicit
coverage decision. CHORUS-HOOK TEST (cheap proof before full spend):
the first volley leads with the hook scene; if its QC fails the plan's
look, fix the plan before firing the rest — never fire a whole song on
an unproven look. GATE: the user approves the plan by scene number
before any render spend; proposals are diffs to plan rows, not prose.

### 4. Fire (volleys, capped, one variable per reroll)
Read references/fire.md and references/performance-window.md. Write
each scene's vehicle before firing it, then fire the vehicle verbatim.
At most 6 videos per volley, including videos made by handed-off
agents — that cap is the budget unit, and the volley manifest (scenes,
takes owed, what each fixes) is stated before firing. Volleys proceed
autonomously on standing authorization ("always fire, never ask", user
2026-11-03, re-asserted 2026-11-05 ~02:45 EST) — the cap is a batching
limit, never a user-interaction gate: never present a volley as waiting
on, triggered by, or "firing on" the user's message, and never beg for
interaction to continue. SINGING vehicles
follow performance-window staging: the vehicle names its line, the
singer is (facing camera; static, MCU-or-closer) during the line, all
gesture and camera movement strictly before the first word or after
the last word. Reroll only the scenes that missed, one named axis per
reroll (facing, delivery, staging, text, wordmark, style), changing
exactly one variable. After two denied rerolls a scene retires: fresh
staging drafted from scratch, never a third reroll of the same vehicle.
Keep every take; never chain from a rejected take; never auto-pick the
newest. GATE: after every volley, VOLLEY_PROGRESS.md + TAKE_HISTORY.md
are updated before anything else is fired.

### 5. QC (scored gates, triage, no silent passes)
Read references/qc.md. Every take is scored against named gates
(G1 character consistency, G2 zero unwanted on-screen text, G3 no
licensed material, G4 performance-window for SINGING scenes, G5
audio-sync placement, G6 banger check on the plan) with pass/flag/fail
per scene and confidence tags. A failed gate is a reroll reason or a
plan rewrite, never a note. TRIAGE: the reviewer (agent + user) looks
at only the worst scenes + first, chorus, and last scenes; the rest
auto-advance with their best take, logged. When two reads disagree,
widen the sample instead of picking one. GATE: no take enters the cut
without a QC row; no master assembles with a failed gate open.
G6 COUNTED RULES + FEEL TRIAGE (2026-11-13, taste research — the
"gates passed, master still wrong" class ends here): (a) no single
vantage held >10 s without a cutaway; (b) every montage span ≥5 s
contains ≥3 distinct collision types per 10 s (scale change, angle
change, world/location change, graphic match, action match,
light/tone flip) — metric-only cutting (uniform shot lengths
regardless of content) FAILS G6; (c) a MOUTH-LIE CUT (singer change
mid-phrase, or a cut to a closed/wrong mouth under a sung line —
see WORD-SYNC singer-cut discipline) FAILS G6; (d) RULE-OF-SIX
TRIAGE READ, per section, by a named reader: score emotion, story
(new information per cut), and rhythm (tension→release, not flat)
1–5 each; ANY section scoring ≤2 on emotion FAILS G6 even if every
numeric gate passes (named failure mode: "MV-5 class"); (e)
GRAIN-TOGGLE TEST on the master: toggle the post grain pass off —
if the frame does not suddenly look plastic, the grain is too light
or absent (see the vehicle LOOK BLOCK).

### 6. Assembly (window-first section-timing)
Read references/assemble.md. QC-passed takes only, trimmed to their
true lyric windows with uniform fit per scene, cuts on line/section
boundaries. WORD-SYNC standard applies: place by measured word times
(take word timestamps vs song word times), warp within caps, montage
cover where no take syncs. NO peak warp, NO time-stretch of the song, NO stretching
a short line to a scene. Suno track sole master audio. Captions in post
as a subtitle track, never burned into footage. `~ WuBu ~` corner bug.
ONE 16:9 master only (standing rule 2026-11-05 — no 9:16 reframe, no
chat copy). ffprobe + md5
verification, CUTLIST.md + MUSIC_VIDEO_LEDGER.md written. GATE: master
boundaries equal lyric times; spot-check frames at line starts.
HEAD/TAIL TRIM LAW (2026-11-13, taste research): no take enters the
cut with >0.5 s of pre-action settle — scene in-point = the latest
of (first frame with frame-diff above the scene's live baseline,
first mouth event −0.25 s); scene out-point = the last motion frame
+ ≤0.3 s; a tail settle longer than 12 frames is trimmed, not
shipped. Where a take's mouth LAGS its own audio (MV-10 class,
0.5–1.4 s), trim the lag out and place the mouth event on the song
onset — do not warp the lag into place and do not ship it as a
disclosed nit; if trimming breaks the warp caps, the slot goes to
montage (bad-word rule). PICTURE LEADS THE BEAT: at every SECTION
boundary the incoming shot's first frame lands 2–6 frames BEFORE
the downbeat (verify on the master: section-boundary cuts sit in
[−6f, −2f] relative to the downbeat); at every PHRASE end the
outgoing singer's reaction holds 0.3–0.5 s into the next phrase
before the cut. MOTION MATCH AT EVERY JOINT (extends the CONTINUITY
METHOD joint check from static to motion): every cut lands 2–4
frames BEFORE a motion peak inside the outgoing take, never on a
settle; the incoming take's first 6 frames contain motion in the
same screen direction or a matched shape/position (graphic match),
verified by frame-diff + eye read; a joint where outgoing motion is
~0 is a QC fail even if the frames match statically. Vehicles
therefore name their exit motion ("ends mid-reach / mid-turn /
mid-crest") so assembly has motion to cut on.

### 7. Delivery + provenance
Deliver the master in chat as an attachment, never as a bare link.
CHAT SIZE RULE (user order 2026-11-06): a chat-sent master must be 50 MB or
under. If the house master exceeds that, send a bitrate-capped delivery
encode of the same cut (video only; the AAC audio stream is copied
untouched, faststart on) and say so plainly — the CRF-18 house master stays
the canonical master on disk and on the CDN.
Announce it to `#wubu-mv-6a90e1` like every other delivery. The
delivery message discloses flags and the honest lipsync limit: this
pipeline maximizes the plausibility of mouth motion against the master
— it has no audio-conditioned generation and must not claim
phoneme-accurate lipsync. The provenance manifest (scene/take/QC/rights
per master) ships in the project record. The MV kickstand jobs read
VOLLEY_PROGRESS.md: mv-kickstand-watch (hourly, read-only) and
mv-kickstand-nag (hourly, nudges only when a project has waited over
6 hours on the user). Kickstand jobs never fire, reroll, or edit a
project — volleys proceed autonomously on standing authorization; they
never wait on the user's message.

## MV-2 v5 proof (2026-11-02) — the timed-pipeline lessons, earned the hard way

MV-2 "Toll Roads Are Dumb" v5 is the proof cut: every take anchors only
to its own vehicle's line, at that line's own song position, in order.
It supersedes v3 (disputed sync) and v4 (Whisper-LCS matching, wrong
chorus occurrence, noise-merge anchor drops). Apply these on every
future build; they are gates, not notes:

- Prompt-grounded anchoring: the vehicle prompt (BEAT line) is the ground
  truth for what a take sings. A take anchors only to its own prompted
  line, at that line's song position. No cross-line matching, no
  noise-merge dropping of anchors, no shifting a first anchor to a
  visible open mouth — word identity outranks open-mouth state.
- Validate anchor-table indexing before building: anchor indices must be
  raw `take_words` indices, not filler-excluded numbering (v5 caught
  S16/S17/S18 written in filler-excluded numbering and fixed them).
- Never format a possibly-None timeline value in a flag/log line: the
  S21 zero-duration Whisper burst (song words 333–338 all at 205.20)
  crashed the first v5 build on exactly that.
- Freeze frames are selected by frame index, never by time +
  `end_frame=1`: `end_frame` is an absolute stream frame number, so the
  old form selected nothing and the first v5 render lost ~11.8s, shipping
  256.21s of video against 268.01s of audio.
- Enforce exact frame counts per segment before concat: each warped
  segment renders 1–3 frames long from fps-after-concat rounding, and
  that accumulates — the second v5 render drifted +0.99s by the tail
  (S26 vocal 1.05s late; a master frame at song 257.97 showed postvocal,
  mouth closed). Fix: force every intermediate to `round(span*24)`
  frames (trim tail / clone last frame), then re-concat. After the fix
  every vocal start sat within 0.062s of its song position.
- Verify the master the way v5 was verified, never from the cutlist
  alone: real video-stream duration + frame count, per-clip durations
  against cutlist spans, cumulative drift, AND frames pulled from the
  master itself at song word times (scene identity + facing + mouth).
  A cutlist's intended spans are not proof — two v5 renders proved it.
- Disclose the honest limit at delivery: v5 fixes WHICH words are on
  screen WHEN, at frame accuracy. It does not claim phoneme-perfect
  mouths — the generator's mouth lags its own take audio inside takes.

## MV-2 v6 time-ratio rule (2026-11-02) — v5 REJECTED by the user

v5 passed internal word-frame checks and was still rejected on
playback: words with no video covering them, frozen motion, and halted
moments from too-slow time splices. The audit of CUTLIST_V5.json
proved the mechanism, so this rule supersedes v5's warp/freeze modes:

- v5's numbers: 49.56 s of the 268.01 s master is frozen picture
  (36.72 s of pure freeze segments + 12.84 s frozen inside warped
  intervals via the >2.5x freeze branch) — 18.5% still image. Of 270
  warped word intervals, only 68 sit near natural speed (0.80–1.25x);
  74 are slowed 1.25–2.5x, 83 sped 0.4–0.8x, 32 squeezed below 0.4x,
  13 frozen outright. Frame-accurate word placement is worthless if
  the picture between the frames does not move at natural speed.
- TIME RATIO IS A GENERATION CRITERION, NOT AN ASSEMBLY FIX. For each
  candidate take, measure its prompted line against the song line it
  must cover: line ratio = song line duration / take line duration
  (first word onset to last word end, both sides). A take is usable
  only if its line ratio sits in 0.80–1.25 AND its word intervals do
  not need warping outside that band to land. Assembly may trim and
  cut on word boundaries; it may NOT setpts-warp a word interval
  outside 0.80–1.25x, may NOT freeze a frame while words are playing,
  and may NOT stretch, squeeze, or slow a mouth to fit.
- REROLL FOR RATIO. A take outside the band is a generation miss,
  not an assembly problem: reroll it with PACING as the named axis —
  prompt the line faster or slower to match the song slot, shorten or
  split the vehicle line so one take covers what fits the slot, or
  restage the scene around a shorter line. One variable per reroll,
  same volley cap (6 per volley), same two-denied-rerolls
  retirement. Worst v5 offenders, reroll first: S13 (0.34x — a 5.40 s
  take squeezed onto a 1.82 s song line), S23 (0.42x), S10 (0.46x),
  S05 (0.47x), S16 (0.51x), S06/R1 (1.49x/1.81x — stretched, then
  frozen), S08 (1.41x), S18 (1.41x).
- EVERY SONG OCCURRENCE GETS ITS OWN TAKE. A take anchors to its own
  line at its own song position, and that position only. Reused
  footage no longer covers vocal words: a repeated chorus line at a
  later song position needs a fresh take generated for that position,
  not a Chorus 1 take replayed. Reuse is retired as vocal coverage.
  Words with no take singing them in that position are a generation
  gap to fill by firing, never a freeze or a repeat to paper over.
- FREEZE IS BANNED DURING WORDS. Frozen frames are allowed only in
  true no-word windows (instrumental gaps, pre-first-word leader),
  and even there they must read as a held shot, not a stalled video.
  While any word plays, the picture must move.
- MOTION QC IS A GATE, NOT A STILL CHECK. v5's still-frame checks at
  word onsets could not see frozen or slowed motion. v6 verifies the
  delivered master itself across whole vocal segments: sample frames
  through each segment and require continuous frame-to-frame motion
  during words; any frozen run over ~0.5 s during words, or any
  interval playing noticeably slow or fast, is a QC fail and a reroll
  reason, not a disclosed nit. A cut that only passes as stills does
  not ship.
- 10-SECOND-FIT + PROPER CUTS (2026-11-02, user order + triple
  devil's-advocate adjudication, full plan in the MV-2 project
  V6_10S_CUT_PLAN.md). No assembly segment over 10 seconds.
  Hard cut on a word/line boundary only — never mid-word. A song
  line over 10s at natural pace is SPLIT before generation at a
  phrase/breath boundary into sub-slots each under 10s, each with
  its own take. Pacing words are a HYPOTHESIS, not a method: they
  move energy directionally, but no evidence shows a 2-3.4x span
  compression, so a pacing reroll is judged as a selection test,
  and the structural fixes are split/shorter lines, not a third
  pacing rewrite. The band is narrowed with a GREY ZONE:
  clear miss <0.60x or >1.60x = reroll/split; grey 0.60-0.80x
  or 1.25-1.60x = re-measure with forced alignment against the
  known lyric sheet plus ear check on first/last words before
  calling it a miss. Never QC on raw Whisper timestamps alone.
  Per-word warp figures are diagnostics, not gates. Report
  corrections folded in: Kling multi-shot per-shot seconds and
  Seedance 2.5 integer-second timestamps ARE documented (shot/
  beat level only, not word level) — neither changes the
  T2V-only word-timing verdict. FRAME RULE (2026-11-03, user:
  "anything with more frames is good, its less frames thats
  bad"): QC at native fps, not 0.5s samples — count frames
  that actually change INSIDE the vocal span and the longest
  near-duplicate run during the words. Gate (refined volley
  9: fraction alone misranks — S08 t9 is 49% changed but
  mean diff 1.92 with max run 3, moving at half rate,
  while S16 t4 is 29% with mean 0.35, essentially still):
  FAIL if vocal near-dup run >=24 frames (1s) during vocal
  OR vocal mean diff <0.5; changed fraction is a quality
  note, not the gate. The old 0.5s-sample motion gate
  passed frame-poor takes (S16 t4) and is superseded for
  the vocal window. Also check the RAW word list for
  repeat defects: the second-delivery scan flags full-line
  repeats only, so a repeated final word (R4 t4's second
  "done") slips past it — and the scan must check for ANY
  beat-word subsequence recurring after the first delivery,
  not just a full-beat recurrence from the beat start
  (volley 10: S16 t6 re-sang its tail "for a dollar and
  a dime" 5.52-8.04 after a grey first delivery, and S22
  t2 repeated its final "done" — both slipped past the
  full-line scan). A take sings its line exactly
  once, no part of it a second time. SPLIT-HALF RULE
  (volley 12): a zero-word full-clip Whisper result is NOT
  a no-line verdict — S22 t4's full-clip decode blanked on
  loud audio while the 0-5s half decoded the line cleanly.
  Split-half recheck before calling any take lineless.
  Mishear classes normalized before matching: tall=toll,
  told=toll, toe=toll, paid=pay, tell=sell (volley 12).
  Audio-driven lip-sync, Kling
  multi-shot, Seedance timestamps, and performance capture are
  the honest escalation ladder if T2V-only keeps missing; each
  needs its own user go-ahead and is not used by default.

## Text-only prompting discipline (2026-11-04) — adapted timed-plan method for a prompt-text-only backend

Backend reality, stated plainly: the generator takes prompt text (plus an optional still image) only. It receives no audio file, no word timings, no lip-sync parameter, and no duration-forcing signal beyond whatever clip-length controls the tool itself offers. Timed-plan cues — local timestamps, control spans, exact lyric quotes — are therefore directional: they raise the chance of usable mouth movement and roughly correct pacing, but they never guarantee frame-accurate sync, and they never make the generator "hear" the song. The pace floor measured through volley 16 (short slots resisting compression below ~0.44x) is structural for this modality, not a prompting failure to be out-pulled.

- Production bible still mandatory, and it travels into every prompt: named cast with immutable speaker IDs (never remapped), identity locks restated in every prompt, vocal ownership per phrase, forbidden elements, camera grammar. The generator sees no global timeline, so each prompt must be self-contained.
- Cue sheet is a planning artifact, not generator input: build it from measured word onsets before writing prompts, cut only at phrase-safe boundaries, and mark any slot that has hit the pace floor as STRUCTURAL (assembly problem, not another generation pull). Record the duration the tool actually returns for a given request length so assembly math stays honest — measure it, never trust the claimed length.
- Prompt construction, in this fixed order: (1) framing + identity lock first, mouth clearly visible and unobstructed, facing camera; (2) performance window with a local time bracket in whole or half seconds and the exact lyric string, repeated at least twice in the prompt; (3) silent-mouth instruction for every other visible character, in positive phrasing ("mouth remains closed and still for the entire line"); (4) articulation emphasis — clear, open mouth shapes on every syllable, no whispering, no mumbling, visible jaw movement; (5) action ordering — entrances, camera moves, and secondary action only before the first word or after the last word, never stacked on the vocal window; (6) end state — mouth closes after the last word and stays closed, clean held pose; (7) reinforcement near the end restating that mouth movement follows the exact lyric.
- "AT NOT OF" (user standing rule, 2026-11-10): lead every scene prompt with 'at <place>', never 'of <place>' — "iPhone video at a gas station", not "of a gas station". Starting at the place grounds the model as an active participant in the scene rather than a passive observer, and the takes read markedly more real. Good prompting and good grammar are rarely the same — embrace the weird phrasing. Applies to every vehicle prompt: the framing text opens by placing the camera at the place, then describes what happens there.
- Short slots: do not request impossible compression. Ask for the shortest reliable duration the tool actually returns, put the vocal performance in the first portion of the clip, and describe the mouth closing after the last word with the remainder as a held pose or gentle exit. Accept that the clip will be longer than the song slot and mark the excess for assembly trimming or a hard cut. Once the pace floor is measured for a slot, stop pulling on it.
- Multi-character: one primary singer per prompt for reliable mouth activity. Keep any non-singer's mouth explicitly closed and the singer in tighter framing. For alternating lines, generate separate clips — a text-only model has no reliable way to hand off speakers mid-clip.
- Timing-first review after every generation: mouth visibly moving inside the described window, still or closed outside it, identity and framing intact, actual duration measured (ffprobe, not the tool's claim). If the mouth performs a different phrase or stays nearly still, revise the prompt — stronger articulation language, tighter framing, repeated lyric, vocal instruction placed earlier — rather than firing an identical pull. If duration stays systematically longer than the song slot and further pulls do not compress it, classify the slot structural and stop generating.
- Assembly for structural gaps: hard cuts, short cross-fades, or a cut to a non-singing reaction shot or visual accent in preference to stretching or looping a mismatched mouth. The original song stays the master audio under all assembled clips; generated clip audio is discarded. Disclose any remaining micro-gap honestly in the final notes.
- Proof from the 2026-11-04 test: an explicit 9-second request returned a measured 9.000s clip, and a corrected hook prompt that named "including the word baby in the middle and the second time saying toll roads are dumb" produced "Toll roads are dumb" (0-2.32s) followed by "Baby toll roads are dumb" (3.8-6.88s) — the full line, with a gap, not a compression fix. Repeated lyric + explicit completeness wording moves the output; it does not repeal the pace floor.

## What this engine refuses (hard stops)

- A plan from a uniform grid or an unmeasured timeline.
- A SINGING vehicle without performance-window staging.
- A take in the cut without a QC row, or a master with a failed gate open.
- A third reroll of the same vehicle (retire + restage instead).
- Generated audio as soundtrack or timing source; any time-stretch of the song.
- A master in an MP4 container whose audio stream is not AAC (MP3-in-MP4 plays silent on phones — MV-2 2026-11-02, MV-6 2026-11-06). The delivery gate ffprobes codec_name and refuses anything but aac.
- Captions burned into generated footage; text or logos generated inside a clip.
- Licensed characters, plots, dialogue, logos, or real-person likeness for commercial use.
- The peak-tween assembly method, in any form, forever. It produced fake alignment on MV-2 v1 and was rejected by the user.
- Any slow-down warp past 2x slow (playback speed below 0.5x) on any
  interval, any frozen frame while words are playing, and any reused
  take covering vocal words at a different song position. (Per-word
  time warping itself is the sanctioned method since 2026-11-06 —
  see WORD-SYNC; speedups are fine, slowdowns are capped.)
- Stop-start flow: a take that opens on a held still and bursts late, or
  joints that do not line up frame-to-frame (see CONTINUITY METHOD).
  A master that reads still → burst → still fails even if every word lands.
- A hard jump cut inside a lyrical passage, or a closed-mouth cover under a sung line. Both produced the MV-5 v2 playback rejection (2026-11-06).
- Slopcannon's name, cannon branding, contest/merch mechanics, wiki text, prompts, or UI — the workflow is rebuilt, the brand is not.

## Alternatives for better results

- If a track is short, a single volley may cover the whole song. Say so in the plan instead of padding scenes.
- If a scene keeps missing on the same axis, restage it from scratch instead of rerolling the same vehicle a third time.
- If the user names a character, a setting, or a story beat with the track, that direction outranks the defaults for that track only.
- If the media tool ever accepts audio input, the Meyer black-frame audio-driving method becomes available and replaces prompt-steering for sync — until then, prompt-steering + coverage budget is the whole sync story. A MuseTalk/LatentSync repaint test on one flat-cartoon take is the other future path; it needs user approval for GPU/cloud spend and is not built.

## Text-only operating discipline — 55-rule fold (2026-11-04), research adjudication, and warp-rescue method

This section folds three things into one mandatory discipline: the user's 55 text-only instructions (2026-11-04), the triple devil's-advocate research adjudication (report at `research_notes/text-only-sung-timing-devils-20261104-0030/report.md`), and the warp-rescue method proven on MV-2 v6. Where this section and an older section disagree, this section governs for text-only work. Nothing here is copied verbatim from any third-party skill; mechanics are adapted into WuBu's own wording.

### Production bible and cue sheet first, always

- Before any scene prompt is drafted, write a one-page production bible locking character names, immutable speaker IDs (LEAD=S1 and so on, never remapped), identity features, camera grammar, and forbidden elements.
- Build an internal word-timed cue sheet from measured song word onsets before writing prompts, even though the generator never sees it. It exists so local timing language is better and phrase-safe cuts can be found. Output the full timed plan JSON before writing individual prompts.
- Never plan a scene boundary through an intelligible word or held note. Land every cut on silence, breath, or phrase end, and document the choice. In the timed-plan beats, keep the H3-style span and the silent-mouth sentence so the prompt step has a clean source to copy from.
- Keep all local timing language in one format (`from X.X to Y.Y seconds`, whole or half seconds only) because the text-only model has no sub-second awareness.

### Prompt construction, in fixed order

Every singing prompt is fully self-contained — the model has no memory of previous prompts or of the global song — so restate identity, framing, and vocal ownership in every single prompt:

1. Framing + identity lock in the first sentence: face and mouth constraint before anything else. Medium close-up or tighter, mouth unobstructed, facing camera, head movement restrained. Restate the full identity lock (face shape, hair, wardrobe, signature prop) every time; consistency degrades faster than length hurts.
2. Performance window, not a vague "sings": `From 0.0 to 3.2 seconds LEAD (S1) sings clearly and articulately, mouth opening and closing on the words "exact line".` Put the exact lyric string in quotation marks at least twice per prompt — once early, once near the end. For completeness-critical lines, name every required word and every repeat explicitly ("including the word baby in the middle and the second time saying…") — the 2026-11-04 hook proof shows this moves completeness, not pace.
3. Silent-mouth sentence immediately after the vocal window for every other visible character, in positive phrasing: "mouth remains closed," "mouth stays closed and still," or "remains silent." For a character that must stay silent, repeat the closed-mouth instruction in both the middle and the end of the prompt. One primary singer per prompt; never ask one prompt to switch speakers mid-clip. When two characters share a frame, keep the non-singer in softer focus or slightly behind and restate the closed-mouth rule twice. For instrumental or non-singing sections, write "mouth remains closed and still throughout" so the model does not invent singing.
4. Articulation clause, always: "Clear open mouth shapes on every syllable, visible jaw drop, lips forming distinct shapes, no still mouth." Ban "whisper," "mumble," "hushed," "softly," and "under breath" from singing prompts; use "clear," "open," "articulated," and "visible jaw movement" instead.
5. Action ordering: any entrance, camera move, or secondary action goes before the first word or after the last word, never stacked on the vocal window. Never stack a loud described event (splash, impact, shout, object interaction) on a vocal window — the model generates sound for the event and the mouth follows that instead of the lyric. Use "steady camera" or "locked-off camera" unless a deliberate post-vocal move is required.
6. End state + reinforcement: "After the final word the mouth closes and stays closed for the remainder of the clip," plus a stable end pose so assembly trimming has a clean frame to cut on. Close with the forbidden checklist as a negative list: "no text, no logos, no extra limbs, no morphing."
- Positive anatomy language only ("one smooth head, two eyes, normal human mouth"); avoid negative phrasing the model may invert. Limit cast per prompt to characters that must be visible. Carry one continuity anchor (same lighting direction, same background element, same wardrobe state) into consecutive prompts. For turnarounds or over-the-shoulder shots, add "seen from behind, back to camera" when the reference is front-facing. If a wide group shot is required, accept readable individual mouth sync is impossible and plan it as non-singing or as a cutaway.
- Short slots: request the shortest reliable duration the tool actually returns (measured, never trusted from the tool's claim) and describe the excess as a held closed-mouth pose or gentle exit. For very short fragments, expand the held pose rather than forcing the model to finish faster. For structural slots, write the vocal into the earliest portion of the clip and the rest as a static or gently exiting closed-mouth pose that trims cleanly. If the tool offers a duration parameter, request the shortest value that has previously returned a usable clip and describe content to fill exactly that length. Document the tool's actual minimum reliable generation length and use it as the hard floor for slot planning.

### Vehicle template — kinds, footer, macros, pilot (2026-11-13, loop 3 measured + survey + probes)

Every vehicle declares its kind, carries the prohibition footer, and
reuses macro-managed identity — measured on slopcore's PROMPTS.md
(101 prompts, 2026-11-12): kinds lips 8 / motion 44 / insert 49,
{END} footer on 91/101, timed beats on 100/101. The transfer is
structure, not length: slopcore prompts are NOT short (median 158
words macro-expanded) — the template change stops appearance
restatement from eating the vehicle budget; it does not impose a
word-count mandate. The short-vs-long A/B (survey §7 #1) is unrun;
validation bar is the next volley measured against the MV-14 baseline
(65/65 KEEP, 7 REJECTs, 5 of them G2 subtitle failures) — pass is
KEEP rate held + G2 subtitle failures down.

- KINDS. `lips`: the singer performs on camera; the vehicle names the
line and the mouth rule. `motion`: nobody sings; the vehicle carries
the action on the song's beats. `insert`: a still-first-frame plate,
silent — the plate is the exact first frame. The kind sets plate +
mouth rules; a vehicle that does not declare its kind is not a
vehicle.
- {END} FOOTER. Every vehicle ends with the prohibition footer,
verbatim: "One continuous shot, no cuts. No text, letters or logos."
Plus the survey #3 block: "No on-screen text, no subtitles, no
captions, no morphing, no duplicate props, no camera shake."
(MV-14: 5 of 7 REJECTs were G2 subtitle failures — the footer is
aimed at those.)
- MACRO-MANAGED IDENTITY. Character and room are written once per
project (identity macros in the project record) and expanded into
every vehicle — never restated in full per vehicle. Appearance
restatement is what inflates vehicles; the macros are what keeps
them tight.
- PILOT PATTERN (volley-0). Before any 6-video volley, fire three
test clips on the new template (the pilot) — burns 3 of the budget
to save the other 3 from a template error. Slopcannon's volleys fire
6 cold; slopcore's intake runs a pilot first.
- ASPECT LINE. Whenever images are attached, write the aspect as
"in exactly 16:9 aspect ratio (landscape)" — bare "16:9" loses to
attached images (probe P2 returned 1152×768 3:2 despite "16:9" in
the text; survey §7 #4). Exact hue does not reliably carry by name
(magenta returned purple); when hue matters under an aspect
conflict, put the TEXT FIRST — text-first held magenta at 20.31%
where image-first lost it to 0.11% (probe P5).
- DURATIONS. Request 5 or 10 seconds only. Durations quantize to
{5, 10} on the current tool: "exactly 7 seconds" returned 10.000s
(probe P4, 2026-11-12). Cut in assembly for anything else. 15s/20s
untested.
- LOOK BLOCK (2026-11-13, taste research — name the hardware, not
the vibe; vague adjectives "cinematic / moody / atmospheric" are
banned as the ONLY style language). After the action text, every
vehicle carries, in fixed order (keep the whole block ≤40 words):
(1) LENS + TEXTURE: "Shot on 35mm film, [28mm|50mm|85mm] lens,
[shallow depth of field, background dissolving | deep focus, sharp
foreground to horizon]. Texture: visible fine 35mm grain, slight
falloff toward the corners." Focal defaults: 35mm journeys/montage,
50mm performance, 85mm singing close-ups. (2) THREE-LAYER DEPTH:
"Foreground: [object/texture within ~1m of lens, slightly soft,
5–15% of frame at an edge/corner] — Midground: [subject + action] —
Background: [world, with one readable event or light change]." A
vehicle naming fewer than two layers is rejected at plan review.
Subject on a thirds intersection, never dead centre except a
deliberate formal/confrontation beat; horizon on a thirds line,
never mid-frame; declare any empty area meant for kinetic type.
Frame-within-a-frame at least once per 10 s beat in montage
sections. (3) ONE MOTIVATED LIGHT: exactly one named key source +
its in-frame motivation + direction + contrast, e.g. "Key: low warm
sun through the window at frame left, 45° to subject, 8:1
chiaroscuro, no fill." Contrast ~2:1–4:1 for comedy/pop brightness,
≥8:1 dramatic; EYES RULE — the key must leave both eyes readable;
singing takes default to Rembrandt/loop lighting, full chiaroscuro
is for montage/non-singing slots only. (4) PALETTE LINE: "Palette:
[2 primaries max] + bone + ink; accent [colour] on ≤10% of frame
area (one prop / one lamp / one garment detail)." One warm accent
per cool shot and vice versa. The PLAN carries a SECTION COLOUR MAP
(verse cool/desaturated, chorus warm/saturated, bridge colour-shift
not set-shift; Kelvin band stated when the section's emotion turns:
warm 2000–3500K, cool 5000–10000K). Never generate grey/monochrome
refs or takes — colour lives in the ref, the grade lives in post.
(5) POSE SILHOUETTE SENTENCE: "Pose: [one verb + one shape]" —
limbs separated from the torso, head clear of the shoulder line; no
"standing and singing" (a standing figure's silhouette is a
rectangle). POSE-AS-CUT: at each 10 s boundary the pose changes
while the world changes around it — the cut hides in the pose
change. (6) ONE MOTIVATED MOVE: move + reason + reveal, e.g.
"Camera: slow push-in over 10s, closing on her face as she realises
— reveals the [carry] glowing behind her, 50mm." No vehicle names
two moves; no "slow zoom" (a push-in is the honest version). Move
vocabulary: singing close-up = locked-off or slow push-in ONLY;
journey/montage = tracking or pull-out; hook hit = push-in landing
on the downbeat; transition = whip pan (the blur hides the cut —
pairs with the two-image morph, which is STAGED as the transition:
the carry crosses the lens or passes behind the subject across the
0.5–1.0 s morph; never ask the morph to be invisible, and cut ON the
morph landing in assembly, never hold on the end-anchor frame). A
locked-off take must carry INTERNAL motion (subject moves, light
changes, crowd crosses) — locked camera + still subject is the
halted-photo failure, not a style. (7) STABILITY BLOCK (positive
phrasing — the tool has no negative-prompt field; exclusions are
written as positive stable states): "Same face, same proportions,
same [canon traits] throughout. Hands relaxed, fingers together, at
rest or holding [one named object]. Locked camera, lighting and
background unchanged." STAGING BANS (checkable): no open hand
mid-gesture toward camera; no fingers spread; no hand gripping +
turning + face acting in one take; no rapid expression change in a
singing take; no extreme close-up of a face in motion (medium
close-up is the safe floor); never two hard problems in one take
(face acting + hand interaction + camera move — pick one).
BACKS-TO-CAMERA IS FIRST-CLASS COVERAGE (MV-14 crowd precedent):
backs, profiles, hands-on-objects, over-the-shoulder for any slot
where the face is the risk; a mouth that can't be trusted is never
shown — kinetic type carries the line. Portrait/close-up vehicles
add: "skin pores and stubble visible, uneven skin tone, fine lines,
soft natural light from one source." REF QC (before a still enters
a vehicle): SILHOUETTE TEST — threshold the ref to solid black at
~120 px wide; if the character/prop isn't identifiable, re-generate
the ref; COLOUR CHECK — the ref visibly contains the palette
accent. CASTING: for each character, generate 3 silhouette-distinct
directions as stills first (turnaround + one action pose + face
sheet) and pick by thumbnail readability.
- POST TEXTURE PASS (assembly, 2026-11-13, taste research): after
grade/match, apply fine monochrome grain weighted to
midtones/shadows (invisible on a still at normal viewing distance,
obvious when toggled off), a fraction-of-a-stop vignette centred on
the optical centre, saturation −10–15%, blacks lifted slightly —
the SAME grain profile on every clip in the cut. Judge grain on the
final export at phone size, never on a 480p preview; keep it light
for the ≤50 MB chat copy.

### Timing-first review, revision rules, and winning patterns

- Review in this order: (1) mouth visibly moving during the described window, (2) mouth closed outside it, (3) identity, (4) actual measured duration (ffprobe, not the tool's claim). Record duration, song slot length, and ratio in every status update so pace-floor decisions stay data-driven.
- If the mouth stays nearly still, revise by moving the vocal instruction earlier, repeating the lyric a third time, and strengthening the articulation clause before any re-roll. If the mouth performs a different phrase, treat it as a prompt failure and rewrite — never re-roll identical text.
- Keep a running "winning prompt patterns" list inside this skill and a per-character reusable vocal block extracted from every successful singing take; later scenes inherit the phrasing that actually produced the strongest mouth movement.

### Structural-slot rule (pace-floor classification)

- Document the measured pace floor for the current tool (MV-2 through volley 16: ~0.44x on short slots). A slot becomes STRUCTURAL when it has hit that floor on pulls along different axes (GAP-B 0.438x, S11 0.439x after restage), or when the warp arithmetic fails: slot ratio x 1.5 still below 0.80 (S12: 0.258 x 1.5 = 0.387; S11: 0.439 x 1.5 = 0.659).
- Once structural, the slot leaves the generation queue immediately: no re-fire, no third same-vehicle pull, no warp beyond the cap. After two failed compression attempts on a slot, stop generating and write the assembly treatment instead. When research or prior volleys have already established a structural gap, lead with the assembly plan rather than proposing another generation.
- Record the classification, the arithmetic, and the assembly method in the slot's QC row.

### Warp-rescue method (sanctioned rescue for held greys)

- Held greys (ratio 0.60–0.80 or 1.25–1.60) may be rescued by a bounded whole-clip warp (video + audio) of at most 1.5x, warped to the band edge, with the lyric-sequence gate, ratio gate, and frame gate all re-run on the warped output. Warping or freezing to manufacture coverage from a clear miss stays out; the viewing-cut fallback stretches were a user-ordered exception with disclosure, not QC passes.
- Adjudication precedents: when Whisper onset/end disagrees with deterministic warp math, the frame-gate vocal window wins; the done→dumb normalization is an established class (a take heard as "done" for a "dumb" slot may stand, recorded as such); onset re-measurement from visual + acoustic evidence (mouth state + RMS jump) is accepted (GAP-C, hook opener); scaled-ratio confirmation per the S09 precedent is accepted (GAP-D, GAP-E, hook opener) when the warped boundaries match the scaled span within ~0.08s.
- Usable band 0.80–1.25 remains the GENERATION criterion (a take whose
  line ratio sits in band needs little or no warp). ASSEMBLY placement
  is per-word time warping (user law 2026-11-06): speedups unrestricted
  (disclose), slowdowns capped at 2x slow. Any freeze during words and
  any reused take covering vocal words at a different song position
  remain banned.

### Assembly coverage taxonomy for micro-gaps

- Hard cut on a word, phrase, or beat boundary (1–2 frames early on the beat where it helps the cut feel locked). When the tool returns a clip longer than the song slot, plan a hard cut or short dissolve at the last clean closed-mouth frame rather than time-stretching.
- Cutaway / insert / B-roll for a missing or failed word: brief, purposeful, then return to the performer. The untouched master audio keeps singing while the picture looks elsewhere; the audience hears the word without needing to see a mouth form it. Never use cutaways as a crutch for a whole section.
- Reaction shot as the honest alternative to a fake mouth: a listening or reacting face (with its own motion — a turn, a glance, a gesture, not a frozen face) while the line continues. Prefer cutting to a non-singing reaction shot or visual accent over looping a mismatched mouth to fill a micro-gap.
- Picture offset of a few frames around a lyric boundary with the master audio untouched. This is explicitly NOT a literal J/L cut — the song is never split — only the picture change may lead or lag the boundary by a few frames, never seconds.
- Visual accent on the stressed word (a cut, a gesture, a camera move on its beat) so the edit carries the accent the mouth cannot. Fast cutting never makes a mouth faster; keep one readable idea per short shot and anchor back to the performer's face between covers. A held pose in moving footage (posture held while camera, breathing, and background motion continue, so frame difference stays non-zero) is allowed; a freeze frame (one frame repeated, motion stopped) during words is banned.

### Edit rule — cutting (user law 2026-11-06, from the MV-5 v2 playback verdict; applies to all MVs and to MV-3)

- Lyrical portions are cut SUSTAINED: hold one continuous picture per singer-passage; cut only where the singer changes or the scene changes. No per-line chopping inside a take, no donor-tail inserts mid-passage, no freeze-leader gaps that read as jumps. Warp, don't cut. A hard jump cut (same angle, same subject, re-cut mid-line) is jarring and banned in lyrical portions.
- Fast cutting belongs ONLY to beat-matched montage: cutaways, refrains-as-montage, and fast back-and-forth sections (rap/bridge). Cuts land on the beat, one readable idea per short shot, anchor back to the performer's face between covers.
- A sung line gets a SUNG picture: the character who sings the line must be shown singing it. Never cover a sung line with another character's mouth, and never cover a sung line with a closed-mouth reaction shot. Reaction/cutaway covers are for silence and gaps only.
- Fast alternating lines (rap/bridge, ~1s per line) are a montage problem, not a per-line generation problem: fire a volley of montage clips (6) staged for alternating energy and beat-matched cutting, instead of asking the model to sing one line per take. The pace floor (~2.5s/line, measured volleys 12/13) makes per-line generation for ~1s lines structural by definition.
- After assembly, run one final pass checking only mouth state at every cut point to avoid closed-to-open or open-to-closed pops.

### Captions, honest language, and the assembly map

- Captions are a subtitle track from measured song word times, using performed words where sheet and performance differ — never a take's generated audio, never the sheet where it differs. Form: line block + per-word highlight. The full line block stays on screen for the line's duration while only the highlight moves at sub-second speed; each word highlights 2–4 frames early. Word-pop (each word appearing alone) is not used for fast fragments. Covered words are still captioned on song time; the caption is the lyric track, the picture is coverage.
- Never claim frame-accurate lip-sync in any status report. Use "directional mouth movement roughly occupying the described window." The final assembly runs under the original master song audio only; generated clip audio is discarded.
- Write assembly notes that honestly disclose every remaining micro-gap and why generation could not close it. End every production with an assembly map listing each structural slot, the chosen generation take (or lack of one), the planned cut strategy, and an explicit disclosure of any remaining micro-gap. Disclosure belongs in the delivery note, never as an on-screen disclaimer.
- A slot covered by cutaway or reaction still gets a QC row recording the method, the caption timing source (song times), motion checks on the cover shots, and an explicit "not a mouth-sung slot" flag, so the cutlist never implies a sync that was not delivered.

### Prompt-only ceiling (say this plainly, every time it matters)

- No vendor publishes a word-timing input or a lip-sync accuracy figure for prompt-only generation. SlopCannon's native timed plan pairs with server-sliced scene audio, which this adaptation does not have — it proves the discipline (cue sheet, control spans, performance windows, silent mouths), not that prompt text alone anchors timing. Documented native durations are discrete or integer seconds, so short slots are excerpts or trims from longer takes, never native generations at exact length. "Singable" here means a mouth visibly forming approximately the right word sequence at approximately the right time under a master-carried soundtrack — not phoneme-accurate, word-onset-accurate, or pace-accurate singing. Repeating the exact lyric in a prompt is supported for word accuracy; no public doc says repetition changes pace or onset — that part is a WuBu heuristic with empirical support (the 2026-11-04 hook test), not a documented control.

### Repaint-test protocol (future, gated — NOT built, NO spend without user go-ahead)

- If an audio/repaint backend is ever approved, the test that settles it is one short, front-facing, face-visible take repainted to its isolated vocal slice, then word-checked by ear/Whisper plus the frame gate for a sung line (not clean speech). Preconditions: visible face every frame, no mic/hand occlusion of the mouth, a vocal stem (not a full mix) where the source requires one. Known caps to record: MuseTalk ~256px face region, LatentSync ~512px, Wav2Lip ~96px mouth crop; side angles, fast-speech jaw lag, and music-bed audio all degrade results. A failed singing test closes the backend thesis for that slot even though the input channel is correct. Repaint plausibility order if ever approved: GAP-B, then S12, then S11; S02 stays covered regardless unless a test specifically proves sub-second viseme discrimination.
- Record corrections: Runway's standalone Lip Sync tool availability is CONFLICTING in secondary sources (described as existing vs retired 27 May 2026 in favour of Act-Two) — treat as UNCONFIRMED pending Runway's own current docs, never list it as an available fallback. The Bone snail post / "99%-from-90% lipsync" claim remains UNVERIFIED across all researchers — never cite it as fact. The Runway MCP connector exists but is NOT connected; it is a route to generation models, not a lip-sync repaint endpoint, and connecting it would be a separate credit-spending route needing its own go-ahead.
