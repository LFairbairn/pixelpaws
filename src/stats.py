from dataclasses import dataclass

MIN_VALUE = 0.0
MAX_VALUE = 10.0


@dataclass
class Stat:
    """A single cat stat (Tummy/Happy/Energy), clamped to [MIN_VALUE, MAX_VALUE]."""

    value: float = MAX_VALUE

    def __post_init__(self) -> None:
        self._clamp()

    def restore(self, amount: float) -> None:
        self.value += amount
        self._clamp()

    def deplete(self, amount: float) -> None:
        self.value -= amount
        self._clamp()

    def _clamp(self) -> None:
        self.value = max(MIN_VALUE, min(MAX_VALUE, self.value))

    @property
    def is_full(self) -> bool:
        return self.value >= MAX_VALUE

    @property
    def is_critical(self) -> bool:
        return self.value < 3

    @property
    def colour(self) -> str:
        if self.value >= 7:
            return "green"
        if self.value >= 4:
            return "yellow"
        return "red"
