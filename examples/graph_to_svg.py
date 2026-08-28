import argparse
from pathlib import Path

from ewokscore import load_graph
from ewokscore.tests.examples.graphs import get_graph

from ewoksdraw import graph_to_svg

parser = argparse.ArgumentParser()
parser.add_argument("workflow", nargs="?", default="acyclic1")
parser.add_argument("--test", action="store_true", default=False)
args = parser.parse_args()

if args.test or args.workflow == "acyclic1":
    graph_to_load, _ = get_graph(args.workflow)
else:
    graph_to_load = args.workflow

graph = load_graph(graph_to_load)
output_path = Path("examples") / f"{Path(args.workflow).name}.svg"
graph_to_svg(graph, output_path)
print(f"Wrote {output_path}")
