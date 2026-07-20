from src.animations import ANIMATIONS, Animation
from src.cat_state import TRANSITIONS, CatEvent, CatState
from src.stats import Stat

# Placeholder balance value: 1 Energy point restored per 5 minutes asleep.
# Not yet specified by the product owner — tune once playtested.
SLEEP_ENERGY_RESTORE_PER_SECOND = 1.0 / 300.0


class Cat:
    def __init__(self, name: str):
        self.name = name
        self.tummy = Stat()
        self.happy = Stat()
        self.energy = Stat()
        self.sounds_played: list[str] = []
        self.last_completed_animation: Animation | None = None

        self.state = CatState.IDLE
        self.current_animation: Animation = ANIMATIONS[self.state]

    def set_state(self, state: CatState) -> None:
        """Force the cat into a given state, e.g. for test setup or loading a save."""
        self.state = state
        self.current_animation = ANIMATIONS[state]

    def press_sleep(self) -> None:
        self._handle(CatEvent.PRESS_SLEEP)

    def on_animation_complete(self) -> None:
        self.last_completed_animation = self.current_animation
        self._handle(CatEvent.ANIMATION_COMPLETE)

    def restore_energy(self, amount: float) -> None:
        self.energy.restore(amount)
        if self.energy.is_full:
            self._handle(CatEvent.ENERGY_RESTORED)

    def tick(self, seconds: float) -> None:
        """Advance game time. Callers control how much time passes — production
        code derives it from the real clock, tests pass synthetic values."""
        if self.state is CatState.SLEEPING:
            self.restore_energy(seconds * SLEEP_ENERGY_RESTORE_PER_SECOND)

    def _handle(self, event: CatEvent) -> None:
        next_state = TRANSITIONS.get((self.state, event))
        if next_state is not None:
            self.set_state(next_state)
