from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from PIL import Image

SUPPORTED_EXTS = frozenset({".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"})


def load_image(path: Path | str) -> NDArray[np.uint8]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Image not found: {p}")
    if p.suffix.lower() not in SUPPORTED_EXTS:
        raise ValueError(
            f"Unsupported format '{p.suffix}'. Supported: {sorted(SUPPORTED_EXTS)}"
        )
    with Image.open(p) as im:
        im.load()
        if getattr(im, "is_animated", False):
            im.seek(0)
        rgb = im.convert("RGB")
        return np.asarray(rgb, dtype=np.uint8)
