# PixelPaws — Requirements Specification

Requirements derived from `virtual_pet_spec.docx` (Project Specification v0.1) and requirements-gathering
sessions with the Chief Product Owner. This document is the source of truth for *what* the game must do;
`project.md` tracks *progress* against it.

Specification source: `virtual_pet_spec.docx` §3–§9
Status: **Draft v1.0** — living document, update as requirements evolve

---

## 1. Conventions

### 1.1 Requirement ID scheme

`REQ-<CATEGORY>-<NNN>`, category-coded and zero-padded to three digits.

| Category code | Area | Spec source |
|---|---|---|
| `ONB` | Onboarding | §3 |
| `STAT` | Cat Stats | §4 |
| `ACT` | Player Actions | §5 |
| `ANIM` | Animations | §6 |
| `AUD` | Sound | §7 |
| `UI` | UI Layout | §8 |
| `SM` | State Machine | §9 |
| `NFR` | Non-Functional | §2, §6 |

### 1.2 Priority

MoSCoW, mapped to the development phases defined in spec §11:

| Priority | Meaning | Phase |
|---|---|---|
| **Must** | Required for a playable core loop | Phase 1 — MVP |
| **Should** | Important, not launch-blocking | Phase 2 — Polish |
| **Could** | Desirable if time allows | Phase 3 — Extras |
| **TBD** | Not yet specified precisely enough to build or test | — |

### 1.3 Status

| Status | Meaning |
|---|---|
| Not Started | No implementation or test exists yet |
| In Progress | Implementation and/or BDD scenario in progress |
| Met | Implemented and demonstrated by a passing, tagged BDD scenario |

### 1.4 Verification method

Following standard SRS practice (Inspection / Analysis / Demonstration / Test), each requirement states how
it will be verified. Behavioural requirements are verified by **Test** — a `pytest-bdd` scenario tagged with
the requirement's ID. Layout/visual requirements that are impractical to assert against a Tkinter canvas are
verified by **Demonstration** (manual run-through) or **Inspection** (code/asset review) instead.

### 1.5 Traceability

Each requirement below lists the feature file and scenario expected to prove it. To close the loop, tag the
corresponding Gherkin scenario with the requirement ID:

```gherkin
@REQ-STAT-002 @REQ-ACT-001
Scenario: Feed action restores Tummy stat to full
  Given the cat's Tummy stat is 2
  When the player presses the Feed button
  Then the Tummy stat is 10
```

A scenario may carry more than one tag when it proves multiple requirements at once. `pytest-bdd` treats
Gherkin tags as pytest markers, so `pytest -m "REQ-STAT-002"` (quoted, since the expression parser needs
the hyphens escaped from the shell/quoting, not from pytest itself) can run just the scenarios proving a
given requirement. These marks are deliberately left unregistered in `pyproject.toml` — with ~40 of them
expected, hand-registering each would just be a second place for the ID list to drift out of sync with this
document — so `PytestUnknownMarkWarning` for `REQ-*` marks is filtered out in `pyproject.toml` rather than
fixed by registration. Section 3 is the running Requirements Traceability Matrix (RTM); update its
Status/Verified-by columns as scenarios land.

---

## 2. Requirements

### 2.1 Onboarding (`ONB`) — spec §3

**REQ-ONB-001** — Cat variant selection
Priority: Must · Verification: Test
The system shall present a variant/colour selection control on the welcome screen before the game starts.
In Phase 1, tabby is the only selectable variant.
*Feature:* `onboarding.feature` → *Scenario:* "Only tabby variant is available in Phase 1"

**REQ-ONB-002** — Cat name entry
Priority: Must · Verification: Test
The system shall require the player to enter a name for the cat on the welcome screen before the game can
start.
*Feature:* `onboarding.feature` → *Scenario:* "Start is disabled until a name is entered"

**REQ-ONB-003** — Start begins the game
Priority: Must · Verification: Test
The system shall begin the game and display the main screen when the player presses Start, provided a
variant is selected and a name has been entered.
*Feature:* `onboarding.feature` → *Scenario:* "Pressing Start with a variant and name begins the game"

