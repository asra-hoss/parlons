# Parlons ! — GitHub Pages publish

- **Brand (final, chosen by Asra): « Parlons ! »** — tagline « Français de A1 à C2 ».
  (Working names during the build were "super-app", then "Parléa"; both are
  superseded — the name Asra approved is **Parlons !**)
- **Repo:** `asra-hoss/parlons` (public)
- **Live URL:** https://asra-hoss.github.io/parlons/
- **Local working copy:** `~/workspace/french/parlons-github/` (this folder = site root)
- **Source of record:** `~/workspace/french/original-b1-product/` (`build/` app source,
  `site-a2/`, `site-b2/` staging trees)

## What's included (Nov 1, 2026)

Four levels in ONE app, Home level selector in the order **A2 → B1 → B2 → C1/C2**,
choice persisted in the browser (`origb1:level`, the app's standing storage family):

- **B1** — the verified B1 product exactly as the Muse artifact `b1` v13 serves it
  (interactive exercises, tab order Listen → Read → Vocab → Grammar → Exercises →
  Writing → Speaking → Flashcards, universal tap-a-word glosses, BYOK API-key
  correction, white-background cartoon thumbnails). Content untouched.
- **A2** — from `content-a2/` staging, per `content-a2/MERGE_NOTE_A2.md`
  (data `book-data-a2.json`, dossiers `orig-a2-u1…u12`, assets under `assets/a2/`).
- **B2** — from `content-b2/` staging, per `content-b2/MERGE_NOTE_B2.md`
  (dossiers `orig-b2-u1…u12`, assets under `assets/b2/`).
- **C1/C2** — from `content-c12/` staging, per `content-c12/MERGE_NOTE_C12.md`
  (dossiers `oric12-u1…u12`, storage family `oric12:`, assets under
  `assets/c12/`; U9 ships dialogue-only — no verified real-voice excerpt
  exists for it, do not invent one).

Also included: **the placement test** (« Test de niveau », Nov 1, 2026) —
Home card above the level selector; four sections (Écouter → Lire →
Écrire → Parler), stop rule, BYOK writing scoring, speaking self-assessment;
result persisted at `origb1:placement-result`.

Not yet included (planned updates to this same repo): **A1** (rebuilt to Asra's
own developmental checklist — awaiting the checklist)
and the Spanish/Russian/Hindi/Arabic localisation pass.

## Tree rules (learned the hard way — keep them)

- EVERYTHING lives under `assets/`: bundle media, `assets/fonts/`,
  `assets/pron/` (B1 clips), `assets/a2/pron/`, `assets/b2/pron/`, and the single
  merged `assets/pron-index.json` (8,535 entries; B1 first, then A2/B2/C12
  additions, Lingua Libre clips repoint shard-TTS entries). Root-level `pron/`
  or `fonts/` copies are NOT used on this host.
- `.nojekyll` at the root (no Jekyll processing).

## Update procedure

1. Edit the app source in `original-b1-product/build/client/src/`
   (new level data: drop the staged JSONs in `site-<lv>/`, run
   `build/convert_levels.py`, register the level via `build/do_merge_edits.py`
   — C1/C2 used its own `build/do_c12_edits.py`).
   ⚠️ `assemble_parlons.py` rmtree's this whole folder INCLUDING `.git`:
   after assembling, re-clone the repo elsewhere, rsync the assembled tree
   over the clone (`--exclude=.git`), then commit + push from the clone.
   ⚠️ Build gotcha (Nov 1): the tailwind plugin's native candidate scanner
   can choke on a binary asset whose byte runs form a toxic token
   (error surfaces as a CSS parse failure in theme.css). Bisect by building
   theme.css + one asset at a time; fix = re-encode that asset's audio
   (done for `C12U07_R1.mp3`, staging + src copies, same audio).
2. `cd build && bun ./build-static.mjs`
3. `python3 build/assemble_parlons.py` (rebuilds this folder from dist + pron trees)
4. Commit and push (below). GitHub Pages serves the `gh-pages` branch.

## Push commands

```sh
cd ~/workspace/french/parlons-github
export GIT_SSH_COMMAND='ssh -o BatchMode=yes -o IdentitiesOnly=yes -i $HOME/.ssh/id_ed25519 -o StrictHostKeyChecking=accept-new -o ProxyCommand=$HOME/workspace/tools/http-connect-proxy.py\ %h\ %p'
git push origin main:main main:gh-pages
```
(Remote: `ssh://git@ssh.github.com:443/asra-hoss/parlons.git` — port 22 is blocked
on this VM, hence SSH-over-443 with the CONNECT proxy, same recipe as
`french-study-app` and `edito-b1`.)

## Status (Nov 1, 2026)

**ACCENT LIGHTENED ONE STEP — Nov 1, 2026:** per Asra (« یکم
بنفشش رو کمرنگ‌تر می‌کنی، خیلی کم »), ONLY the accent token
changed: `--accent` #6c4cf1 → #7a5ff0 (dark-mode variant
#a78bfa → #b59ef9 by the same step); the matching theme-color
in index.html + manifest went with it. Nothing else touched.
Verified in the built bundle (#7a5ff0 present, #6c4cf1 ×0);
commit touches index.html, manifest + the CSS bundle only,
all thumbnails restored from HEAD, byte-identical.

**LINGUA RESTYLE + SPLIT NAVIGATION — Nov 1, 2026:** per Asra
(approved reference: the Lingua-style Listen screen), the whole
app is restyled through the shared theme: white background, soft
lilac pastel tints (`--accent-soft` #efeaff, `--surface-alt`
#f4f1fe), ONE vivid violet accent (`--accent` #6c4cf1), dark ink
text (#221d33), Nunito (self-hosted variable woff2 under
`assets/fonts/`) as the Latin font, Vazirmatn unchanged for
Persian. SPLIT NAVIGATION on the dossier screen: the header strip
now holds ONLY Listen / Read / Vocab / Grammar as icon + label
pills (active = filled violet, white label; rest pale lilac);
Exercises / Writing / Speaking / Flashcards moved to a FIXED
BOTTOM NAVIGATION BAR (white, soft top shadow, safe-area inset;
active item violet, rest grey ink), and the dossier content got
bottom padding (pb-32) so the bar never covers it. Header: lilac
« ← Dossiers » pill, folder icon + dossier title. Listen player:
lilac card, Previous/Next now pale circles with violet ◀◀ / ▶▶
glyphs around the big violet Play disc (her Nov 1 hard rules
untouched: no track line, no autoplay, timer manual, per-question
placement audio unchanged). Grammar's inner per-point sub-tabs
unchanged. Content, data and storage keys untouched. Verified in
the built bundle (bottom-bar « More sections » ×1, #6c4cf1 +
#efeaff + Nunito in CSS, Autoplay ×0, grammarPoint present);
commit touches index.html, manifest, the new bundle, the Nunito
font and this note only — all thumbnails restored from HEAD,
byte-identical.

**GRAMMAR TABBED — Nov 1, 2026:** per Asra (« گرامر رو هم قرار بود
تب کنی »), the Grammar tab no longer stacks every sheet in one long
scroll: it now shows a pill sub-tab strip (same pattern as Vocab) —
one tab per grammar point, labelled with the point's short topic
(the part before the " — " in its title, trimmed; detail part on
collision) — and renders ONLY the selected point's sheet, booklet
layout and 🇫🇷/🇮🇷 flag unchanged. Selection persists per dossier
in origb1:nav (`grammarPoint`, by point number; default = first
point); single-point dossiers show no strip. « Mark as done » for
Grammar unchanged (still ticks all the dossier's points at once).
Verified in the built bundle (« Grammar points » tablist ×1,
`grammarPoint` ×2); commit touches index.html + bundle files only,
all 48 thumbnails restored from HEAD, byte-identical.

**LISTEN PLAYER TRIMMED + PREV/NEXT GLYPHS — Nov 1, 2026:** per Asra
(« 1 / 2 — Bonjour… و اتو پلی رو بردار از اپ اصلی » + « علامت قبل و بعد
هم درست کن تو اپ »), in the shared `ListenTab` player: (1) the track
indicator line (« N / M — title ») is REMOVED entirely; (2) AUTOPLAY
is REMOVED completely — toggle, state and the onEnded auto-advance
logic; a track now simply stops at its end and moving on is manual
via Previous/Next only; (3) the Previous/Next glyphs changed from
skip-style ⏮/⏭ (triangle + bar) to plain double triangles **◀◀ / ▶▶**
(U+25C0 ×2 / U+25B6 ×2), same size/weight, balanced either side of
Play (single ▶, unchanged) in the solid-disc family. Verified in the
built bundle (Autoplay/autoplay ×0, ⏮/⏭ ×0, ◀◀ ×1, ▶▶ ×1, « Lecture
enchaînée » ×0); commit touches index.html + bundle files only, all
48 thumbnails restored from HEAD, byte-identical.

**LISTEN TRANSPORT ICONS UNIFIED — Nov 1, 2026:** per Asra (« علامت های
پلی و قبلی بعدی چرا بهم نمی‌خورن »), the playlist player's Previous/Next
were pale bordered circles beside a solid teal Play disc. Prev/Next are
now solid accent discs with white glyphs (`h-12 w-12 bg-[var(--accent)]
text-lg text-white`), Play unchanged at h-14 — one family, Play
slightly larger; disabled keeps `disabled:opacity-40` (same family,
dimmer). The placement-test player has a single solid accent
« Écouter » pill — already in family, untouched. Verified in the built
bundle (new class ×2, old `h-11` bordered class ×0); commit touches
index.html + new bundle only, 48 thumbnails restored from HEAD,
byte-identical.

**DOSSIER CARDS RESTYLED + LIVE — Nov 1, 2026** (commit `286181b`): per Asra,
the Home dossier card no longer crowds its text beside the thumbnail — the
card is now stacked: clean full-width thumbnail on top (`h-36 w-full
object-cover`), and below it only « Dossier N — « Title » » + the arrow.
Removed from the card in the same pass (her follow-up instruction): the
theme line, the counts line (« pages · texts · listening · words ») and
the « Studied: … » time line — no counts of texts/files/words/minutes
anywhere on Home. Tap behaviour and the dossier screens (incl. the study
timer) are unchanged; the change is in the shared Home card component, so
it applies to all five levels. Verified live: root serves new bundle
`index-tn72fsxk.js` (new card class present, old `h-20 w-28` side-thumb
class absent, counts fragment absent); sample thumbnails from B1/A2/
C1/C2 byte-identical to HEAD (48 JPGs restored from HEAD before commit).

**HOME CLEANUP PUSHED + LIVE — Nov 1, 2026** (commit `83e0afd`): per Asra,
Home reads international now — no explanatory prose, no Persian on Home.
Placement card title is exactly « Placement Test » (`homeButton` changed in
`placement/content/placement_meta.py` + regenerated `placement-data.ts`)
and its French subtitle (« Vous ne savez pas par où commencer ? … ») is
deleted. Also removed from Home: the `meta.authors` line (« Français de
A1 à C2 — contenu 100 % original », `BOOK_META.authors` now `""` in
`data.ts`), the Sources framing paragraph (« Textes, dialogues, grammaire
et exercices : contenu 100 % original … aucun texte de manuel. ») and the
« Correction : avec votre propre clé API … » line. Kept: « Parlons ! »
header, level pills, dossier cards, and ALL Sources credit lines
(per-unité CC BY credits, « Voix des dialogues : voix de synthèse. »,
placement real-voice credits — licence requirement). Test screens
unchanged (their internal title stays « Test de niveau »). Verified
live: root serves new bundle `index-jaymg3y8.js`; bundle grep —
« Placement Test » present, all removed strings absent; commit touched
only `index.html` + the new bundle (48 thumbnails restored from HEAD,
byte-identical).

**A1 PUSHED + LIVE — Nov 1, 2026** (commit `32a7722`): the fifth and
final level is in. Built from Asra's own checklist — the A1 fiches of
Raemdonck, *TCF Entraînement intensif* (Partie 2, pp. 20–24), sent by
her Nov 1 — ordered along her developmental spine (alphabet/phonetics →
greetings → pronouns → être/avoir/aller → -er verbs → articles →
onward), all content 100 % original. Coverage map:
`original-b1-product/content-a1/CHECKLIST-COVERAGE.md` (28/28 grammar
notions, 19/19 vocab themes, 10/10 savoir-faire as Writing/Speaking
prompts, phonetics in U1). Per unité: 3 texts, made dialogue (voix de
synthèse) + ONE long CC BY real-voice excerpt (12/12, licence verified
on each video's own page; U1's assigned Allezy lead was rejected on
speech — bilingual VI/FR — and replaced by a verified same-theme
video, documented in `audio-work-a1/provenance/u01.md`). Gloss coverage
10,814/10,814 (100 %); LL vocab pronunciation 453 entries after the
quality pass (468/480 fetched); pron-index now 9,525 items (1,152
under `assets/a1/`). Selector order A1 → A2 → B1 → B2 → C1/C2;
placement-test A1 result now opens A1 (`bandToLevelId`). Storage
family `oria1:`, dossiers `orig-a1-u1…u12`, staging in
`content-a1/` + `site-a1/` + `audio-work-a1/` (A2 pipeline cloned;
beware the sed trap: `sha256` → `sha156` when adapting scripts with
a2→a1 replacements). Verified live: root + bundle contain
`orig-a1-u1…u12`, A1 dialogue/excerpt MP3s 200, A1 thumbnail 200 at
the illustrated byte size, A1 LL + shard pron clips 200, and A2/B2/
C1/C2 thumbnails byte-identical to the illustrated files (restored
from HEAD before commit), B1 + placement files 200.

**PLACEMENT LISTENING SPLIT PER QUESTION — Nov 1, 2026** (commit
`f0fadc4`): Asra's rule « هر سوال فایل جدا » — each placement
listening question now plays only its own MP3 (`PL_L{n}Q{1..3}.mp3`,
15 files, cut from the PL_L1…L5 masters at transcript-line
boundaries) and the 2-play cap applies per question. Boundaries,
method and the afade/output-`-ss` silence pitfall are documented in
the source project: `placement/audio/SEGMENTS.md`. Data gained
`questionAudio: string[]` per piece (generator-derived); scoring,
stop rule and results untouched (31/31 module checks pass).
Verified live: all 15 per-question files 200, thumbnails
byte-identical (340,255 B sample), pron-index 200.

**PLACEMENT TEST PUSHED + LIVE — Nov 1, 2026** (commit `0aef07e`, on top of
the illustrations commit `edb1e14`): Home card « Test de niveau » above the
level selector; sections Écouter → Lire → Écrire → Parler with the stop rule
(2 consecutive wrong answers end a section); writing scored only via the
learner's own API key (no key → standard notice + writing « non évalué »);
speaking = can-do self-assessment + optional self-check recording
(`pl-speak-selfcheck`, never scored/sent/transcribed); result screen with
per-skill levels + « Commencer le niveau X » (the button is the only thing
that switches level; an A1 recommendation starts at A2 — no A1 level is
wired yet); result persisted at `origb1:placement-result`. Verified live:
root 200 + new bundle, `assets/PL_L1…L5-*.mp3` 200, pron-index 200,
C12 dialogue 200, illustration thumbnails untouched (30,008 B sample).
⚠️ Two gotchas from this run: (1) the build source's thumbnail JPGs are
STALE — thumbnail style updates were applied tree-side only (photos in
`83ca27f`/`12aa8ac`, illustrations in `edb1e14`), so a fresh build's
`dist` carries the old cartoon bytes under the same filenames: after
rsync'ing the assembled tree over the clone, restore every modified
`*.jpg` from HEAD (`git checkout HEAD -- <jpgs>`) before committing, or
the push silently reverts the thumbnails. (2) `/tmp` is a 512 MB tmpfs —
clone the repo under `~/workspace`, never `/tmp`.

**C1/C2 PUSHED + LIVE — Nov 1, 2026** (commit `83ca27f`): live site serves
all four levels; verified live: root 200 + Parlons title, bundle contains
the C1/C2 registration + `oric12-u1`, `assets/pron-index.json` 200 with
8,535 items (2,493 under `assets/c12/`), C12 dialogue/excerpt MP3s and
pron clips (shard + Lingua Libre) 200, B2 regression clip 200.

**PUSHED + LIVE — Nov 1, 2026.** The empty public repo `asra-hoss/parlons`
was created in the browser, then `git push origin main:main main:gh-pages`
succeeded from this VM (both branches created). GitHub Pages serves the
`gh-pages` branch at https://asra-hoss.github.io/parlons/ — verified live
Nov 1, 2026: root page 200 with title « Parlons ! — Français de A1 à C2 »,
`assets/pron-index.json` 200, sample pronunciation clip
`assets/b2/pron/ll/drone.mp3` 200, `manifest.webmanifest` 200.
(Pages took ~2 minutes to build after the push — initial fetches 404'd,
then went 200.)

**A1 U1 DIALOGUE/TEXT FIXED — Nov 1, 2026:** per Asra's review of A1
(« داستان اول چرا یارو باید اسم طرف مقابلش رو هجی کنه »), Unité 1's made
dialogue had Hugo spell CLAIRE's name back to her and an unmotivated
« Voilà le professeur, devant la porte » announcement. Fixed in
`content-a1/unites/u01.py`: Hugo now spells ONLY his own name
(« H, U, G, O. »), the teacher's arrival is spotted naturally
(« Regarde, le professeur arrive ! ») and the pair head into class
(« Allez, on entre ! » / « Oui ! À tout à l'heure ! »). Texte 2: the
teacher now asks « Ça s'écrit comment ? » alongside the name question,
so Sara's spelling has a reason. Dialogue audio rebuilt through the A1
pipeline (A1U01_D1.mp3, 25.7 s, same voices); glosses re-verified
10808/10808 via gen_gloss_overlay_a1.py; one new sentence clip for
Texte 2 (the paragraph's other merged sentence keeps no clip, like 5
pre-existing A1 sentences). Unités 2–12 audited for the same defect
class (vocab-display lines, unmotivated actions) — no other clear cases;
descriptive/informational reading texts are by design. Commit touches
index.html, the JS bundle, the A1U01_D1 MP3, pron-index + 1 pron clip,
and the favicon set (logo.svg + icon PNGs, referenced by index.html);
all 48 thumbnails restored from HEAD, byte-identical.

**LOGO + HOME TRIM — Nov 1, 2026:** per Asra (« لوگو رو درست
کن ») the app carries its own Parlons ! logo (shipped in the
same tree as the U1 fix above, documented here for the record):
a violet (#7a5ff0) rounded speech bubble with a white « ! » —
hand-drawn SVG at `logo.svg` (client/public/). Home header: the
small caps brand line + the big « Dossiers » h1 are replaced by
ONE lockup — the mark inline in App.tsx (fill = var(--accent),
dark mode follows) + the « Parlons ! » wordmark in Nunito;
settings button unchanged. Favicon: build-static.mjs injects
the SVG link ahead of the PNG fallback. The old TEAL placeholder
icons are gone: icon-192 / icon-512 / apple-touch-icon render
the bubble on the lilac tint (#efeaff); manifest entries
unchanged. Same pass, per Asra's Home screenshot: level pills
show ONLY the code (A1 / A2 / B1 / B2 / C1/C2 — « Niveau »
removed) and the « Dossiers » heading is removed — removals
only, nothing else changed.

**CARD CROP FOCAL POINTS — Nov 1, 2026:** per Asra (« عکس ها رو ببین »),
the Home dossier cards' wide short crop (`h-36 object-cover`, default
centre) chopped heads — worst case A1 Dossier 2, whose card cut the
man's face while the square illustration itself is fine. Fix is
code-only (no JPG bytes changed): a per-dossier focal point
(`DOSSIER_THUMB_FOCUS` in App.tsx, object-position Y %) stored beside
`DOSSIER_THUMBS_BY_LEVEL`, applied to the card `<img>`. All 60
thumbnails (A1/A2/B1/B2/C1/C2) were audited — face positions located
per illustration, crop bands simulated at the card's mobile aspect
and visually verified per level. Values frame the faces/subject of
each unité (e.g. A1 U2 → 8%, B1 U8 → 68%, C1/C2 U12 → 91%); the three
people-less B1/A1 still lifes (A1 U6 desk, B1 U4 map, B1 U6 paper
stack) are framed on their subjects. Where one band cannot hold
every figure (B2 U3 reporter vs crouching pair, B2 U10 presenter vs
audience, B2 U12/C12 U12 two-depth scenes) the main subject wins.
Verified in the built bundle (`DOSSIER_THUMB_FOCUS` values +
`objectPosition` present); JPGs all restored from HEAD, byte-identical.

**HOME CARDS SHOW FULL ILLUSTRATION — Nov 1, 2026:** per Asra
(« عکس نصفه … مگه قرار کجا دیگه دیده بشه این عکس »), the focal-point
crop is REVERTED: these illustrations are only ever seen in the Home
cards, so the card must show the WHOLE picture. The card <img> is now
`h-auto w-full` (natural aspect, no fixed height, no object-cover)
and the DOSSIER_THUMB_FOCUS map + thumbFocus wiring are removed from
App.tsx. Nothing else changed (titles, pills, layout below the image).
Verified in the built bundle (object-cover ×0, objectPosition ×0,
« h-auto w-full rounded-xl » present); commit touches index.html, the
new bundle, and this note only — all JPGs restored from HEAD,
byte-identical.
