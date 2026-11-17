# HyperFrames evaluation — 2026-11-17

**Subject:** HeyGen HyperFrames, https://github.com/heygen-com/hyperframes (gifted by the user, Telegram msgs 551/552)
**Repo pinned:** commit `5b2990fc10dbb2ad5806de665b8fa4ede2c175b6` (`v0.9.59-30-g5b2990fc1`, 2026-11-17), cloned to `~/workspace/tools/hyperframes/` (874 MB with LFS golden fixtures)
**CLI pinned:** `hyperframes@0.9.59` (npm), installed project-local at `~/workspace/tools/hyperframes-cli/`
**Browser:** Chrome Headless Shell `linux-152.0.7977.30`, provisioned by `hyperframes browser ensure`
**Verdict: ADOPT-PARTIAL** — adopt as the code-rendered graphics lane (Method C graphics, bumpers/titles, MV kinetic-type slots). Do not adopt as a footage or long-form renderer.

## What it is

Apache-2.0 HTML-to-video framework. A composition is an HTML page: timed elements carry
`class="clip"`, `data-start`, `data-duration` (seconds); one paused GSAP timeline per composition is
registered on `window.__timelines["<id>"]` and the renderer seeks it frame by frame in headless
Chrome, capturing each frame and encoding with FFmpeg (H.264 MP4 by default; WebM/MOV/GIF/HLS/
PNG-sequence also available). Animation runtimes: GSAP (primary), CSS, Lottie, Three.js, WAAPI,
Anime.js via frame adapters. Ships 9 agent skills (core set: `/hyperframes`, `/hyperframes-cli`,
`/hyperframes-registry`, `/media-use`, `/reverse-any-video`, `/style-sampling`) and a registry of
~450 blocks/components (titles, kinetic type, captions, charts, transitions, 3D). CLI surface is
deep: `init / lint / check / snapshot / render / inspect / keyframes / beats / audio / diff /
measure / benchmark`, plus a Studio preview app. Requirements: Node ≥ 22, FFmpeg. This VM has
Node v24.22.1 and FFmpeg 8.1.2 — both fine.

## Install outcome on this VM — works, after three environment fixes

`hyperframes doctor` after install: Node ✓, FFmpeg ✓, CPU/memory ✓; Chrome ✗ until provisioned.
Three gotchas, all solved:

1. **Cache-dir permission refusal.** HyperFrames refuses to install/run its browser from any
   directory whose ancestor chain is group/other-writable. This VM's whole home tree is
   group-writable (`drwxrws---`), so the default `~/.cache` is rejected, and so is any
   `HYPERFRAMES_CACHE_DIR` under `/home/hatch`. Working fix: `HYPERFRAMES_CACHE_DIR=/opt/hf-cache`
   (mode 700; `/` and `/opt` are clean). Consequence: `/opt` does not survive a VM replacement —
   after a rebuild, re-run `hyperframes browser ensure` (one ~40 s download) before rendering.
   (I also ran the tool's own suggested `chmod go-w ~/.cache`; it did not help — the check walks
   up to `/home/hatch` itself — and is not needed given the /opt route.)
2. **512 MB `/tmp` tmpfs fails the render disk check.** The render pre-flight measures free space
   at Node's `os.tmpdir()`. Fix: `TMPDIR=<project>/.tmp` plus `--frames-cache-dir <project>/.frames-cache`.
   With those set, renders run clean.
3. **No GPU path.** There is no libEGL/GPU on this VM (same wall that blocks Blender EEVEE).
   Chrome falls back to software GL and the fast BeginFrame capture "did not run", so capture uses
   the slower `Page.captureScreenshot` path. It works — it is just the slow lane (see Speed).

Also: telemetry was disabled (`hyperframes telemetry disable`). First-ever `check` run aborted
once with no output (cold browser start); the identical second run passed in 77 s. Retry-once on a
silent abort is the right operating rule here.

**Working render invocation (pin this):**

```bash
cd <project>
HYPERFRAMES_CACHE_DIR=/opt/hf-cache TMPDIR=$PWD/.tmp \
  ~/workspace/tools/hyperframes-cli/node_modules/.bin/hyperframes render \
  --fps 24 --crf 18 --frames-cache-dir $PWD/.frames-cache --output out.mp4
```

## Proof render

Original WuBu composition at `~/workspace/tools/hyperframes/proof/wubu-bumper/` (single-file
`index.html`, GSAP 3.15.0 vendored into `assets/` so nothing is fetched at render time):
8 s, 1280×720 — teal orb breathing over a ledger grid, gold "~ WuBu ~" wordmark punching in
letter by letter (glyph-exact, no garble — the thing the video generator cannot do), teal rule +
"WUBUTV STATION", and a ONE SHORT-style count board whose number ticks 1006 → 1012 in six steps
(post-graphic count, per the standing rule that the board carries the count). Corner bug throughout.

- `hyperframes lint`: 1 error on first pass (animating `letterSpacing` — layout properties snap
  under seek-capture; the linter names the fix), fixed to transform/opacity; 2 advisory warnings
  (dense single-file timeline; nested board div) left as-is for a proof.
- `hyperframes check`: **passed** — runtime, layout, motion clean; WCAG contrast 44/44. No audio
  by design (info only).
- Snapshots at 1 / 3.2 / 5 / 7.5 s eye-verified: wordmark exact, count reads 1006 / 1010 / 1012 at
  the right beats, board and bug correct.
- ffprobe of the render: **H.264, 1280×720, 24 fps, 192 frames, 8.000 s** — exactly on spec.

## Determinism test — perceptual, NOT byte-identical

Same composition, same flags, rendered twice:

