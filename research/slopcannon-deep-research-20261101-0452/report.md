# Slopcannon — deep research report

**Research date:** 2026-11-01. **Confidence key:** `verified live` = read in the research browser on 2026-11-01; `index` = search-index / crawled-page text; `user report / secondary` = a third party summarising an X/YouTube post, not the post itself; `speculation` = labelled as such. No login, payment, sign-up or download was performed; the Slopcannon studio itself (behind sign-in) was NOT entered, so anything inside the app is taken from Slopcannon's own public wiki/FAQ, not from hands-on use.

## Summary — the answer first

- **Slopcannon (slop.cc) is real, current, and narrowly defined:** an AI music-video *workstation*, not a one-prompt generator. Song + named reference images + idea in; a numbered, timed scene plan out; every scene fired as one "volley"; bad scenes rerolled singly with full take history; the chosen takes are cut to the *original song* with optional word-timed captions into an MP4 master. `verified live`
- **Creator:** "Bone" (@boneGPT) is presented in secondary coverage as the creator/founder behind Slopcannon, and as an early-access partner for Meta's Muse Wonder (Oct 2026). **No legal name, biography, interview or launch date for Bone/Slopcannon was found in public sources searched** — that is a gap, not a fact to fill in.
- **No true open-source clone of Slopcannon exists.** The closest things are (a) research systems (AutoMV, ViMax) that share the architecture but are not song-workstation products, (b) commercial song-to-video tools (TubeTube, VidMuse, Neural Frames, Revid, BeatMotion, Suno2MV) that each miss at least one of Slopcannon's three pillars (project-wide reference bank + per-scene reroll with take history + song-as-master assembly), and (c) name collisions / unaffiliated tokens that are NOT Slopcannon.
- **The generic "slop cannon" is a different, older idea** (Eigenform, Aug 2026; Handy, 2026): a blind-firehose pipeline with no error-catching. Slopcannon the product is, ironically, an *anti*-slop-cannon design: it is built around the exact fixes Eigenform prescribes (stage separation, QC, visible uncertainty, history management) — which is the core lesson for §6.

---

## 1. Origin and creator

### 1.1 Who is Bone / boneGPT? — verified facts are thin

| Claim | Status | Source |
|---|---|---|
| Bone posts as @boneGPT on X and is the creator/founder behind Slopcannon | `secondary` — stated in third-party coverage, not in a Bone bio found here | The GenAI Magazine: "The creator behind the Slopcannon project, posting as bone (@boneGPT), had early access [to Muse Wonder]" — https://thegenaimagazine.com/meta-muse-wonder-review-benchmarks-price-vs-opus-astra-fable ; Sloptoberfest page: "$9,000.00 from Slopcannon's founder" (unnamed) and main awards "judged by Slopcannon's founder and the Bone Zone Slop Council" — https://sloptoberfest.slop.cc/ |
| Bone had early access to Meta Muse Wonder (released 12 Oct 2026), said it was "neck and neck or better" than Astra/Fable/Opus on his benchmarks, "never talks down to you", predicted Meta wins consumer agents "in a landslide" | `secondary, enthusiastic partner — not independent` | Same GenAI Magazine piece, which itself warns: "This is an enthusiastic early-access partner whose project runs on the model, not an independent test." |
| Bone is tagged by Sloptoberfest entrants (e.g. @thoughtcrime___ tagged @boneGPT + @alexandr_wang) | `user report / secondary` | RuntimeWire, 15–16 Oct 2026 — https://runtimewire.com/article/slopcannon-creator-credits-muse-in-insane-ai-video-posted-for-sloptoberfest — which explicitly warns tags "do not establish a partnership or Wang's involvement." |
| Bone's legal name, prior work, interviews, blog posts, launch announcement | **NOT FOUND** in searches of X/blog/video/interview coverage on 2026-11-01. Do not invent. | — |

