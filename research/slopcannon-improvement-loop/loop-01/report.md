# Slopcannon Improvement Loop — Loop 01

- **Date:** 2026-11-11 (evening EST; report written ~23:55 EST)
- **Order:** user Telegram msg 251 (2026-11-11 23:28 EST) — recursive improvement loop on Slopcannon's CORE, via Kevin Bacon citation-hopping research, loop after loop.
- **Coordinator:** 34f76b7a (loop 1).
- **Scope:** research + writing only. No video generated, no volley fired, no live SKILL.md edit, no commit, no Telegram. Drafted skill edits live in `SKILL_EDITS_PROPOSED.md` (parent verifies and applies).
- **Blind draw (load-bearing):** `compass` — drawn blind via `secrets.choice` from a generic noun list. Load-bearing in two ways: (1) the banked form idea THE COMPASS (see §6); (2) the validation test word — "compass" is plosive-initial (/k/), the hardest alignment case (silent closure before the burst), so every timing proposal in §4 must be hand-checked on plosive-initial words with "compass" as the named exemplar.

## 1. Method (Kevin Bacon guardrails, from the 2026-11-03 devils adjudication)

Solo-first, chain capped at 3 hops, hop 2 crosses a category boundary, one blind random input load-bearing, BAN_LIST respected, never re-search a DONE node, never bank a BAN_LIST endpoint. Chain log below (§2) is the audit data.

## 2. Hop chain (loop 1)

- **Hop 0 (seed):** Slopcannon's core pain point — the word-sync timing grid: measured word times as the authority, ASR anchors, snap-to-onset, warp caps, mouth-anchored verification. The grid is the known weak spot (user: "you keep making bad timing choices"; sprint 3: the grid's single global phase is the loose part; snapper: 166/212 words moved, median |corr| 0.052s).
- **Hop 1 (same category — agentic MV pipeline):** Brian Carpio, "I Built a Music Video Out of Text Files" (briancarpio.com, 2026) — a second, independent build of the same architecture (Demucs + forced alignment + measured word grid + lip-sync measurement), plus song2mv (PyPI, timing layer with `grid.json`: tempo, first beat, bar-start beat, where the song leaves the grid, and its swing) and AutoMV (arXiv 2512.12196, multi-agent MV system, htdemucs + Whisper lyrics + SongFormer structure). NOTE: the rotation's @anabology node (aimv.gg recipe) is NOT marked done by this loop — this hop studied Carpio's adjacent post, not the aimv.gg recipe page; the daily rotation still owns @anabology.
- **Hop 2 (CATEGORY CROSS — MV engineering → speech science):** anticipatory coarticulation — the visible mouth gesture LEADS the acoustic word. Lulaci et al. 2024 (Front. Psychol., doi 10.3389/fpsyg.2024.1446240): lip-rounding cues usable from 15 ms into word-onset /s/; Gow & McMurray 2007: identification 120–160 ms after onset via coarticulatory cues; Terry et al. (Oxford, Interspeech): "the visible gestures — the viseme — are seen BEFORE the corresponding phone is heard" ("school" prerounding: lips round for /uw/ while /k/ or /s/ still produced); Bregler & Konig: acoustic features maximally correlated with visual features 120 ms in the past — the visual signal leads the acoustic by ~120 ms on average.
- **Hop 3 (speech production → audiovisual perception):** McGurk effect + asymmetric sync tolerance. McGurk & MacDonald 1976 (Nature): vision dominates audition in speech perception (/ba/ audio + /ga/ visual → /da/ heard). Temporal window: McGurk strongest at 30 ms audio lead to 170 ms audio lag, weakening at 60 ms audio lead / 240 ms lag; ITU-R BT.1359 (already cited in the 2026-11-02 loop): audio-leading detected at +45 ms, audio-lagging at −125 ms. Shahin et al. 2017: tolerance for audiovisual asynchrony is ENHANCED by the spectrotemporal fidelity of the speaker's mouth movements — a low-fidelity (generated) mouth buys LESS tolerance, not more.
- **Chain cap reached (3 hops).** Next loop force-jumps (see §7).

## 3. Pain points, ranked (evidence from the skill + sprints + hops)

