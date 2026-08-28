from pathlib import Path

from ewokscore.graph import TaskGraph
from pyelk import ELK

from .layout.elk_converter import ElkGraph
from .layout.elk_converter import LaidOutElkGraph
from .layout.elk_converter import convert_ewoks_to_elk_graph
from .layout.elk_converter import extract_task_positions_from_elk_graph
from .layout.elk_link_group_builder import build_svg_link_group
from .layout.ewoks_task_group_builder import build_svg_task_group
from .svg.svg_canvas import SvgCanvas


def graph_to_svg(graph: TaskGraph, output_path: str | Path) -> None:
    task_group = build_svg_task_group(graph)
    elk_graph: ElkGraph = convert_ewoks_to_elk_graph(
        graph,
        task_group.extract_task_sizes(),
        task_group.extract_input_positions(),
        task_group.extract_output_positions(),
    )
    laid_out_graph: LaidOutElkGraph = ELK().layout(elk_graph)

    task_positions = extract_task_positions_from_elk_graph(laid_out_graph)
    task_group.set_task_positions(task_positions)

    canvas = SvgCanvas(width=laid_out_graph["width"], height=laid_out_graph["height"])
    canvas.add_background()
    canvas.add_element(
        build_svg_link_group(laid_out_graph, group_id=f"{graph.graph_id}-links")
    )
    canvas.add_element(task_group)
    canvas.draw(output_path)
