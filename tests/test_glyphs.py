import numpy as np

from asciifier.glyphs import Atlas, default_atlas


def test_atlas_has_space_and_full_block():
    atlas = default_atlas()
    assert " " in atlas.chars
    assert "\u2588" in atlas.chars


def test_atlas_mask_shape_matches_cell_size():
    atlas = default_atlas()
    assert atlas.masks.shape == (len(atlas.chars), atlas.cell_h, atlas.cell_w)


def test_space_mask_is_mostly_empty():
    atlas = default_atlas()
    i = atlas.chars.index(" ")
    assert atlas.masks[i].mean() < 0.1


def test_full_block_mask_is_nearly_full():
    atlas = default_atlas()
    i = atlas.chars.index("\u2588")
    assert atlas.masks[i].mean() > 0.9
