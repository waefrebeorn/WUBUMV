#!/usr/bin/env python3
"""Standalone UVR MDX-Net ONNX CPU runner — torch-free.

Faithful port of audio-separator 0.48.0 MDXSeparator (UVR v5 recipe),
with torch replaced by scipy + onnxruntime only. The lyrics venv's
torchvision/torch 2.15 clash breaks `import audio_separator` for the MDX
path (torchvision::nms missing), so this file re-implements the recipe
directly: same STFT, same chunking, same overlap-add, same ONNX model.

Recipe constants (UVR-MDX-NET-Voc_FT.onnx):
  n_fft=6144, hop=1024, dim_f=3072, dim_t=256, segment_size=256,
  chunk_size=261120, gen_size=254976, trim=3072, compensate=1.01,
  overlap=0.25, batch_size=1, denoise off.
  NOTE: audio-separator's model-data.json holds params ONLY for hash
  cb790d0c... (a different MDX model: n_fft 5120 / dim_f 2560, primary
  Instrumental) — the Voc_FT file's MD5 (d21dc03e...) is NOT in it, and
  the graph itself demands dim_f=3072, so n_fft=6144 is the only
  consistent FFT size (n_bins 3073, truncated to 3072). Verified
  empirically by the excerpt run (vocal/silent contrast + correlation
  vs the Demucs stem — see the sprint report).
STFT: periodic Hann, center=True (zero pad n_fft//2 both sides).
Model input: [1, 4, 2560, T] float32, channels [L_re, L_im, R_re, R_im]
(complex spectrogram — the model outputs the separated complex spec).
"""
import argparse
import time

import numpy as np
import onnxruntime as ort
from scipy.io import wavfile
from scipy.signal import get_window, istft, stft

N_FFT = 6144
HOP = 1024
DIM_F = 3072
SEGMENT_SIZE = 256
CHUNK_SIZE = HOP * (SEGMENT_SIZE - 1)          # 261120
TRIM = N_FFT // 2                               # 3072
GEN_SIZE = CHUNK_SIZE - 2 * TRIM                # 254976
OVERLAP = 0.25
COMPENSATE = 1.01
WINDOW = get_window("hann", N_FFT, fftbins=True)  # periodic Hann == torch.hann_window
# scipy.signal.stft scales its output by 1/sum(window) (== 1/2560 here) while
# torch.stft returns raw DFT sums; istft expects the scaled convention.
# Multiply on STFT / divide on ISTFT to match torch exactly (parity-checked).
WIN_SUM = float(np.sum(WINDOW))


def stft_complex(mix):
    """mix: [2, T] float32 -> [4, DIM_F, frames] float32, channels [L_re, L_im, R_re, R_im].

    Parity-verified vs torch.stft(center=True): torch center-pads with
    REFLECTION (not zeros — reflect gives max|diff| 0.0, zeros gives 23.8),
    so pad explicitly with np.pad(mode='reflect') and use
    boundary=None/padded=False. scipy also scales its output by
    1/sum(window); multiply back (WIN_SUM) to match torch's raw DFT sums.
    """
    pad = N_FFT // 2
    chans = []
    for ch in range(2):
        x = np.pad(mix[ch], pad, mode="reflect")
        _, _, z = stft(x, fs=44100, window=WINDOW, nperseg=N_FFT,
                       noverlap=N_FFT - HOP, nfft=N_FFT, boundary=None, padded=False)
        chans.append(z[:DIM_F, :] * WIN_SUM)
    re_im = np.stack([chans[0].real, chans[0].imag, chans[1].real, chans[1].imag])
    return re_im.astype(np.float32)


def istft_complex(spec):
    """spec: [4, DIM_F, frames] float32 -> [2, T] float32 (explicit pad, manual trim)."""
    pad = N_FFT // 2
    out = []
    for ch in range(2):
        z = (spec[ch * 2] + 1j * spec[ch * 2 + 1]) / WIN_SUM
        z = np.vstack([z, np.zeros((1, z.shape[1]), dtype=np.complex128)])
        _, x = istft(z, fs=44100, window=WINDOW, nperseg=N_FFT,
                     noverlap=N_FFT - HOP, nfft=N_FFT, boundary=False)
        out.append(x[pad:-pad].astype(np.float32))
    return np.stack(out)


def run_model(session, spek):
    """spek: [1, 4, DIM_F, T] -> same shape."""
    return session.run(None, {"input": spek})[0]


