# Lyrics extraction with word-level timings on CPU — research report

Research date: 2026-11-10. Target: CPU-only Linux VM, ~6 GB RAM, Python, current pipeline = faster-whisper `small`, int8, no VAD, 16 kHz mono wav, word timestamps as video-cut grid.
Failure modes: (1) silence on loud/dense sections; (2) repetition loops on repetitive chant; (3) merged words / smeared timestamps in rapid chant; (4) missed words in instrumental-heavy spans.
Method: Kevin-Bacon chaining from faster-whisper / whisper.cpp / WhisperX / Demucs / OpenAI Whisper outward (papers, GitHub, model cards, benchmarks). `verified live` = read via `browser_open` on 2026-11-10; `index` = search-result text only, not opened.

## Summary

**Do not just swap the model. The highest-return change is the pipeline around Whisper, in this order: (a) fix decoding + chunking, (b) segment with RMS-VAD on Demucs-separated vocals and transcribe long (~20–30 s) segments, (c) re-time words with a forced aligner when the lyric sheet is known, (d) only then A/B a non-Whisper ASR.**

Evidence: the only systematic lyrics study (Syed et al., 2025, MSS-ALT) found separation alone barely moves WER on Jam-ALT, while RMS-VAD segmentation — boundaries derived from separated-vocal amplitude — cut long-form WER 23.02% → 20.35% on the original mix and cut the hallucination proxy sharply. A 2026 singing benchmark found Whisper large-v3-turbo the most accurate sung-lyrics engine (88/100) but reproduced failure (1) exactly (20 s of silence over a held-vowel bridge) and failure (2) (13 s decoding a 4 s buffer in a repetition loop) — both traced to the serving/decoding wrapper, not the model. Non-autoregressive / transducer ASRs (Parakeet TDT, SenseVoice/Paraformer) are the principled antidote to (2) and (3) because they do not autoregressively re-emit text, and Parakeet predicts a duration per token; Qwen3-ASR (Jan 2026) is the first major open ASR whose model card explicitly lists singing voice and songs with BGM. No 2026 paper or tool was found that solves all four modes out of the box on a 6 GB CPU.

**Ranked shortlist (detail in §6):**
1. **Fix current faster-whisper config** — free, same stack: pin language, `vad_filter` (conservative) or RMS-VAD segmentation, `condition_on_previous_text=False`, greedy/single-pass with temperature fallback kept, `large-v3-turbo` (or `distil-large-v3` if English-only) instead of `small`, post-filter repetition. Addresses (1)(2)(3)(4) partially.
2. **Demucs (htdemucs) → RMS-VAD segments → transcribe original mix *and* separated vocals, keep the better per segment** — addresses (1)(4), and (2) via boundaries. CPU-feasible; Roformer is better quality but too slow on CPU.
3. **If lyric sheet is known: Qwen3-ForcedAligner-0.6B** (or WhisperX wav2vec2) to re-time words — addresses (3) directly; Qwen is the 2026 successor, single forward pass, 11 languages.
4. **Head-to-head challenger: Parakeet TDT 0.6B v3 via sherpa-onnx / onnx-asr (CPU ONNX)** — native word timestamps, TDT durations, no autoregressive loop. Addresses (2)(3); singing evidence is thin, so test, don't adopt blind.
5. **Qwen3-ASR-0.6B + Qwen3-ForcedAligner** — best singing/BGM claim, but GPU-oriented; trial on CPU, expect slow / RAM-tight at 6 GB.

## Findings

### 1. Best lightweight CPU ASR models/tools for SUNG lyrics in 2026

**Whisper family — still the default, and no new open Whisper weights exist.**
OpenAI has released no new open Whisper since large-v3 (Nov 2023) and large-v3-turbo (Oct 2024, 809 M params, decoder 32→4 layers) — `index`, https://nexgpu.net/en/models/whisper/ . faster-whisper 1.2.1 (31 Oct 2025) is the current PyPI release; its last commit was Nov 2025 per a Sep 2026 survey — `index`, https://awesomeosai.com/self-hosted/speech-to-text . **2026 gotcha: a plain `pip install faster-whisper` now pulls PyAV 19 and every transcription fails (`TypeError: open() got an unexpected keyword argument 'metadata_errors'`); pin PyAV 17 or 18.1.0** — `index`, https://www.pyinns.com/python/llm-and-generative-ai/speech-to-text-python-faster-whisper-2026 .

