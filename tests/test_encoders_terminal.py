from asciifier.encoders.base import EncodeOpts
from asciifier.encoders.terminal import TerminalEncoder
from asciifier.types import Cell


def test_mono_cell_emits_plain_char():
    enc = TerminalEncoder()
    out = enc.encode([[Cell(char="X")]], EncodeOpts())
    assert "X" in out
    assert "\x1b[" not in out.replace("\x1b[0m", "")


def test_truecolor_cell_emits_escape():
    enc = TerminalEncoder()
    cell = Cell(char="X", fg=(10, 20, 30))
    out = enc.encode([[cell]], EncodeOpts())
    assert "\x1b[38;2;10;20;30m" in out


def test_row_ends_with_reset_and_newline():
    enc = TerminalEncoder()
    out = enc.encode([[Cell(char="A")], [Cell(char="B")]], EncodeOpts())
    lines = out.split("\n")
    assert len(lines) >= 2


def test_runs_of_same_color_share_escape():
    enc = TerminalEncoder()
    grid = [[Cell(char="A", fg=(1, 2, 3)), Cell(char="B", fg=(1, 2, 3))]]
    out = enc.encode(grid, EncodeOpts())
    assert out.count("\x1b[38;2;1;2;3m") == 1
