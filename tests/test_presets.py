import pytest

from asciifier.presets import PRESETS, apply_preset


def test_preset_photo_uses_fidelity():
    base = {"mode": "fidelity", "color": "auto"}
    out = apply_preset(base, "photo")
    assert out["mode"] == "fidelity"
    assert out["color"] in ("truecolor", "auto")


def test_explicit_flag_overrides_preset():
    base = {"mode": "luminance", "color": "mono"}
    out = apply_preset(base, "photo", user_set={"mode"})
    assert out["mode"] == "luminance"


def test_unknown_preset_raises():
    with pytest.raises(KeyError):
        apply_preset({}, "unknown")


def test_preset_names_cover_all_four():
    assert set(PRESETS) >= {"photo", "lineart", "pixelart", "logo"}
