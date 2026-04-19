from dataclasses import dataclass
from typing import Protocol

from asciifier.types import Grid


@dataclass(frozen=True, slots=True)
class EncodeOpts:
    include_bg: bool = True


class Encoder(Protocol):
    def encode(self, grid: Grid, opts: EncodeOpts) -> str: ...
