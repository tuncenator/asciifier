import numpy as np

from asciifier.renderers.base import RenderOpts
from asciifier.renderers.edge import EdgeRenderer


def test_uniform_image_no_edges_falls_back_to_luminance():
    img = np.full((8, 8, 3), 128, dtype=np.uint8)
    grid = EdgeRenderer().render(img, RenderOpts(color_mode="mono"))
    for row in grid:
        for cell in row:
            assert cell.char in " .:-=+*#%@"


def test_vertical_edge_produces_vertical_char():
    img = np.zeros((8, 8, 3), dtype=np.uint8)
    img[:, 4:] = 255
    grid = EdgeRenderer().render(img, RenderOpts(color_mode="mono"))
    chars = {grid[y][x].char for y in range(1, 7) for x in (3, 4)}
    assert "|" in chars
