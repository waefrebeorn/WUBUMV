# Slopcannon asset search

Find the references BEFORE drafting any scene. Lyrics are the search context:
every query comes from a lyric line, never from a free-floating mood board.
The output is one reference board per track, and the board is what the
scene plan is drafted from.

## The rule that keeps this legal and WuBu-native

Search pop culture for MECHANICS, never for characters to reproduce. A search
hit gives you a composition, a color, a camera move, a cut, a trope — never
a likeness, a costume, a line of dialogue, a plot beat, or a logo. Every
reference on the board must pass through the SLERM transform:

| Search hit gives you | Board keeps | Generation prompt uses |
| --- | --- | --- |
| A famous character | The ROLE (messenger, counter, keeper, seller) | A WuBuTV cast member in that role, in WuBuTV hues |
| A famous video's look | The COMPOSITION / light / palette / camera move | The same composition, restaged in a WuBuTV set |
| A famous video's cut | The TRANSITION MECHANIC (match cut, doorway pass, scale jump) | That mechanic, between two WuBuTV scenes |
| A lyric's named figure or place | The ARCHETYPE (night worker, tower, count, roster) | The archetype, played by the cast, in-world |

If a lyric names a real pop figure, treat it as a role signal, not casting.
If a reference cannot survive that transform, it goes on the KILLED list
with its reason and is never reused silently.

## Stage 1 — Parse the lyrics into search context

Work from the verbatim `lyrics.txt` in the project folder, section by
section (intro, verse, chorus, bridge, outro), with song timestamps.

For each section, pull out, in writing:

- Concrete nouns: objects, places, things a camera can show.
- Verbs and actions: what somebody DOES, not what they feel.
- Roles implied: who is speaking, who is spoken to, who is counted, kept,
  sold, watched.
- Emotion and stance: the speech act (accuse, dare, beg, refuse, warn).
- Texture words: era, weather, light, color, scale (tower, desk, hall).
- Repeats: any word, object, or image that comes back — that is a motif
  candidate, and motifs outrank one-off images.

A section with no concrete noun still gets a search: search its verb and
its stance ("waiting at a desk music video visual", not "sad song visual").

## Stage 2 — The query ladder (four rungs per scene)

Run all four rungs for every scene's lyric chunk. Stop at three kept
references per scene; more is a mood board, not a board.

1. ARCHETYPE: `<role> archetype visual` — e.g. "night dispatcher archetype",
   "counting clerk archetype". Finds the common, readable version of the
   role the lyric implies.
2. MOTIF: `<object or setting> music video visual` — e.g. "ledger desk music
   video", "tower hallway music video". Finds how that image has been shot.
3. TROPE / MECHANIC: `<trope> music video technique` — e.g. "match cut
   object handoff music video", "one-take hallway music video". Finds the
   HOW, not the WHAT.
4. POP-CULTURE MECHANIC: search the web for how a well-known video handled
   a SIMILAR BEAT (same action, same song shape — verse-to-chorus lift,
   drop, reveal, count, chase). Record the mechanic and its source page.
   Never record the artist's character, plot, or look as something to copy.

Search routes, in order:

