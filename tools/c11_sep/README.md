# c11_sep — C11 MDX-Net vocal/instrumental separator (SLERM)

Sprint 2026-11-12. **Verdict: PASS — all four validation bars met on the full MV-14 track**
(parent-verified; committed as `a2b435bd` in wubutv-network).

Replaces Demucs (torch) as the pipeline segmenter. Pure C11 + the ONNX
weights: no torch, no Python at inference. The ONNX graph
(UVR-MDX-NET-Voc_FT, n_fft=6144, hop=1024, dim_f=3072, dim_t=256) is
interpreted op-by-op in `sep_main.c` / `sep_ops.c` (Conv, MatMul, BN,
GRU-ish recurrences via `sep_gemm.c`, STFT/ISTFT in `sep_stft.c`,
FFT in `sep_fft.c` / `sep_fft64.c`).

## Validation (all in this dir)

| Bar | Result |
|---|---|
| Stem corr vs Demucs | **0.9675** |
| RMS-VAD max \|dStart\| vs Demucs | **0.21 s** |
| Active/silent separation | **242.7×** |
| Runtime, full MV-14 track | **840.4 s** (bar < 894 s; 650 s target NOT met) |

Stage parity JSONs: `stage1_stft_parity.json`, `stage2_block1_parity.json`,
`stage3a_gemm.json`, `stage3b_interp_parity.json` (24/24 checkpoints PASS),
`stage4_fulltrack_validation.json`. `weights_index.json` maps every weight
tensor to its chunk file.

## Build

```sh
make sep_main       # the runner (libc + libm only, -O3 -march=native, OpenMP)
make test_stft test_interp test_block1   # unit tests
make clean
```

## Run

Weights are **not** in this repo (125 `.bin` chunks, ~350 MB). Regenerate
them from the model with `extract_weights.py` (needs the ONNX model —
see `../wubuwizard/README.md` for where to fetch it), then run
`sep_main` per the usage in `SPRINT_2026-11-12_C11_SEP.md`
(`../../research/detection-research/`).

## Known limits

- 650 s runtime target not met — next lever is int8 quantized-matmul
  (scoped, not built).
- Two traps found during the sprint, fixed in-tree: interpreter ops read
  tensor shapes from the instruction dims, never from the reused slot
  table (slot-shape aliasing silently corrupted a BN node); lookup
  tables are built eagerly in the constructor, never lazily under
  OpenMP (lazy build raced the first parallel FFT call).
