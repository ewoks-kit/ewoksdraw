import pytest

from ewoksdraw.geometry.cubic_bezier_path import CubicBezierPath
from ewoksdraw.geometry.cubic_bezier_path import CubicBezierSegment
from ewoksdraw.svg.svg_link_cubic_bezier import SvgLinkCubicBezier

SIMPLE_PATH = CubicBezierPath(
    start=(0, 0),
    segments=[CubicBezierSegment(control1=(1, 1), control2=(2, 2), end=(3, 3))],
)

TWO_SEGMENT_PATH = CubicBezierPath(
    start=(0, 0),
    segments=[
        CubicBezierSegment(control1=(1, 1), control2=(2, 2), end=(3, 3)),
        CubicBezierSegment(control1=(4, 4), control2=(5, 5), end=(6, 6)),
    ],
)


def test_d_attribute_starts_with_move_command():
    link = SvgLinkCubicBezier(SIMPLE_PATH)
    assert link.get_attr("d") == "M 0,0 C 1,1 2,2 3,3"


def test_d_attribute_has_one_curve_command_per_segment():
    link = SvgLinkCubicBezier(TWO_SEGMENT_PATH)
    assert link.get_attr("d") == "M 0,0 C 1,1 2,2 3,3 C 4,4 5,5 6,6"


def test_raises_when_path_has_no_segments():
    empty_path = CubicBezierPath(start=(0, 0), segments=[])
    with pytest.raises(ValueError):
        SvgLinkCubicBezier(empty_path)


@pytest.mark.parametrize(
    "color, stroke_width, stroke_dash, expected_style",
    [
        ("#ff0000", None, None, "stroke:#ff0000"),
        (None, 4, None, "stroke-width:4"),
        (None, None, "5 10", "stroke-dasharray:5 10"),
        (
            "#ff0000",
            4,
            "5 10",
            "stroke:#ff0000;stroke-width:4;stroke-dasharray:5 10",
        ),
        (None, None, None, None),
    ],
)
def test_style_attribute_combinations(color, stroke_width, stroke_dash, expected_style):
    link = SvgLinkCubicBezier(
        SIMPLE_PATH, color=color, stroke_width=stroke_width, stroke_dash=stroke_dash
    )
    assert link.get_attr("style") == expected_style


def test_stroke_width_formatted_without_trailing_zero():
    link = SvgLinkCubicBezier(SIMPLE_PATH, stroke_width=4.0)
    assert link.get_attr("style") == "stroke-width:4"


def test_xml_element_is_a_path_with_link_class():
    link = SvgLinkCubicBezier(SIMPLE_PATH)
    element = link.xml_element
    assert element.tag == "path"
    assert element.get("class") == "link_cubic_bezier"
    assert element.get("d") == "M 0,0 C 1,1 2,2 3,3"