- **large-v3-turbo is the best sung-lyrics Whisper.** In Cukier's Oct 2026 singing bench (9 clips, 4 languages, 593 words, Demucs vocal stems), Whisper large-v3-turbo scored 88/100, best accuracy and best language-switching, free/offline — `verified live`, https://danicuki.substack.com/p/can-ai-hear-you-sing . Caveat: that was MLX on an M3 Max, small corpus, one run per engine.
- **CPU cost warning — turbo is not much faster than large-v3 on CPU.** The encoder (the slow part on CPU) is identical in turbo and large-v3; decoder pruning mainly helps GPU. One 4-core laptop test: whisper.cpp turbo q5_0 took 136 s for an 11 s clip, while faster-whisper transcribed a 127 s recording in 31 s with base.en — `index`, https://www.logeshwaran.org/2026/10/run-whisper-locally.html . Another guide claims large-v3 on an i9 CPU is RTF ~2.5 (2.5× slower than real time) and turbo int8 ~1.5 GB — `index`, https://runaihome.com/blog/whisper-large-v3-self-hosted-transcription-server-2026/ . Treat any "turbo = 8× on CPU" claim as GPU-only. On a 6 GB VM, turbo int8 (~1.5 GB) and small int8 both fit; large-v3 int8 (~2.9 GB) fits only if run alone. Expect a 3-minute song to take several minutes on CPU with turbo/small — acceptable for offline video production, not real time.
- **Distil-Whisper distil-large-v3 / v3.5:** 756 M params, English-only, ~6.3× faster than large-v3, WER within ~1 point — `index`, https://www.promptquorum.com/power-local-llm/local-whisper-stt-comparison . Best CPU Whisper if the repertoire is English-only; useless otherwise.
- **whisper.cpp 1.9.5:** C/C++, no Python, CPU/Metal/CUDA/Vulkan, Silero VAD support, experimental word timestamps, now ships a Parakeet CLI — `index`, https://awesomeosai.com/self-hosted/speech-to-text and https://medium.com/@andrew22dev/the-best-open-source-speech-to-text-models-to-self-host-in-2026-6cc5a8abc134 . Slower than faster-whisper in Python on the laptop test above; choose it only if a dependency-free binary matters.
- **WhisperKit / mlx-whisper:** Apple-Silicon only — irrelevant to a Linux CPU VM.

**Non-Whisper challengers (the interesting 2025–26 shift):**

| Model | Size / langs | Word timestamps | CPU fit | Singing evidence |
|---|---|---|---|---|
| NVIDIA **Parakeet TDT 0.6B v3** (Aug 2025) | 600 M, 25 European langs | Native — TDT decoder predicts token durations | ONNX via sherpa-onnx / onnx-asr; one speech harness measured RTF ~0.03 on CPU (speech, not singing) | NVIDIA advertises "song-to-lyrics"; no lyrics benchmark found. v2 English-only, 6.05% WER (speech). |
| **Qwen3-ASR 0.6B / 1.7B** (29 Jan 2026, Apache-2.0) | 0.6 B / 1.7 B, 30 langs + 22 Chinese dialects | Only via separate Qwen3-ForcedAligner-0.6B | GPU-oriented (Transformers/vLLM); no CPU benchmark found — 0.6 B CPU trial is an experiment | Model card explicitly lists audio types "Speech, Singing Voice, Songs with BGM" — the only major open ASR to do so. 1.7 B: 5.40% avg WER, Open ASR Leaderboard Oct 2026, ahead of Whisper large-v3 (7.16%, 36th). |
| **FunASR SenseVoice Small** (234 M) / **Paraformer** (220 M) | SenseVoice 5 langs (zh/yue/en/ja/ko); Paraformer mainly zh | Yes (Paraformer timestamp prediction) | ONNX int8 ~230 MB; claimed 17× / 15× real time on CPU | Non-autoregressive = structurally immune to repetition loops. No singing benchmark found; language coverage is the limiter. |
| **FunASR-Nano** (800 M) | 31 langs | Via pipeline | Large/slow on CPU (~950 MB int8) | Sherpa-onnx docs say it "handles sung lyrics" — anecdotal, no benchmark. |
| **Moonshine** (27–245 M) | English (+ others) | No native word timestamps in ONNX engine | Very fast on CPU | Skip for this pipeline — no word timings. |
| Meta **MMS / SeamlessM4T** | 100+ langs | Via CTC aligner | Heavy | No singing-specific advantage found; not shortlisted. |

Sources: Parakeet — `index`, https://developer.nvidia.com/blog/nvidia-speech-ai-models-deliver-industry-leading-accuracy-and-performance/ and https://arxiv.org/html/2509.14128v1 ; Qwen3-ASR — `verified live` model card, https://huggingface.co/Qwen/Qwen3-ASR-1.7B-hf , and `index`, https://medium.com/@andrew22dev/the-best-open-source-speech-to-text-models-to-self-host-in-2026-6cc5a8abc134 ; FunASR — `index`, https://www.funasr.com/en/models.html ; speech CPU RTF — `index`, https://metavert.io/speech-recognition (Parakeet int8 via sherpa-onnx, 0.8% WER on a 199 s speech recording, RTF ~0.03; but Parakeet v3 "dropped whole sentences, repeatably and depending on how the audio was chunked" in the same harness — chunking matters).

