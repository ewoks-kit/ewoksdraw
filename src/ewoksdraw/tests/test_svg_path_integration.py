from pathlib import Path

from defusedxml import ElementTree

from ewoksdraw.geometry.cubic_bezier_path import CubicBezierPath
from ewoksdraw.geometry.cubic_bezier_path import CubicBezierSegment
from ewoksdraw.svg.svg_canvas import SvgCanvas
from ewoksdraw.svg.svg_group import SvgGroup
from ewoksdraw.svg.svg_link_cubic_bezier import SvgLinkCubicBezier

PATH = CubicBezierPath(
    start=(0, 0),
    segments=[CubicBezierSegment(control1=(1, 1), control2=(2, 2), end=(3, 3))],
)


def test_group_translate_moves_path_via_transform_not_d_attribute():
    link = SvgLinkCubicBezier(PATH)
    group = SvgGroup()
    group.add_elements([link])
    group.translate(5, 5)

    group_element = group.xml_element
    assert group_element.get("transform") == "translate(5,5)"

    path_element = group_element[0]
    assert path_element.tag == "path"
    assert path_element.get("d") == "M 0,0 C 1,1 2,2 3,3"


def test_canvas_draw_writes_valid_svg_with_path_element(tmp_path: Path):
    output_path = tmp_path / "path.svg"

    link = SvgLinkCubicBezier(PATH, color="#ff0000")
    group = SvgGroup()
    group.add_elements([link])

    canvas = SvgCanvas(width=100, height=100)
    canvas.add_element(group)
    canvas.draw(output_path)

    assert output_path.is_file()

    tree = ElementTree.parse(output_path)
    root = tree.getroot()

    path_elements = [element for element in root.iter() if element.tag.endswith("path")]
    assert len(path_elements) == 1
    assert path_elements[0].get("d") == "M 0,0 C 1,1 2,2 3,3"
