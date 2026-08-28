from ewokscore.graph import TaskGraph
from ewokscore.graph.inputs import _get_all_node_inputs
from ewokscore.graph.inputs import _get_all_task_output_names

from ..config.constants import TASK_GROUP_HORIZONTAL_GAP
from ..svg.svg_task import SvgTask
from ..svg.svg_task_group import SvgTaskGroup


def build_svg_task_group(graph: TaskGraph) -> SvgTaskGroup:
    """Build an SVG task group from an Ewoks task graph."""
    svg_tasks = {}
    for node_id, node_attrs in graph.graph.nodes.items():
        node_inputs = _get_all_node_inputs(node_id, node_attrs)
        node_outputs = _get_all_task_output_names(
            node_attrs["task_type"], node_attrs["task_identifier"]
        )
        svg_tasks[node_id] = SvgTask(
            task_name=node_id,
            input_names=[node_input.name for node_input in node_inputs],
            output_names=node_outputs,
        )
    return SvgTaskGroup(
        svg_tasks,
        horizontal_gap=TASK_GROUP_HORIZONTAL_GAP,
        group_id=str(graph.graph_id),
    )
