from typing import Any

from ewoksdraw.config.constants import LINK_TURN_RADIUS

from ..geometry.cubic_bezier_path import CubicBezierPath
from ..svg.svg_group import SvgGroup
from ..svg.svg_link_cubic_bezier import SvgLinkCubicBezier
from .elk_converter import ElkGraph


def build_svg_link_group(
    laid_out_graph: ElkGraph, group_id: str | None = None
) -> SvgGroup[SvgLinkCubicBezier]:
    """Build an SVG link group from the routed edges of an ELK graph."""
    link_group: SvgGroup[SvgLinkCubicBezier] = SvgGroup(group_id=group_id)

    for edge in laid_out_graph["edges"]:
        for section in edge.get("sections", []):
            points = _section_points(section)
            if len(points) < 2:
                continue
            link_group.add_elements(
                [
                    SvgLinkCubicBezier(
                        CubicBezierPath.from_points(
                            points=points,
                            radius=LINK_TURN_RADIUS,
                        )
                    )
                ]
            )

    return link_group


def _section_points(section: dict[str, Any]) -> list[tuple[float, float]]:
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
    point_dicts = []
    start_point = section.get("startPoint")
    if start_point is not None:
        point_dicts.append(start_point)
    point_dicts.extend(section.get("bendPoints", []))
    end_point = section.get("endPoint")
    if end_point is not None:
        point_dicts.append(end_point)
    return [(point["x"], point["y"]) for point in point_dicts]
