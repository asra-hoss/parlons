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

Three levels in ONE app, Home level selector in the order **A2 → B1 → B2**,
choice persisted in the browser (`origb1:level`, the app's standing storage family):

- **B1** — the verified B1 product exactly as the Muse artifact `b1` v13 serves it
  (interactive exercises, tab order Listen → Read → Vocab → Grammar → Exercises →
  Writing → Speaking → Flashcards, universal tap-a-word glosses, BYOK API-key
  correction, white-background cartoon thumbnails). Content untouched.
- **A2** — from `content-a2/` staging, per `content-a2/MERGE_NOTE_A2.md`
  (data `book-data-a2.json`, dossiers `orig-a2-u1…u12`, assets under `assets/a2/`).
- **B2** — from `content-b2/` staging, per `content-b2/MERGE_NOTE_B2.md`
  (dossiers `orig-b2-u1…u12`, assets under `assets/b2/`).

Not yet included (planned updates to this same repo): **A1** (rebuilt to Asra's
own developmental checklist — awaiting the checklist), **C1/C2** (in production),
the placement test, and the Spanish/Russian/Hindi/Arabic localisation pass.

## Tree rules (learned the hard way — keep them)

- EVERYTHING lives under `assets/`: bundle media, `assets/fonts/`,
  `assets/pron/` (B1 clips), `assets/a2/pron/`, `assets/b2/pron/`, and the single
  merged `assets/pron-index.json` (6,042 entries; B1 first, then A2/B2 additions,
  Lingua Libre clips repoint shard-TTS entries). Root-level `pron/` or `fonts/`
  copies are NOT used on this host.
- `.nojekyll` at the root (no Jekyll processing).

## Update procedure

1. Edit the app source in `original-b1-product/build/client/src/`
   (new level data: drop the staged JSONs in `site-<lv>/`, run
   `build/convert_levels.py`, register the level via `build/do_merge_edits.py`).
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
