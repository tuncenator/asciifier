import numpy as np

from asciifier.renderers.base import RenderOpts
from asciifier.renderers.luminance import LuminanceRenderer


def _render(img, color_mode="mono", invert=False):
    r = LuminanceRenderer()
    return r.render(img, RenderOpts(color_mode=color_mode, invert=invert))


def test_all_black_maps_to_first_ramp_char():
    img = np.zeros((2, 2, 3), dtype=np.uint8)
    grid = _render(img)
    assert grid[0][0].char == " "
    assert grid[0][0].fg is None


def test_all_white_maps_to_last_ramp_char():
    img = np.full((2, 2, 3), 255, dtype=np.uint8)
    grid = _render(img)
    assert grid[0][0].char == "@"


def test_invert_flips():
    img = np.zeros((1, 1, 3), dtype=np.uint8)
    grid = _render(img, invert=True)
    assert grid[0][0].char == "@"


def test_color_mode_sets_fg():
    img = np.full((1, 1, 3), 128, dtype=np.uint8)
    img[0, 0] = [200, 50, 20]
    grid = _render(img, color_mode="truecolor")
    assert grid[0][0].fg == (200, 50, 20)


def test_output_dimensions_match_input():
    img = np.zeros((3, 5, 3), dtype=np.uint8)
    grid = _render(img)
    assert len(grid) == 3
    assert len(grid[0]) == 5
