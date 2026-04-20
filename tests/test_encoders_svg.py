from asciifier.encoders.base import EncodeOpts
from asciifier.encoders.svg import SvgEncoder
from asciifier.types import Cell


def test_svg_root_and_text_element():
    out = SvgEncoder().encode([[Cell(char="X", fg=(255, 0, 0))]], EncodeOpts())
    assert out.startswith("<?xml") or out.startswith("<svg")
    assert "<text" in out
    assert "#ff0000" in out.lower()


def test_svg_escapes_special_chars():
    out = SvgEncoder().encode([[Cell(char="<")]], EncodeOpts())
    assert "&lt;" in out