**P1 — THE ANCHOR IS ~150 ms EARLY, AND THE MOUTH LEADS BY ~120 ms.** Two systematic offsets stack in opposite directions. (a) Whisper's own word timestamps run ~150 ms early and drift by hundreds of ms (Chu et al. 2026, via danmackinlay notebook; WhisperX guide: "Whisper interpolates — and the result drifts by hundreds of milliseconds"); MFA places word boundaries at 20 ms average deviation from hand labels (35 ms noisy). Slopcannon's intake still uses faster-whisper word times as the song anchors. (b) The visible mouth gesture leads the acoustic onset by ~120 ms (hop 2). The swing-keyframe method anchors warps ON the ASR onset — so the anchor is wrong twice over, word-class-dependently (plosive-initial words like "compass" have a silent closure: the lips closed ~100 ms+ before the burst). The snapper's median 0.052 s correction is the pipeline already paying this tax empirically. **This is the loop-1 headline.**

**P2 — NO UNSUNG-WORD FLAG.** Carpio's aligner flags lines the model decided not to sing, so the scene shows them as on-screen text instead of a lipsync scene. Slopcannon has no equivalent: MV-14's "We'll be right back." tag (153.50 s, likely ASR hallucination) got no scene only because the prepro author suspected it; SONG_WORDS.json has no confidence/verification column. Same family: the 2026-11-11 Medium post (Ne0s0u1) notes global alignment glues every repeated lyric to its first occurrence — a monotonic forward matcher is the fix (Slopcannon's prior loop rec #2, provenance quarantine for identical choruses, was never implemented).

**P3 — QC HAS NO MOUTH-OPEN-VS-QUIET NUMBER.** Carpio turned "the lip-sync looks off" into "the jaw was open during 35% of the quiet moments" and drove vocal-loudness jaw control from 0.20 to 0.80 match. Slopcannon's QC has the MAR curve (F-03, banked, never implemented) and audio/visual envelope correlation (F-08, banked) but no combined gate — sync is still judged by eye-read at line/hook onsets. And the standing tolerance note ("mouth can lag take audio ~0.5–1 s") is ~4–8× looser than perception and symmetric where perception is asymmetric (hop 3: +45/−125 ms; McGurk window 30 ms lead–170 ms lag; generated mouths get less tolerance, Shahin 2017).

**P4 — THE GRID HAS ONE PHASE; THE SONG DOESN'T.** Sprint 3: C11 DP beats vs librosa agree at median 0.035 s, but both disagree with the rigid global grid more; tempo autocorrelation is flat (0.6357) across 90.5–92.5 BPM — a plateau, not a peak. song2mv's `grid.json` records per-song grid departures + swing. Slopcannon's `beat_grid.json` is one global phase.

**P5 — KINETIC TYPE STILL MEASURED, NOT RENDERED.** MV-13 v1 overflow: `char_w=0.52*fs` underestimates glyph widths 6–15%; patched per-line in the rebuild script, but `kinetic_ass.py` still estimates widths. The survey already adopted fontTools for real metrics; lego queue has c11_kinetic (wubu_canvas). Ranked last because the patch works — the renderer rebuild is the durable fix.

**P6 — VOLLEY/COORDINATOR FRAGILITY.** Process, not skill core; the revive detector covers it. Not a skill edit; noted only.

## 4. Ranked improvements (evidence + draft edit + validation)

### #1 — FORCED-ALIGN THE KNOWN LYRIC SHEET (intake; fixes P1a + P2) — HIGHEST VALUE

**Evidence:** Carpio: Demucs splits the vocal, stable-ts force-aligns the lyrics WE ALREADY KNOW against that vocal track — "far more accurate than transcribing, because nothing has to be guessed" (90 s on GPU; flags unsung lines). Chu et al. 2026 (via danmackinlay): Whisper timestamps ~150 ms early; MFA 20 ms avg deviation. Medium 2026-11-11 (Ne0s0u1): feeding Whisper a Demucs vocal stem jumped word-match 60% → 100% — "drums smear word timestamps"; monotonic forward matcher for repeated lyrics. Prior loop (2026-11-02) rec #1 said the same; never implemented.
**Blade feasibility:** no GPU — stable-ts needs torch. The blade path is (a) whisper.cpp experimental word timing (`-ml 1`) or Parakeet TDT (80 ms grid, adopted in the survey) as the transcriber, PLUS (b) the C11 snapper (sprint 5, built, median |corr| 0.052 s) as the alignment refiner, PLUS (c) the stay-rule patch (owed) so words with no in-span strong peak don't snap onto the previous word/drum. Demucs stem already exists in the pipeline (14 min/job; sprint 6 failed to replace it — harmonic ≠ vocal).
**Draft edit:** see `SKILL_EDITS_PROPOSED.md` §1 (intake: forced alignment of the known sheet against the Demucs vocal stem; SONG_WORDS.json gains `confidence` + `unsung` flag; monotonic forward walk for repeats; snapper stay-rule).
**Validation:** run the forced-align path vs current faster-whisper times on MV-14 (212 words): report median |Δ| and count of words moved >0.1 s. Bar: forced alignment should move FEWER words than the snapper's 166/212, and residual snapper corrections after forced alignment should shrink toward zero (median <0.02 s). Unsung-flag test: does the aligner flag the MV-14 153.50 s "We'll be right back." tag as unsung? Blind-drawn check: plosive-initial words incl. "compass" in the hand-check set.

### #2 — ANTICIPATORY VISUAL ANCHORS (swing keyframes; fixes P1b) — HIGH VALUE

**Evidence:** hop 2 — visual leads acoustic by ~120 ms (Bregler & Konig); viseme seen before phone heard (Terry et al.); lip-rounding cues usable from 15 ms into onset fricative (Lulaci et al. 2024); word identification 120–160 ms after onset via coarticulation (Gow & McMurray 2007).
**What changes:** swing keyframes sit on the VISIBLE mouth event, which leads the acoustic word onset by ~0.10–0.15 s (word-class dependent: plosive-initial words lead more — the closure is silent; vowel-initial words lead less). The current "~0.5–1 s mouth lag" blanket caution is replaced by (a) the systematic viseme lead (~0.12 s, applied at anchor time) and (b) the residual per-take measured mouth offset (what the caution already says, now bounded and measured, not a 1 s blanket).
**Draft edit:** see `SKILL_EDITS_PROPOSED.md` §2 (V4 correction + swing-keyframe section).
**Validation:** on MV-14 S47 (KEEP, md5 caf260aa38a6134f9306c8b3c76aaf28): measure the MAR curve against forced-aligned word onsets; test whether mouth-open onset precedes acoustic onset by ~0.1 s consistently across ≥10 words, and whether plosive-initial words show a larger lead than vowel-initial ones. Blind-drawn check: "compass" (/k/-initial) must be in the hand-check set — its closure should be visible ~0.1 s before the burst.

### #3 — ASYMMETRIC SYNC TOLERANCE + MOUTH-OPEN-VS-QUIET GATE (QC; fixes P3) — HIGH VALUE

**Evidence:** hop 3 — ITU-R BT.1359 +45/−125 ms; McGurk window 30 ms audio lead–170 ms audio lag, weakening at 60 ms lead / 240 ms lag; Shahin 2017 (low-fidelity mouths → less tolerance). Carpio's measurement: "jaw open during 35% of quiet frames" → loudness-driven jaw 0.20 → 0.80 match. F-03 (MAR curve) + F-08 (envelope correlation) banked, never implemented.
**What changes:** (a) the master gate's mouth-state read becomes asymmetric: a mouth opening up to ~0.12 s AFTER the word onset is inside tolerance; a mouth opening 0.05 s BEFORE the word onset is already a fail (audio-leading is detected ~3× sooner than audio-lagging). (b) New cheap CPU gate: mouth-open fraction during song-silent spans (MAR curve × vocal RMS envelope, both from the take's own ASR word gaps) — a number, not an eye-read; flag for eye review above a calibrated threshold (calibrate on MV-14 KEEPs the same way M6 was calibrated — threshold from the KEEP distribution, never a guess).
**Draft edit:** see `SKILL_EDITS_PROPOSED.md` §3 (QC gates §5 + master-gate mouth-state read).
**Validation:** run the gate on MV-14 takes: KEEPs should cluster low; test discrimination on MV-8 v2 (rejected) vs v3 (accepted) — the same pair M6 discriminated 4.0×. If the gate does not separate v2 from v3, it stays an eye-review flag, never a gate (same rule as M6).

