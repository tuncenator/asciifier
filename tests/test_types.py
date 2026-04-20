from asciifier.types import Cell, RGB


def test_rgb_is_tuple_of_three():
    c: RGB = (10, 20, 30)
    assert c == (10, 20, 30)


def test_cell_has_char_fg_bg():
    cell = Cell(char="X", fg=(255, 0, 0), bg=None)
    assert cell.char == "X"
    assert cell.fg == (255, 0, 0)
    assert cell.bg is None
