import numpy as np

from asciifier.resample import compute_target_size, resample


def test_compute_target_size_fits_terminal():
    cols, rows = compute_target_size(
        src_w=100, src_h=50, term_cols=80, term_lines=24, char_aspect=0.5, scale=1.0
    )
    assert cols <= 80 and rows <= 24


def test_compute_target_size_scale_halves():
    cols, rows = compute_target_size(
        src_w=100, src_h=50, term_cols=80, term_lines=24, char_aspect=0.5, scale=0.5
    )
    cols_full, rows_full = compute_target_size(
        src_w=100, src_h=50, term_cols=80, term_lines=24, char_aspect=0.5, scale=1.0
    )
    assert cols == max(1, cols_full // 2)
    assert rows == max(1, rows_full // 2)


def test_compute_target_size_explicit_width_derives_height():
    cols, rows = compute_target_size(
        src_w=100, src_h=50, term_cols=80, term_lines=24, char_aspect=0.5,
        scale=1.0, width=40,
    )
    assert cols == 40
    assert rows == 10


def test_resample_returns_target_shape():
    src = np.zeros((50, 100, 3), dtype=np.uint8)
    out = resample(src, cols=20, rows=10)
    assert out.shape == (10, 20, 3)
    assert out.dtype == np.uint8