### #4 — PIECEWISE BEAT GRID (per-section phase + swing + departures; fixes P4) — MEDIUM VALUE

**Evidence:** sprint 3 (DP vs librosa 0.035 s; both vs rigid grid worse; flat tempo plateau); song2mv `grid.json` pattern (tempo, first beat, bar-start beat, where the song leaves the grid, its swing).
**What changes:** `beat_grid.json` gains per-section phase + swing + a departure list; the swing-keyframe hint layer reads the section's phase, not the global one. The song is the tempo gospel — and the gospel has verses.
**Draft edit:** see `SKILL_EDITS_PROPOSED.md` §4.
**Validation:** re-run the C11 DP tracker with per-section phase on MV-14/MV-13/MV-12; median |offset| vs the measured grid must drop below the current 0.088 s (DP global). If it doesn't, the piecewise grid is rejected — same honesty rule as sprint 6 (report the fail, keep the tool).

### #5 — KINETIC TYPE: MEASURE, DON'T ESTIMATE (renderer; fixes P5) — MEDIUM VALUE

**Evidence:** MV-13 v1 overflow (char_w underestimates 6–15%); survey adopted fontTools; lego queue c11_kinetic (wubu_canvas). No new research — the fix is already scoped.
**What changes:** `kinetic_ass.py` uses fontTools real glyph advances (or the C11 canvas renderer when it lands); the per-line fs-scaling cap stays as belt-and-braces; add a 0-overflow assertion on the burned frames (full-res read already required at delivery).
**Draft edit:** see `SKILL_EDITS_PROPOSED.md` §5.
**Validation:** rebuild the MV-13 kinetic layer with fontTools metrics; all lines within frame; diff vs the shipped master (md5 2559d575…).

