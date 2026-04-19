import argparse
import sys
from pathlib import Path

from asciifier.color import ColorMode
from asciifier.encoders.base import EncodeOpts
from asciifier.encoders.terminal import TerminalEncoder
from asciifier.loader import load_image
from asciifier.renderers.base import RenderOpts
from asciifier.renderers.block import BlockRenderer
from asciifier.renderers.braille import BrailleRenderer
from asciifier.renderers.edge import EdgeRenderer
from asciifier.renderers.luminance import LuminanceRenderer
from asciifier.resample import compute_target_size, resample
from asciifier.terminal import detect

RENDERERS: dict[str, type] = {
    "luminance": LuminanceRenderer,
    "block": BlockRenderer,
    "braille": BrailleRenderer,
    "edge": EdgeRenderer,
}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="asciifier", description="Image to character-art.")
    p.add_argument("image", type=Path, help="input image path")
    p.add_argument("--mode", choices=["fidelity", "luminance", "edge", "block", "braille"],
                   default="fidelity")
    p.add_argument("--color", choices=["auto", "truecolor", "256", "mono"], default="auto")
    p.add_argument("--scale", type=float, default=1.0)
    p.add_argument("--width", type=int, default=None)
    p.add_argument("--height", type=int, default=None)
    p.add_argument("--invert", action="store_true")
    return p


def _resolve_color(arg: str, mode: str) -> ColorMode:
    if arg != "auto":
        return arg  # type: ignore[return-value]
    caps = detect()
    per_mode_default: dict[str, ColorMode] = {
        "fidelity": "truecolor", "block": "truecolor",
        "luminance": "mono", "edge": "mono", "braille": "mono",
    }
    want = per_mode_default[mode]
    if want == "truecolor" and caps.color != "truecolor":
        return caps.color
    return want


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        img = load_image(args.image)
    except (FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    color_mode = _resolve_color(args.color, args.mode)

    cls = RENDERERS.get(args.mode)
    if cls is None:
        print(f"error: mode '{args.mode}' not yet implemented", file=sys.stderr)
        return 2
    renderer = cls()
    caps = detect()
    cols, rows = compute_target_size(
        src_w=img.shape[1], src_h=img.shape[0],
        term_cols=caps.columns, term_lines=caps.lines,
        char_aspect=renderer.char_aspect, scale=args.scale,
        width=args.width, height=args.height,
    )
    resized = resample(img, cols=cols, rows=rows)
    grid = renderer.render(resized, RenderOpts(color_mode=color_mode, invert=args.invert))
    out = TerminalEncoder().encode(grid, EncodeOpts())
    sys.stdout.write(out)
    return 0
