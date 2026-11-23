# Collection — design package (from Asra, Nov 23, 2026)

VISUAL REFERENCE: `reference-sample.jpg` in this folder is Asra's own mock — the build must follow its look: light Paris-sky theme, Eiffel motif, soft glossy round badges with rich colourful icons, white cards, friendly game feel (Royal Match Collection is the model).

## Model
- The app's progress/roadmap view becomes a COLLECTION.
- Top: title "My Collection", level tabs A1 A2 B1 B2 C1 C2, and an overall progress card: "All levels — X/132 lessons" with a green progress bar.
- SETS = dossiers (75 after the dossier-split job). Grid of round badges, 3 per row: icon + dossier name under it.
- Set states (Asra's rule, confirmed Nov 23):
  - Complete: full colour + green check badge.
  - Started but unfinished: full colour + its own mini progress bar and fraction (e.g. 1/2) under the name.
  - Not started: GREY icon and muted name — the name stays readable.
- Tapping a set opens its panel (like the Bazaar panel in the reference): themed header with the dossier name, an X button to close (required), a progress bar "n/total lessons", and a grid of CARDS = the set's lessons:
  - Done lesson: colourful card.
  - Not-done lesson: greyed card, title still readable.
  - Pager at the bottom ("Set n of N" with arrows) to move between sets.
- Tapping a lesson card opens that lesson (existing lesson URLs).
- Progress data: derive from the same per-lesson completion state the app already tracks; lesson/dossier structure comes from the plan data (const D=) AFTER the dossier-split job — 132 lessons, 75 dossiers.

## Rules
- UI in English; lesson/dossier names in French as in the plan. NO Persian anywhere.
- Do not change lesson pages, lesson order, or dossier structure in this job.
- Nothing else on Home changes except how the roadmap/progress entry opens this view.
