from typing import Any
from typing import TypedDict

from ewokscore.graph import TaskGraph

from ..config.constants import ELK_LAYOUT_OPTION
from ..svg.svg_task_group import TaskSizes


class ElkChild(TypedDict):
    id: str
    width: float
    height: float


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
    ewoks_graph: TaskGraph, task_sizes: TaskSizes
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

    children: list[ElkChild] = [
        {
            "id": task_id,
            "width": task_sizes[task_id].width,
            "height": task_sizes[task_id].height,
        }
        for task_id in ewoks_graph.graph.nodes
    ]

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
        "layoutOptions": ELK_LAYOUT_OPTION,
        "children": children,
        "edges": edges,
    }