**Bottom line for §1:** for sung lyrics, Whisper large-v3-turbo remains the accuracy pick and the only one with a singing bench win; Parakeet v3 and Qwen3-ASR-0.6B are the two challengers worth an A/B, for opposite reasons (Parakeet: native durations + ONNX CPU; Qwen: explicit singing/BGM training).

### 2. Forced-alignment tools for precise word timings (lyric sheet known)

This is the highest-leverage change for failure (3): when the words are known, stop asking an autoregressive decoder for times and align instead.

- **Qwen3-ForcedAligner-0.6B (Jan 2026) — test first.** Non-autoregressive, single forward pass, predicts a start/end for every token, up to 5 min of speech per pass, 11 languages (zh, en, yue, fr, de, it, ja, ko, pt, ru, es), accepts transcripts from *any* ASR (worked example uses Parakeet CTC), Apache-2.0 — `verified live`, https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B-hf . Qwen claims ~42.9 ms average error vs 129.8 ms (NeMo FA) and 133.2 ms (WhisperX), 32.4 ms on human-labelled data — vendor numbers, `index` via https://www.transcribex.io/models/qwen3-asr/ . Independent Oct 2026 pilot (speech, not singing): 30.1 ms MAE clean TIMIT, 32.2 ms on FA-Bench TIMIT, degrading to 52.7 ms at 8 kHz — `verified live`, https://arxiv.org/html/2610.17782v2 . Weights ~1.8 GB (per Nightingale docs, `verified live`, https://nightingale.cafe/docs/lyrics/ ); PyTorch Transformers, bf16 — on a 6 GB CPU VM run it chunked per segment (≤5 min is not a constraint for a song) and sequentially after ASR, not in parallel. 80 ms output grid is its resolution limit.
- **WhisperX 3.8.6 (25 May 2026) — the proven fallback.** faster-whisper + wav2vec2 CTC forced alignment (+ optional pyannote diarization, skip it). Paper: 93.2% vs 85.4% precision at 200 ms tolerance vs Whisper — `index`, https://www.forasoft.com/learn/ai-for-video-engineering/articles-ai/whisperx-diarization-word-level-timestamps . Rule-of-thumb accuracy ~±50 ms on supported languages — `index`, https://whipscribe.com/blog/word-level-timestamps-whisper-2026 . CPU cost: ~3–8 min per song on CPU vs 30–90 s on GPU, ~3.5 GB model downloads — `index`, https://gabrielx.com/elysy-elizs-lyrics-synchronizer/ . wav2vec2 alignment models exist for ~40 languages; singing is out-of-domain for the speech-trained aligner, so expect worse than speech numbers on held vowels/chant. The production pattern is proven in Nightingale (karaoke app): isolated vocals → WhisperX large-v3 or Parakeet v3 → wav2vec2 alignment, with Qwen aligner as an experimental backend and torchaudio `forced_align` as a faster Viterbi — `verified live`, https://nightingale.cafe/docs/lyrics/ .
- **Montreal Forced Aligner (MFA) 3.x — most precise on clean *speech*, weakest fit for singing.** Pilot: 19.1 ms MAE, 68.2% of boundaries within 20 ms on clean TIMIT, RTF 0.021 on CPU (i.e. ~50× real time) — `verified live`, https://arxiv.org/html/2610.17782v2 ; FA-Bench table: MFA 21.8 ms vs Qwen 32.2 ms vs WhisperX 37.2 ms — `index`, https://scicom.app/newsroom/where-words-begin-and-end . But: needs a pronunciation dictionary + acoustic model per language, fails on ~1/5 utterances in some multilingual runs, and a 2024 singing study found the open MFA model only ~10% high-accuracy on singing audio (improved only after training on singing data) — `index`, https://drpress.org/ojs/index.php/jceim/article/download/19965/19545/24043 . Use only for English speech-like vocals; do not use as the singing default.
- **Scicom Whisper-Large-V3/Turbo aligners (Oct 2026, new) — watch/test second.** Whisper fine-tuned with LoRA to predict word start/end as timestamp tokens, trained on human boundaries (47 h, 87 langs): 11.6 ms on FA-Bench TIMIT, 16.0 ms on real landline calls vs 36.5 ms for MFA — `verified live`, https://arxiv.org/html/2610.17782v2 . Models at https://huggingface.co/collections/Scicom-intl/force-alignment , **CC BY-NC 4.0** (non-commercial — check before production use). No singing/music evaluation found.
- **CrisperWhisper 2.0 — promising, unproven on singing.** Fine-tuned Whisper with supervised cross-attention + DTW: ~30 ms mean boundary error on read speech, 41 ms conversational, verbatim mode, seamless long-form via conditional continuation — `index`, https://pypi.org/project/crisperwhisper/0.1.2/ . Speech/disfluency-focused; no lyrics benchmark.
- **whisper-timestamped / stable-ts — legacy.** DTW over Whisper cross-attention on a 20 ms grid; adequate, but strictly less precise than a forced aligner and no 2026 maintenance evidence found. The karaoke tool `lyrics-transcriber` (PyPI 0.81.0, Dec 2025) has moved to AudioShake/RunPod Whisper and is no longer a local CPU pipeline — `index`, https://pypi.org/project/lyrics-transcriber/0.81.0/ .
- **aeneas:** text-audio synchroniser, speech-oriented, no singing evidence and effectively unmaintained for this purpose — not recommended; no primary source worth citing was found in 2026.

