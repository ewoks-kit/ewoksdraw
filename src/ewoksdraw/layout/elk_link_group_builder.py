from ..config.constants import LINK_TURN_RADIUS
from ..geometry.cubic_bezier_path import CubicBezierPath
from ..geometry.cubic_bezier_path import Point
from ..svg.svg_group import SvgGroup
from ..svg.svg_link_cubic_bezier import SvgLinkCubicBezier
from ..utils import get_task_id_from_source_id
from ..utils import get_task_id_from_target_id
from .elk_converter import ElkEdge
from .elk_converter import ElkGraph
from .elk_converter import ElkSection


def build_svg_link_group(
    elk_graph: ElkGraph,
    task_import_errors: dict[str, bool] | None = None,
    group_id: str | None = None,
) -> SvgGroup[SvgLinkCubicBezier]:
    """Build an SVG link group from the routed edges of an ELK graph."""
    link_group: SvgGroup[SvgLinkCubicBezier] = SvgGroup(group_id=group_id)
    svg_links: list[SvgLinkCubicBezier] = []

    for edge in elk_graph["edges"]:
        import_error = _edge_has_import_error(edge, task_import_errors)
        for section in edge.get("sections", list()):
            points = _section_points(section)
            cubic_bezier_path = CubicBezierPath.from_points(
                points=points,
                radius=LINK_TURN_RADIUS,
            )
            svg_link = SvgLinkCubicBezier(cubic_bezier_path, import_error=import_error)
            svg_links.append(svg_link)

    link_group.add_elements(svg_links)
    return link_group


def _edge_has_import_error(
    edge: ElkEdge, task_import_errors: dict[str, bool] | None = None
) -> bool:
    if task_import_errors is None:
        return False
    source_task_id = get_task_id_from_source_id(edge["sources"][0])
    target_task_id = get_task_id_from_target_id(edge["targets"][0])
    return task_import_errors.get(source_task_id, False) or task_import_errors.get(
        target_task_id, False
    )


def _section_points(section: ElkSection) -> list[Point]:
    """Convert an ELK edge section into an ordered list of points.

    :param section: an ELK edge section containing start, bend and end points.
        For example::

            {
                "startPoint": {"x": 10.0, "y": 20.0},
                "bendPoints": [{"x": 30.0, "y": 20.0}],
                "endPoint": {"x": 30.0, "y": 40.0},
            }

    :return: the points ordered from start to end.
        For example::

            [
                {"x": 10.0, "y": 20.0},
                {"x": 30.0, "y": 20.0},
                {"x": 30.0, "y": 40.0},
            ]
    """
    return [
        section["startPoint"],
        *section["bendPoints"],
        section["endPoint"],
    ]
