import random
from pathlib import Path

from ewokscore.graph import TaskGraph
from ewokscore.graph.inputs import _get_all_node_inputs
from ewokscore.graph.inputs import _get_all_task_output_names

from .svg import SvgBackground
from .svg import SvgCanvas
from .svg import SvgTask


def graph_to_svg(graph: TaskGraph, output_path: str | Path):
    canvas_width = 500
    canvas_height = 500

    canvas = SvgCanvas(width=canvas_width, height=canvas_height)
    svg_background = SvgBackground(canvas_width, canvas_height)
    canvas.add_element(svg_background)

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

        svg_task.translate(x=random.randint(5, 400), y=random.randint(5, 400))

        canvas.add_element(svg_task)

    canvas.draw(output_path)
