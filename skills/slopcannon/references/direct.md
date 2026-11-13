# Slopcannon direction — the plan is the contract

Stage 3 of Engine v2. Read references/timeline.md first: the plan is
built FROM LYRIC_TIMELINE.md, never from a uniform grid.

## The plan file

Write `MV_PREPRO_MV-<n>.md` in the project folder. One row per scene,
in song order. Each row carries: scene number, song time in and out
(from the timeline), lyric lines covered, SINGING or CUTAWAY tag,
setting, characters + bank reference IDs, one beat of direction, one
camera move, motif callback, transition into the next scene.

## Rules

- One clear action, in one place, with the camera doing one thing.
  If a scene's direction needs the word "then" more than once, it is
  probably two scenes — except the performance-window order itself
  (vocal first, beat after), which is one event in two phases.
- Scene boundaries sit on section/line boundaries. Cuts land on line
  changes. Short lines (~2–3 s) are pickups inside longer sections,
  never stretched to a full scene. Long holds get an explicit coverage
  decision (which scenes cover the hold, where face time is spent).
- SINGING scenes follow references/performance-window.md: the vehicle
  will name the line, the singer is (facing camera; static,
  MCU-or-closer) during the line, all gesture and camera movement
  strictly before the first word or after the last word. CUTAWAY
  scenes carry no vocal burden and are never promised sync: mouth
  closed or turned away, face in profile or wide.
- Banger test (a plan gate, not a wish): hook in the first 0.5–3 s;
  one repeatable motif returning at least 3 times; chorus escalation
  with the visual peak saved for the LAST chorus; bridge contrast;
  final frame rhyming with the first. A plan failing this goes back
  to planning, not to reroll lottery.
- Keep every scene landable cold: a viewer joining mid-scene grasps
  the beat in the first seconds with no knowledge of the previous
  scene. Withhold at most one fact per scene and spend it in the next
  scene when the song allows it.
- Use the WuBuTV cast and their hue locks. UNC is INK and CADMIUM
  with the exact `~ WuBu ~` wordmark in CADMIUM. LAURA is FOREST only.
  COLONEL is COBALT. PETER is VERMILION. DISPATCHER is INK and BONE.
  SUPER NUMBER HEAD counts. Two primaries maximum per frame plus bone
  and ink; flat fills; ink outline on every edge.
- End the plan with the volley count and the chorus-hook test: state
  the scene total, the scenes per volley, which volley fires first,
  and that the first volley leads with the hook scene — if its QC
  fails the plan's look, fix the plan before firing the rest.
- After the scene list, write POSE_CARDS.md per
  references/pose-reference.md: one pose card per signature pose,
  every scene assigned to exactly one card. Vehicles carry identity +
  outfit + pose blocks in that order, verbatim wherever they repeat.
  SFW poses only; never copy a gallery image, prompt, or workflow file.
