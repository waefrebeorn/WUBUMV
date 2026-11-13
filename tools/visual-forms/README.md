# visual-forms — code-rendered graphics tools

Tools for the visual-first MV forms (see `../../skills/visual-mv-forms/`):
kinetic type is a POST layer — type is never generated inside clips.

- `kinetic_ass.py` — per-word kinetic type: takes a words JSON
  (`{"words": [{word, start, end, ...}]}`) and emits an `.ass` file with
  per-word moves for burning over footage with ffmpeg. Presets: SLAM,
  CASCADE, HIGHLIGHT, STACK, MIXED, plus a palette accent bar layer.
  WuBu palette: COBALT #1B3FD1, VERMILION #E23A1B, CADMIUM #FFC61E,
  BONE #F4EEDC, INK #141414, FOREST #1E4D33.
- `render_countdown_proof.py` — Family I proof: countdown / listicle.
  Deterministic `renderAt(t)`; items land ON measured downbeats of the
  project's beat grid; giant numbers slam with a back-out spring.
- `render_visualizer_proof.py` — Family B proof: audio-reactive
  visualizer. 56-band spectrum + waveform from the track slice's own
  PCM; beat-reactive rings on the measured beat grid.

Both proof renderers are deterministic functions of `t` plus measured
song data — the same `work/beat_grid.json` the assembly uses (one clock
rule). They render frames; the caller muxes audio at encode time.
