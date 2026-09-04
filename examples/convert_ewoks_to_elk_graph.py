from pprint import pprint

from ewokscore import load_graph
from ewokscore.tests.examples.graphs import get_graph

from ewoksdraw.layout.elk_converter import ElkGraphBeforeLayout
from ewoksdraw.layout.elk_converter import convert_ewoks_to_elk_graph
from ewoksdraw.layout.ewoks_task_group_builder import build_svg_task_group
from ewoksdraw.svg.svg_task_group import SvgTaskGroup
from ewoksdraw.svg.svg_task_group import TaskInputPositions
from ewoksdraw.svg.svg_task_group import TaskOutputPositions
from ewoksdraw.svg.svg_task_group import TaskSizes

graph_description, _ = get_graph("acyclic1")
ewoks_graph = load_graph(graph_description)

svg_task_group: SvgTaskGroup = build_svg_task_group(ewoks_graph)
task_sizes: TaskSizes = svg_task_group.extract_task_sizes()
task_input_positions: TaskInputPositions = svg_task_group.extract_input_positions()
task_output_positions: TaskOutputPositions = svg_task_group.extract_output_positions()
elk_graph: ElkGraphBeforeLayout = convert_ewoks_to_elk_graph(
    ewoks_graph, task_sizes, task_input_positions, task_output_positions
)

pprint(dict(ewoks_graph.graph.nodes(data=True)))
pprint(list(ewoks_graph.graph.edges(data=True)))
pprint(task_sizes)
pprint(task_input_positions)
pprint(task_output_positions)
pprint(elk_graph)
