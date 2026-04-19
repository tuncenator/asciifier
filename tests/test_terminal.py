import os
from unittest.mock import patch

from asciifier.terminal import TerminalCaps, detect


def test_detect_truecolor_from_colorterm():
    with patch.dict(os.environ, {"COLORTERM": "truecolor", "TERM": "xterm"}, clear=True):
        caps = detect()
    assert caps.color == "truecolor"


def test_detect_256_from_term():
    with patch.dict(os.environ, {"TERM": "xterm-256color"}, clear=True):
        caps = detect()
    assert caps.color == "256"


def test_detect_mono_fallback():
    with patch.dict(os.environ, {"TERM": "dumb"}, clear=True):
        caps = detect()
    assert caps.color == "mono"


def test_default_size_when_env_missing():
    with patch.dict(os.environ, {"TERM": "xterm"}, clear=True):
        caps = detect()
    assert caps.columns > 0 and caps.lines > 0
