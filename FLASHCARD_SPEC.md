# Flashcard spec — standing rules

These rules are mandatory for every flashcard in the app — existing lessons
(regular-template and new-template) and anything built after this spec was
written. They were set by Asra during the flashcard coverage/audio pass
(Nov 2026) and apply automatically; no lesson should ship a flashcard that
violates any of them.

## 1. Meaning in every flag language

Every flashcard must have a real, human-translated meaning in **every**
language offered by the flag/language switcher: `en`, `fa`, `es`, `ru`,
`hi`, `ar`. There is no English fallback for a missing translation — if a
language is missing, the card is incomplete and must be fixed before
shipping, not patched at runtime.

- Regular-template lessons: store this in the lesson's `D` glossary object,
  keyed by the French word/phrase exactly as it appears in `DECK`, with one
  key per language (`en`, `fa`, `es`, `ru`, `hi`, `ar`), e.g.:
  `D["bienvenue"] = {"display":"bienvenue","en":"welcome","fa":"...", "es":"...","ru":"...","hi":"...","ar":"...","kind":"word"}`.
- New-template lessons: same shape, merged into `window.D` via
  `Object.assign` in the lesson's own script block.
- Before adding a new card, check whether the same French word/phrase
  (case-insensitive) already has a `D` entry anywhere in the corpus and
  reuse that translation rather than re-translating from scratch, to keep
  terminology consistent across lessons.

## 2. Audio — real recording first, human-sounding AI as the only fallback, never robotic TTS

Every flashcard must have audio wired to `window.PRON` (looked up via
`window.__pplay`/`look()`), in this strict order of preference:

1. **A real human recording**, if one exists anywhere in the corpus for
   that exact word/phrase (case-insensitive). Reuse it — do not re-record
   or regenerate audio for a word that already has a real clip elsewhere.
2. **Human-sounding AI-generated audio**, only when no real recording
   exists anywhere in the corpus. The bar is: it must sound like a real
   human speaking, not robotic or machine-like. A flat formant-synthesis
   voice (e.g. espeak/festival-style) does **not** meet this bar and must
   not be used. As of this spec, the approved local pipeline is Piper
   (neural, VITS-based TTS) with the `fr_FR` "siwis" voice model, run
   fully offline — see `assets/ai-pron/` for the generated clips and the
   coverage-report tooling for how the missing-word list is produced.
3. If neither is available (e.g. the local AI voice cannot be run), the
   card must **not** be wired to a fake or silent clip. Flag the word in a
   missing-audio report instead and leave it unwired until real or
   AI audio is produced.

Never substitute silence, a broken link, or a different word's audio.
Never leave a flashcard's speaker button wired to on-the-fly browser TTS
(`speechSynthesis`) as the primary path — that's a last-resort fallback
only for the few words covered by the legacy `CLIP` alphabet set, not a way
to cover ordinary vocabulary.

## 3. Everything baked in — no runtime network calls

No flashcard may depend on an online service at runtime for translation or
audio. Translations live in the lesson's `D` object; audio files are real
static assets (either on the existing audio CDN for real recordings, or
under `assets/ai-pron/` in this repo for generated clips, served from
`chichilang.com`). The app must work fully offline once loaded — no
on-the-fly machine translation, no on-the-fly TTS synthesis, no fetches to
a translation or speech API while the learner is using the app. Generating
new translations or new AI audio is a one-time **build-time** step done by
whoever is adding the card, committed into the repo like any other asset,
never something the app does live.

## 4. Card layout — French + example on the front, meaning only on the back

- **Front of the card:** the French word/phrase, the speaker icon, and (if
  the card has one) a French example sentence using the word. No
  translation of any kind appears on the front.
- **Back of the card:** the translated meaning in the learner's selected
  language, and nothing else — no repeated example sentence, no French
  text.

This matches the existing regular-template flashcard behaviour exactly; the
12 new-template lessons were updated to follow it too (their example
sentences were moved from the back to the front, and the back now shows
only the meaning).

## Reference implementation

- Regular-template lessons: see the `meaningOf()`/flashcard-render code and
  the `D`/`PRON` objects in any `lesson-*/index.html` file whose DECK/D
  shape matches (113 lessons).
- New-template lessons: see the injected script block (search for
  `renderCards` and `flagBtn`) in `lesson-a1-new-*/index.html`,
  `lesson-b2-new-*/index.html`, `lesson-c1-new-negations/index.html` (12
  lessons) — this is the pattern to copy for any future new-template
  lesson.
