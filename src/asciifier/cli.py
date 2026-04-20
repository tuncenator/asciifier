import argparse
import sys
from pathlib import Path

from asciifier.color import ColorMode
from asciifier.encoders.base import EncodeOpts
from asciifier.encoders.html import HtmlEncoder
from asciifier.encoders.png import PngEncoder
from asciifier.encoders.svg import SvgEncoder
from asciifier.encoders.terminal import TerminalEncoder
from asciifier.loader import load_image
from asciifier.presets import apply_preset
from asciifier.renderers.base import RenderOpts
from asciifier.renderers.block import BlockRenderer
from asciifier.renderers.braille import BrailleRenderer
from asciifier.renderers.edge import EdgeRenderer
from asciifier.renderers.fidelity import FidelityRenderer
from asciifier.renderers.luminance import LuminanceRenderer
from asciifier.resample import compute_target_size, resample
from asciifier.terminal import detect

RENDERERS = {
    "fidelity": FidelityRenderer,
    "luminance": LuminanceRenderer,
    "block": BlockRenderer,
    "braille": BrailleRenderer,
    "edge": EdgeRenderer,
}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="asciifier", description="Image to character-art.")
    p.add_argument("image", type=Path, nargs="?", help="input image path")
    p.add_argument("--mode", choices=list(RENDERERS), default=argparse.SUPPRESS)
    p.add_argument("--color", choices=["auto", "truecolor", "256", "mono"], default=argparse.SUPPRESS)
    p.add_argument("--scale", type=float, default=1.0)
    p.add_argument("--width", type=int, default=None)
    p.add_argument("--height", type=int, default=None)
    p.add_argument("--invert", action="store_true", default=argparse.SUPPRESS)
    p.add_argument("--font", type=Path, default=None)
    p.add_argument("--preset", choices=["photo", "lineart", "pixelart", "logo"], default=None)
    p.add_argument("--html", type=Path, default=None, metavar="PATH")
    p.add_argument("--png", type=Path, default=None, metavar="PATH")
    p.add_argument("--svg", type=Path, default=None, metavar="PATH")
    p.add_argument("--info", action="store_true")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("--version", action="store_true")
    return p


def _resolve_color(arg: str, mode: str) -> ColorMode:
    if arg != "auto":
        return arg  # type: ignore[return-value]
    caps = detect()
    per_mode: dict[str, ColorMode] = {
        "fidelity": "truecolor", "block": "truecolor",
        "luminance": "mono", "edge": "mono", "braille": "mono",
    }
    want = per_mode[mode]
    if want == "truecolor" and caps.color != "truecolor":
        return caps.color
    return want


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        from asciifier import __version__
        print(__version__)
        return 0

    if args.info:
        caps = detect()
        print(f"color: {caps.color}")
        print(f"size:  {caps.columns}x{caps.lines}")
        return 0

    preset_defaults = {"mode": "fidelity", "color": "auto", "invert": False}
    user_set = {k for k in preset_defaults if hasattr(args, k)}
    flags = {k: getattr(args, k, v) for k, v in preset_defaults.items()}
    if args.preset:
        flags = apply_preset(flags, args.preset, user_set=user_set)
    mode: str = flags["mode"]
    color_arg: str = flags["color"]
    invert: bool = flags["invert"]

    if args.image is None:
        parser.error("image path required")
    try:
        img = load_image(args.image)
    except (FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    color_mode = _resolve_color(color_arg, mode)
    renderer = RENDERERS[mode]()
    caps = detect()
    cols, rows = compute_target_size(
        src_w=img.shape[1], src_h=img.shape[0],
        term_cols=caps.columns, term_lines=caps.lines,
        char_aspect=renderer.char_aspect, scale=args.scale,
        width=args.width, height=args.height,
    )
    px_w, px_h = renderer.pixel_cell_size
    resized = resample(img, cols=cols * px_w, rows=rows * px_h)

    try:
        grid = renderer.render(
            resized,
            RenderOpts(color_mode=color_mode, invert=invert, font_path=args.font),
        )
    except OSError as e:
        print(f"error: font load failed: {e}. Try --font PATH.", file=sys.stderr)
        return 3

    encode_opts = EncodeOpts()
    if args.html:
        args.html.write_text(HtmlEncoder().encode(grid, encode_opts), encoding="utf-8")
    if args.png:
        PngEncoder(args.png).encode(grid, encode_opts)
    if args.svg:
        args.svg.write_text(SvgEncoder().encode(grid, encode_opts), encoding="utf-8")
    if not (args.html or args.png or args.svg):
        sys.stdout.write(TerminalEncoder().encode(grid, encode_opts))

    return 0
