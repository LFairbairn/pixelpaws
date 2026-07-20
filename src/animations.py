from dataclasses import dataclass

from src.cat_state import CatState


@dataclass(frozen=True)
class Animation:
    name: str
    loop: bool


# Mirrors the Animation column of the state table in virtual_pet_spec.docx §9.
ANIMATIONS: dict[CatState, Animation] = {
    CatState.IDLE: Animation("idle", loop=True),
    CatState.MEOWING: Animation("meow", loop=True),
    CatState.FALLING_ASLEEP: Animation("falling_asleep", loop=False),
    CatState.SLEEPING: Animation("sleeping", loop=True),
    CatState.WAKING_UP: Animation("waking_up", loop=False),
}
