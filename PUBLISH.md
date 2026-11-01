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
