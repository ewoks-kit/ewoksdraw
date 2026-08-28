import warnings
from typing import Any
from typing import TypedDict

from ewokscore.graph import TaskGraph

from ewoksdraw.config.constants import ELK_LAYOUT_OPTIONS

from ..svg.svg_task import IOPositions
from ..svg.svg_task import TaskIOPosition
from ..svg.svg_task_group import TaskIOPositions
from ..svg.svg_task_group import TaskSizes


class ElkPort(TypedDict):
    id: str
    x: float
    y: float
    width: float
    height: float
    layout_options: dict[str, Any]


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
    task_io_positions: TaskIOPositions,
) -> ElkGraph:
    """Convert an Ewoks task graph into an ELK layout graph.

    :param ewoks_graph: the task graph to convert, e.g. from ``ewokscore.load_graph``.
    :param task_sizes: width and height of each task.
    :param task_io_positions: input and output positions of each task.
    """
    node_ids = set(ewoks_graph.graph.nodes)
    if node_ids != task_sizes.keys():
        raise ValueError(
            f"task_sizes {sorted(task_sizes)} do not match ewoks_graph task ids "
            f"{sorted(node_ids)}"
        )

    if node_ids != task_io_positions.keys():
        raise ValueError(
            "task_io_positions "
            f"{sorted(task_io_positions)} do not match ewoks_graph task ids "
            f"{sorted(node_ids)}"
        )

    children: list[ElkChild] = []
    used_ids: set[str] = set()
    for task_id in ewoks_graph.graph.nodes:
        width, height = task_sizes[task_id]
        ports = _convert_io_positions_to_elk_ports(task_id, task_io_positions[task_id])
        children.append(
            {
                "id": task_id,
                "width": width,
                "height": height,
                "layoutOptions": {
                    "org.eclipse.elk.portConstraints": "FIXED_POS",
                },
                "ports": ports,
            }
        )
        used_ids.add(task_id)
        used_ids.update(port["id"] for port in ports)

    root_id = _available_elk_id("__ewoksdraw_root__", used_ids)
    used_ids.add(root_id)

    edges: list[ElkEdge] = []
    for source, target, link_attrs in ewoks_graph.graph.edges(data=True):
        if link_attrs.get("map_all_data", False):
            warnings.warn(
                f"Ewoks link {source!r} -> {target!r} uses 'map_all_data', which "
                "is not yet supported.",
                UserWarning,
                stacklevel=2,
            )

        for mapping in link_attrs.get("data_mapping", []):
            source_output = mapping.get("source_output")
            if not source_output:
                warnings.warn(
                    f"Data mapping on Ewoks link {source!r} -> {target!r} has no "
                    "'source_output', which is not yet supported.",
                    UserWarning,
                    stacklevel=2,
                )
                continue

            edge_id = _available_elk_id(
                f"edge_{len(edges)}_{source}_{target}", used_ids
            )

            edges.append(
                {
                    "id": edge_id,
                    "sources": [f"{source}.output.{source_output}"],
                    "targets": [f"{target}.input.{mapping['target_input']}"],
                }
            )
            used_ids.add(edge_id)

    return {
        "id": root_id,
        "layoutOptions": ELK_LAYOUT_OPTIONS,
        "children": children,
        "edges": edges,
    }


def _convert_io_positions_to_elk_ports(
    task_id: str, io_positions: IOPositions
) -> list[ElkPort]:
    ports = _convert_positions_to_elk_ports(
        io_positions.inputs,
        id_prefix=f"{task_id}.input",
        elk_port_side="WEST",
    )
    ports.extend(
        _convert_positions_to_elk_ports(
            io_positions.outputs,
            id_prefix=f"{task_id}.output",
            elk_port_side="EAST",
        )
    )
    return ports


def _convert_positions_to_elk_ports(
    positions: list[TaskIOPosition], id_prefix: str, elk_port_side: str
) -> list[ElkPort]:
    ports: list[ElkPort] = []

    for index, position in enumerate(positions):
        ports.append(
            {
                "id": f"{id_prefix}.{position.name}",
                "x": position.x,
                "y": position.y,
                "width": 0,
                "height": 0,
                "layoutOptions": {
                    "org.eclipse.elk.port.side": elk_port_side,
                    "org.eclipse.elk.port.index": index,
                    "org.eclipse.elk.port.borderOffset": 0,
                },
            }
        )

    return ports


def _available_elk_id(preferred_id: str, used_ids: set[str]) -> str:
    element_id = preferred_id
    index = 1
    while element_id in used_ids:
        element_id = f"{preferred_id}_{index}"
        index += 1
    return element_id
