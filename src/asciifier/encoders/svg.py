from html import escape

from asciifier.encoders.base import EncodeOpts
from asciifier.types import Grid

CELL_W = 8
CELL_H = 16


def _hex(rgb: tuple[int, int, int]) -> str:
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


class SvgEncoder:
    def encode(self, grid: Grid, opts: EncodeOpts) -> str:
        rows = len(grid)
        cols = max((len(r) for r in grid), default=0)
        w = cols * CELL_W
        h = rows * CELL_H
        parts: list[str] = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="JetBrains Mono, Menlo, Consolas, monospace" font-size="{CELL_H}">',
            '<rect width="100%" height="100%" fill="#000"/>',
        ]
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                px = x * CELL_W
                py = y * CELL_H
                if opts.include_bg and cell.bg is not None:
                    parts.append(
                        f'<rect x="{px}" y="{py}" width="{CELL_W}" height="{CELL_H}" fill="{_hex(cell.bg)}"/>'
                    )
                fg = _hex(cell.fg) if cell.fg is not None else "#fff"
                parts.append(
                    f'<text x="{px}" y="{py + CELL_H - 3}" fill="{fg}" xml:space="preserve">{escape(cell.char)}</text>'
                )
        parts.append("</svg>")
        return "".join(parts)
