import numpy as np

from asciifier.renderers.base import RenderOpts
from asciifier.renderers.braille import BrailleRenderer


def test_all_black_is_empty_braille():
    img = np.zeros((4, 2, 3), dtype=np.uint8)
    grid = BrailleRenderer().render(img, RenderOpts(color_mode="mono"))
    assert len(grid) == 1 and len(grid[0]) == 1
    assert grid[0][0].char == "\u2800"


def test_all_white_is_full_braille():
    img = np.full((4, 2, 3), 255, dtype=np.uint8)
    grid = BrailleRenderer().render(img, RenderOpts(color_mode="mono"))
    assert grid[0][0].char == "\u28FF"


def test_output_shape_matches_2x4_subcell():
    img = np.zeros((8, 4, 3), dtype=np.uint8)
    grid = BrailleRenderer().render(img, RenderOpts(color_mode="mono"))
    assert len(grid) == 2 and len(grid[0]) == 2
