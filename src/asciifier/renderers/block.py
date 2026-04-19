import numpy as np
from numpy.typing import NDArray

from asciifier.color import quantize
from asciifier.renderers.base import RenderOpts
from asciifier.types import Cell, Grid

UPPER_HALF = "\u2580"


class BlockRenderer:
    char_aspect: float = 1.0

    def render(self, img: NDArray[np.uint8], opts: RenderOpts) -> Grid:
        h, w, _ = img.shape
        if h % 2 == 1:
            img = np.concatenate([img, img[-1:]], axis=0)
            h += 1
        top = img[0::2]
        bot = img[1::2]
        grid: Grid = []
        for y in range(h // 2):
            row: list[Cell] = []
            for x in range(w):
                t = tuple(int(v) for v in top[y, x])
                b = tuple(int(v) for v in bot[y, x])
                fg = quantize(t, opts.color_mode)
                bg = quantize(b, opts.color_mode)
                row.append(Cell(char=UPPER_HALF, fg=fg, bg=bg))
            grid.append(row)
        return grid
