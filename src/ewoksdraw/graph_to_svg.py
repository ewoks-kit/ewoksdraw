from pathlib import Path

from ewokscore.graph import TaskGraph
from ewokscore.node.signature import node_signature

from ._config.constants import TASK_GROUP_HORIZONTAL_GAP
from ._layout.elk_backend import layout
from ._layout.elk_converter import ElkGraph
from ._layout.elk_converter import ElkGraphBeforeLayout
from ._layout.elk_converter import convert_ewoks_to_elk_graph
from ._layout.elk_converter import extract_task_positions_from_elk_graph
from ._layout.elk_link_group_builder import build_svg_link_group
from ._svg.svg_canvas import SvgCanvas
from ._svg.svg_task import SvgTask
from ._svg.svg_task_group import SvgTaskGroup
from ._utils import get_edge_sources_and_targets


def _build_svg_task_group(graph: TaskGraph) -> SvgTaskGroup:
    """Build an SVG task group from an Ewoks task graph."""
    source_outputs_per_node, target_inputs_per_node = get_edge_sources_and_targets(
        graph
    )

    svg_tasks = {}
    for node_id, node_attrs in graph.graph.nodes.items():
        signature = node_signature(node_id, node_attrs)

        # Use dict instead of set to remove duplicate while keeping order
        inputs = dict.fromkeys(node_input.name for node_input in signature.inputs)
        # Add eventual missing target inputs
        inputs.update(dict.fromkeys(target_inputs_per_node[node_id]))

        outputs = dict.fromkeys(node_output.name for node_output in signature.outputs)
        # Add eventual missing source outputs
        outputs.update(dict.fromkeys(source_outputs_per_node[node_id]))

        svg_tasks[node_id] = SvgTask(
            task_name=node_id,
            input_names=list(inputs.keys()),
            output_names=list(outputs.keys()),
            import_error=bool(signature.import_error),
        )
    return SvgTaskGroup(
        svg_tasks,
        horizontal_gap=TASK_GROUP_HORIZONTAL_GAP,
        group_id=str(graph.graph_id),
    )


def graph_to_svg(graph: TaskGraph, output_path: str | Path) -> None:
    task_group = _build_svg_task_group(graph)
    elk_graph_before_layout: ElkGraphBeforeLayout = convert_ewoks_to_elk_graph(
        graph,
        task_group.extract_task_sizes(),
        task_group.extract_input_positions(),
        task_group.extract_output_positions(),
    )
    elk_graph: ElkGraph = layout(elk_graph_before_layout)

    task_positions = extract_task_positions_from_elk_graph(elk_graph)
    task_group.set_task_positions(task_positions)

    canvas = SvgCanvas(width=elk_graph["width"], height=elk_graph["height"])
    canvas.add_background()
    canvas.add_element(
        build_svg_link_group(
            elk_graph,
            task_group.extract_import_errors(),
            group_id=f"{graph.graph_id}-links",
        )
    )
    canvas.add_element(task_group)
    canvas.draw(output_path)
