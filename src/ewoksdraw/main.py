import argparse
import random

from ewokscore import load_graph
from ewokscore.graph.inputs import _get_all_node_inputs
from ewokscore.graph.inputs import _get_all_task_output_names

from .svg import SvgBackground
from .svg import SvgCanvas
from .svg import SvgTask


def main():
    parser = argparse.ArgumentParser(description="Saves a worfklow as SVG")

    parser.add_argument("workflow", type=str, help="Workflow to save to SVG")
    parser.add_argument(
        "--test",
        help="The 'workflow' argument refers to the name of a test graph.",
        action="store_true",
    )
    parser.add_argument(
        "--output_svg", type=str, required=True, help="Output SVG file path"
    )

    args = parser.parse_args()

    canvas_width = 500
    canvas_height = 500

    canvas = SvgCanvas(width=canvas_width, height=canvas_height)
    svg_background = SvgBackground(canvas_width, canvas_height)
    canvas.add_element(svg_background)

    if args.test:
        representation = "test_core"
    else:
        representation = None
    graph = load_graph(args.workflow, representation=representation).graph

    for node_id, node_attrs in graph.nodes.items():
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

    canvas.draw(args.output_svg)


if __name__ == "__main__":
    main()
