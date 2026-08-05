from typing import Any
from typing import TypedDict

from ewokscore.graph import TaskGraph

from ewoksdraw.config.constants import ELK_LAYOUT_OPTIONS

from ..svg.svg_task import PortPosition
from ..svg.svg_task_group import TaskPortPositions
from ..svg.svg_task_group import TaskSizes


class ElkPort(TypedDict):
    id: str
    x: float
    y: float
    width: float
    height: float
    layoutOptions: dict[str, Any]


class ElkChild(TypedDict):
    id: str
    width: float
    height: float
    layoutOptions: dict[str, Any]
    ports: list[ElkPort]


class ElkEdge(TypedDict):
    id: str
    sources: list[str]
    targets: list[str]


class ElkGraph(TypedDict):
    id: str
    layoutOptions: dict[str, Any]
    children: list[ElkChild]
    edges: list[ElkEdge]


def convert_ewoks_to_elk_graph(
    ewoks_graph: TaskGraph,
    task_sizes: TaskSizes,
    task_port_positions: TaskPortPositions | None = None,
) -> ElkGraph:
    """Convert an Ewoks task graph into an ELK layout graph.

    :param ewoks_graph: the task graph to convert, e.g. from ``ewokscore.load_graph``.
    :param task_sizes: ``(width, height)`` per task in ``ewoks_graph``, and no
        other task id, e.g. ``{"task1": (39.56, 55.0), ...}``.
    """
    node_ids = set(ewoks_graph.graph.nodes)
    if node_ids != task_sizes.keys():
        raise ValueError(
            f"task_sizes {sorted(task_sizes)} do not match ewoks_graph task ids "
            f"{sorted(node_ids)}"
        )

    if task_port_positions is not None and node_ids != task_port_positions.keys():
        raise ValueError(
            "task_port_positions "
            f"{sorted(task_port_positions)} do not match ewoks_graph task ids "
            f"{sorted(node_ids)}"
        )

    children: list[ElkChild] = []
    for task_id in ewoks_graph.graph.nodes:
        width, height = task_sizes[task_id]
        port_positions = (
            task_port_positions[task_id] if task_port_positions is not None else []
        )
        children.append(
            {
                "id": task_id,
                "width": width,
                "height": height,
                "layoutOptions": {
                    "org.eclipse.elk.portConstraints": "FIXED_POS",
                },
                "ports": _convert_port_positions(task_id, port_positions),
            }
        )

    edges: list[ElkEdge] = []
    for source, target, link_attrs in ewoks_graph.graph.edges(data=True):
        n_mappings = len(link_attrs.get("data_mapping", [])) or 1
        for index in range(n_mappings):
            edges.append(
                {
                    "id": f"edge_{source}_{target}_{index}",
                    "sources": [source],
                    "targets": [target],
                }
            )

    return {
        "id": "root",
        "layoutOptions": ELK_LAYOUT_OPTIONS,
        "children": children,
        "edges": edges,
    }


def _convert_port_positions(
    task_id: str, port_positions: list[PortPosition]
) -> list[ElkPort]:
    ports: list[ElkPort] = []
    side_indices = {"input": 0, "output": 0}

    for position in port_positions:
        if position.id.startswith(f"{task_id}.input."):
            direction = "input"
            side = "WEST"
        elif position.id.startswith(f"{task_id}.output."):
            direction = "output"
            side = "EAST"
        else:
            raise ValueError(
                f"port id {position.id!r} does not belong to task {task_id!r}"
            )

        ports.append(
            {
                "id": position.id,
                "x": position.x,
                "y": position.y,
                "width": 0,
                "height": 0,
                "layoutOptions": {
                    "org.eclipse.elk.port.side": side,
                    "org.eclipse.elk.port.index": side_indices[direction],
                    "org.eclipse.elk.port.borderOffset": 0,
                },
            }
        )
        side_indices[direction] += 1

    return ports
