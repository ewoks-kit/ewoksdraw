import random
from pathlib import Path

from ewokscore.graph import TaskGraph
from ewokscore.graph.inputs import _get_all_node_inputs
from ewokscore.graph.inputs import _get_all_task_output_names

from .svg import SvgBackground
from .svg import SvgCanvas
from .svg import SvgLink
from .svg import SvgTask

from pyelk import ELK

CANVAS_MARGIN = 20


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


# def graph_to_svg(graph: TaskGraph, output_path: str | Path):
#     canvas_width = 1000
#     canvas_height = 1000

#     canvas = SvgCanvas(width=canvas_width, height=canvas_height)
#     svg_background = SvgBackground(canvas_width, canvas_height)
#     canvas.add_element(svg_background)

#     for node_id, node_attrs in graph.graph.nodes.items():
#         node_inputs = _get_all_node_inputs(node_id, node_attrs)
#         node_outputs = _get_all_task_output_names(
#             node_attrs["task_type"], node_attrs["task_identifier"]
#         )
#         svg_task = SvgTask(
#             task_name=node_id,
#             input_names=[n.name for n in node_inputs],
#             output_names=node_outputs,
#         )

#         svg_task.translate(x=random.randint(5, 1000), y=random.randint(5, 1000))

#         canvas.add_element(svg_task)

#     canvas.draw(output_path)


def graph_to_svg(
    graph: TaskGraph,
    layout_option: dict | str | Path | None = None,
    graph_path: str | Path | None = None,
):
    if graph_path is None:
        graph_path = layout_option
        layout_option = {}

    svg_tasks_by_id = {}
    layout_options = dict(layout_option or {})
    edge_routing = layout_options.pop("elk.edgeRouting", "ORTHOGONAL")
    edge_routing = layout_options.pop("org.eclipse.elk.edgeRouting", edge_routing)
    layout_options["org.eclipse.elk.edgeRouting"] = edge_routing

    elk_graph = {"id":"root","layoutOptions":layout_options,"children":[],"edges":[]}

    for node_id, node_attrs in graph.graph.nodes.items():
        node_inputs = _get_all_node_inputs(node_id, node_attrs)
        node_outputs = _get_all_task_output_names(
            node_attrs["task_type"], node_attrs["task_identifier"]
        )
        svg_task = SvgTask(
            task_name=node_id,
            input_names=[n.name for n in node_inputs],
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
                edge_desc = {
                    "id": f"edge_{source}_{target}_{index}",
                    "sources": [
                        svg_tasks_by_id[source].output_port_id(
                            mapping["source_output"]
                        )
                    ],
                    "targets": [
                        svg_tasks_by_id[target].input_port_id(mapping["target_input"])
                    ],
                }
                elk_graph["edges"].append(edge_desc)
        else:
            edge_desc = {
                "id": f"edge_{source}_{target}",
                "sources": [source],
                "targets": [target],
            }
            elk_graph["edges"].append(edge_desc)

    
    elk = ELK()
    result = elk.layout(elk_graph)
    link_coordinates = extract_link_coordinates(result)

    # Compute Canvas size should be done directly in Canvas object.
    children = result["children"]
    max_x = max(child["x"] + child["width"] for child in children)
    max_y = max(child["y"] + child["height"] for child in children)
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
        for section in link["sections"]:
            if section["points"]:
                canvas.add_element(
                    SvgLink(
                        section["points"],
                        section.get("routing"),
                        link.get("color"),
                    )
                )
    
    canvas.draw(graph_path)
    return link_coordinates



    

    

    

    
    
