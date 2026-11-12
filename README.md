# WUBUMV — the music room

Everything music video and music for the WuBuTV network. The home for all
remade tools for working with music files — to create a music video, or to
create music. Anything that has to do with an audio file in the music sense
lives here.

## What lives here (moving in)

- **Slopcannon** — the MV pipeline (Suno intake → timed scene plan → volleys → QC → assembly)
- **Kinetic type** — post-rendered lyric graphics
- **Lyrics extraction on CPU** — faster-whisper config, Demucs / RMS-VAD hybrid, forced alignment
- **Tempo + grid measurement** — spectral-flux onset envelope, autocorrelation, phase search
- **Detection research** — motion gates (TSM / M6), beat tracking, sync measurement
- **C11 beat tracker** — SLERM rebuild of the madmom / BeatNet beat path (in progress)
- **Blender impact frames** — content-aware impact-frame designs

## Rules

- Code and text only — no audio files, no video files, no Suno tracks.
  Those stay on the user machines / the HF media dataset.
- One 16:9 master only per MV; the song is the tempo gospel.
- SLERM: everything here is rebuilt from scratch, not forked.

## What stays in wubutv-network (for now)

The MV project histories (MV-2…MV-14 ledgers, plans, QC) and the episode
factory. They move only once the live pipeline is quiet, so nothing breaks
mid-build.
