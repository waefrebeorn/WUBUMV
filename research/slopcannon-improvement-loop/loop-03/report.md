# Slopcannon improvement loop 3 — report

**Date:** 2026-11-12 · **Coordinator:** 15bdddfb · **Seed:** sprint 8 (c11_voice) FAILED structural — the stall branch (user msg 252, msg 288, msg 313).
**Chain cap:** 3 hops, hop 2 crosses a category boundary. **Blind draw:** one, load-bearing (§8).
**Status:** research only. No code was run, no video generated, no commit, no Telegram write, no skill edit.

## 0. The stall, restated (what loop 3 routes around)

Sprint 8 built the C11 voicing gate (YIN/pYIN + CPP + HNR) and failed the bar it was built to meet:
**boundaries 8/24 mix, 14/24 stem best of 150 combos vs the ≥80% within ±0.5 s bar; 0 combos reach it.**
The medians do not separate sung from instrumental *at all* (within 0.04 dB); pYIN's voiced fraction is
INVERTED; recall ~0.52–0.55 (the gate drops out mid-phrase); the stem leg's voicing decision calls 1,825
frames voiced where librosa calls 7,493. Demucs stays the segmenter. The bar is HELD, not lowered.
Do not re-run sprint 8's calibration.

The stall's shape matters for everything below: **the mix's periodicity is dominated by the accompaniment.**
Any feature computed *on the mix* that needs clean periodicity, clean cycles, or a clean voicing decision
inherits the same failure. Loop 3 therefore ranks highest the features that either (a) use the ONE thing
sprint 8 proved works on the mix (pYIN F0, corr 1.0000, gross error 0.00%), (b) *separate* the voice
instead of detecting it, or (c) need no periodicity at all. Features that need cycle tracking on the mix
are ranked as tests, not rescues — they share the stall's root cause.

## 1. Hop chain (audit data)

- **Seed:** sprint 8 stall — YIN/pYIN/CPP/HNR do not separate sung from instrumental on MV-14's dense mix.
- **Hop 1 (voice science, the other half of the shelf):** jitter / shimmer / voice breaks / vibrato /
  formant–LPC tracking. The clinic's own literature is the source: the voice-quality shelf was built for
  *dysphonia severity on clean sustained vowels*, and the clinic has already argued about it — which is
  exactly the information that decides whether any of it survives a dense mix.
- **Hop 2 (CATEGORY CROSS — voice science → auditory scene analysis / CASA):** Bregman ASA (1990),
  Licklider correlogram (1951), Slaney & Lyon (1990), Wang & Brown CASA + the ideal binary mask.
  Crosses from "measure the voice" to "segregate the auditory scene" — the principled answer to a mix
  whose periodicity is dominated by the accompaniment.
- **Hop 3 (back to the MV):** R5 flow interpolation (symmetric-flow MCFI, Raket et al. 2012) + R9 G7
  formalization + wubu_synth meta-thread (read on disk, verdict: toy) + slopcore PROMPTS.md (measured,
  not just read: 101 prompts) + the per-loop break-the-sync probe (repeated-chorus collapse).
- **Also carried:** R4 birdsong spectral entropy (sprint 8 rec #2 — the small experiment that decides
  before any sprint); the loop-1/loop-2 owed validations (mouth-open-vs-quiet gate, piecewise grid,
  CCA on a voicing curve) — all blocked on the stall, all re-queued behind whichever entry lands first.

Chain cap reached. No DONE node re-searched. No BAN_LIST endpoint banked.

## 2. Ranked entries

### #1 — Vibrato signature: the 5–7 Hz modulation of the F0 track (TOP-1 — sprint scoped in SPRINT_SCOPE.md)

**What it is.** Do not detect the voice's pitch — detect its *wobble*. A sung vowel carries vibrato:
the fundamental frequency undulates periodically at **5–7 Hz** with an extent of about **±1 semitone**
(~50–100 cents each side; classical norm 50–120 cents peak-to-peak). The discriminative signal is the
*temporal* modulation of the F0 contour in the 4–8 Hz band, not the F0 itself. Instruments in the
accompaniment do not produce a regular 5–7 Hz F0 modulation in the vocal range: brass-section vibrato
is slower and less regular, bass is straight, drums have no F0 to modulate. (Confound to test: a synth
lead with an LFO at 5–6 Hz — MV-14's track is brass-driven funk, so measure it; if the accompaniment
carries its own 5–7 Hz modulation, the feature fails and the experiment says so in a day.)

**Where it came from.** Hop 1, voice science — Sundberg's vibrato definition; Nix et al. 2016
(75 college vocal majors: mean vibrato rates 5.0–5.16 Hz across five vowels, SD ~0.6–0.7 Hz; below
~20 cents = straight tone, above ~150 cents = excessive; <4 Hz wide = wobble, >7 Hz narrow = bleat);
Titze's reflex-resonance model (rate largely outside conscious control — it is a physiological
signature, not a performance choice). **Critical interaction, verified in the same literature:
vibrato MASKS small random perturbations** — a sung vowel's jitter/shimmer readings are dominated by
its vibrato, not by cycle irregularity. That is why vibrato outranks jitter/shimmer: the very thing
that corrupts entry #3 *is* entry #1's signal.