---

### 2.2 Cat Stats (`STAT`) — spec §4

**REQ-STAT-001** — Stats initialise at maximum
Priority: Must · Verification: Test
The system shall initialise Tummy, Happy, and Energy to 10 (full) at the start of a new game.
*Feature:* `stats.feature` → *Scenario:* "All stats start at 10"

**REQ-STAT-002** — Tummy depletes while idle
Priority: Must · Verification: Test
The system shall decrease the Tummy stat over time while the cat is in the Idle state.
*Feature:* `stats.feature` → *Scenario:* "Tummy depletes over time while idle"

**REQ-STAT-003** — Happy depletes while idle, slower than Tummy
Priority: Must · Verification: Test
The system shall decrease the Happy stat over time while the cat is in the Idle state, at a slower rate
than Tummy depletes.
*Feature:* `stats.feature` → *Scenario:* "Happy depletes slower than Tummy while idle"

**REQ-STAT-004** — Energy depletes while playing
Priority: Must · Verification: Test
The system shall decrease the Energy stat while the cat is in the Playing state.
*Feature:* `playing.feature` → *Scenario:* "Energy depletes while playing"

**REQ-STAT-005** — Stat bar colour reflects level
Priority: Must · Verification: Test
The system shall render each stat bar green at 7–10, yellow at 4–6, and red at 1–3.
*Feature:* `stats.feature` → *Scenario Outline:* "Stat bar colour matches stat value"

**REQ-STAT-006** — Tummy critical threshold
Priority: Must · Verification: Test
The system shall treat Tummy values below 3 as critical, triggering the Meowing state (see REQ-SM-001).
*Feature:* `feeding.feature` → *Scenario:* "Tummy below 3 is critical"

**REQ-STAT-007** — Happy critical threshold
Priority: Should · Verification: Test
The system shall treat Happy values below 3 as critical, triggering the sad animation (`sad.gif`, spec §6.2).
*Feature:* `playing.feature` → *Scenario:* "Happy below 3 triggers sad state"
> Note: no formal state-machine entry exists yet for a "Sad" state (spec §9 only defines Idle / Meowing /
> Falling Asleep / Sleeping / Waking Up). Treated as Should/Phase 2 pending that design work — see Open
> Questions (§4).

**REQ-STAT-008** — Energy critical threshold
Priority: Should · Verification: Test
The system shall treat Energy values below 3 as critical, triggering a low-energy idle variation
(`sleepy_idle.gif`, spec §6.2).
*Feature:* `sleeping.feature` → *Scenario:* "Energy below 3 triggers sleepy idle animation"
> Same caveat as REQ-STAT-007 — no state-machine entry defined yet.

---

### 2.3 Player Actions (`ACT`) — spec §5

**REQ-ACT-001** — Feed restores Tummy
Priority: Must · Verification: Test
The system shall restore the Tummy stat to 10 when the player presses the Feed (🐟) button.
*Feature:* `feeding.feature` → *Scenario:* "Feed action restores Tummy stat to full"

**REQ-ACT-002** — Play restores Happy and depletes Energy
Priority: Must · Verification: Test
The system shall increase the Happy stat and decrease the Energy stat when the player presses the Play (🎾)
button.
*Feature:* `playing.feature` → *Scenario:* "Play action restores Happy stat and depletes Energy"

**REQ-ACT-003** — Sleep restores Energy over time
Priority: Must · Verification: Test
The system shall restore the Energy stat gradually, over time, while the cat is in the Sleeping state,
following a Sleep (😴) button press.
*Feature:* `sleeping.feature` → *Scenario:* "Sleep action restores Energy over time"

**REQ-ACT-004** — Actions always available
Priority: Must · Verification: Demonstration
The system shall display all three action buttons (Feed, Play, Sleep) at all times, each large, clearly
labelled, and paired with an emoji.
*Feature:* `ui.feature` → *Scenario:* "Action buttons are visible on every screen"

---

### 2.4 Animations (`ANIM`) — spec §6

