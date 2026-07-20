# PixelPaws Project Tracker

Formal, ID-mapped requirements now live in [`REQUIREMENTS.md`](REQUIREMENTS.md) — each `REQ-XXX-NNN` is
traced to a planned BDD feature/scenario there. This tracker remains the day-to-day TODO/progress log.

## Project Setup
- [x] Initialise project with uv (`pyproject.toml`)
- [x] Add dependencies (pillow, pygame, taskipy)
- [x] Add dev dependencies (pytest, pytest-bdd, pytest-cov, pytest-mock, black, ruff)
- [x] Configure Black target version (py312)
- [x] Configure pytest-bdd (`bdd_features_base_dir = "tests/features/"`)
- [x] Create `.gitignore` (.venv/, __pycache__, .pytest_cache, .ruff_cache, .DS_Store, .env)
- [x] `git init`
- [x] Push to GitHub (`LFairbairn/pixelpaws`, public)

## Assets
- [x] Reorganize gifs/piskel sources into `assets/` (idle, meow, falling_asleep, sleeping, waking_up, sad — canonical + `_x10` reference versions)
- [x] Move `.piskel` source files into `assets/piskel/`
- [x] Add `Whisker-stretch.gif` (+x10) — new animation, trigger/state not yet decided
- [ ] Add eating.gif animation (Phase 2 item from spec, ties to kitchen background)
- [ ] Add playing.gif animation (Phase 2 item from spec, ties to garden background)
- [x] Add `walking_left.gif`/`walking_right.gif`/`stand_idle.gif` (+x10) — purpose decided: occasional
  idle wandering (REQ-ANIM-011), implemented in `src/ui.py`
- [x] Add `assets/backgrounds/bedroom.png` — synced to Sleep state (product owner's idea: backgrounds match cat behaviour)
- [ ] Add kitchen background — for Feed/eating
- [ ] Add garden background — for Play
- [ ] Decide background transition logic (how/when the background swaps as state changes) — new scope beyond original spec, will need to be designed alongside the state machine in Game Implementation
- [x] Record raw sound clips into `assets/sounds/` (Hiss.m4a, Meow.m4a, Prrp.m4a, Purr2.m4a)
- [ ] Convert sounds to WAV
- [ ] Map each sound to its game trigger (meow / happy / eating / ambient) and rename accordingly
- [ ] Decide what `Whisker-stretch.gif` is for (idle variation? waking-up step? something else?)

## BDD Tests
- [x] All planned `.feature` files scaffolded in `tests/features/` (`onboarding`, `stats`, `feeding`, `playing`,
  `sleeping`, `state_machine`, `ui`), each scenario tagged with its `REQ-XXX-NNN` ID — see
  [`REQUIREMENTS.md`](REQUIREMENTS.md) §3 for the full traceability matrix. Applied the earlier feedback on the
  `Feeding` draft throughout: deterministic time control (e.g. "When 30 minutes pass") instead of "enough time
  has passed", concrete `Given` values (e.g. "the Tummy stat is 2") instead of "the cat is hungry".
- [ ] Step definitions (`tests/step_defs/`) — not started; feature files are currently inert (0 items collected)
  until steps exist, by design (BDD-first: scenarios before implementation)
- [ ] Feed action restores Tummy stat to full
- [ ] Play action restores Happy stat and depletes Energy
- [ ] Sleep action restores Energy stat over time
- [ ] Stats deplete over time while idle (Tummy faster than Happy)
- [ ] Stat bar colour reflects level (green 7-10 / yellow 4-6 / red 1-3)
- [ ] Tummy critical (below 3) triggers Meowing state
- [ ] Tummy restored from critical returns to Idle state
- [ ] Sleep pressed triggers Falling Asleep → Sleeping transition
- [ ] Energy restored during Sleeping triggers Waking Up → Idle transition
- [ ] Onboarding: selecting variant + naming the cat + pressing Start begins the game

## Game Implementation — Phase 1 (MVP)
## CI
## README
- [x] Create `README.md` — tech stack, project layout, How to Test (uv/task commands), CI badge, credits
- [ ] Fill in How to Play (once Phase 1 MVP exists)
- [ ] Fill in How to Run (once `src/main.py` exists)
- [ ] Add screenshots

## Backlog
Raw ideas — captured as soon as they come up, not yet scoped or committed to a phase. No format
required beyond "who suggested it and what it is"; refine later. Once an idea has enough shape to be
testable, promote it into [`REQUIREMENTS.md`](REQUIREMENTS.md) as a numbered `REQ-XXX-NNN` and delete it
from here.

- Feed action could ignore presses when Tummy is already at/near full (not a strict cooldown timer, just a threshold check) — prevents spamming the eating sound/animation. Came up while drafting the Feeding BDD scenarios; not critical, revisit if it matters once Feed is implemented.

## Phase 2 — Polish
## Phase 3 — Extras
- [ ] Zoomies state (REQ-SM-007, REQ-ANIM-010, REQ-STAT-009) — triggered by rapid Play presses while
  Energy is high. Chief Product Owner idea, 2026-07-20. Trigger-window duration and exit condition are
  open questions — see `REQUIREMENTS.md` §4. Needs a `zoomies.gif` asset before it can be implemented.
