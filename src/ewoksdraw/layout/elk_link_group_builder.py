from ..config.constants import LINK_TURN_RADIUS
from ..geometry.cubic_bezier_path import CubicBezierPath
from ..svg.svg_group import SvgGroup
from ..svg.svg_link_cubic_bezier import SvgLinkCubicBezier
from .elk_converter import ElkSection
from .elk_converter import LaidOutElkGraph


def build_svg_link_group(
    laid_out_graph: LaidOutElkGraph, group_id: str | None = None
) -> SvgGroup[SvgLinkCubicBezier]:
    """Build an SVG link group from the routed edges of an ELK graph."""
    link_group: SvgGroup[SvgLinkCubicBezier] = SvgGroup(group_id=group_id)
    svg_links: list[SvgLinkCubicBezier] = []

    for edge in laid_out_graph["edges"]:
        for section in edge["sections"]:
            points = _section_points(section)
            if len(points) < 2:
                continue

            cubic_bezier_path = CubicBezierPath.from_points(
                points=points,
                radius=LINK_TURN_RADIUS,
            )
            svg_link = SvgLinkCubicBezier(cubic_bezier_path)
            svg_links.append(svg_link)

    link_group.add_elements(svg_links)
    return link_group


def _section_points(section: ElkSection) -> list[tuple[float, float]]:
    """Convert an ELK edge section into an ordered list of points.

    :param section: an ELK edge section containing start, bend and end points.
        For example::

            {
                "startPoint": {"x": 10.0, "y": 20.0},
                "bendPoints": [{"x": 30.0, "y": 20.0}],
                "endPoint": {"x": 30.0, "y": 40.0},
            }

    :return: the points ordered from start to end as ``(x, y)`` tuples.
        For example::

            [(10.0, 20.0), (30.0, 20.0), (30.0, 40.0)]
    """
    point_dicts = [
        section["startPoint"],
        *section["bendPoints"],
        section["endPoint"],
    ]
    return [(point["x"], point["y"]) for point in point_dicts]
