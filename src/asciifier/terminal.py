import os
import shutil
from dataclasses import dataclass
from typing import Literal

ColorMode = Literal["truecolor", "256", "mono"]


@dataclass(frozen=True, slots=True)
class TerminalCaps:
    color: ColorMode
    columns: int
    lines: int


def detect() -> TerminalCaps:
    colorterm = os.environ.get("COLORTERM", "").lower()
    term = os.environ.get("TERM", "").lower()

    if colorterm in ("truecolor", "24bit"):
        color: ColorMode = "truecolor"
    elif "256color" in term:
        color = "256"
    elif term in ("", "dumb"):
        color = "mono"
    else:
        color = "mono"

    size = shutil.get_terminal_size(fallback=(80, 24))
    return TerminalCaps(color=color, columns=size.columns, lines=size.lines)
