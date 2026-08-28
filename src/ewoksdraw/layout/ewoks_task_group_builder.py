from ewokscore.graph import TaskGraph
from ewokscore.node.signature import node_signature

from ..config.constants import TASK_GROUP_HORIZONTAL_GAP
from ..svg.svg_task import SvgTask
from ..svg.svg_task_group import SvgTaskGroup


def build_svg_task_group(graph: TaskGraph) -> SvgTaskGroup:
    """Build an SVG task group from an Ewoks task graph."""
    svg_tasks = {}
    for node_id, node_attrs in graph.graph.nodes.items():
        signature = node_signature(node_id, node_attrs)
        svg_tasks[node_id] = SvgTask(
            task_name=node_id,
            input_names=[node_input.name for node_input in signature.inputs],
            output_names=[node_output.name for node_output in signature.outputs],
            import_error=bool(signature.import_error),
        )
    return SvgTaskGroup(
        svg_tasks,
        horizontal_gap=TASK_GROUP_HORIZONTAL_GAP,
        group_id=str(graph.graph_id),
    )