## 5. What this loop did NOT do (honesty tags)

- No GPU-dependent tool was adopted: LatentSync (Carpio: cautious on still face + rapped vocal, reads as mumbling) and LTX-2.3 (2.5× LatentSync mouth movement, 73 s/5 s on a 5090) are both model-bound for the blade — the portable part is Carpio's MEASUREMENT (mouth-open fraction), not his models. SyncNet (F-01) stays model-bound per the survey.
- WhisperX wav2vec2 alignment was not run on the blade — the feasibility claim for #1 rests on whisper.cpp `-ml 1` / Parakeet + the existing C11 snapper, which still needs the head-to-head in validation.
- The 0.12 s viseme lead is a literature average (speech, not singing; Bregler & Konig's 120 ms is conversational speech). Sung words stretch vowels and hold consonants differently — the number must be re-measured on sung takes (validation for #2), not taken as a constant.
- The McGurk/ITU numbers are broadcast speech, not AI-generated singing video. The direction (asymmetric, audio-lead punished harder) is stable across sources; the exact ms thresholds are calibration targets, not constants.

## 6. Lilypads banked

SOURCES.md entries 40–45 + LILYPAD_ROTATION.md queued nodes (loop-2 seeds). Banked form idea from the blind draw ("compass"): **THE COMPASS** — a compass needle is the continuity object: it always points at the song's next word/beat; the cut hides in the needle swinging across the frame; the needle points the way to the next scene. Test as a still-chain pair before volley use.

## 7. LOOP 2 seed (recursive by construction)

**Next pain point:** the vocal-activity gap sprint 6 exposed and could not close — harmonic ≠ vocal on a dense mix (Demucs RMS 192× separation vs HPSS envelope 1.24×); Demucs stays the segmenter at 14 min/job, and the torch-free roadmap loses this leg. **Loop 2 hop chain:** start at the vocal-activity feature → hop 1: pitch/voicing detection in speech and singing (YIN/autocorrelation voicing on the harmonic layer — sprint 6's own recommendation #3; the HPSS front-end is already trusted, masks corr 0.999229) → hop 2 (category cross): voicing detection in a distant domain — e.g. birdsong / bioacoustics pitch tracking, or laryngeal endoscopy / voice-science jitter-shimmer measures → hop 3: back to MV — a C11 voicing gate as the Demucs replacement, validated against the Demucs reference (bar: ≥80% boundaries within ±0.5 s, the bar sprint 6 missed at 12.5%). **Banked lilypads for loop 2:** SOURCES.md #40–45 (esp. #41 song2mv grid, #43 coarticulation, #44 McGurk/ITU, #45 forced-alignment accuracy); LILYPAD_ROTATION.md queued nodes appended by this loop. **Also queued for loop 2:** the mouth-open-vs-quiet gate calibration (#3) and the piecewise-grid validation (#4) — whichever lands first feeds the other (a calibrated gate needs clean anchors; clean anchors need the piecewise grid).
