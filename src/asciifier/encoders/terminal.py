from asciifier.encoders.base import EncodeOpts
from asciifier.types import Grid

RESET = "\x1b[0m"


def _fg_escape(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f"\x1b[38;2;{r};{g};{b}m"


def _bg_escape(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f"\x1b[48;2;{r};{g};{b}m"


class TerminalEncoder:
    def encode(self, grid: Grid, opts: EncodeOpts) -> str:
        out: list[str] = []
        for row in grid:
            last_fg: tuple[int, int, int] | None = None
            last_bg: tuple[int, int, int] | None = None
            for cell in row:
                if cell.fg != last_fg:
                    if cell.fg is None:
                        out.append("\x1b[39m")
                    else:
                        out.append(_fg_escape(cell.fg))
                    last_fg = cell.fg
                if opts.include_bg and cell.bg != last_bg:
                    if cell.bg is None:
                        out.append("\x1b[49m")
                    else:
                        out.append(_bg_escape(cell.bg))
                    last_bg = cell.bg
                out.append(cell.char)
            out.append(RESET + "\n")
        return "".join(out)
