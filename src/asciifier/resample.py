import numpy as np
from numpy.typing import NDArray
from PIL import Image


def compute_target_size(
    *,
    src_w: int,
    src_h: int,
    term_cols: int,
    term_lines: int,
    char_aspect: float,
    scale: float,
    width: int | None = None,
    height: int | None = None,
) -> tuple[int, int]:
    """Return (cols, rows) for the character grid.

    char_aspect = cell pixel width / cell pixel height (text ~0.5, braille ~0.25).
    """
    if width is not None and height is not None:
        return width, height
    if width is not None:
        rows = max(1, round(width * (src_h / src_w) * char_aspect))
        return width, rows
    if height is not None:
        cols = max(1, round(height * (src_w / src_h) / char_aspect))
        return cols, height

    max_cols = max(1, term_cols)
    max_rows = max(1, term_lines - 1)
    src_ratio = (src_w / src_h) / char_aspect
    fit_cols = max_cols
    fit_rows = max(1, round(fit_cols / src_ratio))
    if fit_rows > max_rows:
        fit_rows = max_rows
        fit_cols = max(1, round(fit_rows * src_ratio))

    scaled_cols = max(1, int(fit_cols * scale))
    scaled_rows = max(1, int(fit_rows * scale))
    return scaled_cols, scaled_rows


def resample(img: NDArray[np.uint8], *, cols: int, rows: int) -> NDArray[np.uint8]:
    pil = Image.fromarray(img)
    resized = pil.resize((cols, rows), Image.Resampling.LANCZOS)
    return np.asarray(resized, dtype=np.uint8)
