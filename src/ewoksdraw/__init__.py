from pathlib import Path

from ewokscore.graph import TaskGraph
from ewokscore.graph.inputs import _get_all_node_inputs
from ewokscore.graph.inputs import _get_all_task_output_names

from ewoksdraw.svg.svg_line import SvgLine

from .svg import SvgCanvas
from .svg import SvgTask

GAP = 10
DEFAULT_HEIGHT = 500


def graph_to_svg(graph: TaskGraph, output_path: str | Path):
    svg_tasks: dict[str, SvgTask] = {}
    width = GAP
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
        svg_task.translate(x=width, y=GAP)
        width += svg_task.width + GAP
        svg_tasks[node_id] = svg_task

    lines = []
    for link_id, link_attrs in graph.graph.edges.items():
        data_mapping = link_attrs.get("data_mapping", None)
        if not data_mapping:
            continue

        source_id, target_id = link_id

        for mapping in data_mapping:
            x1, y1 = svg_tasks[source_id].get_output_pos(mapping["source_output"])
            x2, y2 = svg_tasks[target_id].get_input_pos(mapping["target_input"])

            lines.append(SvgLine(x1, y1, x2, y2))

    if len(svg_tasks) > 0:
        height = max([svg_task.height for svg_task in svg_tasks.values()])
    else:
        height = DEFAULT_HEIGHT
    canvas = SvgCanvas(width=width, height=height + 2 * GAP)
    canvas.add_background()
    for svg_task in svg_tasks.values():
        canvas.add_element(svg_task)
    for line in lines:
        canvas.add_element(line)

    canvas.draw(output_path)
