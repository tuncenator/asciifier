import numpy as np
from numpy.typing import NDArray

from asciifier.color import quantize
from asciifier.renderers.base import RenderOpts
from asciifier.types import Cell, Grid

DOT_BITS: list[tuple[int, int, int]] = [
    (0, 0, 0), (1, 0, 1), (2, 0, 2), (3, 0, 6),
    (0, 1, 3), (1, 1, 4), (2, 1, 5), (3, 1, 7),
]


class BrailleRenderer:
    char_aspect: float = 0.5
    pixel_cell_size: tuple[int, int] = (2, 4)

    def render(self, img: NDArray[np.uint8], opts: RenderOpts) -> Grid:
        if opts.invert:
            img = 255 - img
        h, w, _ = img.shape
        pad_h = (4 - h % 4) % 4
        pad_w = (2 - w % 2) % 2
        if pad_h or pad_w:
            img = np.pad(img, ((0, pad_h), (0, pad_w), (0, 0)), mode="edge")
            h, w = img.shape[:2]

        lum = (0.2126 * img[..., 0] + 0.7152 * img[..., 1] + 0.0722 * img[..., 2]) / 255.0
        on = lum > opts.threshold

        out_rows = h // 4
        out_cols = w // 2
        grid: Grid = []
        for cy in range(out_rows):
            row: list[Cell] = []
            for cx in range(out_cols):
                y0, x0 = cy * 4, cx * 2
                mask = 0
                r_sum = g_sum = b_sum = cnt = 0
                for dy, dx, bit in DOT_BITS:
                    if on[y0 + dy, x0 + dx]:
                        mask |= 1 << bit
                        r_sum += int(img[y0 + dy, x0 + dx, 0])
                        g_sum += int(img[y0 + dy, x0 + dx, 1])
                        b_sum += int(img[y0 + dy, x0 + dx, 2])
                        cnt += 1
                ch = chr(0x2800 + mask)
                fg = None
                if opts.color_mode != "mono" and cnt > 0:
                    fg = quantize((r_sum // cnt, g_sum // cnt, b_sum // cnt), opts.color_mode)
                row.append(Cell(char=ch, fg=fg, bg=None))
            grid.append(row)
        return grid
