from pathlib import Path

from asciifier.encoders.base import EncodeOpts
from asciifier.encoders.png import PngEncoder
from asciifier.types import Cell


def test_png_written_to_disk(tmp_path: Path):
    out_path = tmp_path / "out.png"
    PngEncoder(out_path).encode([[Cell(char="X", fg=(255, 0, 0))]], EncodeOpts())
    assert out_path.exists() and out_path.stat().st_size > 0


def test_png_dimensions_match_grid(tmp_path: Path):
    from PIL import Image
    out_path = tmp_path / "out.png"
    grid = [[Cell(char="A") for _ in range(3)] for _ in range(2)]
    PngEncoder(out_path).encode(grid, EncodeOpts())
    with Image.open(out_path) as im:
        assert im.size == (3 * PngEncoder.CELL_W, 2 * PngEncoder.CELL_H)
