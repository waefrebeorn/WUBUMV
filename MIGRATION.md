# WUBUMV migration record

Decree: Telegram msg 340, 2026-11-13 ~02:45 EST — "you can commit all work
to WuBuMV you are wubuMV". Blanket authorization; WUBUMV is the music-room
identity. Repo: `waefrebeorn/WUBUMV`, PUBLIC, code/text only.

## Phase 1 — DONE 2026-11-13 (this commit)

Remade music tools, COPIED (originals untouched in wubutv-network) into
`tools/` + `skills/` + `research/detection-research/`. 208 files, 7.6 MB,
zero media. Local checkout: `~/workspace/wubumv`.

| What moved | Where | Replaces / verdict |
|---|---|---|
| c11_mir (beat tracker + MIR core + word-time snapper mode) | `tools/c11_mir/` | librosa/Essentia audio features; DP median \|offset\| 0.088s beats librosa 0.145s; all features corr 1.000000 vs librosa; snapper 166/212 words moved, median \|corr\| 0.052s |
| c11_sep (MDX-Net separator, C11) | `tools/c11_sep/` | Demucs (torch). PASS all 4 bars; stem corr 0.9675; runtime 840.4s |
| c11_tsm (per-gap-targeted time-stretch, M7) | `tools/c11_tsm/` | —. PASS all 7 bars; guard hard 0.5, operational 0.7 |
| c11_flow (Farneback optical flow, C11) | `tools/c11_flow/` | cv2.calcOpticalFlowFarneback (never installed). Validated vs cv2 |
| c11_voice (voicing gate: YIN + pYIN + CPP + HNR) | `tools/c11_voice/` | Sprint-6 HPSS boundary gate. FAIL STRUCTURAL (8/24 mix / 14/24 stem vs 80% bar) — bar held, not lowered |
| c11_vibrato (vibrato depth) | `tools/c11_vibrato/` | —. FAIL FAST as delivered; loop-5 re-measurement AMBIGUOUS — RMVPE-on-stem is the arbiter |
| c11_casa (CASA voice-segregation probe) | `tools/c11_casa/` | —. FAIL FAST both bars; classical sensor search is OVER |
| mdx_stemact (stem-activity curve) | `tools/mdx_stemact/` | —. Bars A+B PASS, C FAILS — valid voice-activity curve; stay-rule use has NO sensor |
| wubuwizard (MDX-Net ONNX CPU runner) | `tools/wubuwizard/` | torch Demucs. Corr 0.9675 vs Demucs, 1.78× slower — torch-free fallback |
| lyrics (hybrid extraction + kinetic rebuild) | `tools/lyrics/` | —. faster-whisper turbo backbone + MDX stems for dense spans; re-extracted MV-2/3/4/5/6 from audio |
| tempo-energy (tempo + energy measurement) | `tools/tempo-energy/` | Prompt BPM is a claim — measure (MV-9 133 vs 128, MV-10 ~108 vs 112) |
| visual-forms (kinetic_ass + code-rendered proofs) | `tools/visual-forms/` | —. Type is a POST layer, never generated in-clip |
| Slopcannon skill | `skills/slopcannon/` | The MV pipeline skill (intake → plan → volleys → QC → assembly) |
| visual-mv-forms skill | `skills/visual-mv-forms/` | Visual-first MV forms beyond singing takes |
| video-api-mastery skill | `skills/video-api-mastery/` | Measured media.generate_video / generate_image behaviour |
| Detection-research reports + analysis scripts | `research/detection-research/` | Sprint reports SPRINT_2026-11-11/12_*, DETECTION_FINDERS.md (F-01..F-21), M6 calibration, SPRINT_BRIEF_TEMPLATE.md |

### Build verification (in the new layout, 2026-11-13)

All five C tools build clean with `make`: c11_mir, c11_tsm, c11_flow,
c11_voice (its `../c11_mir/json.c` reference resolves under `tools/`),
c11_sep (`make sep_main`, `make test_stft test_interp test_block1`).
Binaries removed after the check (`make clean`); `.gitignore` covers them.

### Deliberately left out

