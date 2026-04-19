import numpy as np
from numpy.typing import NDArray

from asciifier.color import quantize
from asciifier.renderers.base import RenderOpts
from asciifier.types import Cell, Grid


class LuminanceRenderer:
    char_aspect: float = 0.5

    def render(self, img: NDArray[np.uint8], opts: RenderOpts) -> Grid:
        r = img[..., 0].astype(np.float32)
        g = img[..., 1].astype(np.float32)
        b = img[..., 2].astype(np.float32)
        lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
        if opts.invert:
            lum = 255.0 - lum

        ramp = opts.ramp
        n = len(ramp) - 1
        idx = np.clip((lum / 255.0 * n).round().astype(np.int32), 0, n)

        h, w = idx.shape
        grid: Grid = []
        for y in range(h):
            row: list[Cell] = []
            for x in range(w):
                ch = ramp[int(idx[y, x])]
                fg = quantize(tuple(int(v) for v in img[y, x]), opts.color_mode)
                row.append(Cell(char=ch, fg=fg, bg=None))
            grid.append(row)
        return grid
