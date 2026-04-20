import numpy as np

from asciifier.renderers.base import RenderOpts
from asciifier.renderers.block import BlockRenderer


def test_solid_color_input_emits_full_block():
    img = np.full((4, 4, 3), 128, dtype=np.uint8)
    grid = BlockRenderer().render(img, RenderOpts(color_mode="truecolor"))
    assert len(grid) == 2
    assert len(grid[0]) == 4
    assert grid[0][0].fg == (128, 128, 128)


def test_top_bright_bottom_dark_emits_upper_half_block():
    img = np.zeros((2, 1, 3), dtype=np.uint8)
    img[0, 0] = [255, 255, 255]
    grid = BlockRenderer().render(img, RenderOpts(color_mode="truecolor"))
    cell = grid[0][0]
    assert cell.char == "\u2580"
    assert cell.fg == (255, 255, 255)
    assert cell.bg == (0, 0, 0)
