from pathlib import Path

from ewokscore.graph import TaskGraph
from ewokscore.graph.inputs import _get_all_node_inputs
from ewokscore.graph.inputs import _get_all_task_output_names

from .svg import SvgCanvas
from .svg import SvgTask

GAP = 10
DEFAULT_HEIGHT = 500


def graph_to_svg(graph: TaskGraph, output_path: str | Path):
    svg_tasks = []
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
        svg_tasks.append(svg_task)
        svg_task.translate(x=width, y=GAP)
        width += svg_task.width + GAP

    if len(svg_tasks) > 0:
        height = max([svg_task.height for svg_task in svg_tasks])
    else:
        height = DEFAULT_HEIGHT
    canvas = SvgCanvas(width=width, height=height + 2 * GAP)
    canvas.add_background()
    for svg_task in svg_tasks:
        canvas.add_element(svg_task)
    canvas.draw(output_path)
