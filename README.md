# asciifier

Convert any image into character art, right in your terminal.

`asciifier` picks the best glyph from the entire printable keyspace -- letters,
block elements, box drawing, braille -- and colors each cell with truecolor that
stays faithful to the source pixels. Five rendering modes: `fidelity` (the
default, max reproduction), plus `luminance`, `edge`, `block`, and `braille`.

## Install

Requires Python 3.11+.

    uv pip install git+https://github.com/tuncenator/asciifier.git

Or clone and install locally:

    git clone https://github.com/tuncenator/asciifier.git
    cd asciifier
    uv sync
    uv run asciifier --help

## Usage

    asciifier path/to/image.png

Common options:

    asciifier image.png --mode fidelity          # default, max fidelity
    asciifier image.png --mode block             # clean half-block style
    asciifier image.png --mode braille           # 2x4 subpixel detail
    asciifier image.png --preset photo           # bundled sensible defaults
    asciifier image.png --width 120 --scale 0.8  # size control
    asciifier image.png --html out.html          # export HTML
    asciifier image.png --png out.png            # export PNG
    asciifier image.png --svg out.svg            # export SVG
    asciifier --info image.png                   # show detected terminal caps

### Modes

| Mode | What it does |
|------|--------------|
| `fidelity` | Searches the full glyph atlas for the best `(char, fg, bg)` per cell. Uses truecolor by default. |
| `luminance` | Classic brightness ramp (` .:-=+*#%@`). |
| `edge` | Sobel edges render as directional chars; fills use the luminance ramp. |
| `block` | Unicode half-blocks / quadrants / shades only. Clean, no letters. |
| `braille` | Unicode braille (U+2800-U+28FF) with 2x4 subpixel resolution. |

### Presets

- `photo` -- max fidelity, truecolor.
- `lineart` -- edge mode, mono.
- `pixelart` -- block mode.
- `logo` -- block mode.

### Color

`--color` accepts `auto` (default), `truecolor`, `256`, or `mono`. In `auto`, the
tool checks `COLORTERM` and `TERM` and picks the best option supported.

### Custom font

The fidelity renderer builds its glyph atlas from a bundled JetBrains Mono
Regular. If your terminal uses a different monospace font, point to it for
closer visual match:

    asciifier image.png --mode fidelity --font /path/to/font.ttf

## Development

    uv sync --all-extras
    uv run pytest
    uv run ruff check src tests

## License

MIT. Bundled font (`JetBrainsMono-Regular.ttf`) is distributed under the SIL
Open Font License 1.1 -- see `src/asciifier/fonts/README.md`.
