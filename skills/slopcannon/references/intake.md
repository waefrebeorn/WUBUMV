# Slopcannon intake

- Accept the track as a chat attachment or as a file already placed in `musicvideo/intake/`.

- Name the file `MV-<n>_<title>_suno.mp3` and create `musicvideo/<slug>/` for the project.

- Copy the track into the project folder as `track.mp3` and record its md5 in `musicvideo/intake/INTAKE_LOG.md` with the date, the source and the job.

- Ask which job the track is for when the user does not say. The jobs are anthem, serial bed, channel sting or pips motif. Record the answer in the intake log.

- Save the lyrics verbatim in `musicvideo/<slug>/lyrics.txt`. Owner text is canonical and never paraphrased.

- Measure the duration with ffprobe and write the duration, the md5 and the job into the project notes.

- Register the track as a MUSIC_TAG source with a bed id. Every master that rides it names that bed id.

- Re-time the scene grid to the delivered duration at once. A track that is longer or shorter than planned changes the scene count, never the song.
