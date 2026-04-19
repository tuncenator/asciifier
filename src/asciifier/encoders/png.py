from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from asciifier.encoders.base import EncodeOpts
from asciifier.glyphs import _bundled_font_path
from asciifier.types import Grid


class PngEncoder:
    CELL_W = 8
    CELL_H = 16

    def __init__(self, out_path: Path):
        self.out_path = out_path

    def encode(self, grid: Grid, opts: EncodeOpts) -> str:
        rows = len(grid)
        cols = max((len(r) for r in grid), default=0)
        w = cols * self.CELL_W
        h = rows * self.CELL_H
        img = Image.new("RGB", (w, h), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(str(_bundled_font_path()), size=self.CELL_H)
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                px, py = x * self.CELL_W, y * self.CELL_H
                if opts.include_bg and cell.bg is not None:
                    draw.rectangle(
                        [px, py, px + self.CELL_W - 1, py + self.CELL_H - 1], fill=cell.bg
                    )
                fg = cell.fg if cell.fg is not None else (255, 255, 255)
                draw.text((px, py), cell.char, fill=fg, font=font)
        img.save(self.out_path, format="PNG")
        return str(self.out_path)
