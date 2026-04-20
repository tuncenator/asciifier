import subprocess
import sys


def test_cli_renders_luminance_to_stdout(fixtures_dir):
    result = subprocess.run(
        [sys.executable, "-m", "asciifier",
         str(fixtures_dir / "small_rgb.png"),
         "--mode", "luminance", "--width", "4", "--height", "4", "--color", "mono"],
        capture_output=True, text=True, check=True,
    )
    lines = [l for l in result.stdout.split("\n") if l.strip()]
    assert len(lines) == 4


def test_cli_html_export(fixtures_dir, tmp_path):
    out = tmp_path / "out.html"
    subprocess.run(
        [sys.executable, "-m", "asciifier",
         str(fixtures_dir / "small_rgb.png"),
         "--mode", "luminance", "--width", "4",
         "--html", str(out)],
        capture_output=True, text=True, check=True,
    )
    assert out.exists() and "<pre" in out.read_text()


def test_cli_info_flag(fixtures_dir):
    result = subprocess.run(
        [sys.executable, "-m", "asciifier", "--info",
         str(fixtures_dir / "small_rgb.png")],
        capture_output=True, text=True, check=True,
    )
    assert "color" in result.stdout.lower()


def test_cli_preset_photo(fixtures_dir, tmp_path):
    out = tmp_path / "out.png"
    subprocess.run(
        [sys.executable, "-m", "asciifier",
         str(fixtures_dir / "small_rgb.png"),
         "--preset", "photo", "--width", "4",
         "--png", str(out)],
        capture_output=True, text=True, check=True,
    )
    assert out.exists()


def test_cli_preset_lineart_sets_edge_mode(fixtures_dir, tmp_path):
    # Edge mode with mono produces a 4x8 grid of printable chars.
    result = subprocess.run(
        [sys.executable, "-m", "asciifier",
         str(fixtures_dir / "small_rgb.png"),
         "--preset", "lineart", "--width", "8",
         "--color", "mono"],
        capture_output=True, text=True, check=True,
    )
    # Edge renderer in mono mode emits only ramp/edge chars, never truecolor escapes.
    assert "\x1b[38;2" not in result.stdout


def test_cli_fidelity_fills_terminal(fixtures_dir):
    # Force a known terminal size via COLUMNS/LINES so output is predictable.
    import os
    env = os.environ.copy()
    env["COLUMNS"] = "80"
    env["LINES"] = "24"
    result = subprocess.run(
        [sys.executable, "-m", "asciifier",
         str(fixtures_dir / "small_rgb.png"),
         "--mode", "fidelity", "--color", "mono"],
        capture_output=True, text=True, check=True, env=env,
    )
    lines = [l for l in result.stdout.split("\n") if l]
    # With 4x4 source and fidelity's 8x16 cell, resample produces
    # (cols*8, rows*16) image. For 80-wide terminal and square source,
    # char grid is at least several rows x several cols.
    assert len(lines) >= 3, f"got {len(lines)} lines, expected >= 3"
    assert max(len(l.rstrip()) for l in lines) >= 5
