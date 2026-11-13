# Slopcannon timeline — measure first, plan second

Stage 1 of Engine v2. No scene is planned until this file exists for
the delivered track. The timeline is the contract the plan, the
vehicles, the QC, and the assembly all read from.

## Build it from the delivered track

- Source of truth: the delivered `track.mp3`/`track.mp4` in the project
  folder, fingerprinted by md5. A timeline measured against any other
  file (an earlier upload, a lyric video of a different master, a
  chat timestamp) is void until re-measured against this file.
- Method (in order of preference): forced word alignment of the
  verbatim lyrics against the track's vocal (word start/end times);
  lyric-video frame sweep (bold/highlighted line = line being sung,
  refined to ±1 s) where no aligner is available; beat/downbeat
  tracking for section boundaries, snapped to beats. Record which
  method produced each time.
- Output: `LYRIC_TIMELINE.md` in the project folder with (a) a section
  table (section, start, end, duration, lines covered), (b) a line
  table (line number, section, lyric text, start, end, method), (c)
  notes for the cut (short lines to watch, long holds, drift hazards
  where the old plan would have gone wrong).

## Confidence tags (Eigenform rule, applied to timing)

- [confirmed]: measured from the audio (frame-pinned line start, beat-snapped boundary).
- [inferred]: section label, bracket estimate (±2.5 s), or a boundary placed by lyric sense rather than a detected beat.
- [assumed]: a user claim (a timestamp mentioned in chat) not yet matched to a measured time within tolerance (±250 ms for a word, ±1 beat for a section). An [assumed] time never overrides a measured one; show both until matched.

## Rules the timeline enforces downstream

- Scene boundaries sit on section/line boundaries from this file, and
  cuts land on line changes. A scene that straddles a section boundary
  without a stated reason is a plan error.
- Short lines (~2–3 s) are pickups inside longer sections. Never stretch
  one to a full scene, and never let a scene's window swallow two
  unrelated lines without naming both.
- Long holds get an explicit coverage decision in the plan (which
  scenes cover the hold, where face time is spent, where cutaways
  carry it).
- If the track is re-delivered (new file, new mix, MP3↔MP4 swap), the
  timeline is re-measured and the plan re-derived. Re-time the scene
  grid to the delivered track; never time-stretch the song to fit a
  grid, and never carry forward trims computed against the old master.
- The v1 failure mode, named so it is never repeated: MV-2 v1 sliced
  the song into uniform 10 s blocks while verse lines ran ~10 s and
  chorus lines ~5 s, so the grid drifted in every chorus and the outro
  landed ~10 s early. Uniform grids are a planning bug.
