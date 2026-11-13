# Slopcannon firing — volleys, capped, one variable per reroll

Stage 4 of Engine v2. Read references/performance-window.md before
writing any SINGING vehicle.

## Vehicles first, always

- Write a vehicle file for each scene before firing it, such as
  `mv<n>_s<kk>_vehicle.txt` in the project folder. The full scene
  prompt lives in the vehicle: setting, characters with hue locks,
  the wordmark rule for UNC, camera move, action, zero on-screen
  text, no licensed material.
- SINGING vehicles: the vehicle names its line; the singer is written
  as `NAME (facing camera; static, medium close-up)` during the line;
  all gesture and camera movement sit strictly before the first word
  or after the last word; delivery wording is open, articulated
  mouth shapes with a relaxed jaw on held notes. A CUTAWAY vehicle
  states the singer is not singing in the shot.
- Name the anti-text stack in every vehicle, including no rectangular
  border, box, frame, emblem, or patch enclosing the wordmark, no
  single glyphs or numerals anywhere, no sign panels, and blank
  tickets/props. Text and facing are separate gates.

## Firing

- Fire with `media.generate_video` using the vehicle as the prompt.
  Fire at most 6 videos in one volley, including videos made by
  handed-off agents. That cap is the budget unit: state the volley
  manifest (scenes, takes owed, what each fixes) before firing.
- Save each finished take as `mv<n>_s<kk>_t<t>.mp4` in the project
  takes folder and record its md5 in the take history.
- Keep rejected takes on disk and never chain a later scene from a
  rejected take. Never auto-pick the newest take.

## Rerolls and retirement

- When a scene misses, name exactly one axis that missed (facing,
  delivery, staging, text, voice, wordmark, style) and reroll only
  that scene on that axis. Change exactly one variable per reroll
  (direction, reference subset, model, or seed): change three things
  and you learn nothing. Diagnose facing vs delivery vs staging
  before rerolling a SINGING miss.
- Retire a scene after two denied rerolls. Draft a fresh staging for
  it from scratch and fire that instead of a third reroll of the same
  vehicle.
- Record the volley progress after every volley: fired scenes, active
  takes, missed scenes with their axis, scenes still to fire — so the
  next volley resumes cleanly and the kickstand jobs can read state.
