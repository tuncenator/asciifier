from asciifier.encoders.base import EncodeOpts
from asciifier.encoders.html import HtmlEncoder
from asciifier.types import Cell


def test_html_is_self_contained_document():
    out = HtmlEncoder().encode([[Cell(char="X", fg=(10, 20, 30))]], EncodeOpts())
    assert out.startswith("<!DOCTYPE html>")
    assert "<pre" in out
    assert "color:#0a141e" in out.lower()


def test_escapes_html_special_chars():
    out = HtmlEncoder().encode([[Cell(char="<")]], EncodeOpts())
    assert "&lt;" in out
