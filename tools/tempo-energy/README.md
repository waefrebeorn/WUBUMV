# tempo-energy — tempo + energy measurement from the delivered audio

**Audio analysis is a required intake step: prompt BPM is a claim.**
Measured vs stated, MV-9 133 vs 128, MV-10 ~108 vs 112, MV-12 131.5 vs
128, MV-13 97.0 vs 96, MV-14 92.0 exact.

## Method

Spectral-flux onset envelope + autocorrelation over 60–200 BPM (0.5 BPM
steps), RMS energy in 2 s / 5 s windows. System python3 with numpy +
scipy — no librosa, no aubio. Proven on MV-9/MV-10/MV-11, then run per
track (this copy is the MV-14 one, the latest).

## Run

```sh
python3 analyze_tempo_energy.py
```

Point the `PROJ` / `WAV` constants at the top of the script at the
track first (16 kHz mono WAV, decoded from the delivered track). The
script prints the tempo candidates + energy profile and writes
`tempo_energy_raw.json` next to itself.
