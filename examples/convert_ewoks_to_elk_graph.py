from pprint import pprint

from ewokscore import load_graph
from ewokscore.tests.examples.graphs import get_graph
from ewoksdraw import build_svg_task_group
from ewoksdraw.layout.elk_converter import ElkGraph
from ewoksdraw.layout.elk_converter import convert_ewoks_to_elk_graph
from ewoksdraw.svg.svg_task_group import SvgTaskGroup
from ewoksdraw.svg.svg_task_group import TaskSizes

graph_description, _ = get_graph("acyclic1")
ewoks_graph = load_graph(graph_description)

svg_task_group: SvgTaskGroup = build_svg_task_group(ewoks_graph)
task_sizes: TaskSizes = svg_task_group.extract_task_sizes()
elk_graph: ElkGraph = convert_ewoks_to_elk_graph(ewoks_graph, task_sizes)

pprint(dict(ewoks_graph.graph.nodes(data=True)))
pprint(list(ewoks_graph.graph.edges(data=True)))
pprint(task_sizes)
pprint(elk_graph)
