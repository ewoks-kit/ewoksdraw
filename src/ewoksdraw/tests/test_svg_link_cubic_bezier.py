import pytest

from ewoksdraw.geometry.cubic_bezier_path import CubicBezierPath
from ewoksdraw.geometry.cubic_bezier_path import CubicBezierSegment
from ewoksdraw.svg.svg_link_cubic_bezier import SvgLinkCubicBezier

SIMPLE_PATH = CubicBezierPath(
    start={"x": 0, "y": 0},
    segments=[
        CubicBezierSegment(
            control1={"x": 1, "y": 1},
            control2={"x": 2, "y": 2},
            end={"x": 3, "y": 3},
        )
    ],
)

TWO_SEGMENT_PATH = CubicBezierPath(
    start={"x": 0, "y": 0},
    segments=[
        CubicBezierSegment(
            control1={"x": 1, "y": 1},
            control2={"x": 2, "y": 2},
            end={"x": 3, "y": 3},
        ),
        CubicBezierSegment(
            control1={"x": 4, "y": 4},
            control2={"x": 5, "y": 5},
            end={"x": 6, "y": 6},
        ),
    ],
)


def test_d_attribute_starts_with_move_command() -> None:
    link = SvgLinkCubicBezier(SIMPLE_PATH)
    assert link.get_attr("d") == "M 0,0 C 1,1 2,2 3,3"


def test_d_attribute_has_one_curve_command_per_segment() -> None:
    link = SvgLinkCubicBezier(TWO_SEGMENT_PATH)
    assert link.get_attr("d") == "M 0,0 C 1,1 2,2 3,3 C 4,4 5,5 6,6"


def test_raises_when_path_has_no_segments() -> None:
    empty_path = CubicBezierPath(start={"x": 0, "y": 0}, segments=[])
    with pytest.raises(ValueError):
        SvgLinkCubicBezier(empty_path)


def test_style_attribute_has_only_color() -> None:
    link = SvgLinkCubicBezier(SIMPLE_PATH, color="#ff0000")
    assert link.get_attr("style") == "stroke:#ff0000"


def test_style_attribute_has_only_stroke_width() -> None:
    link = SvgLinkCubicBezier(SIMPLE_PATH, stroke_width=4.0)
    assert link.get_attr("style") == "stroke-width:4"


def test_style_attribute_has_only_stroke_dash() -> None:
    link = SvgLinkCubicBezier(SIMPLE_PATH, stroke_dasharray="5 10")
    assert link.get_attr("style") == "stroke-dasharray:5 10"


def test_style_attribute_combines_color_stroke_width_and_stroke_dash() -> None:
    link = SvgLinkCubicBezier(
        SIMPLE_PATH, color="#ff0000", stroke_width=4, stroke_dasharray="5 10"
    )
    assert (
        link.get_attr("style") == "stroke:#ff0000;stroke-width:4;stroke-dasharray:5 10"
    )


def test_style_attribute_is_none_without_color_stroke_width_or_stroke_dash() -> None:
    link = SvgLinkCubicBezier(SIMPLE_PATH)
    assert link.get_attr("style") is None


def test_xml_element_is_a_path_with_link_class() -> None:
    link = SvgLinkCubicBezier(SIMPLE_PATH)
    element = link.xml_element
    assert element.tag == "path"
    assert element.get("class") == "link_cubic_bezier"
    assert element.get("d") == "M 0,0 C 1,1 2,2 3,3"
