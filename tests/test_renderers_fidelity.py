import numpy as np

from asciifier.renderers.base import RenderOpts
from asciifier.renderers.fidelity import FidelityRenderer


def test_solid_white_picks_full_block_like_glyph():
    img = np.full((16, 8, 3), 255, dtype=np.uint8)
    grid = FidelityRenderer().render(img, RenderOpts(color_mode="truecolor"))
    assert len(grid) == 1 and len(grid[0]) == 1
    assert grid[0][0].fg == (255, 255, 255)


def test_solid_black_picks_empty_like_glyph():
    img = np.zeros((16, 8, 3), dtype=np.uint8)
    grid = FidelityRenderer().render(img, RenderOpts(color_mode="truecolor"))
    assert grid[0][0].fg == (0, 0, 0)


def test_half_split_image_produces_reasonable_split():
    img = np.zeros((16, 8, 3), dtype=np.uint8)
    img[:8, :] = 255
    grid = FidelityRenderer().render(img, RenderOpts(color_mode="truecolor"))
    cell = grid[0][0]
    assert cell.fg == (255, 255, 255)
    assert cell.bg == (0, 0, 0)
