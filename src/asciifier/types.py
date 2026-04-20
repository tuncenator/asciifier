from dataclasses import dataclass
from typing import TypeAlias

RGB: TypeAlias = tuple[int, int, int]


@dataclass(frozen=True, slots=True)
class Cell:
    char: str
    fg: RGB | None = None
    bg: RGB | None = None


Grid: TypeAlias = list[list[Cell]]
