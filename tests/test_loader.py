import numpy as np

from asciifier.loader import load_image


def test_load_returns_rgb_ndarray(fixtures_dir):
    img = load_image(fixtures_dir / "small_rgb.png")
    assert img.shape == (4, 4, 3)
    assert img.dtype == np.uint8
    np.testing.assert_array_equal(img[0, 0], [255, 0, 0])


def test_load_missing_file_raises(tmp_path):
    import pytest
    with pytest.raises(FileNotFoundError):
        load_image(tmp_path / "nope.png")


def test_load_strips_alpha(fixtures_dir, tmp_path):
    from PIL import Image
    p = tmp_path / "rgba.png"
    Image.new("RGBA", (2, 2), (10, 20, 30, 128)).save(p)
    img = load_image(p)
    assert img.shape == (2, 2, 3)
