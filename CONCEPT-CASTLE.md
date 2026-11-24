# Castle Path — Wish Bubble Progress (concept brief)

Artwork: `castle-bubbles.webp` in this branch (autumn mountain valley, one winding
stone path climbing to a castle with a glowing golden crown, iridescent wish
bubbles floating beside the path).

## The concept (owner's words, settled Nov 23, 2026)
The learner is a traveller walking up the path to the castle door (the castle =
the end of the level, the crown = the final prize). The numbered stones on the
path are the lessons. Beside the path float **wish bubbles** — the rewards.

## Bubble mechanics (exact)
1. A bubble whose lesson is not yet reached is **grey / dull**.
2. When its lesson is completed, the bubble becomes **colourful and glowing** —
   ready.
3. The bubble then **pops by itself** — no tap needed, **no sound**, nothing
   jumps out. It bursts into a soft burst of **golden light and sparkles**, and
   its little star is released.
4. Right after the pop, **the whole view steps forward** along the path —
   one step closer to the castle. This must be a true forward movement of the
   viewpoint (the castle grows larger, foreground stones pass by), **NOT a
   zoom or a crop** — the castle, including its crown, must always stay fully
   in frame.
5. Repeat bubble after bubble until the traveller reaches the **castle door**.

## Build rules
- Build a self-contained interactive prototype page under `/progress-copy/`
  only. NEVER touch the real Progress page or the Roadmap.
- Use `castle-bubbles.webp` as the scene artwork (copy it into
  `/progress-copy/` in the build).
- The prototype must be playable: a "complete lesson" control steps through
  the sequence — bubble turns colourful, pops with light, view glides one
  step forward — so the owner can flip through the whole journey to the door.
- App UI language: English. No Persian anywhere in the app.
