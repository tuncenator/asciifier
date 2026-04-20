from typing import TypedDict


class PresetDict(TypedDict, total=False):
    mode: str
    color: str
    invert: bool


PRESETS: dict[str, PresetDict] = {
    "photo":    {"mode": "fidelity", "color": "truecolor"},
    "lineart":  {"mode": "edge",     "color": "mono"},
    "pixelart": {"mode": "block",    "color": "truecolor"},
    "logo":     {"mode": "block",    "color": "truecolor"},
}


def apply_preset(flags: dict, name: str, user_set: set[str] | None = None) -> dict:
    if name not in PRESETS:
        raise KeyError(f"Unknown preset '{name}'. Known: {sorted(PRESETS)}")
    user_set = user_set or set()
    out = dict(flags)
    for k, v in PRESETS[name].items():
        if k not in user_set:
            out[k] = v
    return out