**Slermable core.** F0 contour → detrend → bandpass 4–8 Hz → modulation depth (RMS of the bandpassed
contour, in cents) per frame → threshold + smoothing → vocal-activity curve → boundaries. Every input
already exists and is validated: pYIN on the mix (corr 1.0000, gross 0.00% — sprint 8 bar 1, mix leg
PASSED), c11_mir's STFT, and the sprint-8 boundary-scoring harness (ref segments + ±0.5 s window).

**C11 feasibility — HIGH.** The F0 track is already produced by c11_voice's pYIN (lego in, do not rewrite).
The new code is a detrending + bandpass + modulation-depth pass over a 1-D contour — tens of lines,
no new estimator, no separation, no cycle tracking, no model. Runs in seconds on the blade.

**Validation bar (held, same as sprint 8 — not lowered).** (a) On MV-14: vibrato-band modulation depth
separates sung from instrumental spans — median sung depth > median instrumental depth with no overlap
of the interquartile ranges, on the MIX F0 track (not the stem — the stem test is trivial, Demucs
already silences the accompaniment there). (b) Boundaries from the vibrato curve reach **≥80% within
±0.5 s** of the Demucs ref segments (sprint 8's bar, same harness, same ref — with sprint 8's own
caveat carried: a perfect gate tops out at 20/24 because ref segments 11–12 are wordless-outro Demucs
bleed). (c) **Falsifier, built into the sprint:** MV-14 is a *chant* track — chant singing may be
straight-tone. If the vocal carries no vibrato, the modulation depth is flat everywhere and the entry
FAILS FAST (a 1-day measurement, not a sprint). A null result here is a result: it kills the entry
and routes loop 4 to CASA. (d) Synth-LFO confound check: measure the modulation depth on the
instrumental-only spans; if any span shows 5–7 Hz modulation above the sung median, the feature is
contaminated and the bar is not met.

**Replaces / enables.** Replaces the c11_voice gate as the vocal-activity sensor if it passes — same
bar, same harness, a different (temporal) feature. Enables: the mouth-open-vs-quiet gate calibration
(loop 1 #3, owed — calibrate MAR × vibrato-depth instead of MAR × vocal RMS); CCA AV-sync (loop 2 #3,
owed — the vibrato curve is the audio feature); the snapper stay-rule patch (an in-span peak-evidence
signal — vibrato depth inside the snapped span is exactly the "is the voice actually there" evidence
sprint 5's follow-up needs).

### #2 — CASA: correlogram + harmonic grouping + the ideal binary mask (the principled route)

**What it is.** Stop asking "is the voice present in this frame" and *segregate the scene*: decompose
the mix into time–frequency units, group the units that share a common periodicity (the voice's F0)
into one stream, and read vocal-activity boundaries off the voice stream's mask. The classical
formulation is Wang & Brown's CASA: stage 1 segregates voiced portions by harmonicity via multipitch
tracking and unvoiced portions by onset/offset analysis; stage 2 groups T–F units across time by
speaker characteristics; the target is the **ideal binary mask** (retain a T–F unit iff the target is
stronger than the interference in it). The front end is the **correlogram** (Licklider 1951; Slaney &
Lyon 1990): a short-time autocorrelation computed per frequency channel — a 3-D function (channel ×
lag × time) in which components sharing common AM/FM are revealed. Bregman's ASA (1990) supplies the
grouping principles: continuity in pitch/timbre, harmonic relations, common amplitude/frequency
modulation, onset/offset synchrony.

**Where it came from.** Hop 2, category cross — voice science → auditory scene analysis. Slaney & Lyon
(Duda & Lyon, Asilomar 1990): "components sharing common AM/FM are revealed" by the correlogram;
"common amplitude modulation groups components into sound sources." Shao et al. 2010 (Computer Speech
and Language 24): the two-stage monaural CASA system estimating the ideal binary mask. The cross is
the point: every hop-1 feature measures the *mixture*; CASA is the only classical family that
*unmixes* it without a neural separator.

**Slermable core.** STFT (c11_mir, validated corr 1.000000) → per-channel autocorrelation (the YIN
machinery from c11_voice, lego-able — autocorrelation is autocorrelation) → correlogram → harmonic
grouping by common F0 (pYIN's multi-threshold candidates are the seed for multipitch) → binary mask →
boundaries from the mask. The expensive residue to AVOID is Lyon's full cochlear model (cascade
filterbank + AGC — the 1990 paper itself notes it is expensive to simulate on conventional hardware);
the feasible residue is a correlogram on STFT magnitudes, which is the same math with a cheaper
front end.

**C11 feasibility — MEDIUM, multi-sprint.** The correlogram itself is cheap (autocorrelation per
channel is O(channels × lags) per frame, all integer-friendly). The hard part is **multipitch tracking**
— two periodic sources at once (voice + bass/brass), deciding which F0 is the voice's. That is a
research problem inside the sprint, not a solved subroutine. Scope as an experiment first (below),
not as a full gate build.

**Validation bar.** Experiment-first: on the MV-14 mix, does the correlogram show a dominant peak at
the voice's F0 lag during sung spans that is absent (or subordinate to the accompaniment's lag) during
instrumental spans? Pass = the voice-lag peak separates sung from instrumental spans on ≥80% of the
ref segments. Full-gate bar (only if the experiment passes): boundaries from the CASA vocal-stream
mask reach ≥80% within ±0.5 s of the Demucs ref — the same held bar. **Honest scope:** this is the
highest-ceiling entry and the longest build. If #1 lands, #2 becomes the second-generation sensor,
not the next sprint.

**Replaces / enables.** Replaces Demucs as the segmenter *if* it ever reaches the bar — a classical,
CPU-cheap, model-free separator would remove the pipeline's heaviest dependency (Demucs 894 s/track;
MDX-Net ONNX 1,592 s — both dwarf every other stage). Enables: true per-word vocal-activity on the
mix (the snapper's stay-rule evidence, the G7 gate's clean input, CCA without a stem).

