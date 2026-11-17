# Gossip Goblin — X (Twitter) Timeline Inventory
**Handle:** @gossip_goblin (task brief; TwStalker renders as @Gossip_Goblin)  
**Display name:** Gossip Goblin  
**Creator:** Zack London  
**Slice:** X timeline only, as complete as publicly reachable WITHOUT login  
**Scrape date:** 2026-11-16 / 2026-11-17 03:06–03:09 UTC crawl of TwStalker  
**Primary source that worked:** https://twstalker.com/gossip_goblin

> **Coverage warning — read first:** TwStalker's text extraction is noisy and incomplete. It rendered the recent timeline posts (text + a few media images) but did **NOT** render in extractable text: dates/timestamps, like/retweet/reply counts, the profile header block (bio / location / link / follower counts / join date), or any "load more" pagination links. All items below with no date/engagement are marked as such — do not treat order as verified chronology beyond "recent timeline as served on 2026-11-17". Older posts beyond this recent batch were **not reachable** via any working mirror in this run (see Routes Tried). Anything sourced from press / cross-platform coverage instead of the X timeline itself is marked **LEAD-LEVEL**.

---

## 1. Profile Header Facts

| Field | Value | Source / verification |
|---|---|---|
| Display name | Gossip Goblin | Verified — TwStalker page title: "Gossip Goblin @Gossip_Goblin - Twitter Profile \| TwStalker" |
| Handle | @gossip_goblin / @Gossip_Goblin (case-insensitive) | Verified — TwStalker URL + title |
| Profile picture | Present — TwStalker image: `https://ton-0.twimg.com/profile_images/1997311160928890880/77jxKJhT.jpg` (not downloaded, per task) | Verified — TwStalker extraction, Image 0 |
| Bio text (verbatim) | **NOT RECOVERED** — header block did not appear in TwStalker text extraction | Unverified — LEAD-LEVEL gap |
| Location | **NOT RECOVERED from X header.** Cross-platform press says: Los Angeles native, based in Sweden / Stockholm area (The AI Live Show profile: "based in Sweden"; Hollywood Reporter via EuropeSays: LA native, partner is a theatre actress in Stockholm; The Daring Creatives: moved to Sweden about four years ago) | LEAD-LEVEL — press, not X bio |
| Link(s) in bio | **NOT RECOVERED from X header.** Contextual, press-verified project link: godsdontgivegifts.com — the film site carrying the Ambassador Program, screening/ticket signup (The Daring Creatives, Gods Don't Give Gifts page, updated 2026-10-12) | LEAD-LEVEL for X bio; verified as project site |
| Followers (X) | **NOT RECOVERED** — TwStalker extraction listed follower *suggestions* ("You might like" / following-network cards with other accounts' counts), not Gossip Goblin's own count. Do NOT confuse those cards (e.g. @pmarca 6.6M, @boneGPT 65K) with this account. | Unverified — LEAD-LEVEL gap |
| Following (X) | **NOT RECOVERED** — same reason as above | Unverified |
| Post count (X) | **NOT RECOVERED** | Unverified |
| Join date | **NOT RECOVERED** | Unverified |
| Pinned post | **NOT IDENTIFIABLE** from TwStalker extraction — no pin marker rendered. First items served were a reply and lore-title posts (see inventory #1–#3); none can be confirmed as pinned. | Unverified |
| Creator identity | Zack London, AI filmmaker / writer / illustrator; studio: Gossip Goblin, Inc.; universe: the Thirteen Cycles of Humanity (press spells it both "Thirteen" and "13 Cycles") | LEAD-LEVEL — The AI Live Show creator profile; MakeUseOf, 2026-10-13 |
| Known works (context) | *Pomegranate*, *WOODNUTS*, *The Patchwright*, *Gods Don't Give Gifts* (104-min anthology feature, Fable, US theatrical Dec 4, 2026 — moved from Oct 30) | LEAD-LEVEL — press |

**What TwStalker DID pollute the extraction with:** ~70 "suggested / network" profile cards (other accounts' bios + follower counts) after the timeline — excluded from this inventory except where a retweeted author is a timeline item.

---

## 2. Post Inventory — TwStalker Recent Timeline

Order = order served by TwStalker on 2026-11-17 (presumed newest-first, NOT verified — no timestamps extracted). Dates: **none shown** in extraction for any item — all marked "not shown". Engagement: **none shown** for any item.

| # | Date | Type | Text / summary | Media | Engagement |
|---|---|---|---|---|---|
| 1 | not shown | Reply | "@halcanary These are early screenings boss - stay tuned for more updates." — reply about early screenings of the film | none indicated | not shown |
| 2 | not shown | Original (lore-title) | "Carnal Pursuits" — one-phrase lore title post; no other text extracted (likely caption/title for attached media not described in text) | media likely, not described in extraction — LEAD-LEVEL | not shown |
| 3 | not shown | Original (recruitment) | Full ambassador recruitment post — see Voice Sample V1 (long version). "Hello future goblin ambassadors! We're looking for the most wild and devoted among you to help us spread the gossip goblin lore (and news of the upcoming film!) / In exchange for your valiant efforts, you'll be rewarded with rare merch, access to screenings and events, a chance to be featured in future lore, and more!" | 1 image — TwStalker: `[Image 6: Gossip_Goblin tweet picture]` `https://ton-0.twimg.com/media/HUh7R2TXMAIHyDA.jpg` (not downloaded) | not shown |
| 4 | not shown | Retweet — @fableshowrunner (Fable) | "Amazing to see the lines of fans and international film buyers at our AMC preview screening this week! / Gods Don't Give Gifts is a Toy Story moment for animation - setting a new path - and it's coming to theatres in the US and the world - history is being made!" | none indicated in extraction | not shown |
| 5 | not shown | Retweet — @SamyazaSpeaks | "Obliteration Episode 2 / Coming Soon / Made with @AskVenice This time in 4k" | media likely (episode promo) — not described — LEAD-LEVEL | not shown |
| 6 | not shown | Original (short) | "Ambassadors welcome!" — short companion / header line to the recruitment push; extraction shows it as its own item immediately before a repeated long recruitment post | none indicated | not shown |
| 7 | not shown | Original (recruitment, duplicate / re-post) | "Hello future goblin ambassadors! We're looking for the most wild and devoted among you to help us spread the gossip goblin lore (and news of the upcoming film!) / In exchange for your valiant efforts, you'll be rewarded with rare merch, access to screenings and events, a chance to…" [truncated in extraction] — appears to be the same recruitment copy as #3, served twice (either a re-post, a quote/self-repeat, or TwStalker duplication — cannot distinguish without timestamps) | 1 image — `[Image 13: Gossip_Goblin tweet picture]` (URL not separately listed in footer) | not shown |
| 8 | not shown | Retweet — @jordanbayne | "What a privilege to see @Gossip_Goblin Gods Don't Give Gifts sneak preview last night. Beautiful visuals, sound design and score, and great performances. Congratulations to Zack London, my friend Todd Terrazas and the team. So psyched to share that room with so many friends." | 1 image — `https://ton-0.twimg.com/media/HW29czNakAAQp97.jpg` (retweet author's tweet picture; not downloaded) | not shown |
| 9 | not shown | Original (short / reflective) | "Might as well ask what we learned today." | none indicated | not shown |
| 10 | not shown | Original (lore-title) | "Grieving Freshies" — one-phrase lore title post | media likely, not described — LEAD-LEVEL | not shown |
| 11 | not shown | Retweet — @GenMagnetic | "I can't believe what I just saw. / Just wait till the world sees this. / Gods Don't Give Gifts. @Gossip_Goblin" | none indicated | not shown |
| 12 | not shown | Reply | "@TermSheet_Hero The line was original "derivative slop" but we thought it'd be too on the nose." [sic — extraction grammar; likely "The line was originally 'derivative slop'…"] — behind-the-scenes joke about a film line; connects to the Grimes-character line reported in press: "A slideshow of derivative drivel?" | none indicated | not shown |
| 13 | not shown | Retweet — @kiyasu | Japanese text: "チェコ発、人間の「対話」を常識外れに表現した怪作品。ブラックユーモアとシュルレアリスム的想像力が凝縮した、異質なコマ撮りアート。" — approx.: "From Czechia, a strange work expressing human 'dialogue' in an unconventional way. Black humour and surrealist imagination condensed — an unusual stop-motion art [piece]." Retweeted without added comment in extraction (quote vs pure RT not distinguishable) | none indicated | not shown |
| 14 | not shown | Original (quote / aphorism) | ""Everybody who disagrees with me is a bot"" — quotation marks in original extraction; standalone aphorism / quoted line | none indicated | not shown |
| 15 | not shown | Original (lore-title) | "Nameless Beings" — one-phrase lore title post | media likely, not described — LEAD-LEVEL | not shown |

**Count:** 15 timeline items inventoried from TwStalker (11 attributable to @gossip_goblin as author/reposter in own voice: 8 originals/replies + counting duplicates; 5 retweets of others included in the 15 — breakdown: Originals 6 incl. 1 duplicate recruitment, Replies 2, Short originals 2 — total own-authored items 9 distinct + 1 duplicate serving; Retweets 5: #4, #5, #8, #11, #13. Note #6+#7 may be one post split by extraction — count is therefore 14–15, stated as 15 servings.)

**Date range covered:** **Cannot be established from the source.** No timestamps were extracted. Contextually (LEAD-LEVEL), the content is all *Gods Don't Give Gifts* theatrical-rollout era: AMC preview screening, sneak preview, ambassador recruitment — which press dates to Oct–Nov 2026 (trailer Oct 6, 2026; AFM Nov 10–15, 2026; release Dec 4, 2026). The recent batch is therefore *probably* Oct–Nov 2026, but no individual post date is verified.

**Where coverage stops and why:** TwStalker served only this one recent batch, with no extractable pagination / "load more" outlinks in the text version, and its `/with_replies` variant returned an error page. All other mirrors failed (below). So coverage stops at ~15 recent servings — there is **no older-post inventory** (no 2023–2025 Cycles of Humanity era posts, no thread archives) from X in this run.

---

## 3. Routes Tried — Log

| Route | URL / query | Result |
|---|---|---|
| TwStalker profile (primary) | https://twstalker.com/gossip_goblin | **WORKED (partial)** — profile + ~15 recent timeline servings extracted (608 lines, paged 0–372 / 372–608). No dates, no engagement, no header block, no pagination links in text extraction. Remainder of page = suggested-account cards. |
| TwStalker with_replies variant | https://twstalker.com/Gossip_Goblin/with_replies | **EMPTY / ERROR** — returned TwStalker error image page (2 lines). |
| XCancel | https://xcancel.com/gossip_goblin | **BLOCKED** — HTTP 451. Not retried (per instruction not to repeat failed open). |
| Nitter (main) | https://nitter.net/gossip_goblin | **EMPTY / UNAVAILABLE** — nitter.net now serves only a project legal/funding notice (Oct 10 update: X Corp cease-and-desist Aug/Sep 2026, no legal counsel); no user timeline rendered. |
| Nitter (Poast instance) | https://nitter.poast.org/gossip_goblin | **FAILED** — browser.open: requires a resolvable public HTTP(S) URL / fetch failed, no status. Not retried. |
| Sotwe | https://www.sotwe.com/gossip_goblin | **BLOCKED** — HTTP 403 access denied. Not retried. |
| Direct X | https://x.com/gossip_goblin | **BLOCKED** — domain blocked by policy in this tool; also login-gated per task brief. |
| Xitter | — | **NOT TRIED** — down, per task brief (standing note: Xitter down, fall back cross-platform). |
| Web search: bio/profile | `"gossip_goblin Gossip Goblin Zack London Twitter bio"` | Worked for press context only — no X bio text returned. Gave creator identity (Zack London, Sweden, Thirteen Cycles, studio) — marked LEAD-LEVEL above. |
| Web search: site:x.com | `"gossip_goblin" site:x.com` | **EMPTY** — no results found. Search engine does not index the timeline this way. |
| Web search: lore titles | `"Gossip Goblin" "Carnal Pursuits" OR "Grieving Freshies" OR "Nameless Beings"` | **EMPTY for X** — no indexed matches for those posts; titles are therefore TwStalker-only evidence (still verbatim from TwStalker). |
| Web search: Second Cycle | `"Gossip Goblin" "Second Cycle of Humanity"` | Worked for film context — confirms Second Cycle is the *Gods Don't Give Gifts* setting (transhumanism, bodies disposable, consciousness commodified, Niiro Cradle) in Screen Daily / MakeUseOf / The Daring Creatives. No individual X posts returned. |
| Web search: ambassador/trailer | `"@Gossip_Goblin" ambassador OR screenings OR trailer` | Worked for corroboration — Ambassador Program on godsdontgivegifts.com: "devoted fans to spread the word, with artifacts, screening access and a chance to have your likeness put into the Gossip Goblin universe" (The Daring Creatives) — matches the X recruitment post's rewards, with "featured in future lore" ≈ likeness-in-universe. |

---

## 4. Recurring Series / Formats Identified

1. **One-phrase lore-title drops** — the signature X format in this batch: a bare evocative title as the entire text — "Carnal Pursuits", "Grieving Freshies", "Nameless Beings". Presumably captions/titles for an attached image or clip (media not described by TwStalker — LEAD-LEVEL). Voice = chapter headings from the Cycles universe, posted without explanation. Shown, never explained.
2. **Goblin Ambassador recruitment** — repeated, in two servings (long + short "Ambassadors welcome!"): fans recruited as lore-spreaders for the film, paid in merch / screenings / events / being "featured in future lore". This is the theatrical rollout's street-team mechanic, mirrored on godsdontgivegifts.com.
3. **Screening-social-proof retweet chain** — retweeting praise from preview screenings (@jordanbayne sneak preview, @GenMagnetic "I can't believe what I just saw", @fableshowrunner AMC buyers screening). The account amplifies witnesses rather than reviewing itself.
4. **Film-rollout originals (short, dry)** — replies and one-liners around *Gods Don't Give Gifts*: early-screenings reply, the "derivative slop" line-origin joke. Conversational, self-aware about the "AI slop" charge — disarming it by quoting it.
5. **Aphorism / quoted-line posts** — ""Everybody who disagrees with me is a bot"" — standalone, in quotation marks, reads as an in-universe line or a satire of discourse.
6. **Third-party work signal-boosts** — retweets with no goblin content (@SamyazaSpeaks "Obliteration Episode 2", @kiyasu Czech stop-motion post): curatorial retweets of adjacent AI / strange-animation work.
7. **(Context, NOT seen as a tagged X series in this batch — LEAD-LEVEL)** "(Second Cycle of Humanity)"-tagged pieces and trailer drops: no post in the TwStalker batch literally carries a "(Second Cycle of Humanity)" tag or a trailer link in extracted text. Press verifies: teaser Sep 28, 2026 (15 sec), full trailer Oct 6, 2026 (1m48s, YouTube), trailer views 15–16M claimed across platforms. If those were announced on X, they are in the older, unreachable part of the timeline.

---

## 5. Voice Samples — Verbatim Quotes

Short quotes, ≤50 words each, exactly as extracted from TwStalker unless noted. V1–V15 are from the X timeline (TwStalker). V16–V20 are corroborating voice/context quotes from press/project sources, labelled as such — included because the X batch alone is thin on long-form narration, and the parent study needs his narration register; do NOT attribute V16–V20 as X posts.

### From the X timeline (TwStalker, verbatim)

> **V1 — Ambassador recruitment (long, #3):** "Hello future goblin ambassadors! We're looking for the most wild and devoted among you to help us spread the gossip goblin lore (and news of the upcoming film!)"

> **V2 — Ambassador rewards (#3, cont.):** "In exchange for your valiant efforts, you'll be rewarded with rare merch, access to screenings and events, a chance to be featured in future lore, and more!"

> **V3 — Lore title (#2):** "Carnal Pursuits"

> **V4 — Lore title (#10):** "Grieving Freshies"

> **V5 — Lore title (#15):** "Nameless Beings"

> **V6 — Short recruitment (#6):** "Ambassadors welcome!"

> **V7 — Screenings reply (#1):** "These are early screenings boss - stay tuned for more updates." [addressed to @halcanary]

> **V8 — Reflective one-liner (#9):** "Might as well ask what we learned today."

> **V9 — Aphorism (#14):** ""Everybody who disagrees with me is a bot""

> **V10 — Line-origin joke, reply (#12):** "The line was original "derivative slop" but we thought it'd be too on the nose." [to @TermSheet_Hero; extraction grammar preserved]

> **V11 — Retweeted screening praise, @fableshowrunner (#4):** "Gods Don't Give Gifts is a Toy Story moment for animation - setting a new path - and it's coming to theatres in the US and the world - history is being made!"

> **V12 — Retweeted witness, @GenMagnetic (#11):** "I can't believe what I just saw. / Just wait till the world sees this. / Gods Don't Give Gifts."

> **V13 — Retweeted sneak-preview praise, @jordanbayne (#8, excerpt):** "What a privilege to see @Gossip_Goblin Gods Don't Give Gifts sneak preview last night. Beautiful visuals, sound design and score, and great performances."

> **V14 — Retweeted adjacent work, @SamyazaSpeaks (#5):** "Obliteration Episode 2 / Coming Soon / Made with @AskVenice This time in 4k"

> **V15 — Retweeted, @kiyasu (#13, Japanese, verbatim):** "チェコ発、人間の「対話」を常識外れに表現した怪作品。ブラックユーモアとシュルレアリスム的想像力が凝縮した、異質なコマ撮りアート。"

### Corroborating voice / lore register (NOT X posts — labelled sources)

> **V16 — Film premise, official synopsis via press (Cosmic Book News / film coverage):** bodies are disposable, consciousness is bought and sold, memories can be installed or removed, and death is no longer final; NiiroCore controls 97 percent of the planet's "mindshare". [Paraphrase in source except quoted "mindshare" — LEAD-LEVEL as wording]

> **V17 — London on the anthology (via Cosmic Book News):** "part speculation, part critique" — hoping audiences can "take a premise seriously, follow its emotional consequences, and let the results be strange, funny, grotesque, and sad."

> **V18 — In-film line, Grimes character Zayinth Alda (via Billboard / Consequence coverage, Nov 5, 2026):** "You dragged me to the slag heaps for this? A slideshow of derivative drivel?" — the released clip line that V10's "derivative slop" joke is playing on.

> **V19 — Pinned YouTube comment under *Pomegranate* (via The Daring Creatives — YouTube, not X):** "Pomegranate is just the beginning. Bigger, more delightfully provocative announcements coming soon!"

> **V20 — Ambassador Program, project site wording (via The Daring Creatives summary of godsdontgivegifts.com):** asks devoted fans to spread the word, with artifacts, screening access and a chance to have your likeness put into the Gossip Goblin universe as the rewards. [Source paraphrase — LEAD-LEVEL as wording; corroborates V1/V2]

**Voice read (from V1–V15):** Two registers alternate. (1) *Lore-oracle:* bare noun-phrase titles, no verb, no explanation, no hashtag — the post IS a chapter heading; the media (unseen here) must carry it. (2) *Showman-recruiter / dry peer:* warm direct address ("Hello future goblin ambassadors!", "boss"), valiant-effort mock-heroic framing for fan labour, and short self-deprecating jokes that steal the "slop" insult by quoting it first. No long narration threads, no lore dumps, no hashtags, and almost no links appear in the extracted X text at all — on X he titles and recruits; the long lore lives in the films themselves.

---

## 6. Gaps & Next Routes (for parent)

- **Header facts (bio/location/link/counts/join date/pinned)** — still open. Needs a live-browser view of x.com or TwStalker with full HTML (the text extractor dropped the header), or another mirror that renders the header block.
- **Dates + engagement per post** — still open for all 15 items, same reason.
- **Older timeline (pre-rollout, Cycles-era titles/threads)** — not reached by any working no-login mirror in this run. Xitter down, Nitter legally shuttered, XCancel 451, Sotwe 403.
- **Media descriptions** — TwStalker gave direct image URLs for 2 items only and no alt text; descriptions beyond "tweet picture" would need visual inspection (not done — task said do not download media).
- No media was downloaded. Nothing was posted anywhere.
