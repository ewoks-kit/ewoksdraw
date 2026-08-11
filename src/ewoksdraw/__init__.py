import random
from typing import Any

from ewokscore.graph import TaskGraph
from ewokscore.graph.inputs import get_all_node_inputs
from ewokscore.graph.inputs import get_all_task_output_names
from pyelk import ELK

from .svg import SvgBackground
from .svg import SvgCanvas
from .svg import SvgLink
from .svg import SvgTask

CANVAS_MARGIN = 20
DEFAULT_LAYOUT_OPTIONS = {
    "org.eclipse.elk.algorithm": "layered",
    "org.eclipse.elk.direction": "RIGHT",
    "org.eclipse.elk.spacing.nodeNode": 60,
    "org.eclipse.elk.layered.spacing.nodeNodeBetweenLayers": 80,
    "org.eclipse.elk.layered.spacing.edgeEdgeBetweenLayers": 20,
    "org.eclipse.elk.edgeRouting": "SPLINES",
    "elk.layered.edgeRouting.splines.mode": "CONSERVATIVE_SOFT",
}


def _random_link_color() -> str:
    return f"hsl({random.randint(0, 359)}, 75%, 65%)"


def extract_link_coordinates(elk_result: dict) -> list[dict]:
    link_coordinates = []

    for edge in elk_result.get("edges", []):
        sections = []
        for section in edge.get("sections", []):
            points = []

            start_point = section.get("startPoint")
            if start_point is not None:
                points.append({"x": start_point["x"], "y": start_point["y"]})

            for bend_point in section.get("bendPoints", []):
                points.append({"x": bend_point["x"], "y": bend_point["y"]})

            end_point = section.get("endPoint")
            if end_point is not None:
                points.append({"x": end_point["x"], "y": end_point["y"]})

            sections.append(
                {
                    "id": section.get("id"),
                    "points": points,
                    "routing": section.get("routing"),
                }
            )

        link_coordinates.append(
            {
                "id": edge["id"],
                "sources": edge.get("sources", []),
                "targets": edge.get("targets", []),
                "color": _random_link_color(),
                "sections": sections,
            }
        )

    return link_coordinates


def graph_to_svg(
    graph: TaskGraph,
    layout_option: dict | None = None,
    node_ports: dict[Any, dict[str, list[str]]] | None = None,
) -> str:
    """Render an Ewoks task graph and return the complete SVG document."""

    svg_tasks_by_id: dict[str, SvgTask] = {}
    link_metadata_by_id: dict[str, dict[str, Any]] = {}
    requested_layout_options = dict(layout_option or {})
    edge_routing = requested_layout_options.pop(
        "org.eclipse.elk.edgeRouting",
        requested_layout_options.pop(
            "elk.edgeRouting", DEFAULT_LAYOUT_OPTIONS["org.eclipse.elk.edgeRouting"]
        ),
    )
    layout_options = {**DEFAULT_LAYOUT_OPTIONS, **requested_layout_options}
    layout_options["org.eclipse.elk.edgeRouting"] = edge_routing

    elk_graph: dict[str, Any] = {
        "id": "root",
        "layoutOptions": layout_options,
        "children": [],
        "edges": [],
    }

    for node_id, node_attrs in graph.graph.nodes.items():
        port_override = (node_ports or {}).get(node_id, {})
        if "inputs" in port_override:
            node_inputs = port_override["inputs"]
        else:
            node_inputs = [
                item.name for item in get_all_node_inputs(node_id, node_attrs)
            ]
        if "outputs" in port_override:
            node_outputs = port_override["outputs"]
        else:
            node_outputs = get_all_task_output_names(
                node_attrs["task_type"], node_attrs["task_identifier"]
            )
        svg_task = SvgTask(
            task_name=node_id,
            input_names=node_inputs,
            output_names=node_outputs,
        )
        svg_tasks_by_id[node_id] = svg_task
        task_desc = {
            "id": node_id,
            "width": svg_task.width,
            "height": svg_task.height,
            "layoutOptions": {"org.eclipse.elk.portConstraints": "FIXED_POS"},
            "ports": svg_task.elk_ports(),
        }
        elk_graph["children"].append(task_desc)

    for source, target, link_attrs in graph.graph.edges(data=True):
        data_mapping = link_attrs.get("data_mapping") or []
        if data_mapping:
            for index, mapping in enumerate(data_mapping):
                edge_id = f"edge_{source}_{target}_{index}"
                source_output = mapping.get("source_output")
                target_input = mapping.get("target_input")
                source_endpoint = source
                if source_output is not None:
                    source_endpoint = svg_tasks_by_id[source].output_port_id(
                        source_output
                    )
                target_endpoint = target
                if target_input is not None:
                    target_endpoint = svg_tasks_by_id[target].input_port_id(
                        target_input
                    )
                edge_desc = {
                    "id": edge_id,
                    "sources": [source_endpoint],
                    "targets": [target_endpoint],
                }
                elk_graph["edges"].append(edge_desc)
                link_metadata_by_id[edge_id] = {
                    "source_node_id": str(source),
                    "source_output": (
                        None if source_output is None else str(source_output)
                    ),
                    "target_node_id": str(target),
                    "target_input": (
                        None if target_input is None else str(target_input)
                    ),
                    "map_all_data": False,
                }
        else:
            edge_id = f"edge_{source}_{target}"
            edge_desc = {
                "id": edge_id,
                "sources": [source],
                "targets": [target],
            }
            elk_graph["edges"].append(edge_desc)
            link_metadata_by_id[edge_id] = {
                "source_node_id": str(source),
                "source_output": None,
                "target_node_id": str(target),
                "target_input": None,
                "map_all_data": bool(link_attrs.get("map_all_data")),
            }

    elk = ELK()
    result = elk.layout(elk_graph)
    link_coordinates = extract_link_coordinates(result)

    # Compute Canvas size should be done directly in Canvas object.
    children = result["children"]
    max_x = max(
        (child["x"] + child["width"] for child in children),
        default=CANVAS_MARGIN,
    )
    max_y = max(
        (child["y"] + child["height"] for child in children),
        default=CANVAS_MARGIN,
    )
    for link in link_coordinates:
        for section in link["sections"]:
            for point in section["points"]:
                max_x = max(max_x, point["x"])
                max_y = max(max_y, point["y"])
    canvas_width = max_x + CANVAS_MARGIN
    canvas_height = max_y + CANVAS_MARGIN

    canvas = SvgCanvas(width=canvas_width, height=canvas_height)
    svg_background = SvgBackground(canvas_width, canvas_height)
    canvas.add_element(svg_background)

    for child in children:
        svg_task = svg_tasks_by_id[child["id"]]
        svg_task.set_translation(x=child["x"], y=child["y"])

        canvas.add_element(svg_task)

    for link in link_coordinates:
        link_metadata = link_metadata_by_id.get(link["id"], {})
        for section in link["sections"]:
            if section["points"]:
                canvas.add_element(
                    SvgLink(
                        section["points"],
                        section.get("routing"),
                        link.get("color"),
                        link_id=link["id"],
                        **link_metadata,
                    )
                )

    return canvas.to_string()