### #3 — R8 voice-break degree + jitter/shimmer: the blind-drawn entry (TEST, not a rescue)

**What it is.** The remaining voice-quality shelf, after CPP/HNR failed: **jitter** (cycle-to-cycle
period variability: local jitter, RAP 3-cycle, PPQ5 5-cycle), **shimmer** (cycle-to-cycle amplitude
variability, in dB or %), and **voice breaks** (Praat: number = count of inter-pulse intervals longer
than 1.25 / pitch floor — 16.67 ms at a 75 Hz floor; degree = total break duration / total analysed
duration). The hypothesis: the sung voice's cycle irregularity differs from the accompaniment's —
brass is very regular (low jitter), drums are aperiodic (high jitter), the voice sits between with
*structured* irregularity — and voice-break degree spikes where the voice drops out mid-phrase.

**Where it came from.** Hop 1, voice science — and the loop's blind draw (§8). The draw selected this
leg out of a 12-item pool; the method makes the draw load-bearing, so this leg gets a full entry and
its own bar rather than being folded into jitter/shimmer as an afterthought. The clinic literature
was web-verified from two angles: Patel et al. 2018 (ASHA panel chose CPP *over* jitter/shimmer as
the voice-quality measure — "the most contentious choice in the entire protocol"); Maryn et al. 2009
meta-analysis (smoothed CPP the most robust correlate of dysphonia severity); Titze 1995 (perturbation
valid only for nearly-periodic Type 1 signals, values <~5% reliable); Deliyski 2005 (fail below ~30 dB
SNR); Boersma 2009 (software-specific: 1% added noise gives Praat 0.02% jitter vs MDVP 0.6% on the
same sound); Brockmann 2011 (loudness/SPL is the largest confound).

**Slermable core.** Pulse train → inter-pulse intervals → jitter/shimmer/voice-break statistics per
frame. The pulse train is the problem: it needs glottal-cycle identification on the mix, which is the
same voicing-decision machinery sprint 8's stem leg failed at (1,825 vs 7,493 voiced frames).

**C11 feasibility — LOW as a mix feature, MEDIUM on the stem.** The statistics are trivial; obtaining
the pulse train is not. On the Demucs stem the pulse train is computable (the voice is isolated) —
but on the stem, separation is already trivial, so the feature adds nothing. On the mix, the feature
needs exactly the cycle tracking the stall broke.

**Validation bar (held).** Same bar: boundaries ≥80% within ±0.5 s. Plus a *validity pre-check* that
must pass before any boundary scoring: jitter/shimmer computed on MV-14's mix must satisfy Titze's
conditions (Type 1 periodicity, SNR >30 dB) on the sung spans — if the mix violates them (it almost
certainly does: drums + brass + room), the entry fails at the pre-check and is reported as such.
**The inversion, stated honestly:** the clinic abandoned jitter/shimmer for dysphonia severity
because they need clean, steady, periodic vowels. Our job (sung-vs-instrumental on a dense mix) is a
*different* job — but the abandonment reasons (needs clean cycles, steady vowels, high SNR) cut
against our material too. The one reason this is still a test and not a dismissal: the voice may be
the *only* nearly-periodic component in the mix during sung spans, so the *presence* of measurable
low jitter could itself be the signal — brass is too regular, drums too irregular, voice in between.
That is a hypothesis to measure in a day, not a sprint to build.

**Replaces / enables.** Nothing if it fails (expected). If it passes, it is a second independent
vocal-activity sensor alongside vibrato — two sensors that fail differently are worth more than one
sensor that fails alone (Winners League: overlap average across independent identifications).

### #4 — R5 flow interpolation for BAD-WORD spans: symmetric-flow MCFI (assembly rescue)

