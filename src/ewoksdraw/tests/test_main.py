from pathlib import Path

from ewoksdraw.svg import SvgCanvas, SvgTask


def test_basic_use(tmp_path):
    svg_task = SvgTask(params={"title": "My Task Title"})
    canvas = SvgCanvas(width=500, height=500)
    canvas.add_element(svg_task)
    output_path = Path(tmp_path) / "output.svg"
    canvas.generate_svg(output_path)

    assert output_path.is_file()