**If the lyric sheet is known, the pipeline should be: transcribe (or take the sheet) → align with Qwen3-ForcedAligner per line/verse → fall back to WhisperX wav2vec2 for unsupported languages.** That decouples *what* was sung from *when*, which is exactly what fixes smear (3).

### 3. Vocal separation as pre-processing before ASR

**Yes, but the benefit is mostly in segmentation, not in feeding separated vocals to Whisper — and artifacts can hurt.**

The systematic study is Syed et al., "Exploiting Music Source Separation for Automatic Lyrics Transcription with Whisper" (arXiv:2506.15514, Jun 2025, ICME 2025 workshop) — `verified live`, https://arxiv.org/html/2506.15514v1/ , code https://github.com/jaza-syed/mss-alt :

- Short-form (~20 s groups), Whisper large-v2, beam 5: Jam-ALT WER — original mix 20.99%, Hybrid Demucs mdx separated 21.17%, mdx_extra 21.08% (no gain); MUSDB-ALT — 23.59% / 23.98% / 20.00% (gain with better separation); clean vocal *stems* 14.19% (large headroom — separation quality is the bottleneck, and current separators leave artifacts Whisper trips on).
- Long-form, RMS-VAD segmentation (boundaries from separated-vocal RMS, Cut & Merge, onset/offset 0.1, min silence 1 s, max 30 s): Jam-ALT original mix 23.02% → **20.35%**; separated vocals 22.87% → 20.72%; MUSDB-ALT original 25.82% → 22.72%, separated 21.90% → 20.07%. RMS-VAD on the *original mix* already achieves the new open-source SOTA on Jam-ALT — the gain is from boundaries, not vocal cleanliness.
- Separation artifacts can *trigger* hallucinations: hallucination proxy IR₁₀ (blocks of ≥10 sequential insertions) was consistently low for original audio and stems but higher for some separated-vocal cases; RMS-VAD reduced IR₁₀ (Jam-ALT original 1.31 → 0.35), supporting the hypothesis that segment boundaries interrupting vocal activity cause hallucinations.
- Whisper systematically deletes non-lexical vocables (ooh/ah/la) and backing vocals — over half deleted even on clean stems. Separation cannot fix this; expect chant vocables to be under-transcribed by any Whisper pipeline.

**What runs on CPU, and at what cost:**

| Separator | Quality (vocals SDR) | CPU cost | Verdict for 6 GB VM |
|---|---|---|---|
| **Demucs htdemucs / htdemucs_ft** (PyTorch) | 9.0 dB / 9.20 dB MUSDB-HQ | ~1.5× track length (guide); HT-Demucs FT ONNX: full bag RTF 0.49 on M4 Pro, PyTorch CPU RTF 0.69 for a 3-min song | **First choice.** `pip install demucs`, `--two-stems=vocals`. Run sequentially, not alongside Whisper. ONNX export (2026, StemSplit) is 1.31× faster than PyTorch on CPU and needs no PyTorch at inference — worth testing if Demucs is too slow. |
| **MDX-Net ONNX** (UVR_MDXNET_KARA_2.onnx) via `audio-separator` | Good karaoke-vocal model, widely used | ONNX Runtime CPU, lightweight | **Lightest practical choice.** `pip install audio-separator`, CPU install documented. Best if Demucs PyTorch is too heavy/slow. |
| **BS-Roformer / Mel-Band Roformer** via `audio-separator` / UVR | Best public: ~11.35 dB vocals (MVSep); BS-Roformer 12.72 dB with extra data | "Slow enough on CPU to leave running while you make dinner" | **Do not use on this VM** except as an offline quality reference. GPU-oriented. |
| **audio-separator 0.47.0** (Aug 2026, MIT) | — | CPU/GPU/Docker, pip | The CLI wrapper for MDX/Roformer/Demucs models; use it for MDX-Net ONNX. |

Sources: Demucs SDR/CPU — `index`, https://thestudiodesk.com/blog/best-ai-stem-separation-tools and https://tomodahinata.com/en/blog/demucs-v4-music-source-separation-production-guide ; ONNX Demucs — `index`, https://stemsplit.io/blog/htdemucs-ft-onnx-export ; audio-separator — `index`, https://pypi.org/project/audio-separator/ .