**What it is.** The BAD-WORD RULE currently cuts a bad word's span to montage. Flow interpolation
lets the take *keep* the span: synthesize the missing motion between the good frames on either side
of the bad word by motion-compensated frame interpolation — estimate the optical flow, warp both
boundary frames to the intermediate time, fill the occlusion holes, blend. The classical pipeline
(Avid US6665450B1, expired): motion vectors at the intermediate time → warp both frames → blend by
the time factor. The quality improvement is Raket et al. 2012 (ISVC, Saarland): **reparametrize the
TV-L1 flow energy so the flow is estimated AT the unknown intermediate frame** — a symmetric data
fidelity term; the estimation becomes more robust to noise and large displacements, the workload more
than halves versus bidirectional methods, and the estimated flows are used directly on the unknown
frame, avoiding temporal-warping problems. FFmpeg's `minterpolate` (mci mode: overlapped-block / adaptive
overlapped-block motion compensation, bilateral/bidirectional motion estimation, epzs–umh search) is
the available reference implementation for comparison — no build needed to measure against it.

**Where it came from.** Hop 3 — the 1102 report §2 rescue, via loop 2's queue. It was "needs GPU" in
2026-11-02; sprint 7's C11 Farneback (validated vs cv2, synthetic EPE 0.0004–0.019 px, Middlebury
within 0.06 px) makes the flow estimator slermable now. The full timing-methods report (20261103-0233)
was read in full before this scoping, as loop 2 required — and it carries the warning that governs
the bar: "interpolation only as a deliberate inspected pass (it invents mouth shapes)."

**Slermable core.** C11 Farneback flow (sprint 7, on disk, validated) → forward-warp both boundary
frames to the intermediate time (symmetric-flow reparametrization per Raket) → occlusion hole-filling
→ blend. The flow estimator exists; the build is the warping/blending/hole-filling pipeline plus the
symmetric-flow estimation pass.

**C11 feasibility — HIGH.** Farneback is done and validated. Warping + blending + hole-filling is
standard image code. The blade cost is the flow itself (already measured in sprint 7) times two
boundary frames per interpolated span — trivial against a 10 s take.

