from dataclasses import dataclass
from functools import lru_cache
from importlib.resources import files
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from PIL import Image, ImageDraw, ImageFont

CELL_W = 8
CELL_H = 16


def _bundled_font_path() -> Path:
    return Path(str(files("asciifier.fonts").joinpath("JetBrainsMono-Regular.ttf")))


def _candidate_chars() -> list[str]:
    chars: list[str] = []
    chars.extend(chr(c) for c in range(0x20, 0x7F))
    chars.extend(chr(c) for c in range(0xA1, 0x100))
    chars.extend(chr(c) for c in range(0x2500, 0x2580))
    chars.extend(chr(c) for c in range(0x2580, 0x25A0))
    chars.extend(chr(c) for c in range(0x2800, 0x2900))
    chars.extend(["\u2190", "\u2191", "\u2192", "\u2193", "\u2219", "\u2218", "\u221E", "\u2248"])
    return chars


@dataclass(frozen=True, slots=True)
class Atlas:
    chars: list[str]
    masks: NDArray[np.float32]
    cell_w: int
    cell_h: int


def _render_mask(font: ImageFont.FreeTypeFont, ch: str) -> NDArray[np.float32]:
    im = Image.new("L", (CELL_W, CELL_H), 0)
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), ch, fill=255, font=font)
    arr = np.asarray(im, dtype=np.float32) / 255.0
    return arr


@lru_cache(maxsize=4)
def _build_atlas(font_path: str, cell_w: int, cell_h: int) -> Atlas:
    chars = _candidate_chars()
    font = ImageFont.truetype(font_path, size=cell_h)
    masks = np.stack([_render_mask(font, c) for c in chars], axis=0)
    return Atlas(chars=chars, masks=masks, cell_w=cell_w, cell_h=cell_h)


def default_atlas() -> Atlas:
    return _build_atlas(str(_bundled_font_path()), CELL_W, CELL_H)


def atlas_from_font(path: Path) -> Atlas:
    return _build_atlas(str(path), CELL_W, CELL_H)
