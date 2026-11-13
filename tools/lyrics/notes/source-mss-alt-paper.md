# MSS-ALT paper — Syed et al. 2025
URL: https://arxiv.org/html/2506.15514v1/ — read 2026-11-10, verified live (browser_open)
Also: https://github.com/jaza-syed/mss-alt ; datasets https://huggingface.co/datasets/audioshake/jam-alt , https://huggingface.co/datasets/jazasyed/musdb-alt

- Jam-ALT 79 songs/283min, MUSDB-ALT 39 songs/166min. Faster-whisper, Whisper large-v2, beam 5, language provided.
- Short-form groups (~20s): Jam-ALT WER original 20.99, separated mdx 21.17, mdx_extra 21.08; MUSDB-ALT 23.59 / 23.98 / 20.00; vocal stem 14.19. So separation alone: ~no gain on Jam-ALT, clear gain on MUSDB-ALT, stems far better — separation quality/artifacts matter.
- Long-form: native vs RMS-VAD. Jam-ALT original mix 23.02 -> 20.35 with RMS-VAD; separated 22.87 -> 20.72. MUSDB-ALT original 25.82 -> 22.72; separated 21.90 -> 20.07; stem 17.51 -> 14.98. RMS-VAD = Hybrid Demucs separated vocals, RMS/VAD score, Cut & Merge, onset/offset 0.1, min silence 1s, max segment 30s. Improvement comes from better segment boundaries, not vocal quality (similar on mix and separated).
- RMS-VAD reduces hallucination proxy IR10 (blocks of >=10 sequential insertions): e.g. Jam-ALT original 1.31 -> 0.35. Hypothesis: boundaries interrupting vocal activity cause hallucinations.
- Whisper systematically deletes non-lexical vocables (ooh/ah/la) and backing vocals: >half deleted even on clean stems; separation cannot fix.
- Longer context helps: groups ~20s much lower WER than merged lines ~3.5-4.6s (Jam-ALT 20.99 vs 29.46 original).
- LyricWhiz English Jam-ALT long-form WER 23.70; RMS-VAD original-mix 20.35 is new open-source SOTA on Jam-ALT, close to LyricWhiz effect without LLM/multiple rounds.
