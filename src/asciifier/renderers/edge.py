import numpy as np
from numpy.typing import NDArray

from asciifier.color import quantize
from asciifier.renderers.base import RenderOpts
from asciifier.types import Cell, Grid

EDGE_CHARS = {0: "|", 1: "\\", 2: "-", 3: "/"}

_SOBEL_X = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
_SOBEL_Y = _SOBEL_X.T


def _conv2(a: NDArray[np.float32], k: NDArray[np.float32]) -> NDArray[np.float32]:
    pad = np.pad(a, 1, mode="edge")
    h, w = a.shape
    out = np.zeros_like(a)
    for dy in range(3):
        for dx in range(3):
            out += k[dy, dx] * pad[dy:dy + h, dx:dx + w]
    return out


class EdgeRenderer:
    char_aspect: float = 0.5

    def render(self, img: NDArray[np.uint8], opts: RenderOpts) -> Grid:
        lum = (0.2126 * img[..., 0] + 0.7152 * img[..., 1] + 0.0722 * img[..., 2]).astype(np.float32)
        gx = _conv2(lum, _SOBEL_X)
        gy = _conv2(lum, _SOBEL_Y)
        mag = np.hypot(gx, gy)
        ang = np.arctan2(gy, gx)

        max_mag = float(mag.max()) if mag.size else 0.0
        threshold = opts.threshold * max_mag if max_mag > 0 else float("inf")

        ramp = opts.ramp
        n = len(ramp) - 1
        lum_idx = np.clip((lum / 255.0 * n).round().astype(np.int32), 0, n)

        h, w = lum.shape
        grid: Grid = []
        for y in range(h):
            row: list[Cell] = []
            for x in range(w):
                if mag[y, x] >= threshold:
                    a = ang[y, x]
                    bucket = int((a % np.pi) / (np.pi / 4)) % 4
                    ch = EDGE_CHARS[bucket]
                else:
                    ch = ramp[int(lum_idx[y, x])]
                fg = quantize(tuple(int(v) for v in img[y, x]), opts.color_mode)
                row.append(Cell(char=ch, fg=fg, bg=None))
            grid.append(row)
        return grid
