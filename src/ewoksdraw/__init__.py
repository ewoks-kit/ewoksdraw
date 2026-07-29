from pathlib import Path

from ewokscore.graph import TaskGraph
from ewokscore.graph.inputs import _get_all_node_inputs
from ewokscore.graph.inputs import _get_all_task_output_names

from .svg.svg_canvas import SvgCanvas
from .svg.svg_task import SvgTask
from .svg.svg_task_group import SvgTaskGroup

GAP = 10.0
DEFAULT_HEIGHT = 500


def build_svg_task_group(graph: TaskGraph) -> SvgTaskGroup:
    svg_tasks = {}
    for node_id, node_attrs in graph.graph.nodes.items():
        node_inputs = _get_all_node_inputs(node_id, node_attrs)
        node_outputs = _get_all_task_output_names(
            node_attrs["task_type"], node_attrs["task_identifier"]
        )
        svg_tasks[node_id] = SvgTask(
            task_name=node_id,
            input_names=[n.name for n in node_inputs],
            output_names=node_outputs,
        )
    return SvgTaskGroup(svg_tasks, horizontal_gap=GAP, group_id=str(graph.graph_id))


def graph_to_svg(graph: TaskGraph, output_path: str | Path):
    task_group = build_svg_task_group(graph)
    canvas = SvgCanvas(width=task_group.width, height=task_group.height + 2 * GAP)
    canvas.add_background()
    canvas.add_element(task_group)
    canvas.draw(output_path)
