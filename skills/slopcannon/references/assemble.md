# Slopcannon assembly — window-first section-timing

Stage 6 of Engine v2. Read references/qc.md first: only QC-passed
takes enter the cut, and no master assembles with a failed gate open.

## Cut rules

- QC-passed takes only, in plan order. Trim each take to its TRUE
  lyric window from LYRIC_TIMELINE.md with a uniform fit per scene:
  the scene's cut points are its section/line boundaries, and cuts
  land on line changes.
- NO peak warp, NO time-stretch of the song, NO stretching a short
  line to a scene, NO slowing a take to cover a hold. If a scene's
  window is shorter than its take, trim. If longer, cover the hold
  with the planned hold coverage. The cheap peak-tween method is
  DEAD and must never be reused in any form.
- Concatenate the trimmed takes in song order with ffmpeg.

## Audio, captions, masters

- Mux the original Suno track as the only master audio. Drop all
  generated scene audio outright: it is never a soundtrack and never
  a timing source.
- Add lyric captions in post as a subtitle track, from the lyric
  timeline's word times. Never burn captions into the generated
  footage. A caption fix never triggers a re-render.
- Add the `~ WuBu ~` corner bug in assembly.
- Build a 16:9 network master and a 9:16 reel from the same cut.
  Keep both in the project `masters/` folder.

## Verify and log

- Verify the master with ffprobe for duration, frame count, and
  aspect ratio, and record its md5. GATE: master boundaries equal
  lyric times; spot-check frames at line starts; verify full-length
  alignment, not just the first 30 s.
- Write `CUTLIST.md` with the active take per scene and its trim
  points. Log the master in `MUSIC_VIDEO_LEDGER.md` with its
  provenance manifest (scene/take/QC/rights).
- Deliver the master in chat as an attachment and announce it to
  `#wubu-mv-6a90e1`, disclosing flags and the honest lipsync limit:
  this pipeline maximizes the plausibility of mouth motion against
  the master; it has no audio-conditioned generation and must not
  claim phoneme-accurate lipsync.