**REQ-ANIM-001** — Idle animation
Priority: Must · Verification: Test
The system shall play `idle.gif` on loop as the default state animation.
*Feature:* `state_machine.feature` → *Scenario:* "Idle state plays looping idle animation"

**REQ-ANIM-002** — Meow animation
Priority: Must · Verification: Test
The system shall play `meow.gif` on loop while the cat is in the Meowing state.
*Feature:* `feeding.feature` → *Scenario:* "Tummy critical plays meow animation"

**REQ-ANIM-003** — Falling-asleep animation
Priority: Must · Verification: Test
The system shall play `falling_asleep.gif` once when the Sleep action is triggered, then transition to the
Sleeping state.
*Feature:* `sleeping.feature` → *Scenario:* "Sleep pressed plays falling-asleep animation once"

**REQ-ANIM-004** — Sleeping animation
Priority: Must · Verification: Test
The system shall play `sleeping.gif` on loop while the cat is in the Sleeping state.
*Feature:* `sleeping.feature` → *Scenario:* "Sleeping state plays looping sleeping animation"

**REQ-ANIM-005** — Waking-up animation
Priority: Must · Verification: Test
The system shall play `waking_up.gif` once when Energy is restored, then transition to the Idle state.
*Feature:* `sleeping.feature` → *Scenario:* "Energy restored plays waking-up animation once, then returns to idle"

**REQ-ANIM-006** — Eating animation
Priority: Should · Verification: Test
The system shall play `eating.gif` when the Feed action is used.
*Feature:* `feeding.feature` → *Scenario:* "Feed action plays eating animation"

**REQ-ANIM-007** — Playing animation
Priority: Should · Verification: Test
The system shall play `playing.gif` when the Play action is used.
*Feature:* `playing.feature` → *Scenario:* "Play action plays playing animation"

**REQ-ANIM-008** — Sad animation
Priority: Should · Verification: Test
The system shall play `sad.gif` when the Happy stat is critical (see REQ-STAT-007).
*Feature:* `playing.feature` → *Scenario:* "Happy critical plays sad animation"

**REQ-ANIM-009** — Sleepy idle animation
Priority: Should · Verification: Test
The system shall play `sleepy_idle.gif` as an idle variation when the Energy stat is low (see REQ-STAT-008).
*Feature:* `sleeping.feature` → *Scenario:* "Energy low plays sleepy idle variation"

---

### 2.5 Sound (`AUD`) — spec §7

**REQ-AUD-001** — Meow sound
Priority: Should · Verification: Test
The system shall play the recorded meow sound when the Tummy stat reaches critical level.
*Feature:* `feeding.feature` → *Scenario:* "Tummy critical plays meow sound"

**REQ-AUD-002** — Happy sound
Priority: Should · Verification: Test
The system shall play the happy sound when the Play action is used.
*Feature:* `playing.feature` → *Scenario:* "Play action plays happy sound"

**REQ-AUD-003** — Eating sound
Priority: Should · Verification: Test
The system shall play the eating sound when the Feed action is used.
*Feature:* `feeding.feature` → *Scenario:* "Feed action plays eating sound"

**REQ-AUD-004** — Silence during sleep
Priority: Should · Verification: Test
The system shall play no sound effects (ambient/silence only) while the cat is in the Sleeping state.
*Feature:* `sleeping.feature` → *Scenario:* "No sound effects play during sleep"

---

### 2.6 UI Layout (`UI`) — spec §8

**REQ-UI-001** — Cat name displayed
Priority: Must · Verification: Demonstration
The system shall display the cat's name prominently at the top of the screen at all times during play.
*Feature:* `ui.feature` → *Scenario:* "Cat name is shown at the top of the screen"

**REQ-UI-002** — Cat sprite centred
Priority: Must · Verification: Demonstration
The system shall display the animated cat sprite, scaled up, in the centre of the screen on a Canvas widget.
*Feature:* `ui.feature` → *Scenario:* "Cat sprite is shown centred on screen"

