# PixelPaws

[![CI](https://github.com/LFairbairn/pixelpaws/actions/workflows/ci.yml/badge.svg)](https://github.com/LFairbairn/pixelpaws/actions/workflows/ci.yml)

A virtual pet game built in Python and Tkinter, featuring a hand-drawn pixel art tabby cat. Adopt and care for your cat by feeding, playing, and tucking it in for a nap.

Built by Lynsey Fairbairn & Chief Product Owner Daughter (age 8) as a summer holiday project!

---

## Project Goals

This project is as much about *how* it's built as what it ends up being:

- **BDD-first development** — game behaviour is described as Given/When/Then scenarios (`pytest-bdd`) before it's implemented, so each feature starts from a plain-English description of what should happen.
- **Requirements gathering practice** — the Chief Product Owner is 8 years old and has genuine, often surprising opinions about what the cat should do. Turning her ideas into concrete requirements (and re-checking assumptions when scope changes, like the background system) is deliberate practice, not a shortcut.
- **Learning over speed** — first time using Tkinter and pytest-bdd. The priority is understanding *why* something works, not just getting it working.
- **A real project for a kid to be part of** — from pixel art in Piskel to deciding what the cat needs, the Product Owner is involved in actual decisions, not just the idea.

---

## Challenges

**Backgrounds, and not being an artist.** The Product Owner asked for backgrounds that match what the cat is doing — a bedroom for sleeping, a kitchen for eating, a garden for playing. Hand-drawing rooms in Piskel isn't a realistic option (the cat sprite is hard enough), so backgrounds are generated with **ComfyUI** running a locally-hosted diffusion model, using text-to-image prompts. The Product Owner describes what she wants (e.g. "a cosy bedroom with a window and the moon outside"), and that description becomes the prompt — so she's still directing the art even though neither of us is drawing it by hand.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Primary language |
| Tkinter | GUI framework |
| Pillow | Image loading/scaling for pixel art sprites |
| pygame.mixer | Audio playback |
| Piskel | Pixel art and animation authoring |
| ComfyUI + local diffusion model | Text-to-image background generation |
| uv | Package and project management |
| pytest + pytest-bdd + pytest-cov + pytest-mock | BDD and unit testing |
| Ruff | Linter |
| Black | Code formatter |
| Taskipy | Task runner shortcuts |
| GitHub Actions | CI pipeline |

---

## How to Play

_TBD — coming once Phase 1 (MVP) is implemented._

---

## Project Layout

```
pixelpaws/
├── pyproject.toml
├── project.md                # Living progress/TODO tracker
├── virtual_pet_spec.docx     # Original game spec
├── .github/
│   └── workflows/
│       └── ci.yml
├── assets/
│   ├── *.gif                 # Canonical (native size) animations
│   ├── *_x10.gif              # Pre-scaled reference exports — not loaded by the game
│   ├── piskel/                # Piskel source files
│   ├── backgrounds/
│   └── sounds/
├── src/
│   └── __init__.py
└── tests/
    ├── features/              # Gherkin .feature files
    └── step_defs/             # pytest-bdd step definitions
```

---

## How to Run

_TBD — coming once `src/main.py` is implemented._

---

## How to Test

```bash
# Install dependencies
uv sync

# Run everything: lint, format check, and tests with coverage
uv run task check

# Or run individually:
uv run task lint      # ruff linting
uv run task format    # black format check
uv run task test      # pytest (incl. BDD scenarios) with coverage report
```

---

## Screenshots

_TBD._

---

## Credits

Game design, background prompts, and sound effect recordings by the Chief Product Owner (age 8). Pixel art, animation, built and engineered by Lynsey Fairbairn.