def demix(session, mix):
    """mix: [2, T] float32, peak-normalized. Returns separated [2, T] float32."""
    step = int((1 - OVERLAP) * CHUNK_SIZE)
    pad = GEN_SIZE + TRIM - (mix.shape[-1] % GEN_SIZE)
    mixture = np.concatenate(
        (np.zeros((2, TRIM), dtype=np.float32), mix,
         np.zeros((2, pad), dtype=np.float32)), axis=1)
    result = np.zeros((1, 2, mixture.shape[-1]), dtype=np.float32)
    divider = np.zeros((1, 2, mixture.shape[-1]), dtype=np.float32)
    n_chunks = (mixture.shape[-1] + step - 1) // step
    t0 = time.time()
    for i, start in enumerate(range(0, mixture.shape[-1], step)):
        end = min(start + CHUNK_SIZE, mixture.shape[-1])
        actual = end - start
        window = None
        if OVERLAP != 0:
            window = np.hanning(actual).astype(np.float32)
            window = np.tile(window[None, None, :], (1, 2, 1))
        part = mixture[:, start:end]
        if end != start + CHUNK_SIZE:
            part = np.concatenate(
                (part, np.zeros((2, (start + CHUNK_SIZE) - end), dtype=np.float32)), axis=-1)
        spek = stft_complex(part)[None, :, :, :]           # [1, 4, 3072, 256]
        spek[:, :, :3, :] = 0                           # zero first 3 bins (UVR recipe)
        spec_pred = run_model(session, spek)
        tar = istft_complex(spec_pred[0])               # [2, CHUNK_SIZE]
        tar = tar[None, :, :]
        if window is not None:
            tar[..., :actual] *= window
            divider[..., start:end] += window
        else:
            divider[..., start:end] += 1
        result[..., start:end] += tar[..., : end - start]
        if (i + 1) % 5 == 0 or i + 1 == n_chunks:
            print(f"  chunk {i + 1}/{n_chunks}  {time.time() - t0:.1f}s", flush=True)
    tar_waves = result / np.maximum(divider, 1e-8)
    tar_waves = tar_waves[:, :, TRIM:-TRIM]
    return tar_waves[0][:, : mix.shape[-1]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("input_wav")
    ap.add_argument("out_vocals")
    ap.add_argument("--out-inst", default=None)
    ap.add_argument("--excerpt", type=float, default=None,
                    help="only process the first N seconds (validation)")
    ap.add_argument("--threads", type=int, default=2)
    args = ap.parse_args()

    sr, data = wavfile.read(args.input_wav)
    assert sr == 44100, f"expected 44100 Hz, got {sr}"
    mix = data.astype(np.float32)
    if data.dtype == np.int16:
        mix = mix / 32768.0
    if mix.ndim == 1:
        mix = np.stack([mix, mix])
    else:
        mix = mix.T  # [2, T]
    if args.excerpt:
        mix = mix[:, : int(args.excerpt * sr)]
    print(f"mix: {mix.shape[1] / sr:.2f}s, peak {np.abs(mix).max():.4f}")

    peak = np.abs(mix).max()
    mix_n = mix / peak if peak > 0 else mix

    so = ort.SessionOptions()
    so.intra_op_num_threads = args.threads
    so.inter_op_num_threads = 1
    so.log_severity_level = 3
    t0 = time.time()
    session = ort.InferenceSession(args.model, providers=["CPUExecutionProvider"],
                                   sess_options=so)
    print("model loaded in %.1fs; input %s" % (
        time.time() - t0,
        session.get_inputs()[0].shape))
    t0 = time.time()
    vocals = demix(session, mix_n) * peak
    wall = time.time() - t0
    print(f"demix done: {wall:.1f}s wall for {mix.shape[1] / sr:.1f}s of audio "
          f"({wall / (mix.shape[1] / sr):.2f}x realtime)")
    wavfile.write(args.out_vocals, sr, (np.clip(vocals.T, -1, 1) * 32767).astype(np.int16))
    print("wrote", args.out_vocals)
    if args.out_inst:
        inst = (-vocals * COMPENSATE) + mix
        wavfile.write(args.out_inst, sr, (np.clip(inst.T, -1, 1) * 32767).astype(np.int16))
        print("wrote", args.out_inst)


if __name__ == "__main__":
    main()
