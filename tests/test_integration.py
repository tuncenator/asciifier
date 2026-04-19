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
