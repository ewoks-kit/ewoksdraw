import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator

import pytest
from PIL import Image

from ewoksdraw.svg.svg_canvas import SvgCanvas
from ewoksdraw.svg.svg_task_anchor_link import SvgTaskAnchorLink


@pytest.fixture
def inkscape_tmp_path() -> Iterator[Path]:
    # Snap applications have a private /tmp; use the project directory instead.
    with TemporaryDirectory(
        prefix="inkscape-test-", dir=Path(__file__).resolve().parent
    ) as directory:
        yield Path(directory)


def test_inkscape_renders_link_color(inkscape_tmp_path: Path) -> None:
    inkscape = shutil.which("inkscape")
    if inkscape is None:
        pytest.skip("Inkscape is required for this rendering test")

    svg_path = inkscape_tmp_path / "circle.svg"
    png_path = inkscape_tmp_path / "circle.png"

    canvas = SvgCanvas(width=100, height=100)
    canvas.add_element(SvgTaskAnchorLink(cx=50, cy=50, radius=20))
    canvas.draw(svg_path)

    # PATH-resolved Inkscape and test-owned paths; no shell or user input.
    result = subprocess.run(  # noqa: S603
        [
            inkscape,
            str(svg_path),
            "--export-type=png",
            "--export-area-page",
            "--export-width=100",
            f"--export-filename={png_path}",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 0 and png_path.is_file(), (
        f"Inkscape export failed (exit status {result.returncode}): {png_path}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )

    with Image.open(png_path) as image:
        pixel = image.convert("RGBA").getpixel((50, 50))

    assert isinstance(pixel, tuple), pixel
    expected = (176, 147, 255, 255)
    assert all(abs(actual - wanted) <= 1 for actual, wanted in zip(pixel, expected)), (
        pixel
    )
