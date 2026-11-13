# STUDIO WORKFLOW — events in every build

How a WuBuMV build uses the Event Library (`EVENT_LIBRARY.md`), the canon
shelf (`WINNERS_CANON.md`), and the spent-events ledger (`USED_EVENTS.md`).
Written to be followed cold by any future build coordinator. This workflow
plugs into the Slopcannon pipeline at Stage 3 (Plan) and Stage 5 (QC); it
does not replace any Slopcannon stage or gate — where anything seems to
conflict, Slopcannon governs.

## 0. The principle

A scene plan made of subjects at places ("at the pier, she sings") produces
atmospheres. A scene plan made of EVENTS produces a video. Every slot in the
plan is a happening with a start → peak → payoff, chosen from the library,
distinct from every other slot in the video, and checked against what the
last two videos already spent. The user's standing verdict (2026-11-13):
*bland events and same events make a bland video.*

## 1. At scene-plan time (Slopcannon Stage 3)

1. **Map the song first.** Sections, energy arc, word grid, lyric nouns and
   verbs — the usual plan inputs. Mark the slots: intro, verses, pre-chorus,
   choruses, bridge, instrumental spans, tail. Note every lyric line with a
   concrete noun+verb (visual-pun candidates, Family 11) and every counted
   or listed lyric (Family 11.3 / 4.1 candidates).
2. **Assign every slot a DISTINCT event from EVENT_LIBRARY.md.** Write the
   assignment into the scene table as its own column: `EVENT: 5.1 The Chain
   Reaction (final action lands on "go")`. The event is the scene's verb.
   Rules:
   - No event repeats within the video. Not "similar": the same library
     entry twice is a plan defect. (A *motif* may return — the carry object,
     a signature move reprised bigger — but a motif return is staged as a
     new event entry or an explicit escalation, never a re-run.)
   - Every slot gets an event, including singing slots. Singing is paired
     with the slot's event (the singer sings *while* it happens), never
     staged as a held vantage of a singing face.
   - Montage slots draw EVENTS, not atmospheres: a montage scene's row
     names a happening (a cascade, a build, a chase), never a mood ("city
     vibes", "dreamy streets").
   - Density follows the energy arc: choruses and hooks draw High-energy
     events; verses Mid; the bridge draws a *texture-break* event (a
     different family from both choruses, not just a quieter one).
3. **Write the event into the vehicle FIRST.** When the vehicle prompt is
   drafted, the event sentence comes before style, lens, or look detail:
   *what happens* (start → peak → payoff, with the peak's beat/word named),
   then the LOOK block and the rest. If a vehicle can't state its event in
   one sentence, the plan row is wrong — fix the plan, not the prose.
4. **Check the assignment against USED_EVENTS.md.** For each assigned event,
   look at the two most recent MVs in the ledger:
   - Event unused in both → clear.
   - Event used in either → allowed ONLY with a materially different
     staging: different family-adjacent variant, different setting class,
     different peak mechanics (e.g. last video's 6.4 was a rising tide in a
     street; this one is a flooded room rising around furniture). "Same
     event, new characters" is NOT materially different.
   - Signature-tier events (1.1 Morph Chain, 1.6 Elemental Body, 3.1
     Deadpan Flight, 6.1 Moving Floor, 10.5 Micro-Event) are rationed:
     never in consecutive MVs at all.
   Record the check in the plan (one line per reused-with-new-staging
   event, naming the difference).
5. **Intro rule (first-3-seconds).** The intro slot gets a High-energy
   event — top of the library's energy range for its family — and frame 0
   is the event already in motion (peak image first, per the banger test).
   No establishing drift, no settle-then-start.

## 2. At volley time

- Fire vehicles as written; the event is part of the vehicle, not a
  garnish. A reroll that keeps failing ON THE EVENT (the happening won't
  generate) restages the event (different mechanics, same slot job) — it
  does not quietly drop to a plain singing take. Record restages in the
  take ledger like any other staging change.
- Pilot/volley-0 should include the video's riskiest event when budget
  allows: learn early whether the signature happening is stageable.

## 3. At QC (Slopcannon Stage 5, alongside G-gates)

- **The event-read test.** For every scene, the QC reader writes ONE
  sentence: what happens in this scene? If the honest sentence is "she
  sings at the pier" — nothing happens — the scene FAILS, exactly like a
  motion-law fail, and the slot goes back for a restage with a real event.
  The sentence goes in the QC/ledger record (the montage edition's
  gag-readability check is this test's parent; this extends it to every
  scene, not just montage).
- **Distinctness audit.** List the shipped scenes' events; any duplicate
  library entry inside one master is a QC finding, disclosed at delivery
  at minimum, restaged if it's in a chorus/intro slot.
- A scene whose event reads but is the *ledger-repeat without the planned
  different staging* also fails the audit — the difference must be visible
  on screen, not just claimed in the plan.

## 4. After delivery

- Append the shipped video's events to `USED_EVENTS.md`: one row per
  scene (or per main event for long videos), library entry number + the
  concrete staging in a few words. This append is part of delivery
  bookkeeping, like the delivered flag.
- If a build *invents* an event that worked and isn't in the library,
  add it to EVENT_LIBRARY.md in the same pass (name, arc, canon optional,
  energy, slots, feasibility, repeat-risk) — the library grows from the
  floor, not just from research.

## 5. Worked micro-example

Song section: second verse, lyric "the letter never came". Weak plan row:
"SINGER at a mailbox, sad, sings the line." Library pass: Family 11.5 The
Door Reveal (the mailbox door opens on "never" — inside is a tiny lit
room where a postman sleeps) or Family 5.4 Runaway Object (the letter
itself escapes and is chased) or Family 9.1 (a whole queue at the post
office freezes). Vehicle leads: "At the corner mailbox at dawn: she pulls
the slot door open ON the word 'never'; inside, impossibly, a tiny lit
room…" — event first, then look, lens, grade. QC sentence test: "the
mailbox opens onto a tiny room" — an event. Ledger: USED_EVENTS gains
"11.5 Door Reveal (mailbox → tiny room)".

## 6. Library refresh (standing, light)

Once a quarter or when a new awards cycle lands (VMAs ~September, UKMVA
~October, Grammys ~February): skim the new winners, add any new signature
events to WINNERS_CANON.md and any new stageable happenings to
EVENT_LIBRARY.md. Recommended direct pass (noted as a gap in the founding
research): site-search promonews.uk and videostatic.com for graphics-led
winners. A refresh is a text-only commit, same as any studio-pack update.