- **All media**: *.mp4/*.wav/*.bin chunks/*.npz/*.npy, the 66 MB
  `UVR-MDX-NET-Voc_FT.onnx` model (fetch from the UVR /
  audio-separator model hub — see `tools/wubuwizard/README.md`),
  c11_sep weight chunks (~350 MB, regenerate with `extract_weights.py`),
  compiled binaries, `__pycache__`, logs, venvs, the Blender tarball.
- **c11_frames / c11_kinetic / c11_spec**: do not exist yet (lego top-3,
  scoped not built).
- **Loop-06 wav files** and all other audio: see phase 2.
- `tools/lyrics/scripts/` are per-project adaptations (MV-2 set +
  MV-5 stem scripts) — paths at the top of each script point at the
  project they were written for; adapt before reuse.

### Notes

- `tools/c11_mir/json.c` carries an uncommitted fix vs the
  wubutv-network master copy: a 1-byte heap overflow in
  `json_escape_string` (`need` 1 → 2), caught by ASan in sprint 8,
  fixed 2026-11-12. The fix is documented in the code comment; the
  copy here includes it.
- `tools/c11_sep/test_block1.c` has one pre-existing `-Wcomment`
  warning (`/*` inside a comment about weight paths). Upstream, not
  introduced by this migration.
- Some READMEs in the copied trees still cite absolute
  `~/workspace/...` paths — those point at the original locations
  and are historical; the tools themselves are self-contained.

## Phase 2a — DONE 2026-11-13 (research-text move)

Copied (originals untouched) into `research/`, text only, 21 files,
420,498 B, zero media. Layout mirrors the source trees:

- `research/slopcannon-improvement-loop/loop-01/` — report.md +
  SKILL_EDITS_PROPOSED.md (loop-01's proposed skill edits; loop-1
  verification was applying them the same night)
- `research/slopcannon-improvement-loop/loop-02/` … `loop-06/` —
  report.md + SPRINT_SCOPE.md each
- `research/tsm-driedger-2014/` — SPRINT_SCOPE.md + report.md
  (c11_tsm's spec; the c11_tsm README points at it)
- `research/media-capabilities-survey-2026-11-12/` — report.md +
  probes.md (P0–P5 probe results; part of the same survey)
- `research/lilypads/series-2026-sep-nov/` — report.md (ranked
  Sep–Nov 2026 AI series survey; clearly survey-class)
- `research/slopcannon-deep-research-20261101-0452/` — report.md +
  notes/*.md (clones-generic, contest-reception, slop-cc-live)

Deliberately left out (text-only rule + brief scope):
- Loop-06 wavs (4 × ~5 MB) and loop-05 .npy curves — audio/binary,
  never in WUBUMV.
- Loop-06 `cca_s25t2/` PNG frames — images, never in WUBUMV.
- Loop-04/05/06 supporting experiment scripts + JSONs
  (entropy/formant/vibrato/snapper/CCA .py + .json, ~1.9 MB curve
  JSONs) — outside the brief's report.md + SPRINT_SCOPE.md scope;
  a later phase can move them if the parent wants.
- TSM dir's scripts/logs/JSONs/PNG (`tsm_*.py`, grade logs,
  winners_league.png, stretched/, strips/) — same reason.
- Deep-research `AGENTS.md` — coordinator working file, not
  research content.
- Per-creator lilypad studies (anabology, clawdslop, deadsun_0,
  nu_vogue_art, soundboostcom — report.md + notes/ each) — individual
  studies, not clearly survey-class; left out per the brief.
- five-shows-craft, performance-analysis, self-tools-survey — STAY
  per MIGRATION.md phase-2 inventory.
- MV project histories (MV-2..MV-14) — pipeline NOT quiet, Q10
  running on MV-5; the filtered text-only snapshot waits for Q10
  to close + parent go-ahead. (Done later the same day — Phase 2b.)

## Phase 2b — DONE 2026-11-13 (this commit; MV project histories)

Gate cleared: MV-5 Q10 closed 2026-11-13 ~04:45 EST (v5 delivered,
wubutv-network commit e3c855a2). Filtered TEXT-ONLY snapshot of every
MV project history, COPIED (originals untouched in wubutv-network)
into `projects/<project-dir-name>/`, mirroring the source layout,
plus the musicvideo-level shared files (`KICKSTAND.md`,
`MONDO_INDEX.md`, `README.md`) at `projects/` root.
**3,322 files, 20.51 MB, zero media.**

| Project | Files | Size |
|---|---|---|
| MV-1_ON_FILE | 3 | 8 KB |
| MV-2 toll-roads-are-dumb | 398 | 2.70 MB |
| MV-3 i-am-your-dad | 252 | 1.49 MB |
| MV-4 this-time-its-real | 174 | 0.99 MB |
| MV-5 easy-now-easy-now | 437 | 4.61 MB |
| MV-6 sell-the-lemons | 143 | 2.05 MB |
| MV-7 the-nobody-man | 438 | 2.62 MB |
| MV-8 wipe-and-its-still-there | 284 | 1.94 MB |
| MV-9 gotta-hold-it | 113 | 0.36 MB |
| MV-10 aging-tropes | 93 | 0.38 MB |
| MV-11 water-hit-my-balls | 315 | 1.17 MB |
| MV-12 micro-soft-lost-the-bet | 200 | 0.67 MB |
| MV-13 movin-on-newton | 335 | 0.83 MB |
| MV-14 clip-it | 134 | 0.67 MB |
| shared (musicvideo level) | 3 | 19 KB |

Composition: 1,322 .json (word grids, cutlists, gate results),
965 .txt (vehicles, plans, notes), 406 .py (build/gate scripts),
314 .md (ledgers, TAKE_HISTORY, LYRICS_REDO_NOTES, Q-notes),
210 .log (gate logs), 52 .ass (kinetic captions), 32 *_DELIVERED.flag,
15 .sh, 4 .csv, 2 .srt. MV-1_ON_FILE is an on-file reference project —
its history is almost entirely media in the source, so its text
snapshot is genuinely just 3 files; nothing was padded.

Deliberately left out (hard media rule + brief scope):
- ALL media (~24.7 GB across the projects): *.mp4/*.mov/*.wav/*.mp3,
  *.png/*.jpg/*.webp stills and frames, masters/, takes/, stems/.
- Image-evidence dirs: frames*/, *_frames (incl. MV-8's per-scene
  *_motion_frames), frame_reads/, audit_frames/, verify_frames/.
