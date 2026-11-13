# wubuwizard — MDX-Net ONNX vocal separation on CPU (torch-free)

A model-runner example (not a Demucs home): run the UVR-MDX-NET-Voc_FT
model with onnxruntime on CPU, no torch. Sprint 2026-11-12:
**corr 0.9675 vs Demucs, but 1.78× SLOWER** — adopted as the torch-free
fallback segmenter, not the faster one. (c11_sep is the fast path.)

## Files

- `mdx_onnx_cpu.py` — the runner (chunked STFT → ONNX → ISTFT →
  vocal/instrumental WAVs). Recipe: n_fft=6144, hop=1024, dim_f=3072,
  dim_t=256.
- `check_parity.py` — parity check of the ONNX output vs a reference
  separation.

## Model (NOT in this repo)

`UVR-MDX-NET-Voc_FT.onnx` (66 MB) is a third-party model file — fetch
it from the UVR / audio-separator model hub (`UVR-MDX-NET-Voc_FT.onnx`)
and point the runner at it. A copy also lives in the original workspace
under `tools/audio-separator-models/`.

## Traps (banked)

- audio-separator's `model-data.json` holds parameters for a DIFFERENT
  MDX model — do not trust it for this one; the recipe above is the
  measured one.
- `torch.stft(center=True)` reflect-pads; the C11 STFT in c11_sep had
  the same zero-pad error — fixed there.

Full report: `../research/detection-research/SPRINT_2026-11-12_WUBUWIZARD_CPU_DEMUCS_UVR.md`.