**Practical rule:** always transcribe *both* the original mix (segmented by RMS-VAD) and the separated vocals, and keep per-segment the output with the better confidence / fewer hallucinations. Never transcribe separated vocals with Whisper's *native* long-form segmentation — that combination is where the literature found "significant degradation".

### 4. Decoding and chunking techniques vs repetition loops / timestamp smear

All of these are cheap, testable today, and several map directly onto the four failure modes. Defaults quoted are faster-whisper / OpenAI Whisper unless noted.

**Against (2) repetition loops:**
- `condition_on_previous_text=False` — the single most effective change. With it on, each window is prompted with the previous window's text, so one repeated line seeds the next window indefinitely. Multiple 2026 guides and an experiment on 700 verified-silent chunks agree: VAD gate + this flag + a phrase filter cut hallucinations 61 → 3 — `index`, https://localaimaster.com/blog/whisper-hallucination-fix , https://typilot.com/blog/whisper-hallucinations-silence-fix , https://dev.to/ji_ai/whisper-hallucinates-on-silence-61-of-700-pauses-became-thank-you-2182 . Cost: slightly less cross-window consistency.
- **Keep the temperature fallback ladder** `(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)` — do *not* set a single temperature 0 for determinism. The ladder re-decodes when `compression_ratio_threshold` (2.4) or `logprob_threshold` (-1.0) trips, which is the guardrail that catches degenerate output. Disabling it was implicated in shipped repetition bugs — `index`, https://localaimaster.com/blog/whisper-hallucination-fix and https://dev.to/hackx-in/chunking-whisper-into-1-second-pieces-makes-dictation-slower-hmp (whisper.cpp: `no_timestamps=true` + `temperature_inc=0` produced the same sentence 24×; keep timestamps on).
- **Greedy / single-pass decoding with a token cap** for chant: the singing bench fixed a small-model loop ("oh, oh, oh" intro, 13 s per 4 s buffer) with "greedy, one pass, 160-token cap" — `verified live`, https://danicuki.substack.com/p/can-ai-hear-you-sing . In faster-whisper terms: `beam_size=1` (greedy) instead of the default beam 5, and cap output per segment.
- faster-whisper-only knobs: `repetition_penalty` (default 1 = off; try 1.1–1.2) and `no_repeat_ngram_size` (default 0 = off; try 3) — `index`, https://localaimaster.com/blog/whisper-hallucination-fix .
- **Post-filter (safety net, not first line):** collapse a phrase repeated ≥3× / a single word ≥5×, retry the chunk once with different decoding, then discard; drop segments whose `no_speech_prob` is high *and* text matches known boilerplate. A segment is skipped as silence only when *both* `no_speech_prob > no_speech_threshold` (0.6) *and* `avg_logprob < logprob_threshold` (-1.0) — tune the pair together, not one alone.

**Against (1) silence on loud/dense sections and (4) missed words:**
- **Pin the language** (`language="en"` etc.) — never auto-detect per window on songs. Auto-detection on 2 s of singing locked onto the wrong language (Italian → Hindi, Devanagari output) and language-switching failures caused whole-song silence in the bench — `verified live`, https://danicuki.substack.com/p/can-ai-hear-you-sing .
- **Do not use generic speech VAD aggressively on singing.** Held vowels, steady pitch and breath placement break speech VADs: the bench's Whisper sidecar went silent for 20 s over held "Ah"s, Deepgram Nova-3 multi produced zero words for 50 s, Gemini's VAD ended activity mid-line — `verified live`, https://danicuki.substack.com/p/can-ai-hear-you-sing . If using faster-whisper `vad_filter=True` (Silero VAD, default threshold 0.5, min silence 2000 ms, 400 ms padding), keep it conservative and try `min_silence_duration_ms=500` only as a test — and prefer RMS-VAD on *separated vocals* (§3) for segmentation, which is music-aware. A plain energy detector (50 ms frames, −42 dBFS floor, 500 ms hangover, 12 s cap) was enough to take Gemini from 41–55 to 63–80 in the same bench.
- **Loud/dense ≠ silent:** check the obvious before blaming the model — clipping/limiting in the mix, and Whisper's 30 s window being filled by a dense hook with no clean onset. Transcribing the separated vocal stem and the mix separately (§3) is the diagnostic: if the stem transcribes and the mix doesn't, it's masking, not a decoder failure.
- **Longer segments help:** ~20 s groups beat ~4 s lines by ~8 WER points in MSS-ALT (§3). Do not chop songs into 1–2 s pieces: Whisper's encoder always processes a 30 s window, so 1 s chunks cost ~10× the compute of 10 s chunks — `index`, https://dev.to/hackx-in/chunking-whisper-into-1-second-pieces-makes-dictation-slower-hmp .

