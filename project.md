# PixelPaws Project Tracker

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
- [ ] Add walking.gif animation (new idea, not in original spec — purpose/trigger TBD)
- [x] Add `assets/backgrounds/bedroom.png` — synced to Sleep state (product owner's idea: backgrounds match cat behaviour)
- [ ] Add kitchen background — for Feed/eating
- [ ] Add garden background — for Play
- [ ] Decide background transition logic (how/when the background swaps as state changes) — new scope beyond original spec, will need to be designed alongside the state machine in Game Implementation
- [x] Record raw sound clips into `assets/sounds/` (Hiss.m4a, Meow.m4a, Prrp.m4a, Purr2.m4a)
- [ ] Convert sounds to WAV
- [ ] Map each sound to its game trigger (meow / happy / eating / ambient) and rename accordingly
- [ ] Decide what `Whisker-stretch.gif` is for (idle variation? waking-up step? something else?)

## BDD Tests
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
- [x] First draft written: `Feeding` feature (3 scenarios) — reviewed, revisions pending (deterministic time control instead of "enough time has passed"; concrete Given values instead of "the cat is hungry")

## Game Implementation — Phase 1 (MVP)
## CI
## README
- [x] Create `README.md` — tech stack, project layout, How to Test (uv/task commands), CI badge, credits
- [ ] Fill in How to Play (once Phase 1 MVP exists)
- [ ] Fill in How to Run (once `src/main.py` exists)
- [ ] Add screenshots

## Future Ideas
- Feed action could ignore presses when Tummy is already at/near full (not a strict cooldown timer, just a threshold check) — prevents spamming the eating sound/animation. Came up while drafting the Feeding BDD scenarios; not critical, revisit if it matters once Feed is implemented.
## Phase 2 — Polish
## Phase 3 — Extras