**Three different "Muse"s — do not conflate them (important, and a common trap):**
1. **Meta Muse Wonder** — Meta's frontier model family, released 12 Oct 2026. This is the "Muse" credited alongside Slopcannon in the thoughtcrime Sloptoberfest case (§3). Whether Muse actually generated any part of that video is *unproven* — the credit is the creator's claim, amplified by a Wang quote-post.
2. **muse.slop.cc** — an earlier Slopcannon host/name. A YouTube making-of is described as "video made on muse.slop.cc" (https://www.youtube.com/watch?v=5UeNFfqOYks). This is Slopcannon's own product surface, not Meta's model.
3. **Muse (Stillmotion storytelling course), Muse DAO, Adobe Muse** — unrelated; they pollute search results and should be ignored.

### 1.2 What is slop.cc, end to end, and how has it changed?

`verified live` — homepage https://slop.cc/ (2026-11-01): headline "Song in. Music video out." / "SLOPCANNON turns a song, reference images, and an idea into a timed, editable music video." / "Brainstorm with a project-aware Producer. Fire every scene. Reroll the misses. Keep the hits. Assemble the final cut with the original song."

The five-step product, as stated on both homepage and FAQ https://slop.cc/faq :
1. **Load it** — song, people/visual references, idea.
2. **Direct it** — brainstorm with the Producer until the timed story and scene references feel right.
3. **Fire it** — review the exact credit total; the Cannon launches the ready scenes and attaches clips automatically.
4. **Keep the hits** — watch the timeline; change/reroll only the scenes that missed; earlier takes stay available.
5. **Finish it** — cut the active takes to the song, add optional captions, download the master.

**Changes over time (dated, from the site's own news + wiki):**
- **Legacy Studio vs current studio:** the homepage still links a "Legacy Studio" alongside "Start a film", and the wiki describes a newer "quieter chat, with Studio mode — one column: talk to the Producer, review scenes on the stage, and switch to Studio mode for the timeline" plus "Create mode vs Studio mode" as FAQ Q16. Inference (`speculation`, but strongly suggested by the naming): the current chat-first Producer workflow replaced an earlier Studio, which is kept as Legacy. The exact cutover date was not published on pages read.
- **24 Sep 2026:** "Make films from Claude and other agents — Connect SLOPCANNON to Claude, Claude Code or any MCP client and sign in once." (homepage news, `verified live`)
- **27 Sep 2026:** "Start from your own footage — Upload a video and restyle it scene by scene, cut to the original's timing." (homepage news, `verified live`) — i.e. the workstation expanded from song-only to video-restyle input.
- **29–30 Sep 2026:** "Inside the Cannon: a guide to every feature" + the Director's Wiki (134 guides, 391-term glossary per FAQ; 12 Inside-the-Cannon guides at https://slop.cc/wiki/features, all updated 30 Sep 2026). This is a documentation/content push, not just a feature: camera, light, animation/anime, genre/style, prompting/planning guides.
- **Oct 2026:** Sloptoberfest, the first contest (§3), plus SLOPTV community compilations — a distribution/community push.
- **"At launch" pricing language** in the FAQ ("At launch, every generated clip uses Quality 2K…") suggests the credit system described in §2 is the launch configuration; other quality tiers are implied as possible later ("Other modes use credits at their normal rates" on the contest page) but no other tier is documented on pages read.

**What slop.cc is NOT:** it is not a music generator (you bring the song), not a social feed (SLOPTV/SlopCast are showcases), and not the docs.slopcannon.dev tool (§4.5).

---

## 2. How it works, in detail

All of this section is Slopcannon's own public documentation (`verified live` via wiki/FAQ, 2026-11-01) unless marked otherwise. The underlying video model(s) are **not named** on pages read — the wiki says each scene is rendered with "its own timing, direction, audio excerpt and references" but does not publish which video model(s) power Quality 2K. Do not assume Veo/Kling/etc.

### 2.1 Intake
- **Song:** upload a song. Slopcannon "privately analyzes the song's timing and words" (scene-timeline guide). Detected words can be corrected or ignored.
- **References:** upload "a clear image of each person or thing" and give it a name — people, outfits, props, places. One or two clear photos per subject, not a dozen similar ones (wiki's own "common mistakes").
- **Idea / plot:** a sentence, mood, image, or a full plot. The Producer brainstorms from song/mood/image.
- **Rights gate:** "You need the rights or permission for every face, logo and image you upload. SLOPCANNON asks you to confirm that once per project before your media is used; AI generation does not create those rights." (reference-bank guide). For agents, "Human confirmation remains required for content rights and paid generation actions." (FAQ Q18)
- **Own footage (new):** upload a video; Slopcannon restyles it scene by scene against your references, keeping the source timing.

### 2.2 The Producer (chat) and planning
- The Producer is "the chat you work with inside every SLOPCANNON project. It reads the project itself (the song, the references, the scene plan and the takes), so its suggestions are about your film rather than a generic one." (https://slop.cc/wiki/the-producer)
- It can: brainstorm a concept; plan a complete story against the song with a timed scene per passage; revise a *range* of scenes without rebuilding the rest; propose new references/variants and say which scenes they belong to; explain real project/provider status when a render needs attention.
- **Model choice:** "Each project's Producer runs on a language model you can choose. The chip beside Attach in the chat [shows it]. Every reply names the model that wrote it. If the chosen model cannot answer a turn, a backup model [answers]." Model list was not visible without sign-in.
- **Approval model:** "The Producer proposes; you approve. Plans, edits and new references arrive as proposals you can accept" — not auto-applied. Short turns beat one enormous prompt; approving a whole plan without reading the scene list is listed as a common mistake (cheaper to change a scene before it is rendered).
- **External agents:** documented MCP capabilities for Claude, Claude Code, Codex, Grok or any MCP client — "let your agent plan, [reroll, assemble]" (wiki index summary). Contest rules confirm films may be made "in Slopcannon or its MCP". No public tool list was readable without sign-in.

### 2.3 Scene timeline — the heart of the product
- "The scene timeline is the song laid out as a film: numbered scenes, each tied to a passage of the track, with its own direction, references, words and takes. It is what lets you change scene 11 without touching scenes 1 to 10." (https://slop.cc/wiki/scene-timeline)
- **Each scene carries everything needed to render alone:** number + place in the song; direction (what happens, camera move, light); the subset of references assigned to *that* scene; its take history with the cut's take marked; its own audio excerpt, "which is what the Cannon uses when it renders that scene."
- **Timing:** cuts are planned to land on the music; a performance scene "knows which line is being sung." Mouth movement can be switched off scene by scene for moments that should not be sung.
- **Scene-planning rule (wiki, repeated):** one clear action, in one place, with the camera doing one thing. "If a scene's direction needs the word 'then' more than once, it is probably two scenes." Scenes that ignore song structure so cuts land between beats are a listed mistake.
- **Song sections:** the wiki talks in terms of "passages" / verse / chorus / acts, but does **not** publish a beat-detector, section labeller, or scene-count formula. The Starbelo write-up's example prompt ("Write a music video plot in 8 scenes that follow the song's sections") is a *user* prompt pattern, not Slopcannon's internal rule — do not present 8 scenes as a product limit.
- **Limits NOT published on pages read:** maximum song length, maximum scene length, maximum scene count, maximum number of references. Absence here means "not in public docs read", not "unlimited".

### 2.4 Reference bank — character consistency mechanism
- One reusable pool per project (people, outfits, props, places). Each scene gets only the subset it needs: "a scene with the singer alone carries only the singer, and a scene at the diner carries the singer, the waitress and the diner." Giving a model every reference at once forces it to guess who belongs in frame — the wiki's central consistency insight.
- **Variants, not edits:** when a story changes (coat gets dirty in rain, character ages, room wrecked), create a *variant* and assign it only to later scenes; earlier scenes keep the clean version. The Producer can propose variants and name their scenes.
- **Identity vs outfit:** the wiki's exercise is to "write a reference label that describes identity separately from outfit and mood" — a directly borrowable design rule (§6).

### 2.5 Firing the Cannon (generation volley) and rerolls
- **Volley:** "Every ready scene is launched together as one coordinated volley, each with its own timing, direction, audio excerpt and references, and finished clips attach themselves to the timeline as they arrive." Scenes render in parallel; you can start watching before the last scene finishes.
- **Cost preview (critical UX):** "Before a volley, SLOPCANNON shows the exact number of Cannon Credits it needs. A first pass charges for the saved timeline's length; later rerolls charge only for the scene you reshoot. If the balance is short, nothing is submitted and nothing is deducted."
- **Recovery:** accepted jobs keep processing if you close the browser and recover on the same or another device/account. A render that fails with nothing to deliver releases its credit hold; the scene keeps direction, references and earlier takes. A finished-but-undownloadable take is a retrieval problem — contact Support with the job ID, do not pay to reshoot.
- **Moderation:** a scene stopped by content moderation can have its direction "cleaned up" (sanitised) and rerolled while keeping creative intent.
- **Reroll rules (wiki):** reroll *one* scene, not the film; change direction, references, or nothing — but "rerolling with no change and hoping for a different result" is a listed mistake; watch the whole cut first (a weak-alone scene may work between neighbours, and vice versa); batch reshoots of the short list so new takes can be compared side by side; mark the chosen take before assembling (forgetting this is a listed mistake).
- **Take retention:** unpicked takes are kept until deleted — 7 days after you choose another; every take of a finished project 28 days after last activity (90 days without a film), each after dated notice + email. "Finished films are never deleted."

### 2.6 Assembly, audio sync, captions, aspect ratios
- **Assembly:** "Final assembly turns the chosen takes into one finished video: every scene in timeline order, trimmed to the song, with the original track underneath and optional captions on top. The result is an MP4 master." Assembly is included (no separate charge) and can be repeated after a reroll.
- **Audio sync — the key design decision:** "The original song, not the audio of any clip, becomes the soundtrack, so the performance and the cuts stay locked to the music you uploaded." Generated clip audio is dropped. Each scene's clip is trimmed to its passage of the song. This is why a delivered track that differs from the planned track is dangerous (§6: re-time the grid, never the audio).
- **Lip-sync:** not a separate lip-sync pass in the docs; it is *guided* performance — each scene carries its audio excerpt and its line, mouth movement is toggleable per scene, and the pre-assembly checklist is to "check that the singer's mouth matches the lines where it should, that characters wear the right variant in each act, and that no scene still points at an empty or failed take." No phoneme-level claim is published; treat "lip-sync" as best-effort guided generation, not a guarantee.
- **Captions (in post, never in the generated footage):** built from the song's word timing — "each word lands where the singer sings it rather than where a line of lyrics happens to begin." Correct a scene's words via Edit CC; if your text has the same word count as the transcript, each word keeps its timing, otherwise words are spread evenly across the scene's sung span. Editing captions never changes what the video model was told and never spends credits. Reset returns to heard words.
  - **12 looks:** Kinetic, Karaoke, Lyric sheet, Neon, Quiet, Punch, Comic, One word, Pill, Subtitle, Build, Typewriter (plus No captions default; older Classic/Cannon looks preserved only on projects that used them). Colour, size, place are adjustable; the Finish button names the look (e.g. "Finish video · Kinetic captions").
  - **Crucial delivery split:** "Captions are drawn into the picture when the film is finished on your device; the Finish card says so while captions are on, and asks you to keep the tab open until it is done. … Assembly on SLOPCANNON's servers makes the film without captions." Preview uses the same renderer as the master.
  - **9:16 safe band:** captions stay between 14% and 65% of frame height and away from side rails — "the band all three platforms [TikTok/Reels/Shorts] leave clear" — so platform buttons never cover them. Long lines wrap to a third row on tall frames, or split in half by sung half.
- **Aspect ratios:** landscape, square, portrait and vertical including 9:16 for phone-first video. **Choose before the first pass** — "every scene is composed for it" and changing aspect after the first pass is a listed mistake (i.e. no free reframe; a new aspect is effectively a new pass).

### 2.7 Credits / pricing (the only pricing published)
- **8 Cannon Credits per finished second at Quality 2K.** Standard packs ≈ $0.222 per finished second ≈ **$13.33 per finished minute** (wiki + FAQ agree; contest page values minutes identically: 960 min = $12,796.80).
- Worked cost: a 3-minute song first pass ≈ 180 s × 8 = 1,440 credits ≈ $40 at standard-pack rates, before any rerolls; a 10-second scene reroll ≈ 80 credits ≈ $2.22. (Arithmetic from published rates, not a quoted pack price — pack sizes/discounts were not on pages read.)
- Assembly, status checks, recovery, downloads, caption changes, project editing: included. Failed/no-deliverable renders: no lasting charge. Insufficient balance: nothing submitted, shortfall shown, smallest covering pack suggested.
- No free tier, trial amount, subscription price, or per-pack price was found on public pages read; Starbelo's "paid or trial-based — check the site" is consistent with that gap. Do not quote a monthly price for Slopcannon.

---

## 3. Public examples and reception

### 3.1 The community case credited to Slopcannon + Muse (the mission's named case)
- **What happened:** @thoughtcrime___ (~5.4K X followers) posted a full AI music video on **15 Oct 2026** as a claimed official Sloptoberfest submission, crediting Slopcannon and Muse, tagging Bone (@boneGPT) and Alexandr Wang (@alexandr_wang). `secondary` via Starbelo (updated 2026-11-01) and RuntimeWire (15–16 Oct 2026).
- **Numbers (as reported, X, 17 Oct 2026):** the video itself 253,111 views, 866 likes, 395 bookmarks; Wang's quote-post ("the dopamine release from watching this video was insane") 245,380 views, 1,843 likes.
- **What this does NOT prove:** RuntimeWire's caution is the correct reading — a tag is not a partnership, a quote-post is not an endorsement of the tool, a social post alone is not a valid Sloptoberfest entry (the contest requires the official form), and the post alone does not prove Muse (the model) generated any part of the clip. Starbelo's write-up also derives a reusable prompt pattern from the case (lyrics + timestamps in, named characters in, 8 scenes following song sections out) — useful as a *user workflow*, not as Slopcannon documentation.
- **Paid-work signal:** Starbelo reports creator Jason Rink says he is already using Slopcannon for paid client work (via a Rink X post). `secondary, unverified here` — no client, price or deliverable was independently confirmed.

### 3.2 Sloptoberfest 2026 (the contest that manufactures examples)
- **Live page:** https://sloptoberfest.slop.cc/ — "AN AI FILM CONTEST BY SLOPCANNON", first edition, October 2026, 19 awards, $50,896.80 total value: $38,100 USDC on Solana + 960 Slopcannon minutes ($12,796.80).
- **Prizes:** Golden Cannon $25,000 (funded by Marc Andreessen @pmarca); Best in Show $5,000 + 600 min; 2nd $1,500 + 120 min; 3rd $1,000 + 60 min; Best Cinematography $500 + 60 min; StealthGPT "CAN'T BELIEVE IT'S SLOP!" $2,500 + 60 min; w.ai "BIG WIN TOGETHER" $1,000; AgenC Prize $500; The Eugene $100 + 10 min; The Next Ten $100 + 5 min each; every winner also gets a StealthGPT subscription. Founder personally $9,000; StealthGPT $2,500; WOMBO/w.ai $1,000; AgenC $500; Eugene Ray $100.
- **Judging/rules:** main awards judged by the founder + "Bone Zone Slop Council"; sponsors choose their own awards; sponsor awards can stack, one main award per creator; all creation/editing must be entirely inside Slopcannon or its MCP (outside source assets may be imported); multiple films welcome, one entry per film; public film link + creator name/contact via the official form; X posts/replies alone do not count.
- **Deadline discrepancy — report it, don't smooth it:** the live page on 2026-11-01 says films due **1 Nov 2026, 4:00 a.m. EST**, winners **7 Nov 2026**. An earlier crawl/search snippet said 31 Oct 11:59 p.m. ET; the SLOPTV Vol. 2 description said "Submit by Oct 29"; RuntimeWire (15 Oct) said "by October 29th". The deadline evidently moved/extended during October. Cite the live page for the current date.
- **Why it matters for a builder:** a cash-and-credits contest is Slopcannon's distribution strategy — it buys public examples, stress-tests the workflow, and seeds the community library (SLOPTV) at the cost of prize money rather than ads.

### 3.3 Other public examples
- **SLOPTV Vol. 2** (https://www.youtube.com/watch?v=yZfTk7mDV2U, ~17 days before 2026-11-01): 1.5 hours of community Slopcannon films, every film credited. Recurring creators: JB (@jbro_1776), burnz (@burnzzz0), Devon (@Devon8zzh — a whole shrimp-emperor series: "Slop Caesar", "Alexander — The Shrimp Who Conquered the Known World", "Welcome to Shrimp Slopolis"), Flutterwhat (@flutterwhat), Jason Rink (@JasonRink — "You and Your Slop Cannon (a 1957 civic guidance film)"), AirBuddDwyer (Hank Hill/Creed parody covers), BarDarlingLocal, LapreAndrew, dogsnfishing, lalopenguin, Roll1er, pixhell, kiss4bliss. The compilation itself discloses: "AI parody: some films show AI likenesses of real public figures. All of it is parody." This is the best public corpus for judging real output quality — parody + novelty + recurring-character series dominate, not straight artist videos.
- **"Making the Girl Who Got Away on the Slopcannon"** (https://www.youtube.com/watch?v=5UeNFfqOYks, ~20 days before 2026-11-01): a making-of, described as "video made on muse.slop.cc" — evidence of the earlier muse.slop.cc surface and of users documenting process, not just output.
- **Press example — NY Ledger, 4 Oct 2026** (https://thenyledger.com/markets/ai-slop-is-coming-for-hollywood-some-of-it-is-already-better/): an AI video of a fake Anthropic CEO Dario Amodei singing "Hit the Breaks Except for Me", made with Slopcannon from "little more than an audio file, a few images, and an idea". The author contrasts it with the SNL sketch mocking Amodei the same weekend (which needed writers/actors/a studio) and says he watched the Slopcannon video more than the SNL sketch — a favourable reception data point, but from a single opinion column, and the subject is parody of a real CEO (rights/parody risk, §6 QC).
- **Merch + channels:** official merch via imaginesupply.co (linked from SLOPTV description); SlopCast (below) is a separate curator.

### 3.4 What users praise / complain about — honest limits
- **Praise (evidenced):** speed from idea to full timed video; scene-level control without rebuilding the film; the Wang quote-post reaction; a creator monetising it for client work (secondary); the sheer volume/energy of the community corpus (1.5-hour compilation within weeks of launch-era activity).
- **Complaints:** **no systematic user-complaint corpus was found** (no Trustpilot/Reddit review set for slop.cc in searches). The closest thing to complaints is Slopcannon's own "common mistakes" lists, which read as the failure modes users actually hit: firing before reading the plan (then paying for rerolls), rerolling with no change, rebuilding the whole plan to fix one scene, forgetting to mark the new take, changing aspect ratio after the first pass, packing several actions into one short scene, correcting lyrics in the scene's audio guidance instead of its caption (which changes the next render), choosing server assembly and expecting captions, judging a caption look from one bright frame, leaving a master undownloaded past its link window, paying to regenerate a finished-but-undownloadable take instead of contacting Support. Treat these as `product-documented pitfalls`, not as verified user reviews.
- **Structural criticism (not Slopcannon-specific):** parody likenesses of real people/characters (Hank Hill, Creed, My Little Pony, Amodei) dominate the public corpus — the product's rights-confirmation gate is doing real work here, and a builder should expect moderation/rights to be a live issue, not a checkbox.

---

## 4. Knockoffs, clones, and attempts

**Headline finding: there is no known open-source recreation of Slopcannon itself.** No GitHub repo, tutorial, or agent skill found in searches claims to replicate slop.cc's workstation (Producer + reference bank + volley + take history + song-master assembly). What exists is a spectrum from *closest architecture* to *closest product* to *name-only lookalikes*. Status labels are as of 2026-11-01.

### 4.1 Table — every relevant attempt found

| Project / tool | Type | What it gets right (vs Slopcannon) | What it misses | Status |
|---|---|---|---|---|
| **AutoMV** — https://m-a-p.ai/AutoMV/ , arXiv 2512.12196, GitHub multimodal-art-projection/AutoMV | Research, open | Closest architecture: MIR (beats/structure/stems/aligned lyrics) → Screenwriter + Director agents → shared character bank → keyframes + story/singer video gens → Verifier agent iterating. Explicitly targets full-length songs, lyric/music alignment, identity consistency. Benchmarked on 30–60 songs. | Not a product: no hosted workstation, no take-history UX, no credit/assembly workflow; paper-scale compute (8× A800 in paper). Research code, not a Slopcannon clone. | Alive as research (paper Dec 2025-era, site live) |
| **ViMax** — HKUDS/ViMax, ~12.8k stars, arXiv 2606.07649 | Open framework | Agentic director/screenwriter/producer, character bank, graph-based visual consistency, VLM-QC judger, design–generation–redesign loop. Strongest open QC/consistency ideas. | General film, not song-timed: no lyric timestamps, beat/section planning, or song-as-master assembly. Novel/script in, not MP3+lyrics in. | Alive, active |
| **sigurdtho/musicvideo-pipeline-template** — https://github.com/sigurdtho/musicvideo-pipeline-template | Open template (MIT) | Closest *buildable* pipeline: local, mostly-automated; Claude Opus headless stages; `master.md` single source of truth (lyrics/characters/style/specs); ComfyUI (Flux.2 Klein stills, Wan 2.2 clips), ACE-Step songs, BS-RoFormer stems, WhisperX alignment, beat tracking, SyncNet, karaoke overlays, human phone gates (top song takes, 480p preview <30 MiB). | Template, not product: "draft extracted from a working personal setup… no test suite", assumes RTX 4090 + local GPU stack; no volley/take-history UI, no MCP workstation. | Alive (draft) |
| **TubeTube** (tubetube.io) | Commercial | Word-by-word scene timing to audio; same characters every scene; 14 engines (Kling, Veo 3.1, Seedance 2, Hailuo 2.3, Gemini Omni Flash); 16:9 + 9:16; ~15 min median; public API + CLI; credits refunded for unused portion. Closest commercial timing model. | No named reference bank / per-scene take-history workstation described; song is generated or narrated in-platform as often as uploaded; watermark without paid plan. | Alive |
| **VidMuse** (vidmuse.ai) | Commercial | Agent workflow closest to Producer: Creative Brief → Reference Generation → Scene & Shots List → Storyboard → Video Generation; multi-model (Kling 3, Veo 3.1, Seedance 2, Hailuo 2.3); native Suno integration; performance/viral/TVC templates. | Competitor comparisons note fixed-interval (not musically intelligent) segmentation in places and no Slopcannon-style volley/take-history; $39/mo Pro, 4,000 credits, no rollover per competitor pages. | Alive |
| **Neural Frames** (neuralframes.com) | Commercial, musician-first | Strongest audio analysis: tempo/key/lyrics/structure + 8 stems driving visuals; Autopilot full song in 10–15 min; frame-by-frame (1 credit/sec), timeline + text-to-video editors; lyric + lip-synced Vocal Video modes; 4K top tier; 40k+ artists / 2M+ videos claimed. | Audio-reactive art bias: reactivity over narrative/character consistency (independent reviews note hallucination/continuity weakness); no Producer-chat + take-history workstation. | Alive (Berlin, since end 2022) |
| **Revid** (revid.ai) | Commercial | Beat-synced AI scenes from any track or Suno link; consistent characters/styles; full timeline editor; captions, Spotify-Canvas loops, direct publishing to TikTok/YouTube/Instagram/X. | Generalist (150+ formats): music video is one workflow, not a dedicated workstation; AutoMV paper found its baseline "good lyrics-visual alignment but almost no narrative structure". | Alive |
| **BeatMotion** (beatmotion.io) | Commercial | Scene per lyric line; word-level captions synced to vocals; regenerate individual scenes, switch caption styles/art style; 16:9 + 9:16; Suno/Udio/own recordings. Credit math published: Standard ~111/min, Advanced ~222/min, Premium lip-sync singer ~555/min. | Lyric-line granularity (not song-section scene planning); singer is a cast member, not a user reference bank; video in 5–7 min implies lighter QC. | Alive |
| **Suno2MV** (suno2mv.com) | Commercial | Most Slopcannon-like *editing* discipline: upload audio, verify word-level lyric sync free, edit 4–8 shots, single-shot reroll without re-rendering all, 15–30 s chorus-hook test before full commit; Whisper word timestamps; Flux keyframes + Hailuo motion; 16:9/9:16/1:1. | Only 4–8 shots (not a full scene timeline for a whole song); Suno-focused; smaller scale. | Alive |
| **Glif** (glif.app Suno tool) | Commercial | Suno link → BPM/energy/beat positions, vocal separation + transcription, character reference sheet before scenes, lip-sync driven by isolated vocal, beat-synced cuts, multi-model (Kling 3, Seedance 2). | Workflow tool on a general platform, not a dedicated MV workstation with volley/take history. | Alive |
| **Atlabs** (atlabs.ai) | Commercial | Suno link or MP3 ≤200 MB → auto tempo/mood/genre → 6 scene concepts → Narrative vs Performance (lip-synced) → Cast consistency → Kling 3 / Veo 3.1 / Seedance 2 in one subscription; $15–29/mo tiers. | Concept-count (6) and template feel; no take-history/volley discipline published. | Alive |
| **SunoMV / suno.bi** | Commercial | Suno link → lyric-sync preview + storyboard free (3 links/day); prompt-hash cache so regenerating a shot with same prompt doesn't re-charge. | Suno-only framing; export needs Pro ($39.9/mo, 5,000 credits). | Alive |
| **Kaiber** (kaiber.ai) | Commercial, incumbent | Beat Sync batches (up to 10 videos at once on Pro); famous via Linkin Park "Lost". | The cautionary tale: $10–99/mo but credit drain (Creator $29/mo = 1,500 credits ≈ 4 min 1080p if every render works first try, per comparisons); loop-heavy visuals, face morphs between shots, **no lip-sync** (beat triggers colour flashes, not mouths). | Alive, but losing musicians to Neural Frames/Revid on price/consistency |
| **freebeat / Solmi / Sondo / MVLAND / MusVideo** | Commercial, adjacent | Each nails one slice: freebeat = quick beat-synced singer videos from Spotify/Suno/YouTube links; Solmi = lip-synced performer; Sondo = phone-first song+photo; MVLAND = cinematic beat-synced; MusVideo = Gemini audio analysis + 4 models (Grok 6–30 s scenes, Kling 3, Wan 2.5). | None combines reference bank + section planning + volley + take history + song-master assembly. Mostly short-form / single-workflow. | Alive (various) |
| **MiniMax Video Agent** (Hailuo) | Commercial agent | True agentic: brief → narrative → scene scripts → shot composition → generation → edit + synced audio; character consistency in Hailuo 2.3. | General video agent, not song-timed; 60 s demo scale, not full-song workstation. | Alive (beta-era) |
| **ShowMaker Studio** | Commercial / guide | Best public lip-sync *diagnosis* (four causes: wrong audio, line longer than clip, model said wrong words, face too small in wide shot; ~15 words ≈ 6 s, so don't cram 25 words into 8 s). | A studio/guide, not a Slopcannon clone; use its diagnostic as a QC checklist (§6). | Alive |
| **Tuidra musicvideo-maker** (GitHub, via dev.to) | Open, lyric-video only | Whisper + phonetic/Romaji matching of user lyrics to audio, MoviePy assembly, lyric overlay on video. | No generated scenes, no characters, no narrative — lyric video, not music video. | Alive (niche, Japanese-focused) |
| **lyrics-transcriber** (PyPI 0.73) | Open pipeline piece | Word-level karaoke assets: AudioShake/Whisper transcription, Genius/Spotify/Musixmatch lyrics, human review UI, ASS/LRC/CDG/video export. | Transcription/alignment only — a *component* for §6, not a video generator. | Alive |
| **cinetic skill** (GitHub Leonxlnx/cinetic) | Open agent skill (motion design) | "Taste and slop" catalogue: hard bans (incl. text/logo rules), per-frame review, lint script — the QC-checklist idea in executable form, directly applicable to §6 gates. | Motion-design skill, not music video; no audio/song logic. | Alive |
| **SlopCast** (slopcast.tv) | Curator, NOT generator | Human-curated AI-MV jukebox/TV app (Samsung TVs), credits per video, human watches every submission before air. | Does not generate anything — a distribution/curation answer to slop, not a clone. | Alive |
| **SlopBop** (slopbop.com) | Agentic label, NOT workstation | Synthetic artists with personality/voice/taste; public jams (users write lyrics, most popular becomes single); mixtape commissions. | Music label concept; videos are an output of the label, not a user workstation. | Alive |

### 4.2 Tutorials / agent skills that *attempt* the same thing
- **The Starbelo prompt pattern** (§3.1) is the closest thing to a "tutorial" for Slopcannon itself: lyrics + timestamps + named one-line character looks → 8 section-following scenes → paste into Slopcannon. It is a *use* tutorial, not a recreation.
- **sigurdtho's template + cinetic's taste-and-slop catalogue + AutoMV/ViMax papers** together are the closest thing to a build-it-yourself curriculum: pipeline template (how to stage it), papers (how to architect agents + verifier), skill (how to QC it). No single tutorial ties them into a Slopcannon-equivalent product.
- **No agent skill, MCP server, or open repo found that exposes Slopcannon's own API/MCP** — Slopcannon's MCP is documented as a *client-facing* capability (connect Claude/Codex/Grok to Slopcannon), not as an open-source server to self-host.

### 4.3 Scam / lookalike warning
- **docs.slopcannon.dev is NOT the music workstation** (see §4.5 below) — the single most likely confusion for a builder searching the name.
- **Unaffiliated tokens:** a Solana token literally named "slopcannon" (SLOPCANNON) appears on CoinGecko/DexScreener (one crawl: ~$0.00012, FDV ~$118k; prices moved sharply between crawls) and a separate meme token $SLOPCAT / "SLOPCANNON CAT" (slopcat.site, contract on pump.fun). **No endorsement, link, or acknowledgement of either token was found on slop.cc or sloptoberfest.slop.cc.** Treat both as unaffiliated name reuse; do not buy, integrate, or cite them as Slopcannon. A larpcheck.app note flags the $slopcannon coin as "partly real" (a real token with a creator-fee coin framing) — that is about the token, not about the workstation.
- **No evidence found** of a fake slop.cc login/phishing clone in searches, but the token + docs collisions are enough to require exact-domain verification (slop.cc, sloptoberfest.slop.cc) for anything claiming to be Slopcannon.

### 4.5 The unrelated docs.slopcannon.dev — why it is NOT the workstation
- **What it is:** "Slopcannon is an AI slop detection tool for GitHub pull requests. It analyzes code changes to identify patterns commonly associated with AI-generated code that may need human review." — https://docs.slopcannon.dev/ (crawled 2026-07-21).
- **Its "slop" taxonomy (code, not video):** mystery fallbacks (empty catch blocks, generic error handling), silent failures (swallowed exceptions, ignored return values), overly verbose code, copy-paste artifacts, complexity bloat.
- **Its features:** automated PR scanning via GitHub webhooks, an objective "slop score", team insights over time, "Ghost Mode" (analyse silently without posting PR comments, the default), install as a GitHub App, per-repo/org settings, dashboard.
- **Why the confusion happens:** identical name ("Slopcannon"/"slop cannon"), same "AI slop" vocabulary, and a shared theme (catching low-quality AI output). **Why it is unrelated:** different domain (.dev vs .cc), different medium (code PRs vs music video), different company/product surface, no cross-link, no shared founder credit found, and its docs predate the Sloptoberfest-era music product's public push. It is, however, a *useful cousin* for §6: its slop-score + ghost-mode ideas are exactly the kind of silent, scored QC pass a good video pipeline needs — borrowed as an idea, not as a product relationship.

---

## 5. The generic "slop cannon" idea

### 5.1 Definition (Eigenform, the canonical post)
- "A slop cannon is an AI pipeline that fires out fluent, confident output at scale without catching its own errors." / "A slop cannon is what you get when you try to prompt your way to accuracy." — https://www.eigenform.ai/insights/how-not-to-build-a-slop-cannon/ (published 2026-08-20, updated 2026-09-29).
- Key distinction: "The term, sometimes written slopcannon, describes the *system* rather than the model." / "not a bad model, but a badly designed system around a model." And: "AI slop is low-quality content generated by AI and published at scale with little human checking. It tends to read smoothly while being vague, repetitive or wrong."
- The unit of trust: "Because model outputs are non-deterministic, the unit of trust should be the system's ability to catch and correct its own errors, not any single output's correctness."

### 5.2 The five Eigenform principles (verbatim in substance)
1. **Shorter is almost always better** — split work into smaller sub-agents that check each other's outputs. If agent B needs agent A's output, it will demand a proper job; a single agent whose step A failed will more likely hallucinate and continue.
2. **Fixable is better than perfect** — use a QC pass with a checklist instead of a "don't make mistakes" instruction. "Submitting its work to a second QC agent with a list of common mistakes to check for definitely will [reduce mistakes]." Test the rubric before testing the model.
3. **Design for the smallest model that works** — cost, and fragility: a pipeline that only works on the latest flagship is vulnerable to guardrail/system-prompt edits beyond your control and is probably badly designed. Benchmark candidates on *your* task, not a general leaderboard.
4. **It's OK to fail, it's not OK to fail silently** — tag outputs by confidence: [confirmed_data], [inferred_information], [necessary_assumption], [code_results], colour-coded in UI, so uncertainty stays visible. "Visible uncertainty is a better signal of harness quality than confident-sounding output."
5. **Chat history is a variable** — do not passively accumulate history. Feed an agent only the specific information it should respond to (e.g. agent A's output + what to do with it), not the entire conversation that produced it. Otherwise contexts become "insane and self-contradictory glossolalia" and the model starts forgetting bits as you yell corrections.
- **Case study (the proof):** NextMaps' exploration-analytics pipeline, stress-tested on Western Australian gold licence E 09/1325 with 56 WAMEX reports (1995–2022) whose boundaries shifted repeatedly. The naive system would misattribute neighbouring major gold discoveries to the licence. The good harness **computed every place/drillhole's true distance from the licence boundary from coordinates before the model wrote a word**, then ran a separate verification pass against the same ground truth. Result: a "High" prospectivity rating justified *only* from inside-boundary evidence (Thunderbolt occurrence, 322 drillholes, 18.8 g/t Au intercept inside the licence), explicitly refusing to use neighbours, and volunteering what it could not support (resource figures spanning several tenements; only 7 holes in the NE). The postscript: Thunderbolt is now described by Benz Mining as its largest upside target — the pipeline found it from pre-2022 public data alone.

### 5.3 The people-sense (Handy / AugmentedSWE) — same term, different lens
- Handy (https://handyai.substack.com/p/the-slop-cannons-in-your-engineering): a "slop cannon" is also a *person* who "weaponized these tools against their own team" — runs 3+ agents in parallel by default, generates "like a lawn sprinkler", confuses volume for value, velocity for progress, tokens for problems solved; PRs large/fast/confident, median needing a follow-up patch within two weeks; posts terminal screenshots with rocket emojis; cannot explain their own diff; distrusts human review more than the model. Detection metrics: revert/hotfix rate 2× team average; median PR >800 lines = yellow flag, >1,500 = slop cannon; token burn 3× median at/below-median shipped value; "read the prompts, not just the code."
- AugmentedSWE (https://www.augmentedswe.com/p/ai-slop-cannons-and-their-consequences): "a very high-output software engineer that doesn't emphasize quality enough"; short-term productivity is eaten by technical debt; "agentic passive voice" ("Claude wrote a PR that did x") as a tell.
- **Lesson for a video builder:** the human failure mode and the pipeline failure mode are the same shape — *throughput without a checkpoint*. A music-video tool that lets a user fire 100 scenes and publish without ever watching a cut is a slop cannon with a nicer UI, whatever its branding.

### 5.4 Anti-pattern lessons distilled (the bridge to §6)
- **Stage separation:** compute facts before the model writes (timing, boundaries, word times); let the model write only what it can write; verify after against ground truth. Never ask the model to *derive* the timing it will be judged against.
- **QC checklists, not exhortations:** "don't make mistakes" / "be accurate" / "no garbled text" in a prompt is the slop-cannon move. A second pass with a named checklist (text, logos, hands, faces, continuity, sync) is the fix.
- **Confidence tagging:** confirmed (measured from audio/file) vs inferred (section label, mood) vs assumed (user claim, uncorroborated lyric) must be visible in the UI and in the project file — and must gate what gets published vs what gets flagged.
- **History management:** the project state (song analysis, scene plan, reference assignments, take choices) is the memory — not the chat transcript. Feed each agent only its stage's inputs + the compact state.
- **Fixable > perfect, and cheap to catch:** per-scene reroll, cost preview, take history, and "fail visibly" (list empty/failed scenes *before* assembly instead of silently skipping them — Slopcannon's own assembly prompt pattern) are what make errors cheap. A system that charges for a full re-render to fix one scene, or silently drops a failed scene, is a slop cannon even if its clips look good.

---

## 6. Best version — synthesis for a builder

This section is **synthesis / recommendation**, not a report of what Slopcannon does. Each recommendation names the source it is borrowed from; where a recommendation goes beyond any source, it is marked `builder inference`.

### 6.1 Design stance (one paragraph)
Build a *workstation*, not a generator: a durable project (song analysis + scene plan + reference bank + take history + assembly manifest) that a user *and* a chat agent can both edit, where every expensive action shows its exact cost before it runs, every scene can be fixed alone, and the final master is assembled from the user's song — never from generated audio. Borrow Slopcannon's project model, AutoMV's verifier, Eigenform's harness discipline, and the commercial tools' timing math. Avoid Kaiber's credit-drain opacity, the one-shot prompt box, and any design where a failed scene silently disappears.

### 6.2 Intake and timing — the foundation everything else stands on
1. **Ingest + fingerprint first.** Accept MP3/MP4 (and WAV/FLAC/M4A — LyricMV's format list is a sane baseline). On ingest, record: file hash, container/codec (ffprobe), duration, sample rate, channel layout, loudness (LUFS), and a chroma/audio fingerprint. Store the *delivered* file as immutable; never overwrite it with a re-encode. (`builder inference` from the mission's MP3-or-MP4 requirement + aidust.io's ffprobe advice.)
2. **Separate the stems you need, once.** Vocal stem (for lyric alignment + lip-sync guidance + caption timing) and instrumental stem (for beat/section analysis without vocal interference). BS-RoFormer (sigurdtho template) / Demucs-class separation is the open baseline; Neural Frames' 8-stem idea is overkill unless you drive stem-reactive visuals — for a narrative MV, vocal + instrumental + a drum/onset track suffice.
3. **Beat + section detection, computed — not prompted.** Beat/downbeat tracking (librosa/madmom/Essentia class; MTL Audio Locators' recipe is a good reference: features → clustering → boundaries **snapped to nearest beats** → section labels by position heuristics). Output a section map (Intro/Verse/Pre-Chorus/Chorus/Bridge/Outro + bar numbers) with *boundary confidence* (confirmed = beat-snapped + lyric-boundary agreement; inferred = audio-only). Section *labels* are heuristic — boundaries are more reliable than labels (MTL's own limitation note) — so surface that uncertainty, per Eigenform principle 4.
4. **Lyric timestamps by forced alignment, not by transcription alone.** Take the user-supplied lyrics as the *text of record*; align them to the vocal stem with WhisperX-class forced alignment (word start/end times). Diff the alignment against a straight transcription: every word where transcription ≠ supplied lyric, every dropped word under loud instruments, every scat/name mishearing becomes a **flagged caption/lyric item** for the user to correct *before* planning — exactly Slopcannon's "correct the detected words" step, but made explicit as a QC gate. If the user supplies no lyrics, transcription *is* the text of record and gets a lower confidence tag.
5. **Re-timing a grid to the delivered track (the mission's hardest requirement).** This is where most clones silently fail, so make it a first-class subsystem:
   - **Never trust a plan made against a different master.** If the user re-uploads, swaps MP3↔MP4 audio, or the chat conversation references timings from an earlier version, treat the new file as a *new timeline* until proven otherwise.
   - **Anchor + warp:** fingerprint/align the new audio to the old grid with cross-correlation on chroma/onset envelopes at multiple anchor points (start, each section boundary, end). Compute offset + drift (linear tempo/silence-trim differences) and, if drift is non-linear (different edit), fall back to dynamic time warping on chroma and *re-derive* section boundaries from the new file rather than stretching the old ones.
   - **Rule:** re-time the *scene grid* (scene start/end, word times, caption times) to the delivered track; **never time-stretch the song** to fit the video, and never stretch/speed video audio — the song is the master clock (Slopcannon's assembly rule, generalised). If alignment confidence at any anchor is low, flag that section as [assumed] and require a human listen before firing it.
   - **MP4 input:** extract the audio stream losslessly-ish (no re-encode if possible), record its exact start offset / any leading silence, and keep the video's own frame rate + timebase in the project file so a later 9:16 reframe doesn't drift by a frame.
   - **Chat conversation as a timing source:** parse any timestamps the user mentions in chat as *claims* (tagged [assumed] until matched to a detected beat/word time within tolerance, e.g. ±250 ms for a word, ±1 beat for a section). Never let a chat timestamp silently override a measured one — show both and ask.

### 6.3 Scene planning — from song map to shootable plan
- **Schema (borrow from Slopcannon + AutoMV):** each scene is a self-contained record: `id, section, start, end, duration, lyric_span (word indices), direction (one action, one place, one camera move, light), references[] (by name, per-scene subset only), audio_excerpt_id, lip_sync (on/off + which line), take_history[], chosen_take, status, cost_to_reroll, qc_flags[]`. This record — not the chat — is what the video model is prompted from, and what the agent edits.
- **Planning rules (Slopcannon's, kept):** one action per scene; "then" more than once = split; cuts on beats/section boundaries; chorus gets a *change in knowledge* (or visual escalation), not just a brighter location; performance scenes know their line; non-sung moments get lip-sync off.
- **Planner agents (AutoMV/Eigenform):** split planning into Screenwriter (story arc across sections, character appearances per section) and Director (per-scene shot/camera/light + reference assignment), with a third *Continuity* checker that verifies: every named character in a scene has a reference assigned; no scene assigns every reference; variants are used only in their scenes; no scene asks for more than the model can do in its duration (ShowMaker's rule: ~15 words ≈ 6 s of speech — if a line is longer than its scene, split the scene or cut the line's coverage, don't speed the delivery).
- **Cost preview before any fire** (Slopcannon's best UX idea): show exact credit/time cost for the full volley *and* per-scene reroll cost, and block submission if balance is short — with the shortfall stated, not a partial fire.
- **Chat as director (the mission's chat-conversation input):** the chat agent must speak in scene numbers ("Scene 7", "the second chorus"), name references, and state cost impact *before* the user approves — Slopcannon's Producer pattern. Proposals are diffs to the scene plan, not free text; the user approves a diff. History fed to the planner is the compact project state + the current diff, never the raw transcript (Eigenform principle 5).

### 6.4 Character reference banks — the consistency engine
- **Borrow Slopcannon wholesale:** one pool per project; named references (person/outfit/prop/place); per-scene subset assignment; variants for story change (never edit the original); identity described separately from outfit and mood in the label.
- **Additions (`builder inference` + ViMax):** store per-reference: canonical image(s) (1–2 clear, front-ish, well-lit — not a dozen), a short identity card (face/hair/build/skin tone in neutral terms, outfit, palette), and a *negative* list (what this reference is not). On generation, pass only the scene's subset + its identity cards; on QC, run a face/identity similarity check between the generated take's first/mid/last frames and the reference (threshold → flag, not auto-reject). Keep a "character appears in scenes X, Y, Z" index so a variant change can be scoped correctly.
- **Rights gate (Slopcannon + §3 parody lesson):** per-project confirmation for every face/logo/image; a separate gate for *real-person likeness* (parody disclosure, platform synthetic-media rules) and for *licensed characters/logos* (block or require proof). Log the confirmation in the project file — it is part of the deliverable's provenance, not a popup to click past.

### 6.5 Generation volleys and reroll rules
- **Volley (Slopcannon):** fire all ready scenes in parallel; attach each finished clip to its scene as a new take as it arrives; jobs survive browser close/device change; failed/no-deliverable = credit hold released, scene keeps its plan.
- **Reroll discipline (Slopcannon + aidust.io's "change one thing per run"):**
  1. Watch the whole cut before rerolling anything.
  2. Name the defect in one sentence + one measurable fix (direction change, reference swap, or — only with a stated reason — same-prompt retry).
  3. Reroll only the listed scenes, together, so takes can be compared side by side.
  4. Keep every take; mark the chosen take explicitly; never auto-pick the newest.
  5. One variable per reroll: if you change direction *and* references *and* aspect, you learn nothing.
  6. If a take is finished but undownloadable, or moderation-refused, follow the recovery/sanitise path — do not pay to reshoot blind.
- **Model strategy (Eigenform principle 3 + commercial reality):** support a small model matrix (e.g. one cinematic, one stylised, one fast/cheap) behind the same scene schema; benchmark on *your* scenes; never let a single flagship model's guardrail change break the whole pipeline. Allow per-scene model override, but record it in the take (provenance).
- **Scene-length realism:** video models generate short clips (commercial tools advertise ~3–30 s/scene depending on model). Plan scenes to fit the model's native duration; if a section is longer than one clip, split it into multiple scenes at beats — do not ask one clip to cover a whole chorus and hope.

### 6.6 QC gates — the anti-slop-cannon layer (run before assembly, and again on the assembled master)
Run these as *separate, named checks* with pass/flag/fail per scene, not as prompt adjectives. This is Eigenform's QC checklist + docs.slopcannon.dev's scored-detection idea + cinetic's hard-ban catalogue, applied to video:

| Gate | What it checks | Fail / flag action |
|---|---|---|
| **On-screen text** | OCR every take's frames (sampled + first/last): any rendered text that is not in the approved text list, any garbled/misspelled word, any text that drifts/morphs across frames. | Flag → either remove the text from the shot's direction and re-render, or (preferred) **do not generate important text at all** — add it in post as a real overlay (aidust.io / versely.studio consensus: models "paint" text as texture, they do not typeset). |
| **Wordmarks / logos** | Logo/brand detection + a blocklist of protected marks; any logo that reads differently in frame 1 vs frame 40; any unapproved brand appearing. | Flag → crop/blur in post if incidental, or reroll with the logo removed from direction; never ship a morphing logo. |
| **Licensed / rights material** | Faces/characters/logos vs the rights gate (§6.4): real-person likeness, copyrighted character, stock/watermarked imagery, unconfirmed reference. | Hard fail → block assembly until confirmed, replaced, or disclosed as parody per platform rules. |
| **Lip-sync** | Per performance scene: word-time alignment of the take's mouth movement vs the lyric span (phoneme/viseme plausibility, not pixel perfection); line-longer-than-scene check; face-size check (wide shots have too few mouth pixels — ShowMaker rule: shoot dialogue medium or closer, use wides for entrances/reactions). | Flag → split the line across scenes, tighten framing, toggle lip-sync off for that scene (story scene, not performance), or reroll with a closer framing. Do not speed delivery. |
| **Character / continuity** | Identity similarity vs reference bank (first/mid/last frame); outfit/variant correctness per act; prop/location continuity across adjacent scenes. | Flag → reroll that scene with the correct subset/variant; if drift is systemic, fix the reference (one clear image) before rerolling more scenes. |
| **Anatomy / motion** | Hands, faces, limbs, object permanence (appearing/vanishing/merging objects), flicker. Sample at half speed on edges/hands/text (morphic guidance). | Flag → trim before the failure point (the classic edit fix), reroll, or simplify the scene (fewer interacting elements). |
| **Audio / sync** | Assembled master: song waveform alignment to scene boundaries (cuts on beats), no gaps/overlaps, no generated-audio bleed, loudness in range, caption word times vs vocal times. | Hard fail → re-assemble from the manifest; never patch by stretching audio. |
| **Captions** | Caption text vs corrected lyrics (exact match after user corrections); timing per word; contrast/readability on brightest *and* darkest shots; safe-band compliance (9:16: 14–65% height, clear of side rails); no face covered by a caption block in the vertical master. | Fix in post (captions are overlays, never a reason to re-render) and re-assemble — free. |
| **Provenance / disclosure** | Every take records model, prompt/direction version, references used, cost; master records song source + rights confirmations + AI-disclosure text for the target platform. | Missing provenance = do not publish; platforms increasingly require synthetic-media disclosure. |

**Confidence tagging on the QC report itself (Eigenform):** each scene's QC line is tagged [confirmed] (measured: timing, OCR, loudness), [inferred] (model-judged: identity similarity, lip-sync plausibility), or [assumed] (user claim: rights, lyric correctness where no alignment exists). The user sees the tags; a scene with only [assumed] on a rights or sync item cannot be marked ready.

### 6.7 Assembly — song as master, captions in post, two masters
- **Assembly order (Slopcannon, kept):** chosen takes only, in timeline order, each trimmed to its song passage; **original song as the sole soundtrack**; generated clip audio dropped entirely (no bleed, no ducking tricks). Assembly is free to repeat — so re-assembly after a caption fix or a single-scene swap costs nothing.
- **Captions in post (Slopcannon + BeatMotion/Suno2MV):** render captions from the corrected word-time map (ASS/LRC-style timing data kept in the project file) with a real typesetting renderer, in the chosen look (karaoke sweep, kinetic, punch, subtitle, etc.), colour/size/place adjustable, previewed with the same renderer as the master. Never bake captions into generated footage; never let a caption fix trigger a re-render.
- **16:9 and 9:16 masters — do not just crop.** Slopcannon's rule (choose aspect before the first pass) is honest about cost but wasteful for a builder who must ship both. Best version:
  - Plan once (sections, lyrics, references, story), but **compose per aspect**: keep a shared scene plan with per-aspect framing notes (subject position, safe areas, caption band) and generate per-aspect takes *or* generate once with safe-area framing (subject centred, action within the 9:16 crop box of the 16:9 frame) and verify both crops.
  - `Builder recommendation:` if budget allows, generate two volleys (one per aspect) from the same plan — it costs ~2× generation but avoids the "vertical is a bad crop of horizontal" failure that dominates short-form complaints. If budget does not allow, generate 16:9 with a 9:16 safe-area overlay shown during planning, then do a dedicated 9:16 QC pass (face not covered, captions in 14–65% band, no platform-button collisions) and re-render only the scenes that fail the vertical pass.
  - Deliver both masters + a caption-sidecar (SRT/ASS) + the project manifest (scene plan, take choices, QC report, rights confirmations) so the video is re-editable without the tool.
- **Delivery specs (sane defaults):** MP4 (H.264, progressive), 1080p masters (4K only as an upscale pass, not a generation resolution — generation at 2K-class quality, per Slopcannon's Quality 2K framing), loudness-normalised song, thumbnail/poster frame per aspect, and a 15–30 s chorus-hook cut for short-form testing *before* committing to a full-song render (Suno2MV's best idea — test the aesthetic cheaply).

### 6.8 Delivery, pricing, and what to avoid
- **Pricing model to copy:** Slopcannon's — per finished second, exact total shown before firing, reroll charged per scene only, assembly/captions/downloads free, failed renders refunded, insufficient balance blocks submission (no partial fire). This is the single most trust-building pricing design in the set; Kaiber's opaque credit drain is the anti-pattern.
- **Strongest ideas borrowed, by source:**
  - *Slopcannon:* project-not-prompt-box; per-scene reference subsets; volley + take history; song-as-master; captions in post with a 9:16 safe band; cost preview; "list empty scenes before assembling, don't skip them."
  - *AutoMV:* MIR-first planning; Screenwriter/Director split; shared character bank; Verifier agent iterating (not just generating).
  - *ViMax:* graph/dependency tracking for consistency; VLM-QC judger; design–generation–redesign loop.
  - *Eigenform:* stage separation (compute before writing, verify after); QC checklist over exhortation; confidence tags, colour-coded; history as a compact variable.
  - *docs.slopcannon.dev (idea only):* a scored, silent (ghost-mode) detection pass that flags without blocking creative flow — the QC report should exist even when the user doesn't ask for it.
  - *sigurdtho template:* single source of truth file (`master.md`-style) + human phone gates + small preview artifacts before committing to full cost.
  - *Suno2MV:* free timeline/lyric verification + chorus-hook test before full spend; single-shot reroll.
  - *BeatMotion/Neural Frames:* published per-minute credit math; stem-aware timing; word-level caption timing.
  - *ShowMaker:* lip-sync diagnosis (four causes) as a checklist, not a vibe.
- **Weakest ideas to avoid:**
  - One giant prompt / one-shot full-song generation (no scene to fix, no take to keep).
  - "Don't make mistakes" / "no garbled text" as the QC strategy; generating important text/logos inside the clip instead of overlaying in post.
  - Letting chat history be the project memory (long, contradictory, forgotten instructions).
  - Charging for full re-renders to fix one scene; silently dropping failed/empty scenes; server assembly that drops captions without warning.
  - Aspect ratio as an afterthought (crop-and-hope vertical).
  - Credit opacity (Kaiber pattern) and token/name lookalikes as distribution (the $SLOPCANNON/$SLOPCAT pattern).
  - Claiming model/partnership involvement from a tag or quote-post (the thoughtcrime/Wang lesson) — in product copy *and* in QC provenance, a claim needs a record, not a mention.
  - Parody/likeness as a default: if the public corpus is mostly real-person/character parody, the rights gate is not a footnote — it is a launch blocker.

---

## Could not verify / open questions
1. **Bone's identity, background, and Slopcannon's launch date** — not found in public sources searched; X itself was not directly readable (sign-in/paywall-adjacent) and no interview/blog was indexed. The mission's "what did he post and blog, when" cannot be fully answered from the open web alone; the dated public record found here is Sep–Oct 2026 (wiki Sep 29–30, MCP Sep 24, own-footage Sep 27, Sloptoberfest Oct, Muse Wonder early-access Oct 12).
2. **Which video model(s) power Slopcannon's Quality 2K**, and whether Meta Muse Wonder powers the Producer or any generation step — not published on pages read. The thoughtcrime "Muse" credit is unverified as a technical claim.
3. **Slopcannon pricing beyond the per-second rate** (pack sizes, subscription, trial amount, free tier) and **limits** (max song/scene length, max references, max scenes) — not on public pages read; the studio is behind sign-in and was not entered.
4. **Whether muse.slop.cc is a former name, a subdomain product, or the same app** — only a YouTube description attests to it; no Slopcannon page found here explains the relationship. The current homepage links "Legacy Studio" without explaining its lineage.
5. **Sloptoberfest winners** — due 1 Nov, announced 7 Nov 2026 (after this research date for the announcement); winners, and whether thoughtcrime's X post became a valid entry, are not yet knowable.
6. **Systematic user reviews/complaints for slop.cc** — no review corpus found; §3.4's pitfalls are product-documented, not independently verified user complaints.
7. **Affiliation of docs.slopcannon.dev, $SLOPCANNON, $SLOPCAT with slop.cc** — no affiliation found; treated as unrelated, but absence of a link is not proof of no relationship (no denial statement was found either).

## Sources
- https://slop.cc/ — homepage, verified live 2026-11-01
- https://slop.cc/faq — FAQ (19 Qs), verified live 2026-11-01
- https://slop.cc/wiki/features — Inside the Cannon index, verified live 2026-11-01
- https://slop.cc/wiki/the-producer — Producer guide, updated 2026-09-30, verified live
- https://slop.cc/wiki/reference-bank — reference bank guide, updated 2026-09-30
- https://slop.cc/wiki/scene-timeline — scene timeline guide, updated 2026-09-30
- https://slop.cc/wiki/firing-the-cannon — firing guide, updated 2026-09-30
- https://slop.cc/wiki/takes-and-rerolls — takes/rerolls guide, updated 2026-09-30
- https://slop.cc/wiki/final-assembly — assembly guide, updated 2026-09-30
- https://slop.cc/wiki/cannon-credits — credits guide, updated 2026-09-30
- https://slop.cc/wiki/video-captions — captions guide, updated 2026-09-30
- https://slop.cc/wiki/caption-styles — 12 caption looks, updated 2026-09-30
- https://sloptoberfest.slop.cc/ — contest page, live 2026-11-01 (deadline now 1 Nov 2026 4am EST, winners 7 Nov)
- https://starbelo.com/use-case/ai-music-video-slopcannon-alexandr-wang/ — thoughtcrime case, updated 2026-11-01, secondary
- https://runtimewire.com/article/slopcannon-creator-credits-muse-in-insane-ai-video-posted-for-sloptoberfest — 15–16 Oct 2026, secondary, with caution on tags
- https://thegenaimagazine.com/meta-muse-wonder-review-benchmarks-price-vs-opus-astra-fable — Bone early-access account, secondary
- https://thenyledger.com/markets/ai-slop-is-coming-for-hollywood-some-of-it-is-already-better/ — 4 Oct 2026, Amodei Slopcannon video
- https://www.youtube.com/watch?v=yZfTk7mDV2U — SLOPTV Vol. 2, 1.5h community compilation
- https://www.youtube.com/watch?v=5UeNFfqOYks — Making the Girl Who Got Away, "made on muse.slop.cc"
- https://docs.slopcannon.dev/ — UNRELATED GitHub-PR slop detector, crawled 2026-07-21
- https://www.eigenform.ai/insights/how-not-to-build-a-slop-cannon/ — generic slop-cannon, 2026-08-20 / updated 2026-09-29
- https://handyai.substack.com/p/the-slop-cannons-in-your-engineering — people-sense slop cannon
- https://www.augmentedswe.com/p/ai-slop-cannons-and-their-consequences — people-sense slop cannon
- https://m-a-p.ai/AutoMV/ and https://arxiv.org/pdf/2512.12196 — AutoMV research system
- https://arxiv.org/pdf/2606.07649v2.pdf — ViMax
- https://github.com/sigurdtho/musicvideo-pipeline-template — local pipeline template
- https://github.com/Leonxlnx/cinetic/blob/main/skills/cinetic/references/taste-and-slop.md — taste-and-slop QC catalogue
- https://dev.to/tuidra/auto-generate-lyric-music-videos-from-mp3-with-python-whisper-and-tuidra-4m3k — Tuidra lyric video
- https://pypi.org/project/lyrics-transcriber/0.73.0/ — lyrics-transcriber
- https://www.revid.ai/vs/neural-frames — Revid vs Neural Frames comparison, checked Sep 2026
- https://www.designer-daily.com/best-kaiber-alternative-6-ai-music-video-makers-without-the-credit-drain-234185 — Kaiber credit-drain comparison
- https://rareconnections.io/neural-frames-review — Neural Frames review
- https://beatmotion.io/faq — BeatMotion credit math
- https://suno.bi/best-ai-music-video-generator — 8-tool comparison, updated 2026-10-10
- https://vidmuse.ai/blog/the-ultimate-guide-to-vidmuse — VidMuse workflow/pricing
- https://beatmotion.io/tools/suno-to-video , https://suno2mv.com/ , https://glif.app/use-cases/suno-music-videos , https://www.atlabs.ai/blog/best-5-ai-music-video-tools-for-your-suno-song-in-2026-(reddit-recommended) — BeatMotion, Suno2MV, Glif, Atlabs
- https://slopcast.tv/ — SlopCast curator (not a generator)
- https://www.slopbop.com/ — SlopBop agentic label (not a workstation)
- https://www.slopcat.site/ and https://www.coingecko.com/en/new-cryptocurrencies?items=300&page=2 — unaffiliated $SLOPCAT / $SLOPCANNON tokens
- https://aidust.io/blog/video-to-video-ai-troubleshooting/ , https://www.versely.studio/blog/why-ai-video-artifacts-happen-fixes , https://gptproto.com/news/ai-video-generates-wrong-text — text/logo QC consensus
- https://showmaker.studio/blog/ai-video-lip-sync — lip-sync diagnosis
- https://musictechlab.io/blog/music-data/automatic-song-structure-analysis-how-ai-detects-intro-verse-chorus — section detection recipe + limits
