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

## Phase 2 — INVENTORY ONLY (parent decides; nothing moved)

### MV project histories (MV-2..MV-14) — ~24.7 GB on disk, mostly media

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
