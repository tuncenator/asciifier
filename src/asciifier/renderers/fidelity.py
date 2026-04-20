import numpy as np
from numpy.typing import NDArray

from asciifier.color import quantize
from asciifier.glyphs import Atlas, atlas_from_font, default_atlas
from asciifier.renderers.base import RenderOpts
from asciifier.types import Cell, Grid

_LUM_W = np.array([0.299, 0.587, 0.114], dtype=np.float32)


def _two_color_palette(patch_flat: NDArray[np.float32]) -> tuple[NDArray[np.float32], NDArray[np.float32]]:
    """Return (bright, dark) colour centres for the patch.

    Pixels are split by luminance around the mid-luminance of the patch; each
    side's mean is a palette centre. For a flat patch both centres collapse to
    the single colour so solid-colour cells produce fg == bg == patch colour.
    """
    lum = patch_flat @ _LUM_W
    lo, hi = float(lum.min()), float(lum.max())
    if hi - lo < 1e-6:
        c = patch_flat.mean(axis=0).astype(np.float32)
        return c, c
    mid = 0.5 * (lo + hi)
    bright_mask = lum >= mid
    dark_mask = ~bright_mask
    bright = patch_flat[bright_mask].mean(axis=0) if bright_mask.any() else patch_flat.mean(axis=0)
    dark = patch_flat[dark_mask].mean(axis=0) if dark_mask.any() else patch_flat.mean(axis=0)
    return bright.astype(np.float32), dark.astype(np.float32)


class FidelityRenderer:
    char_aspect: float = 8.0 / 16.0

    def render(self, img: NDArray[np.uint8], opts: RenderOpts) -> Grid:
        atlas: Atlas = atlas_from_font(opts.font_path) if opts.font_path else default_atlas()
        if opts.invert:
            img = 255 - img
        cw, ch = atlas.cell_w, atlas.cell_h
        h, w, _ = img.shape
        pad_h = (ch - h % ch) % ch
        pad_w = (cw - w % cw) % cw
        if pad_h or pad_w:
            img = np.pad(img, ((0, pad_h), (0, pad_w), (0, 0)), mode="edge")
            h, w = img.shape[:2]

        rows_out = h // ch
        cols_out = w // cw

        masks = (atlas.masks > 0.5).astype(np.float32)

        grid: Grid = []
        for cy in range(rows_out):
            row: list[Cell] = []
            for cx in range(cols_out):
                patch = img[cy * ch:(cy + 1) * ch, cx * cw:(cx + 1) * cw].astype(np.float32)
                patch_flat = patch.reshape(-1, 3)

                # Determine the patch's two-colour palette first, then pick the
                # glyph whose mask distributes those colours in the pattern
                # closest to the source. This decouples colour selection from
                # mask fit: a solid patch yields fg == bg == mean (any glyph
                # reconstructs perfectly, the first candidate wins) and a
                # bimodal patch yields fg at the bright extreme and bg at the
                # dark extreme regardless of which glyph the font's rasterised
                # mask happens to align with.
                bright_c, dark_c = _two_color_palette(patch_flat)

                errors = np.empty(masks.shape[0], dtype=np.float32)
                for gi in range(masks.shape[0]):
                    m = masks[gi][..., None]
                    recon = m * bright_c + (1.0 - m) * dark_c
                    errors[gi] = float(((patch - recon) ** 2).sum())
                best = int(errors.argmin())

                ch_best = atlas.chars[best]
                fg_rgb = tuple(int(round(v)) for v in np.clip(bright_c, 0, 255))
                bg_rgb = tuple(int(round(v)) for v in np.clip(dark_c, 0, 255))
                row.append(Cell(
                    char=ch_best,
                    fg=quantize(fg_rgb, opts.color_mode),
                    bg=quantize(bg_rgb, opts.color_mode),
                ))
            grid.append(row)
        return grid