**Against (3) timestamp smear in rapid chant:**
- Smear is a *decoder* artefact: Whisper emits segment timestamps and interpolates word times from cross-attention, drifting by seconds after silences. The fix is not a decoding knob — it is (§2) re-timing with a forced aligner, or (§1) a TDT/CTC model whose timestamps come from the acoustics. As a stopgap, keep `word_timestamps=True` (never `no_timestamps`), use short segments (RMS-VAD, ≤30 s, ideally verse-length), and cap words per segment so a single segment cannot smear across seconds.
- **Split-half / overlap strategy (proposed, not literature-proven):** decode each RMS-VAD segment twice — once as-is and once split at its midpoint with 2–3 s overlap — and keep the run whose word timings are monotonic and whose per-word durations are plausible (e.g. no word >2 s in rapid chant, no word spanning a detected vocal onset). This is a cheap consistency check to add to the test harness; no source was found validating it on lyrics, so treat it as an experiment, not a recommendation.

**Suggested faster-whisper starting config (test A/B against current):**
```python
model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
segments, _ = model.transcribe(
    wav, language="en",  # pin it
    word_timestamps=True,
    vad_filter=True, vad_parameters=dict(min_silence_duration_ms=500, threshold=0.5),
    condition_on_previous_text=False,
    beam_size=1,  # greedy for chant; compare beam_size=5 on non-chant
    temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
    compression_ratio_threshold=2.4, logprob_threshold=-1.0, no_speech_threshold=0.6,
    repetition_penalty=1.1, no_repeat_ngram_size=3,
)
# + post-filter: collapse >=3x repeated phrases / >=5x repeated single words; drop high-no_speech_prob boilerplate
```
Pin `av==18.1.0` (PyAV 19 breaks faster-whisper 1.2.1). Run Demucs/RMS-VAD segmentation *before* this call (segments as separate files, ≤30 s), not Whisper's native long-form.

### 5. 2026-new tools, papers, datasets, benchmarks for lyrics transcription

- **Qwen3-ASR family (29 Jan 2026)** — §1/§2. The single most important 2026 release for this pipeline: singing/BGM in the model card, best open ASR on the Oct 2026 leaderboard, plus a dedicated forced aligner. Technical report arXiv:2601.21337 (cited on the model card).
- **VocalParse (arXiv:2605.04613, May 2026)** — unified singing-voice transcription on a large audio-language model (built on Qwen3-ASR): joint lyrics + melody + word–note correspondence, lyric-conditioned mode, SOTA on singing datasets — `index`, https://arxiv.org/html/2605.04613v1 , code https://github.com/pymaster17/VocalParse . Research-grade, not a CPU pipeline; watch for a distilled / ONNX version.
- **"Where Words Begin and End" (arXiv:2610.17782, Oct 2026)** — the 2026 aligner benchmark (72 systems surveyed, 9 benchmarked on human boundaries) + released Whisper-LoRA aligners at 11.6 ms — `verified live`, https://arxiv.org/html/2610.17782v2 . Also a companion noise-robust aligner paper (arXiv:2610.22583) benchmarking Qwen3-FA / WhisperX / MFA on conversational and disfluent speech — `index`, https://arxiv.org/pdf/2610.22583 .
- **MSS-ALT / Jam-ALT / MUSDB-ALT (2025, current SOTA reference)** — §3. Jam-ALT benchmark site https://audioshake.github.io/jam-alt/ ; datasets https://huggingface.co/datasets/audioshake/jam-alt and https://huggingface.co/datasets/jazasyed/musdb-alt . No newer lyrics benchmark was found in 2026; Jam-ALT + MUSDB-ALT remain the evaluation sets to use for A/B testing.
- **LyricWhiz (ISMIR 2023) — no direct 2026 successor.** Whisper + GPT-4 multi-round + LLM correction; English Jam-ALT long-form WER 23.70, now beaten by RMS-VAD alone (20.35) without an LLM — `verified live` via MSS-ALT paper. Its 2026 descendants are LIWhiz (lyric *intelligibility* prediction for the ICASSP 2026 Cadenza Challenge, Whisper features — not transcription) and the Greek Interspeech 2026 Whisper fine-tuning study (2-stage adaptation of large-v3 → WER 27.2% on Greek songs) — `index`, https://arxiv.org/html/2512.17937v2/ and https://www.isca-archive.org/interspeech_2026/frangiadaki26_interspeech.pdf . Lesson: fine-tuning Whisper on singing helps, but no off-the-shelf singing fine-tune was found.
- **Singing ASR bench (Oct 2026, independent)** — Cukier, §1/§4: https://danicuki.substack.com/p/can-ai-hear-you-sing . Small (593 words) but the only 2026 bench that measures *singing* rather than speech, and the only one to reproduce failure modes (1) and (2) with named causes.
- **CrisperWhisper 2.0 (2026)** — §2. **audio-separator 0.47.0 (Aug 2026)** and **HT-Demucs FT ONNX export (2026)** — §3. **faster-whisper 1.2.1 / WhisperX 3.8.6 / whisper.cpp 1.9.5** — maintenance status in §1/§2; note faster-whisper appears unmaintained since Nov 2025, which is a risk for the PyAV-19 class of breakage.
- **No 2026 lyrics-specific fine-tune, dataset or benchmark was found that is directly deployable on a 6 GB CPU VM.** The gap is real: the field's 2026 work is Qwen3-ASR / VocalParse (large, GPU) and aligner benchmarks (speech).

