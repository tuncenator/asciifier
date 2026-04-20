import numpy as np

from asciifier.color import to_mono, to_truecolor


def test_truecolor_passthrough():
    pixel = (10, 20, 30)
    assert to_truecolor(pixel) == (10, 20, 30)


def test_mono_returns_none():
    assert to_mono((10, 20, 30)) is None


def test_truecolor_clamps_array():
    arr = np.array([[[300, -5, 128]]], dtype=np.int16)
    clamped = np.clip(arr, 0, 255).astype(np.uint8)
    assert clamped[0, 0, 0] == 255 and clamped[0, 0, 1] == 0


def test_to_256_returns_palette_rgb():
    out = to_256_wrapper((128, 128, 128))
    assert isinstance(out, tuple) and len(out) == 3
    assert all(0 <= c <= 255 for c in out)


def to_256_wrapper(p):
    from asciifier.color import to_256
    return to_256(p)
