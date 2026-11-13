# Can AI Hear You Sing? — Cukier, Oct 2026
URL: https://danicuki.substack.com/p/can-ai-hear-you-sing — read 2026-11-10, verified live
- 9 clips real singing, 4 languages + medley, 593 words, Demucs vocal stems. Whisper large-v3-turbo (MLX, M3 Max) 88/100 best accuracy + best language switching, free. ElevenLabs 85, fastest final 1.1s.
- Failure mode (1) reproduced: Whisper sidecar produced nothing for 20s across held-vowel bridge of Garota de Ipanema; ElevenLabs 95 vs Whisper 79 on that take. Cause unpinned: VAD gate or decoder.
- Speech VAD/endpointing is the recurring villain: Deepgram Nova-3 multi produced zero words for 50s of 99 Luftballons; Gemini Live VAD declared ACTIVITY_END mid-line, 11-12s holes. Fix: disable server VAD, own energy detector (50ms frames, -42 dBFS floor, 500ms hangover, 12s cap) took Gemini 41-55 -> 63-80.
- Repetition loop (2): on "oh, oh, oh" intro, Whisper small spent 13s decoding each 4s buffer in repetition loop under beam search + temperature fallback re-decoding up to 6x. Fix reported: greedy, one pass, 160-token cap.
- Pin language when known; language locked from 2s guess (medium heard Italian as Hindi 59%, wrote Devanagari). Only a final with >=4 words can lock language in their fix.
- German weakest everywhere; only Whisper turbo >70.
- Note: small corpus, one run per engine, Demucs stems not stage mic.
