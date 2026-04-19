from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

import numpy as np
from numpy.typing import NDArray

from asciifier.color import ColorMode
from asciifier.types import Grid


@dataclass(frozen=True, slots=True)
class RenderOpts:
    color_mode: ColorMode
    invert: bool = False
    ramp: str = " .:-=+*#%@"
    threshold: float = 0.5
    font_path: Path | None = None


class Renderer(Protocol):
    char_aspect: float

    def render(self, img: NDArray[np.uint8], opts: RenderOpts) -> Grid: ...