**Validation bar.** (a) Take a KEEP take, delete a 0.3–0.5 s span, interpolate it back: the
interpolated span's **M6 must sit in KEEP range** (sprint 2 gate: usable-window M6 ≤ 0.10 with longest
duplicate run < 0.30 s — the interpolated span must read as motion, not a freeze) and the **eye
cannot tell** (full-res read of the interpolated frames against the originals, same reviewer, blinded
order). (b) **The mouth test (the timing report's warning, made a gate):** interpolated mouths must
not read as a *different word* — for a BAD-WORD span the take's own mouth is wrong there anyway, so
the failure mode is an invented mouth that contradicts the neighbouring words; eye-check the
interpolated mouth shapes against the phonemes on either side. (c) Reference comparison: the C11
result must be at least as clean as `minterpolate` mci on the same deleted span (M6 + eye), or the
difference is documented and the ffmpeg path is the fallback.

**Replaces / enables.** Replaces the cut-to-montage half of the BAD-WORD RULE for short spans
(0.3–0.5 s, one word): the take keeps its span with synthesized motion instead of losing it to a
cut. Enables: MV-12 Q2-adjacent density work, MV-13 S25/S04-class repairs, and any future take whose
only defect is one bad word in an otherwise KEEP span. Does NOT fix the vocal-activity gap — it
routes around its consequence in assembly.

### #5 — R9 G7 wrong-lyric gate, formalized (the safety gate)

**What it is.** A take that sings the *wrong part of the song* currently has no gate: QC checks
identity (G1), text (G2), motion, sync — but not whether the words sung are the words the scene was
planned for. Formalize the 1102 report §5 candidate: run take ASR (already produced for every take —
`work/qc_take_asr.jsonl`), compute the **word-set overlap** between the take's ASR words and the
scene's planned words (`SONG_WORDS.json`): overlap < 0.5 → REJECT, with a hand-check override for
homophones and near-identical choruses (provenance quarantine for identical choruses — the same line
sung in C1 and C2 must not false-REJECT). Boundary check at assembly: last 0.5 s + first 0.5 s across
each cut.

**Where it came from.** Hop 3 — 1102 report §5 rescue, via loop 2's queue. Grounded in the MV-14
ledger this session: **7 REJECT rows, ALL G1 identity or G2 text — ZERO wrong-segment REJECTs in
MV-14** (5 subtitle failures: S16, S19, S25 t2, S55 t1, S62 t1; 2 identity: S18 wardrobe, S25 hair).
The bar as originally stated ("flags every known wrong-segment take") cannot be validated on MV-14
positives because MV-14 has none in its ledger — either wrong-segment takes don't happen, or nobody
caught them, and the ledger cannot distinguish the two. The cross-MV grep for wrong-segment cases
was still running when this report was written; its result is a note for the parent, not a dependency.

**Slermable core.** Word-set overlap ratio (Jaccard or containment) on two word lists that already
exist. No new estimator, no audio work, no model. The C11 in it is a string-set comparison — or it
stays a Python QC script; the gate is the *rule*, not the language.

**C11 feasibility — TRIVIAL (or no C11 at all).** The honest statement: this does not need a sprint's
worth of C. It needs a QC script + a ledger rule + the positives construction below. Scoped as a
small build, not a sprint.

**Validation bar.** Construct positives by **cross-pairing**: for each of the 65 KEEP takes, compute
overlap of its ASR words against *every other* scene's planned words — a take paired with the wrong
scene must score < 0.5 (it is, by construction, singing a different part of the song), and the 65
KEEP takes paired with their OWN scenes must score ≥ 0.5 with **zero false REJECTs**. Pass = 100% of
cross-pairs flagged + 0/65 false REJECTs on own-pairs. If the still-running cross-MV grep surfaces
real wrong-segment takes, add them as positives — they strengthen the bar, they don't change it.

**Replaces / enables.** Replaces nothing — it is a new safety gate, the first QC check that reads
*what* the take sings rather than how it looks or moves. Enables: the loop-1 #1 forced-alignment
work (the gate's ASR input gets cleaner as alignment improves) and the provenance quarantine rule for
identical choruses as a standing QC note.

### #6 — Formant / LPC tracking (the no-pitch-tracking sensor)

**What it is.** Formants are the vocal tract's resonances — peaks in the LPC spectrum, tracked per
frame (Praat: formants = peaks in the LPCs run at each moment; VoiceSauce computes formants + HNR +
spectral tilt as the singing-voice feature set). A sung vowel holds stable formants (F1/F2) across its
duration; instrumental spectra move differently (brass formants shift with pitch; drums have none).
The discriminative idea: formant *stability* (low frame-to-frame F1/F2 variance) during a sustained
vowel vs the accompaniment's formant motion. It needs **no pitch tracking at all** — LPC is a filter
computation on the waveform, which is why it survives the stall's root cause (the voicing decision)
even though it shares the mix's spectrum.

**Where it came from.** Hop 1 follow-on — the Vienna Talk singing-voice toolbox (formants by LPC
alongside vibrato, loudness/RMS, brilliancy/normalized spectral centroid, spectral tilt H1–H2);
Praat's formant tracker; VoiceSauce.

**Slermable core.** LPC (Levinson–Durbin — classical, integer-friendly, a few dozen lines) → formant
peaks from the LPC polynomial roots → F1/F2 tracks → stability statistic per frame. LPC is already
the kind of small classical DSP the pipeline slerms routinely (cf. c11_mir's feature set).

**C11 feasibility — MEDIUM.** LPC itself is easy. The hard part is formant *tracking* (associating
peaks across frames, rejecting spurious peaks when the accompaniment dominates the spectrum) — on a
dense mix the LPC spectrum is the *mixture's* spectrum, and the voice's formants may not be the
peaks. That is the experiment, not the build.

**Validation bar.** Experiment-first, same shape as #2: on MV-14, does F1/F2 stability separate sung
from instrumental spans (median sung stability > instrumental, non-overlapping IQRs)? Only if the
experiment passes does it earn a boundary bar (≥80% within ±0.5 s). **Honest scope:** ranked below
vibrato because the mix-spectrum contamination is a bigger unknown than the chant-vibrato question,
and vibrato's falsifier is faster.

**Replaces / enables.** A second no-pitch-tracking sensor alongside CASA's correlogram. If vibrato
fails (straight-tone chant) AND formants fail (mix spectrum dominates), the vocal-activity gap has no
cheap sensor left and loop 4 must face the separation-first answer (CASA full build or Demucs stays
forever).

### #7 — Slopcore vehicle-template changes (measured — proposed skill edits, parent applies)

**What it is.** The closest outside vehicle-writing reference, measured this session rather than
cited from the survey: cloned `obie/slopcore`, read `skills/music-video/examples/queso/PROMPTS.md`
(1,458 lines, 86,841 B), measured all **101 prompts**: expanded median **158 words** (mean 159.2,
range 67–284); by kind — lips median 251.5 (211–284, n=8), motion 188.5 (135–260, n=44), insert 114
(67–181, n=49); **100/101 carry timed beats** (second timestamps relative to clip start, per
word/phrase); **91/101 end with the {END} prohibition footer** ("One continuous shot, no cuts. No
text, letters or logos."); 98/101 name the camera; 77/101 mention sing/mouth/lips; durations mostly
4 s (69/101). Identity via macros (HER 50 words, HERFAR 35, HIM 17, ROOM 19, MOVE 9, END 10)
expanded into every prompt. Rules header: clip time = seconds from the clip's first frame; every clip
starts one beat before its shot (beats every 0.612 s); kinds — `lips` (sings on camera; model gets
plate + clean vocal of only those words), `motion` (plate + song from t0), `insert` (plate = exact
first frame, silent); "He never sings. Nobody but her sings."; "All type is drawn by the engine."

**What transfers — and what does not (the honest correction to the survey's #1 claim).** The survey
ranked "short-vehicle A/B" #1 on the claim that slopcore prompts are short. **They are not short**
(158-word median; lips 251 words) — the length is spent on **timed beats + mouth rules**, not
appearance restatement (appearance is macro-managed, written once, expanded everywhere). Slopcannon's
440-word vehicles sit ~2.8× above slopcore's median, but the gap is not "short vs long" — it is
"macro-managed identity + timed beats" vs "appearance restated per vehicle." And the timed beats work
in slopcore because the model gets **audio** (clean vocal / song) — Muse's tool has no audio input,
so per-word timed beats in text are a nudge at best (timing-methods report: second-counts in prompts
are folklore/unproven). What transfers, as proposed skill edits (draft only — parent applies):
(a) the **kinds system** (lips / motion / insert — a vehicle declares its kind, and the kind sets the
plate + audio + mouth rules); (b) the **{END} prohibition footer** on every vehicle (91/101 carry it —
the survey's #3 prohibition block, now measured, not just claimed); (c) **macro-managed identity**
(write the character/room once, expand everywhere — stops appearance restatement from eating the
vehicle budget); (d) the **pilot pattern** (three test clips before the batch — slopcore's intake runs
a pilot; Slopcannon's volleys fire 6 cold).

**Validation bar.** Vehicle-template change, not a detector: (a) kinds + footer + macros land in the
skill as proposed edits; (b) the next volley fired on the new template is measured the same way
(vehicle word count, KEEP rate, G1/G2 REJECT count) against the MV-14 volley baseline (65/65 KEEP,
7 REJECTs, 5 of them G2 subtitle failures). Pass = KEEP rate held + G2 subtitle failures down
(the footer + kinds are aimed at the text failures, which are 5/7 of MV-14's REJECTs).

**Replaces / enables.** Replaces the free-form vehicle with a kinds-declared, macro-managed,
footer-closed vehicle. Enables: the pilot pattern as a standing volley-0 (three test clips before any
6-video volley — burns 3 of the budget to save the other 3 from a template error).

### #8 — wubu_synth meta-thread: VERDICT — TOY, do not adopt as-is

**What it is.** Loop 2's queue asked: survey wubu_synth's spec→C codegen templates, generate
c11_voice's scaffolding from them, report whether the meta-tool saves a sprint's worth of hand-written
C. Read on disk this session: `lego-harvest-scratch/wubuwizard/src/wubu_synth.c` (82 lines, 3
templates: scalar_add, scalar_mul, buffer_sum, `{name}` substitution + compile-verify) and
`src/wubu_codesynth.c` (69 lines, 5 templates: add/mul/bufsum/max/min, keyword-matched operation →
template, defaults to add); headers 22 lines each.

**Verdict: the premise fails on inspection.** There are **no scaffolding templates** — no WAV reader,
no JSON emitter, no argument parsing, no self-test harness. The "program synthesis 7-hop" framing
(HEURIGYM, Apeiron, EvoAgent, Code-as-Policies) is aspirational labeling on printf-style template
substitution. `wubu_synth_compile_verify` writes to /tmp, hardcodes a (2,3)→"5" smoke test, and
returns 0 for BOTH compile failure and verification failure (conflated). The idea (a template library
for shared scaffolding) is still valid, but the templates would need to be WRITTEN first — that is a
build, not an adoption. (Note: `AUDIO/wubusynth/` in the same repo is a different thing — audio synth
Python, not codegen. Do not confuse them.)

**The narrowed residue (ranked here so it is not lost).** A `c11_scaffold` template library — WAV
reader, JSON emitter, argument parsing, self-test harness — written once, lego'd into every sprint.
But it is a **build**, scoped like any other: write the four templates by hand (they are the exact
scaffolding every sprint from c11_mir to c11_voice has hand-written), verify each against the sprint
that already has a working version, then reuse. Do NOT scope it as "generate from wubu_synth" — there
is nothing to generate from.

**Validation bar.** The library earns its keep when the next sprint's scaffolding is assembled from
its templates with zero hand-written WAV/JSON/argparse code and the sprint's validation still passes
unchanged. No sprint is gated on it.

### #9 — R4 birdsong spectral entropy: the small experiment (queued, pre-sprint decision)

**What it is.** Sprint 8's own recommendation #2: a small entropy experiment decides before any
sprint — spectral entropy on the mix vs the stem, as a note-vs-noise feature (loop 2 #2, SA+). A
sustained sung vowel is low-entropy (peaky spectrum); drums/noise are high-entropy; brass sits in
between. If entropy separates sung from instrumental spans on the mix, it is a third cheap sensor
and — more importantly — the **in-span peak-evidence signal the snapper's stay-rule patch needs**
(sprint 5 follow-up, currently unbuildable on the c11_voice curve).

**Validation bar.** Experiment, not sprint: entropy (mix) separates sung from instrumental spans with
non-overlapping IQRs on MV-14. Pass → it becomes a snapper stay-rule input; fail → the stay-rule
patch waits on vibrato (#1) or CASA (#2). Cost: an afternoon of measurement on existing curves.

## 3. The per-loop break-the-sync probe (loop 3)

**The repeated-chorus collapse probe.** The snapper is the timing authority (per-word ASR anchors),
and loop 1 #1 recorded the known failure: a global alignment *glues repeats to the first occurrence*
(Ne0s0u1: "global alignment glues repeats to the first occurrence"). MV-14's C2/C3 "Fourth law" chant
runs to FOUR repeats — the exact material. Probe: run the snapper on the C2/C3 spans and check whether
the word times advance through repeats 2–4 or collapse onto repeat 1's times. **Pass = times advance
(a distinct time per repeat, within ±0.1 s of the ASR anchors); fail = any repeat's words land on an
earlier repeat's times.** If it fails, the monotonic-forward-walk fix (loop 1 #1) is not a nice-to-have
— it is a correctness bug in the timing authority, and it outranks new sensors. (Secondary probe,
inside the top-1 sprint: the vibrato-absence check — a straight-tone chant span must report *absent*,
not hallucinate modulation. A detector that cannot say "not here" cannot be trusted when it says
"here.")

## 4. Loop-4 seed

1. **Whichever of #1/#2 lands first** becomes the vocal-activity sensor: calibrate the mouth-open-vs-quiet
   gate (loop 1 #3, owed) and CCA AV-sync (loop 2 #3, owed) on its curve. The gate and CCA were blocked
   on c11_voice; they are unblocked by the first sensor that passes the held bar.
2. **If vibrato fails fast (straight-tone chant):** the voice-activity gap is still open — loop 4
   runs the formant experiment (#6) and the birdsong-entropy decision (#9) in parallel, and scopes the
   CASA experiment (#2) as the next sprint if either shows separation.
3. **TSM squeeze-guard band measurement (owed from TSM validation):** one moderate-squeeze take to set
   the guard precisely in the 0.5–0.87 alpha band — a measurement task for c11_tsm, not a loop-4 entry,
   but loop 4 checks it landed.
4. **Flow-interpolation eye-check results (#4)** feed back into the BAD-WORD RULE: if interpolated
   mouths read clean, the rule gains an "interpolate first, cut second" branch for short spans.
5. **G7 cross-pairing positives (#5)** become a standing QC fixture: every future volley's takes get
   cross-paired automatically, so a wrong-segment take cannot ship silently again.
6. **The wubu_synth residue (#8):** if a sprint's scaffolding is ever written twice the same way,
   scope `c11_scaffold` as a lego build — but only from the hand-written templates, never from
   wubu_synth as-is.

## 5. Proposed skill edits (draft only — parent applies, no skill edited this loop)

1. **Vehicle template:** add the kinds system (lips / motion / insert — a vehicle declares its kind;
   the kind sets plate + mouth rules), the {END} prohibition footer on every vehicle, and macro-managed
   identity (character/room written once, expanded everywhere). Source: slopcore PROMPTS.md, measured
   §2 #7. Note the honest correction: slopcore prompts are NOT short (158-word median) — the template
   change is about structure, not length.
2. **BAD-WORD RULE (conditional on #4 passing):** add an "interpolate first, cut second" branch for
   0.3–0.5 s spans — only after the M6 + eye + mouth tests pass.
3. **QC gates:** add G7 (word-set overlap < 0.5 → REJECT, cross-pairing positives as the fixture,
   homophone hand-check override) once #5's validation passes.
4. **Snapper stay-rule (conditional):** vibrato depth (#1) or spectral entropy (#9) as the in-span
   peak-evidence signal — only once one of them separates on the mix.

## 6. Honest scope

- **No code was run.** No C was written, no estimator executed, no measurement beyond the on-disk
  counts in this report. Every validation bar is written to fail honestly — including the falsifiers
  (straight-tone chant kills #1 in a day; Titze's validity pre-check kills #3 before boundary scoring;
  the synth-LFO confound check can kill #1 on instrumental spans).
- **Web-verified claims:** jitter/shimmer validity conditions + ASHA 2018 CPP choice (Patel et al.
  2018; Maryn et al. 2009; Titze 1995; Deliyski 2005; Boersma 2009; Brockmann 2011); vibrato norms
  (Sundberg; Nix et al. 2016; Titze reflex-resonance); voice-break definitions (Praat manual,
  fon.hum.uva.nl); CASA (Bregman 1990; Licklider 1951; Slaney & Lyon 1990; Shao et al. 2010);
  MCFI (Raket et al. 2012; Avid US6665450B1; FFmpeg minterpolate docs); formants (Praat; VoiceSauce;
  Vienna Talk 2010). Full citations in SOURCES.md entries 56+.
- **Measured on disk (reproducible):** slopcore PROMPTS.md — 101 prompts, expanded median 158 words
  (lips 251.5 / motion 188.5 / insert 114), 100/101 timed beats, 91/101 {END} footer; wubu_synth —
  82 + 69 lines, 3 + 5 templates, zero scaffolding templates; MV-14 ledger — 7 REJECT rows, 0
  wrong-segment (5 G2 subtitle, 2 G1 identity).
- **Still running at report time:** the cross-MV grep for wrong-segment cases (backgrounded session;
  result pending). It does not gate any entry — G7's validation constructs its own positives by
  cross-pairing — but if it surfaces real wrong-segment takes, they join the positives.
- **What this loop did NOT do:** no re-run of sprint 8's calibration; no lowering of the 80% bar;
  no video generation; no commit; no Telegram write; no skill edit.

## 7. Top 5 (for the parent's report)

1. **Vibrato signature (5–7 Hz F0 modulation)** — top-1 sprint `c11_vibrato`, scoped in SPRINT_SCOPE.md.
   Uses sprint 8's one proven mix result (pYIN corr 1.0000); fails fast if the chant is straight-tone.
2. **CASA correlogram + ideal binary mask** — the principled unmixing route; experiment-first
   (voice-lag peak separation), full gate only if the experiment passes.
3. **Voice-break degree + jitter/shimmer (R8, blind draw)** — the clinic shelf's last leg; validity
   pre-check first (Titze conditions), boundaries second; expected to fail, measured either way.
4. **Flow interpolation, symmetric-flow MCFI (R5)** — Farneback exists (sprint 7); build the warp/blend/
   hole-fill pipeline; bar is M6 in KEEP range + eye can't tell + mouths don't read as another word.
5. **G7 wrong-lyric gate (R9)** — word-set overlap < 0.5 → REJECT; positives constructed by
   cross-pairing the 65 KEEP takes; zero false REJECTs on own-pairs.

## 8. Blind draw (method audit)

Drawn with `secrets.choice` from a 12-item candidate pool of loop-3 ideas:
`vibrato signature, correlogram, formant tracks, voice break degree, symmetric flow, kinds system,
macro identity, pilot pattern, cross-pairing, squeeze guard band, birdsong entropy, mouth-open gate`.
**Draw: "voice break degree"** (first draw accepted, no discard). Checked: 0 whole-word occurrences
of "voice break degree" / "voice break" / "voice-break" in `~/workspace/wubutv-network/ideas/BAN_LIST.md`
(3,185 lines; "break" alone occurs 30×, all as the "break room" setting noun — not the feature);
not among banked form ideas (COMPASS, VESSEL, CRADLE SHOT, SATELLITE ORBIT, HARBOR, RIVER, FEATHER).
**Deviation, stated plainly:** loops 1–2 drew from a neutral *noun* list and banked a visual form idea
(COMPASS, VESSEL). Loop 3's pool was loop-3 *ideas*, and the draw landed on a technical entry — so
this loop banks the voice-break feature itself (§2 #3) rather than a separate form idea. The draw is
load-bearing in the method's sense: it forced the weakest hop-1 leg into a full entry with its own
validation bar instead of letting it dissolve into jitter/shimmer as an afterthought.

## Addendum — cross-MV wrong-segment grep landed (2026-11-12 09:58:37Z)

The grep pending at report time has finished (468 s wall, exit 0). It changes §2 #5's grounding in one
respect: **real wrong-segment positives DO exist — in MV-2, not MV-14.**

- First grep (case-insensitive, whole MV tree): 4 files, ALL in MV-2_toll-roads-are-dumb —
  `SYNC_V3_WORKING.md`, `masters_work_v3/VOLLEY_V4_MANIFEST.md`, `DEVILS_ADVOCATE_V4.md`, `TAKE_HISTORY.md`.
- Second grep ("wrong-segment"/"wrong segment" in `work/*.md` + `MV*_PROGRESS.md`): zero hits.
- `qc_take_asr.jsonl` confirmed: 2,576 lines.

The matching lines, read in full:

- **MV-2 S04 t3 — proven wrong-segment take.** TAKE_HISTORY.md: "VERDICT: KEEP — fixes the audit's
  wrong-segment finding (**t3 sang 30–40s lyrics at 43–48s**). S04 active = t4." DEVILS_ADVOCATE_V4.md:
  "**S04 was singing the WRONG SEGMENT (proven).**" The re-fire (t4, md5
  a83e89f76c03292eeb5c4dd3ddc0cb81) covers the window lyric in order (LCS match 15/19) and is the active
  take. This is a genuine G7 positive with its ground truth on disk: t3's ASR vs S04's planned words
  should score overlap < 0.5, t4's ≥ 0.5.
- **MV-2 S21 — second candidate.** SYNC_V3_WORKING.md: "wrong-segment and S21 proven window-collapse
  on the leader-fixed collisions ('the', 'the', 'ones'); the picture sang the wrong segment." Needs a
  read of the S21 record before it counts as a positive — noted here, not yet verified.

**Consequence for G7's validation bar (§2 #5):** the bar is unchanged (cross-pairing construction +
zero false REJECTs on own-pairs), but it is now STRENGTHENED — MV-2 S04 t3 joins the positives as a
real historical case, and S21 is a candidate pending verification. The cross-pairing construction
remains necessary (one positive is not a validation set), but the gate now has a real-world case to
catch, not only synthetic ones. MV-14's ledger still has zero wrong-segment REJECTs — the ledger
cannot distinguish "doesn't happen" from "nobody caught it," and MV-2 proves it happens.
