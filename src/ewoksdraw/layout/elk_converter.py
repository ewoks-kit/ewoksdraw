from typing import Any

from ewokscore.graph import TaskGraph

from ..config.constants import ELK_ALGORITHM
from ..config.constants import ELK_DIRECTION
from ..config.constants import ELK_ROUTING_MODE
from ..config.constants import ELK_SPACING_LINK
from ..config.constants import ELK_SPACING_TASK_LAYERS
from ..config.constants import ELK_SPACING_TASKS
from ..svg import TaskSizes

ElkGraph = dict[str, Any]

LAYOUT_OPTIONS = {
    "org.eclipse.elk.algorithm": ELK_ALGORITHM,
    "org.eclipse.elk.direction": ELK_DIRECTION,
    "org.eclipse.elk.spacing.nodeNode": ELK_SPACING_TASKS,
    "org.eclipse.elk.layered.spacing.nodeNodeBetweenLayers": ELK_SPACING_TASK_LAYERS,
    "org.eclipse.elk.spacing.edgeEdge": ELK_SPACING_LINK,
    "org.eclipse.elk.edgeRouting": "SPLINES",
    "elk.layered.edgeRouting.splines.mode": ELK_ROUTING_MODE,
}


def convert_ewoks_to_elk_graph(
    ewoks_graph: TaskGraph, task_sizes: TaskSizes
) -> ElkGraph:
    """Convert an Ewoks task graph into an ELK layout graph.

    :param ewoks_graph: the task graph to convert, e.g. from ``ewokscore.load_graph``.
    :param task_sizes: ``(width, height)`` per task in ``ewoks_graph``, and no
        other task id, e.g. ``{"task1": (39.56, 55.0), ...}``.
    :returns: an ELK graph, i.e.
        ``{"id": str, "layoutOptions": dict,
        "children": [{"id", "width", "height"}, ...],
        "edges": [{"id", "sources": [str], "targets": [str]}, ...]}``.
    """
    node_ids = set(ewoks_graph.graph.nodes)
    if node_ids != task_sizes.keys():
        raise ValueError(
            f"task_sizes {sorted(task_sizes)} do not match ewoks_graph task ids "
            f"{sorted(node_ids)}"
        )

    children = []
    for task_id in ewoks_graph.graph.nodes:
        width, height = task_sizes[task_id]
        children.append({"id": task_id, "width": width, "height": height})

    edges = []
    for source, target, link_attrs in ewoks_graph.graph.edges(data=True):
        n_mappings = len(link_attrs.get("data_mapping") or []) or 1
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
        "layoutOptions": LAYOUT_OPTIONS,
        "children": children,
        "edges": edges,
    }
