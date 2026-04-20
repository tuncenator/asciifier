from html import escape

from asciifier.encoders.base import EncodeOpts
from asciifier.types import Grid

_PREAMBLE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>asciifier</title>
<style>
body { margin: 0; background: #000; }
pre { margin: 0; line-height: 1; font-family: 'JetBrains Mono', Menlo, Consolas, monospace; font-size: 12px; }
span { display: inline-block; white-space: pre; }
</style></head><body><pre>"""

_POSTAMBLE = "</pre></body></html>"


def _hex(rgb: tuple[int, int, int]) -> str:
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


class HtmlEncoder:
    def encode(self, grid: Grid, opts: EncodeOpts) -> str:
        parts: list[str] = [_PREAMBLE]
        for row in grid:
            for cell in row:
                styles: list[str] = []
                if cell.fg is not None:
                    styles.append(f"color:{_hex(cell.fg)}")
                if opts.include_bg and cell.bg is not None:
                    styles.append(f"background:{_hex(cell.bg)}")
                style_attr = f' style="{";".join(styles)}"' if styles else ""
                parts.append(f"<span{style_attr}>{escape(cell.char)}</span>")
            parts.append("\n")
        parts.append(_POSTAMBLE)
        return "".join(parts)