| | render1 | render2 |
|---|---|---|
| bytes | 228,857 | 232,597 |
| md5 | `7fffac23b58dee000323225aceca10f3` | `e140c054a88e9ba27c5ff51dafee3bda` |

Decoded-frame comparison (ffmpeg `psnr`, all 192 frames): **average 55.3 dB, min 53.3 dB,
max 66.5 dB**. So the README's "same input, same frames, same output" holds at the picture level —
every frame agrees to ≥53 dB, far above the 20–45 dB floors in the project's own golden-fixture
harness — but the MP4 bytes differ (~1.6% size delta), consistent with the published audit's
caveat: determinism here is a PSNR contract, not a hash contract. **Operating rule: never gate a
re-render on file md5; gate on PSNR/snapshot diff (the CLI's own `diff`/`snapshot` commands do
this natively).**

## Speed test — capture-bound, ~40–50× realtime at 720p24 on this VM

| | wall (whole CLI call) | CLI-reported render | capture stage |
|---|---|---|---|
| render1 | 386 s | 5 m 38.5 s | 5 m 04.7 s |
| render2 | 412 s | 5 m 03.7 s | (same profile) |

Compile ~16 s, setup ~7 s, assemble ~3 s — everything else is frame capture on the software-GL
screenshot path across 1.5 shared CPUs (nproc reports 4). The frames cache did not speed the
second render (it caches extracted *source-media* frames; this composition has none). Practical
budget: **≈ 45–50 s of wall clock per finished second at 720p24.** A 10 s bumper ≈ 7 min;
a 60 s piece ≈ 45–50 min. `--quality draft` and the `benchmark` command exist for faster
presets but were not measured here.

## Fit analysis

**(a) Method C dynamic graphics for the shows — STRONG FIT, the main adoption.**
Credits, count boards, verdict/moral cards, singer-credit graphics (ON AIR), the ONE SHORT board:
today these are hand-rolled ffmpeg/post work. HyperFrames makes them HTML — exact text every
time (wordmark law is satisfiable *by construction*: glyph-spelled in markup, swept in snapshots),
frame-exact timing against the song grid, and re-skinnable per show by editing variables. The
proof's count board is literally the ONE SHORT device. Render cost is per-graphic (2–10 s each),
which fits the speed budget.

**(b) MV visual forms (kinetic typography slots) — FIT for short slots.**
The visual-mv-forms skill's kinetic-type family currently leans on post/ffmpeg type. HyperFrames
gives per-letter GSAP control (stagger, blur, punch) with a lint that actively bans the motions
that break under seek-capture. Good for hook/title/lyric-accent slots of ~5–15 s. Not a
whole-MV renderer at this speed.

**(c) Bumpers / titles — FIT.**
Station bumpers are 10 s — exactly the proof's shape and the only format that has ever performed
for us. A bumper becomes a parameterized HTML template (show name, arc card, count) instead of a
one-off build. ~7 min per render on this VM is acceptable for a template rendered occasionally,
painful for bulk variants — render overnight/in parallel lanes if a slate is needed.

**(d) Where it does NOT fit.**
- Generated footage: it renders HTML, not filmed/generated scenes. The media generation pipeline,
  Slopcannon volleys, and show unit production are untouched by it.
- The C11 SLERM tools: no overlap — different layer entirely (it *consumes* FFmpeg; it does not
  replace c11_flow/mmap/superflux-class instruments).
- Long-form assembly: at ~50× realtime on this VM, episode-length renders are out; assembly stays
  ffmpeg/concat as now. HyperFrames output slots in as *elements* inside the existing assembly.
- Anything needing WebGL-heavy 3D at speed: software GL capture is the only path here.

## Verdict: ADOPT-PARTIAL

Adopt as the standing code-rendered graphics lane, effective immediately for new work:

1. **Integration points:** (i) Method C device builds for the morphed shows (credits, boards,
   verdict cards) — build as HyperFrames projects under the episode's work dir, render at
   1280×720/24/CRF 18, drop into the existing single assembly pass; (ii) bumper/title templates
   for the station; (iii) kinetic-type slots in MV builds per the visual-mv-forms skill.
2. **Pinning discipline (non-negotiable):** upstream ships multiple releases a day (0.9.59 today,
   repo HEAD already 30 commits past it). Pin the CLI exactly (`hyperframes@0.9.59`, already the
   pattern in scaffolded `package.json` scripts), pin the repo commit above, vendor GSAP into
   each project, and upgrade only deliberately via `hyperframes upgrade --project . --check`.
3. **Environment wrapper:** always run with `HYPERFRAMES_CACHE_DIR=/opt/hf-cache`,
   `TMPDIR=<project>/.tmp`, `--frames-cache-dir <project>/.frames-cache`. After any VM rebuild,
   re-run `browser ensure` first. Retry a silent `check` abort once.
4. **QC gates:** `lint` + `check` must pass (fix every error), `snapshot` the key beats and
   eye-read them, ffprobe the render. Determinism checks by PSNR, never md5.
5. **Budget rule:** plan ~1 min of render wall per finished second at 720p24 on this VM; keep
   individual renders ≤ ~15 s of finished video.

## Files

- Evaluation (this file): `~/workspace/research_notes/hyperframes-eval-20261117/EVALUATION.md`,
  mirrored to WUBUMV `research/hyperframes-eval-20261117/`.
- Proof composition + renders: `~/workspace/tools/hyperframes/proof/wubu-bumper/`
  (`index.html`, `assets/gsap.min.js`, `renders/render1.mp4`, `renders/render2.mp4` — renders
  stay local, not committed). Composition source mirrored to WUBUMV `tools/hyperframes-proof/`.
- Clone: `~/workspace/tools/hyperframes/` @ `5b2990fc`; CLI: `~/workspace/tools/hyperframes-cli/`.