## Ranked shortlist — what to test first

Test on 3–5 of your own worst tracks (one per failure mode + one clean control), with the known lyric sheet where available. Score: WER (jiwer) + words recovered in the failing span + % words with plausible durations + wall time / peak RAM.

| # | Test | Install / CPU cost (6 GB VM) | Word-timestamp accuracy | Failure modes addressed |
|---|---|---|---|---|
| 1 | **Fixed faster-whisper config** (§4 snippet): turbo (or distil-large-v3 if EN-only), pinned language, conservative VAD, `condition_on_previous_text=False`, greedy + token cap, fallback ladder kept, repetition penalty/ngram, post-filter; pin PyAV 18.1.0 | `pip install faster-whisper av==18.1.0`; turbo int8 ~1.5 GB RAM, minutes per song on CPU | Native Whisper words, ~<200 ms typically, worse after silence — still the weak link | (1) partial (language pin + VAD discipline), (2) yes, (3) partial, (4) partial |
| 2 | **Demucs htdemucs → RMS-VAD segments (≤30 s, min silence 1 s) → transcribe mix + separated vocals, keep better per segment** | `pip install demucs`; ~1.5× track length CPU, run sequentially; or MDX-Net ONNX via `audio-separator` if lighter | Same as #1 per segment, but boundaries no longer cut words — the MSS-ALT SOTA recipe (20.35% vs 23.02% WER) | (1) yes, (2) yes (boundaries), (4) yes; (3) no |
| 3 | **Known lyrics → Qwen3-ForcedAligner-0.6B** (fallback WhisperX wav2vec2 for unsupported langs) | `pip install transformers` (from source until official release); ~1.8 GB weights, single forward pass per segment, sequential after ASR | ~30–43 ms MAE (speech benchmarks; singing unmeasured) vs WhisperX ~37–77 ms, MFA ~19 ms on clean speech | (3) yes — this is the fix for smear; (1)(2)(4) no (timing only) |
| 4 | **Parakeet TDT 0.6B v3 via sherpa-onnx / onnx-asr** (CPU ONNX), A/B vs #1+#2 | `pip install sherpa-onnx` / `onnx-asr`; 600 M ONNX int8, small RAM, fast on CPU (speech RTF ~0.03) | Native TDT word timestamps (duration per token) — no published lyrics accuracy | (2) yes (no autoregressive loop), (3) yes (duration prediction); (1)(4) unproven on singing |
| 5 | **Qwen3-ASR-0.6B + Qwen3-ForcedAligner** | Transformers/vLLM, 0.6 B; GPU-oriented, CPU trial only — expect slow, RAM-tight | Aligner as #3 | (1)(4) possibly (singing/BGM training); (2)(3) via aligner |
| 6 | **Watch / later:** Scicom Whisper-LoRA aligner (11.6 ms, NC licence), CrisperWhisper 2.0, VocalParse, BS-Roformer (quality reference only, too slow on CPU) | — | — | — |

**Do not test first:** Whisper `small` with default settings (current pipeline — the baseline to beat); `large-v3` full (no accuracy gain over turbo worth 2× RAM/CPU here); MFA as the singing aligner; Roformer on CPU; Moonshine (no word timestamps); `lyrics-transcriber` (now cloud-based); aeneas / stable-ts (superseded).

## Could not verify / open questions

