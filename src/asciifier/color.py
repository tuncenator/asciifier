from typing import Literal

from asciifier.types import RGB

ColorMode = Literal["truecolor", "256", "mono"]


def to_truecolor(pixel: RGB) -> RGB:
    r, g, b = pixel
    return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))


def to_mono(pixel: RGB) -> None:
    return None


def quantize(pixel: RGB, mode: ColorMode) -> RGB | None:
    if mode == "truecolor":
        return to_truecolor(pixel)
    if mode == "256":
        return to_256(pixel)
    return to_mono(pixel)


def to_256(pixel: RGB) -> RGB:
    """Map RGB to the closest xterm 256-color entry, returning the palette RGB."""
    r, g, b = pixel
    levels = (0, 95, 135, 175, 215, 255)

    def nearest(v: int) -> int:
        return min(range(6), key=lambda i: abs(levels[i] - v))

    ri, gi, bi = nearest(r), nearest(g), nearest(b)
    cube_rgb = (levels[ri], levels[gi], levels[bi])
    cube_err = sum((cube_rgb[i] - pixel[i]) ** 2 for i in range(3))

    gray_levels = [8 + 10 * i for i in range(24)]
    gray_v = min(gray_levels, key=lambda v: abs(v - (r + g + b) // 3))
    gray_rgb = (gray_v, gray_v, gray_v)
    gray_err = sum((gray_rgb[i] - pixel[i]) ** 2 for i in range(3))

    return cube_rgb if cube_err <= gray_err else gray_rgb