- Binaries and caches: *.pyc/__pycache__, *.so, *.bin, *.npy, *.npz.
- Other musicvideo-level shared trees (intake/, notes/,
  pose-library/, slopcannon-learning/, tools/, video-api-lab/,
  visual-forms/) — outside this phase's scope;
  detection-research/ already moved in Phase 1.

Note: gate .log files are force-added past this repo's `*.log`
gitignore — the phase brief names gate logs as history evidence, so
they are tracked from this commit on.

## Phase 2 — INVENTORY ONLY (parent decides; nothing moved)

### MV project histories (MV-2..MV-14) — ~24.7 GB on disk, mostly media

**Status: the filtered text-only snapshot below was taken in
Phase 2b (see above) once Q10 closed. Media stayed behind, as
recommended.**

| Project | Size |
|---|---|
| MV-2 toll-roads-are-dumb | 1.3 GB |
| MV-3 i-am-your-dad | 2.5 GB |
| MV-4 this-time-its-real | 804 MB |
| MV-5 easy-now-easy-now | 3.1 GB |
| MV-6 sell-the-lemons | 1.3 GB |
| MV-7 the-nobody-man | 3.7 GB |
| MV-8 wipe-and-its-still-there | 3.3 GB |
| MV-9 gotta-hold-it | 964 MB |
| MV-10 aging-tropes | 1.0 GB |
| MV-11 water-hit-my-balls | 3.1 GB |
| MV-12 micro-soft-lost-the-bet | 1.2 GB |
| MV-13 movin-on-newton | 1.9 GB |
| MV-14 clip-it | 1.2 GB |

**Recommendation:** move TEXT ONLY, as a filtered snapshot, once the live
pipeline is quiet (per the repo README): ledgers, TAKE_HISTORY.md,
scene plans, `.ass` kinetic files, word grids, gate JSONs,
LYRICS_REDO_NOTES.md — never takes/, masters/, stems, or wavs. Media
never moves to WUBUMV; the HF media dataset stays the media home.

### research_notes — text reports

| Item | Size | Recommendation |
|---|---|---|
| slopcannon-improvement-loop (loops 01–06) | 27 MB total; ~3 MB text + 4 wavs (~24 MB) in loop-06 | MOVE the text reports to `research/` (they are the Slopcannon improvement record — core music-room knowledge); leave the loop-06 wavs out |
| tsm-driedger-2014 (TSM method spec + scope) | 2.4 MB | MOVE — it is c11_tsm's spec; the c11_tsm README already points at it |
| slopcannon-deep-research-20261101 | 92 KB | MOVE (pipeline research) |
| media-capabilities-survey-2026-11-12 | 48 KB | MOVE (pipeline research) |
| mv-improvement-program-2026-11-12 | 52 KB | MOVE once the Q7+ chain runs — it is the live MV fix queue |
| five-shows-craft | 76 KB | STAY in wubutv-network for now — it is the TV-shows side, moves with the five-shows work |
| performance-analysis-2026-11-12 | 84 KB | STAY — platform performance analytics, not music-room material |
| self-tools-survey-2026-11-12 | 32 KB | STAY — general Muse tooling survey, not music-specific |

### Rules that stay

- Code/text only, forever. No audio, no video, no Suno tracks.
- Media lives on the HF media dataset (`WaefreBeorn/wubutv-network-media`).
- MV project histories move only once the live pipeline is quiet.