- Text and trope research: `browser.search` (technique, history, "how did
  they shoot / cut this" questions).
- Image reference ideas: `/opt/hatch/bin/image-search "<query>" --max-results 5`
  (see the image-search skill: keep `media_url` and `page_url` for
  provenance; a thumbnail is not a durable copy). Pick the result that
  matches the lyric image, never blindly the first one.
- Do not download licensed artwork into a project folder. The board holds
  URLs plus a one-line description of the composition/color/move taken.
  The description is the asset; the URL is the provenance.

## Stage 3 — The reference board

Write `ASSET_BOARD.md` in the project folder before `MV_PREPRO` is drafted.
One row per scene:

- Scene + song time + lyric lines covered.
- Archetype found (role + source query).
- Visual motif (object/setting + image reference URLs, max 3, with page URLs).
- Pop-culture mechanic (technique + source page) + WuBu-native translation
  (cast member, set, hues, one camera move).
- FIRST / LAST / NEW / TRANSITION slot for this scene (see Stage 4).
- Status: KEPT, DEMOTED, or KILLED (with reason). Killed rows stay on the
  board, struck through, so a later volley never re-admits them quietly.

## Stage 4 — Scene-to-scene assembly grammar

This is how scenes chain instead of just following each other. Every joint
between two scenes must name all four slots. A joint missing one is an
unplanned cut, and unplanned cuts are where videos go generic.

- FIRST SCENE: establishes world, cast, and motif object inside the first
  three seconds, cold-landable (a viewer joining here grasps the beat with
  no prior scene). It plants the motif object the whole video will carry.
- LAST-SEEN CARRY: every scene ends by planting exactly one carry — an
  object in a hand, a color accent, a gesture, a line callback, a camera
  position. The NEXT scene must pick that carry up in its first frame.
  This is the bridge-cliff rule, generalized from the STATION chains: the
  last frame of one scene is the first frame of the next, in spirit if the
  set changes.
- NEW SCENE: introduces exactly ONE new thing — one character, one set,
  one object, one color accent. Never two. The viewer must be able to say
  what changed.
- TRANSITION: pick one per joint, never the same mechanic twice in a row:
  match cut on object or gesture; color wipe in a cast hue; sound-bridge
  cut on the beat or the drop; doorway or arch pass-through; mirror or
  reflection swap; scale jump (close-up of the motif object to wide of the
  same object); lyric-word cut (cut on the word that names the next image).
  Name the mechanic in the plan, not just "cut to".
- BANGER TEST, applied to every joint before the scene is fired:
  - Hook: does the first three seconds ask a question the viewer wants
    answered?
  - Drop payoff: on a chorus or drop, does the picture PAY OFF (a reveal,
    a scale jump, a withheld fact spent) instead of just cutting louder?
  - Repeatable motif: is there one image a viewer could describe to a
    friend in one sentence?
  - Rewatch hook: is one detail withheld here that pays off in a later
    scene?
  A joint failing two or more of these gets restaged, not fired.

## Stage 5 — The double / triple research flow

The board is not finished when it is full. It is finished when it survives
adversarial passes. This is the same flow as the Slopcannon research passes,
run per track on the board itself:

- PASS 1 (gather): collect broadly, tag each reference HIGH / MEDIUM / LOW
  confidence, keep the source page for every row.
- PASS 2 (devil's advocate): attack every KEPT row. Is it generic? Is it a
  licensed copy wearing an archetype costume? Does it fit the lyric, or
  does it merely rhyme with one keyword? Does it repeat the previous
  scene's mechanic? Demote or kill what fails, with the reason written.
- PASS 3 (attack the attack): defend the survivors. Is the attack killing a
  good mechanic because of one weak example? Restore it with a better
  source, or re-translate it (same mechanic, different set) and say so.
- PASS 4 (triple — attack the survivors on hard songs): test every survivor
  against the worst case for THIS track: a tempo change, a dense lyric
  passage, a section with no chorus, a motif that appears only once. What
  survives Pass 4 is the board the scene plan is drafted from. What dies
  stays on the KILLED list.

The in-flight Slopcannon deep-research passes feed Pass 1 and Pass 2 with
methods and failure modes; they never replace the per-track board. A method
that survives research but fails this track's Pass 4 is killed for this
track.

## What the scene plan takes from the board

`MV_PREPRO` scenes are drafted ONLY from KEPT board rows. Each scene's plan
line names its board row, its LAST-SEEN carry from the previous scene, its
ONE new thing, and its transition mechanic. If a scene cannot name all
three, it is not drafted yet — run one more query rung for that lyric chunk
instead of inventing a visual.

## Guardrails carried over

- No licensed characters, tracks, brands, logos, or copied dialogue, plots,
  or looks — mechanics and archetypes only, SLERM-transformed.
- Zero on-screen text in generated footage; captions live in post, never
  burned in.
- The `~ WuBu ~` wordmark hard gate still applies to every UNC frame.
- The Suno track stays the timing authority; a reference never moves a cut
  off the beat.
