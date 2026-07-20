from enum import Enum, auto


class CatState(Enum):
    IDLE = auto()
    MEOWING = auto()
    FALLING_ASLEEP = auto()
    SLEEPING = auto()
    WAKING_UP = auto()


class CatEvent(Enum):
    PRESS_SLEEP = auto()
    ANIMATION_COMPLETE = auto()
    ENERGY_RESTORED = auto()


# Mirrors the state table in virtual_pet_spec.docx §9. Only entries with a
# supporting trigger implemented so far are listed (e.g. Tummy-critical
# detection isn't wired up yet, so no Meowing transitions exist here).
TRANSITIONS: dict[tuple[CatState, CatEvent], CatState] = {
    (CatState.IDLE, CatEvent.PRESS_SLEEP): CatState.FALLING_ASLEEP,
    (CatState.FALLING_ASLEEP, CatEvent.ANIMATION_COMPLETE): CatState.SLEEPING,
    (CatState.SLEEPING, CatEvent.ENERGY_RESTORED): CatState.WAKING_UP,
    (CatState.WAKING_UP, CatEvent.ANIMATION_COMPLETE): CatState.IDLE,
}