**REQ-UI-003** — Stat bars displayed
Priority: Must · Verification: Demonstration
The system shall display three horizontal, colour-coded stat bars (🐟 Tummy, ⭐ Happy, 💤 Energy) at the
bottom of the screen, each labelled with its emoji and name.
*Feature:* `ui.feature` → *Scenario:* "Stat bars are shown at the bottom of the screen"

---

### 2.7 State Machine (`SM`) — spec §9

**REQ-SM-001** — Idle → Meowing
Priority: Must · Verification: Test
The system shall transition the cat from Idle to Meowing when the Tummy stat becomes critical.
*Feature:* `state_machine.feature` → *Scenario:* "Idle transitions to Meowing when Tummy critical"

**REQ-SM-002** — Idle → Falling Asleep
Priority: Must · Verification: Test
The system shall transition the cat from Idle to Falling Asleep when the Sleep button is pressed.
*Feature:* `state_machine.feature` → *Scenario:* "Idle transitions to Falling Asleep when Sleep pressed"

**REQ-SM-003** — Meowing → Idle
Priority: Must · Verification: Test
The system shall transition the cat from Meowing back to Idle once the Tummy stat is restored above the
critical threshold.
*Feature:* `feeding.feature` → *Scenario:* "Meowing returns to Idle once Tummy is restored"

**REQ-SM-004** — Falling Asleep → Sleeping
Priority: Must · Verification: Test
The system shall transition the cat from Falling Asleep to Sleeping automatically once the falling-asleep
animation completes.
*Feature:* `sleeping.feature` → *Scenario:* "Falling Asleep transitions to Sleeping on animation completion"

**REQ-SM-005** — Sleeping → Waking Up
Priority: Must · Verification: Test
The system shall transition the cat from Sleeping to Waking Up once the Energy stat is restored.
*Feature:* `sleeping.feature` → *Scenario:* "Sleeping transitions to Waking Up when Energy restored"

**REQ-SM-006** — Waking Up → Idle
Priority: Must · Verification: Test
The system shall transition the cat from Waking Up back to Idle automatically once the waking-up animation
completes.
*Feature:* `sleeping.feature` → *Scenario:* "Waking Up transitions to Idle on animation completion"

> **Gap in source spec:** §9's state table lists "Playing" as a transition target from Idle ("Play pressed")
> but defines no row of its own (no animation, no exit transition back to Idle). There is currently no
> `REQ-SM` entry for entering/exiting a Playing *state* — only the stat effects of the Play *action*
> (REQ-ACT-002, REQ-STAT-004) are specified. See Open Questions (§4) before writing `state_machine.feature`
> scenarios that touch Playing.

---

### 2.8 Non-Functional (`NFR`) — spec §2, §6

**REQ-NFR-001** — Technology stack
Priority: Must · Verification: Inspection
The system shall be implemented in Python 3.12 using Tkinter for the UI, Pillow for image handling, and
pygame.mixer for audio, per spec §2.

**REQ-NFR-002** — Crisp pixel-art scaling
Priority: Must · Verification: Inspection
The system shall scale all 32×32 sprites 3–4x using nearest-neighbour resampling so pixel art renders
crisply, not blurred.

**REQ-NFR-003** — Accessible for young players
Priority: Must · Verification: Demonstration
The system's buttons and on-screen text shall be large and clearly labelled, suitable for use by young
children.

---

## 3. Requirements Traceability Matrix (RTM)

