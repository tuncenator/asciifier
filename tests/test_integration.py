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