- **No CPU benchmark on singing exists for Parakeet, Qwen3-ASR-0.6B, SenseVoice or the Qwen aligner.** All CPU speed claims above are speech benchmarks or vendor claims; singing (held vowels, chant, dense mixes) changes VAD, decoding time and accuracy. The A/B on your own tracks is the verification step — do not adopt on specs alone.
- **Qwen3-ForcedAligner on singing / chant:** its 30–43 ms figures are read/conversational speech; held vowels and rapid chant may degrade it like every other aligner. No lyrics-specific evaluation found.
- **Turbo vs small CPU time on your VM:** sources conflict (turbo's encoder is identical to large-v3, so CPU gains are small; faster-whisper is much faster than whisper.cpp on CPU). Measure wall time for one song before committing.
- **faster-whisper maintenance:** last release 1.2.1 (Oct 2025), last commit Nov 2025; the PyAV 19 breakage is a symptom. If it breaks again, the fallback is whisper.cpp (actively maintained, 1.9.5) or sherpa-onnx.
- **Licences for production video work:** Whisper MIT; Demucs code MIT but weights "mainly for research use" (check before commercial use); Qwen Apache-2.0; Parakeet CC-BY-4.0; Scicom aligner CC BY-NC 4.0 (non-commercial); BS-Roformer community weights vary. Verify per-model before shipping.
- **Split-half / overlap re-decode (§4):** proposed by this research, not found in literature — unvalidated.
- **Non-lexical vocables / backing vocals:** the literature shows >50% are deleted even on clean stems; no tool found solves this. If chant vocables ("oh/ah/la") must appear in the video, budget for lyric-sheet alignment (§2) rather than pure ASR.

## Sources

- Syed et al., Exploiting Music Source Separation for ALT with Whisper, arXiv:2506.15514 — https://arxiv.org/html/2506.15514v1/ (`verified live` 2026-11-10); code https://github.com/jaza-syed/mss-alt ; Jam-ALT https://audioshake.github.io/jam-alt/
- Cukier, Can AI Hear You Sing?, Oct 2026 — https://danicuki.substack.com/p/can-ai-hear-you-sing (`verified live`)
- Qwen3-ForcedAligner-0.6B model card — https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B-hf (`verified live`); Qwen3-ASR-1.7B — https://huggingface.co/Qwen/Qwen3-ASR-1.7B-hf (`verified live`)
- Nightingale lyrics/transcription docs — https://nightingale.cafe/docs/lyrics/ (`verified live`)
- Where Words Begin and End, arXiv:2610.17782 — https://arxiv.org/html/2610.17782v2 (`verified live`); summary https://scicom.app/newsroom/where-words-begin-and-end (`index`)
- VocalParse, arXiv:2605.04613 — https://arxiv.org/html/2605.04613v1 (`index`)
- NVIDIA Parakeet/Canary — https://developer.nvidia.com/blog/nvidia-speech-ai-models-deliver-industry-leading-accuracy-and-performance/ (`index`); Canary/Parakeet v3 paper https://arxiv.org/html/2509.14128v1 (`index`)
- WhisperX guide — https://www.forasoft.com/learn/ai-for-video-engineering/articles-ai/whisperx-diarization-word-level-timestamps (`index`); word-timestamp comparison https://whipscribe.com/blog/word-level-timestamps-whisper-2026 (`index`); ELYSY/WhisperX CPU timings https://gabrielx.com/elysy-elizs-lyrics-synchronizer/ (`index`)
- faster-whisper / PyAV gotcha — https://www.pyinns.com/python/llm-and-generative-ai/speech-to-text-python-faster-whisper-2026 (`index`); https://whipscribe.com/tools/faster-whisper (`index`)
- Whisper CPU speeds — https://runaihome.com/blog/whisper-large-v3-self-hosted-transcription-server-2026/ (`index`); https://www.logeshwaran.org/2026/10/run-whisper-locally.html (`index`); https://www.promptquorum.com/power-local-llm/local-whisper-stt-comparison (`index`)
- Hallucination/repetition fixes — https://localaimaster.com/blog/whisper-hallucination-fix (`index`); https://typilot.com/blog/whisper-hallucinations-silence-fix (`index`); https://dev.to/ji_ai/whisper-hallucinates-on-silence-61-of-700-pauses-became-thank-you-2182 (`index`); https://dev.to/hackx-in/chunking-whisper-into-1-second-pieces-makes-dictation-slower-hmp (`index`)
- Separation tools — https://thestudiodesk.com/blog/best-ai-stem-separation-tools (`index`); https://stemsplit.io/blog/htdemucs-ft-onnx-export (`index`); https://pypi.org/project/audio-separator/ (`index`); https://tomodahinata.com/en/blog/source-separation-asr-preprocessing-whisper-accuracy (`index`); https://tomodahinata.com/en/blog/demucs-v4-music-source-separation-production-guide (`index`)
- FunASR / SenseVoice / Paraformer — https://www.funasr.com/en/models.html (`index`); self-hosted STT survey https://awesomeosai.com/self-hosted/speech-to-text (`index`)
- Speech CPU harness (Parakeet RTF) — https://metavert.io/speech-recognition (`index`)
- CrisperWhisper 2.0 — https://pypi.org/project/crisperwhisper/0.1.2/ (`index`)
- LyricWhiz — https://arxiv.org/html/2306.17103v4 (`index`); lyrics-transcriber — https://pypi.org/project/lyrics-transcriber/0.81.0/ (`index`)
- MFA singing study — https://drpress.org/ojs/index.php/jceim/article/download/19965/19545/24043 (`index`); Greek ALT Interspeech 2026 https://www.isca-archive.org/interspeech_2026/frangiadaki26_interspeech.pdf (`index`); LIWhiz/Cadenza https://arxiv.org/html/2512.17937v2/ (`index`)
- Qwen3-ASR singing/BGM and leaderboard — https://medium.com/@andrew22dev/the-best-open-source-speech-to-text-models-to-self-host-in-2026-6cc5a8abc134 (`index`); https://www.transcribex.io/models/qwen3-asr/ (`index`)
