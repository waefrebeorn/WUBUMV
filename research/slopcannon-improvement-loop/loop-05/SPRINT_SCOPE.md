# SPRINT_SCOPE.md — c11_sep (Slopcannon improvement loop 5, top-1)

**Sprint:** c11_sep — C11 separation runner (MDX-Net/Demucs, torch-free, faster than Demucs).
**Parent:** loop 5 report §0 (adoption decided) + §3 #1. **Goal:** separate a
track faster than torch Demucs' 894 s on the blade, torch-free, validated
against the MDX-Net ONNX port (which loop 5 adopted as-is as the pipeline's
segmenter). The ONNX port proves the recipe and supplies the validation
target; c11_sep is the sprint that makes it cheap.

**Held bar — runtime <894 s on the blade** (target: int8 path at 2–4×
realtime, i.e. <650 s for the 161.6 s MV-14 track), **stem corr ≥0.95 vs the
Demucs stem, RMS-VAD boundaries within ±0.5 s of `hpss_mv14_ref.json`,
active/silent RMS ratio ≥100×.** Do NOT lower any bar. Do NOT re-run sprint
8's calibration. Do NOT touch c11_voice's code except to lego in its
autocorrelation/YIN machinery if needed (it is not needed for this sprint).

## 1. Problem

The pipeline's segmentation job now runs on the MDX-Net ONNX port (loop 5
adopted it as-is: full-track corr 0.9676 vs Demucs, 17 RMS-VAD segments,
active/silent 248.8× — verified in loop 5). The port WORKS but is 1.78×
SLOWER than torch Demucs (1,592 s vs 894 s) because the ONNX model eats 95%
of each chunk on 1.5 shared CPUs. Torch Demucs is broken in the current venv
(the torchvision `operator torchvision::nms does not exist` clash), so there
is no fast separator available at all — only the slow working one. The
classical sensor search is over (voicing, vibrato, formants, entropy, CASA
all failed); separation is the only route to a voice-activity sensor, and
its cost is now the pipeline's bottleneck. The C11 runner is the only route
that plausibly beats 894 s: a quantized-matmul U-Net forward in C11.

## 2. Background (verified, cite in the sprint report)

- UVR v5 MDX-Net recipe (audio-separator 0.48.0 source, read by the
  wubuwizard sprint): n_fft=6144, hop=1024, dim_f=3072, dim_t=256,
  segment_size=256, chunk_size=261,120, gen_size=254,976, trim=3,072,
  compensate=1.01, overlap=0.25, batch_size=1, denoise off; complex
  spectrogram in/out ([L_re, L_im, R_re, R_im]); first 3 bins zeroed;
  Hann-window overlap-add; mix peak-normalized to 1.0 then rescaled;
  instrumental = mix − vocals×1.01.
- The ONNX graph is authoritative for the model params:
  `UVR-MDX-NET-Voc_FT.onnx` (66,762,490 B, SHA-256
  `534b2070fcc7df514b13ef660dc8cbb328679c2374d04354a5c42bb14ecce111`) —
  audio-separator's model-data.json holds params for a DIFFERENT MDX model
  (n_fft 5120 / dim_f 2560); do not trust it. The graph input
  `['batch_size', 4, 3072, 256]` → dim_f=3072 → n_fft=6144.
- torch.stft(center=True) REFLECT-pads, it does not zero-pad (wubuwizard
  trap 2, verified: reflect-pad matches center=True exactly, max diff 0.0;
  zero-pad disagrees by max 22.3 on chunk edges). WuBuRVC's `wubu_stft.c`
  carries the same wrong assumption — fix it before it fronts this runner.
  scipy scales its STFT by 1/sum(window) (= 1/3072 at n_fft 6144) while
  torch returns raw DFT sums — multiply on STFT, divide on ISTFT.
- Wubuwizard runner patterns (lego-harvest-scratch/wubuwizard): kernel
  dispatch table (`wubu_kernel.h`), thread pool with no atomics
  (`thread_pool.h`), quantized matmul Q8_K (`quantized_matmul.c`,
  `quantized_dot_generic.c`), GGUF + safetensors readers, tensor store.
