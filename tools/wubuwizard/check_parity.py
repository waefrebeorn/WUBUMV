"""Parity checks for the standalone MDX port (no torchvision import):
1. scipy STFT vs torch.stft on one chunk (same Hann periodic, center=True).
2. scipy ISTFT round-trip error on the same chunk.
"""
import numpy as np
import torch
from scipy.io import wavfile
from scipy.signal import get_window, istft, stft

import sys
sys.path.insert(0, "/home/hatch/workspace/wubuwizard-cpu-sep")
from mdx_onnx_cpu import CHUNK_SIZE, DIM_F, HOP, N_FFT, WINDOW, istft_complex, stft_complex

sr, data = wavfile.read("/home/hatch/workspace/wubuwizard-cpu-sep/mv14_44k.wav")
mix = (data[:CHUNK_SIZE].T.astype(np.float32) / 32768.0)

# --- torch reference ---
t = torch.tensor(mix)
win = torch.hann_window(N_FFT, periodic=True)
z = torch.stft(t, n_fft=N_FFT, hop_length=HOP, window=win, center=True, return_complex=False)
# z: [2, F, T, 2] -> [4, F, T] in [L_re, L_im, R_re, R_im] order
zt = z.permute(0, 3, 1, 2).reshape(4, -1, z.shape[2])[:, :DIM_F, :]
print("torch stft shape:", tuple(zt.shape))

mine = stft_complex(mix)
print("scipy stft shape:", mine.shape)
print("STFT max|diff|:", float(np.abs(mine - zt.numpy()).max()))
print("STFT mean|diff|:", float(np.abs(mine - zt.numpy()).mean()))
print("STFT scale (max|torch|):", float(np.abs(zt.numpy()).max()))

# --- ISTFT round trip (scipy only) ---
rt = istft_complex(mine)
print("ISTFT round-trip max|diff| vs input:", float(np.abs(rt - mix).max()))
print("ISTFT round-trip mean|diff|:", float(np.abs(rt - mix).mean()))

# --- ISTFT parity vs torch.istft(center=True) on the same spectrum ---
import torch as _t
zc = _t.stft(t, n_fft=N_FFT, hop_length=HOP, window=win, center=True, return_complex=True)
torch_istft = _t.istft(zc, n_fft=N_FFT, hop_length=HOP, window=win, center=True).numpy()
print("ISTFT vs torch max|diff|:", float(np.abs(rt - torch_istft).max()))
print("ISTFT vs torch mean|diff|:", float(np.abs(rt - torch_istft).mean()))