| ID | Title | Priority | Feature file | Status |
|---|---|---|---|---|
| REQ-ONB-001 | Cat variant selection | Must | onboarding.feature | Not Started |
| REQ-ONB-002 | Cat name entry | Must | onboarding.feature | Not Started |
| REQ-ONB-003 | Start begins the game | Must | onboarding.feature | Not Started |
| REQ-STAT-001 | Stats initialise at maximum | Must | stats.feature | Not Started |
| REQ-STAT-002 | Tummy depletes while idle | Must | stats.feature | Not Started |
| REQ-STAT-003 | Happy depletes slower than Tummy | Must | stats.feature | Not Started |
| REQ-STAT-004 | Energy depletes while playing | Must | playing.feature | Not Started |
| REQ-STAT-005 | Stat bar colour reflects level | Must | stats.feature | Not Started |
| REQ-STAT-006 | Tummy critical threshold | Must | feeding.feature | Not Started |
| REQ-STAT-007 | Happy critical threshold | Should | playing.feature | Not Started |
| REQ-STAT-008 | Energy critical threshold | Should | sleeping.feature | Not Started |
| REQ-ACT-001 | Feed restores Tummy | Must | feeding.feature | Not Started |
| REQ-ACT-002 | Play restores Happy, depletes Energy | Must | playing.feature | Not Started |
| REQ-ACT-003 | Sleep restores Energy over time | Must | sleeping.feature | Not Started |
| REQ-ACT-004 | Actions always available | Must | ui.feature | Not Started |
| REQ-ANIM-001 | Idle animation | Must | state_machine.feature | Not Started |
| REQ-ANIM-002 | Meow animation | Must | feeding.feature | Not Started |
| REQ-ANIM-003 | Falling-asleep animation | Must | sleeping.feature | Not Started |
| REQ-ANIM-004 | Sleeping animation | Must | sleeping.feature | Not Started |
| REQ-ANIM-005 | Waking-up animation | Must | sleeping.feature | Not Started |
| REQ-ANIM-006 | Eating animation | Should | feeding.feature | Not Started |
| REQ-ANIM-007 | Playing animation | Should | playing.feature | Not Started |
| REQ-ANIM-008 | Sad animation | Should | playing.feature | Not Started |
| REQ-ANIM-009 | Sleepy idle animation | Should | sleeping.feature | Not Started |
| REQ-AUD-001 | Meow sound | Should | feeding.feature | Not Started |
| REQ-AUD-002 | Happy sound | Should | playing.feature | Not Started |
| REQ-AUD-003 | Eating sound | Should | feeding.feature | Not Started |
| REQ-AUD-004 | Silence during sleep | Should | sleeping.feature | Not Started |
| REQ-UI-001 | Cat name displayed | Must | ui.feature | Not Started |
| REQ-UI-002 | Cat sprite centred | Must | ui.feature | Not Started |
| REQ-UI-003 | Stat bars displayed | Must | ui.feature | Not Started |
| REQ-SM-001 | Idle → Meowing | Must | state_machine.feature | Not Started |
| REQ-SM-002 | Idle → Falling Asleep | Must | state_machine.feature | Not Started |
| REQ-SM-003 | Meowing → Idle | Must | feeding.feature | Not Started |
| REQ-SM-004 | Falling Asleep → Sleeping | Must | sleeping.feature | Not Started |
| REQ-SM-005 | Sleeping → Waking Up | Must | sleeping.feature | Not Started |
| REQ-SM-006 | Waking Up → Idle | Must | sleeping.feature | Not Started |
| REQ-NFR-001 | Technology stack | Must | — (inspection) | Not Started |
| REQ-NFR-002 | Crisp pixel-art scaling | Must | — (inspection) | Not Started |
| REQ-NFR-003 | Accessible for young players | Must | — (demonstration) | Not Started |

---

## 4. Open Questions

Items referenced above that need a decision with the Chief Product Owner before they can become firm,
testable requirements:

1. **Playing state** (§9 gap, see REQ-SM-006 note) — does entering Play define a distinct game *state*
   (like Sleeping does), with its own animation and an exit transition back to Idle? Or is Play only a
   momentary action that adjusts stats without changing state?
2. **Happy-critical and Energy-critical reactions** (REQ-STAT-007, REQ-STAT-008) — these currently only
   specify an animation (spec §6.2), not a formal state-machine entry or exit condition. Do they need one,
   or are they visual-only overlays on top of Idle?
3. **Walking animation** — `walking.gif` referenced in `project.md` but has no trigger or requirement
   defined yet; not included in this document until scoped.
4. **Background transitions** — background-swapping logic (`project.md`) is not yet designed; once it is,
   it should get its own `REQ-UI` or `REQ-SM` entries.

---

## 5. Change Log

| Date | Change |
|---|---|
| 2026-07-13 | v1.0 — initial requirements set drafted from `virtual_pet_spec.docx` §3–§9 |