- WuBuRVC engine plumbing (waefrebeorn/WuBuRVC, surveyed via GitHub API):
  C11 STFT + FFT (`wubu_stft.c`, `wubu_fft.c`), audio IO + resample
  (`wubu_audioio.c`), weight-extraction pattern (`.pth` → flat `WUBU`
  binary), inference plumbing + parity method (`wubu_rvc_parity.c`),
  RMVPE pitch tracker (corr 0.9999 — the §3 #5 vibrato arbiter, NOT this
  sprint's job).

## 3. Inputs (all exist, all on disk)

- Model: `~/workspace/wubuwizard-cpu-sep/UVR-MDX-NET-Voc_FT.onnx` (scratch
  only, never commit).
- Executable spec: `~/workspace/wubuwizard-cpu-sep/mdx_onnx_cpu.py` (the
  UVR recipe in numpy/scipy + onnxruntime) + `check_parity.py`.
- Validation targets: `mdx_vocals_full.wav` / `mdx_inst_full.wav`
  (161.6 s, the adopted segmenter's own outputs) +
  `detection-research/c11_mir/separation_mv14/mv14_44k_(Vocals)_htdemucs.wav`
  (Demucs reference stem) + `c11_mir/hpss_mv14_ref.json` (12 ref segments)
  + `c11_mir/make_ref_segments.py` (RMS-VAD recipe, verbatim).
- Lego bin: `~/workspace/lego-harvest-scratch/wubuwizard/` (kernel, thread
  pool, quantized matmul, readers) + WuBuRVC pieces (surveyed; lego the
  C files from the user's own repos per the LEGO RULE, msg 233).

## 4. Lego in (do not rewrite)

- `wubu_audioio.c` (WuBuRVC) — WAV read/write + resample, as-is.
- `wubu_fft.c` + `wubu_stft.c` window/FFT tables (WuBuRVC) — extend to
  complex-out + ISTFT, and **fix the padding: reflect, not zeros** (§2).
- `wubu_kernel.h` dispatch + `thread_pool.h` (wubuwizard) — conv/GEMM
  dispatch, per-frame parallel STFT.
- `quantized_matmul.c` / `quantized_dot_generic.c` (wubuwizard) — int8 GEMM
  for the U-Net convolutions.
- Weight-extraction pattern from WuBuRVC `tools/extract_*_weights.py` —
  `.onnx` → flat `WUBU` binary (fp16→fp32), loadable without ORT/torch.
- Parity method from `wubu_rvc_parity.c` — C11 vs reference corr checks at
  every stage (STFT → layer outputs → stem).

## 5. Write from scratch

- MDX-Net U-Net forward in C11 (conv blocks, norms, the 3072-bin ×
  256-frame complex-spectrogram path) — the model graph is the spec;
  extract each layer's weights with the WuBuRVC pattern.
- The UVR chunking / overlap-add driver (`mdx_onnx_cpu.py` is the
  executable spec: chunk 261,120, overlap 0.25, trim 3,072).
- ONNX weight reader *or* a one-shot extractor that dumps the .onnx
  tensors to the flat format (safetensors_reader/gguf_reader patterns
  cover the file-format half; the ONNX protobuf parse is the new piece —
  or extract with onnxruntime once, in Python, and ship the flat file).

## 6. Validation bar (same as the wubuwizard sprint's)

1. STFT parity vs torch ≤1e-4 (max|diff|, float32).
2. Stem corr vs Demucs ≥0.95 (full track, mono).
3. RMS-VAD boundaries ±0.5 s of `hpss_mv14_ref.json` (starts within 0.21 s
   is the MDX port's measured level; match it, don't beat it as a bar).
4. Active/silent RMS ratio ≥100× on the ref masks (MDX port measured
   248.8× in loop 5's re-check; Demucs 203.7× on the same masks).
5. **Runtime <894 s on the blade** (target <650 s). If the C11 forward
   can't beat ORT's ~32 s/chunk, the sprint reports that with the numbers
   and the ONNX port stays the torch-free fallback — the fail-fast is part
   of the scope, not a failure to report.

## 7. Experiment-first rule (the loop-4 lesson, applied)

Before writing the full U-Net forward, build the smallest end-to-end slice
first: STFT → ONE conv block → ISTFT, parity-checked against the ONNX
port's layer outputs at each stage. If the single-block parity fails, stop
and report — do not write the remaining blocks on a broken foundation.
The wubuwizard sprint's parity method (§4) is the template: corr checks at
every stage, no number without a disk source.

## 8. What this sprint does NOT do

- No change to the adoption decision (MDX-Net ONNX as-is is the segmenter
  until c11_sep passes its bar — the bar, not the sprint, decides the swap).
- No RMVPE vibrato arbiter (§3 #5 of the loop-5 report — a separate
  measurement, not this sprint).
- No mouth-open/CCA/stay-rule calibration — those calibrate on the MDX
  stem-activity curve (§3 #2 of the loop-5 report) once c11_sep makes the
  stem cheap, or on the ONNX stem now; they are not this sprint's bars.
- No Demucs model run (torch is broken in this venv; the 894 s figure is
  sprint 6's measured number, reused).

## 9. Files (to be written by the sprint)

- `detection-research/SPRINT_2026-11-12_C11_SEP.md` — sprint report.
- `detection-research/c11_sep/` — C11 runner + validation JSON + parity
  scripts + run logs.
- `DETECTION_FINDERS.md` run entry.
- No commit (parent owns commits). No video generation, no Telegram.
