import argparse
from pathlib import Path

from ewokscore import load_graph
from ewokscore.tests.examples.graphs import get_graph

from ewoksdraw import graph_to_svg

parser = argparse.ArgumentParser()
parser.add_argument("workflow", nargs="?", default="acyclic1")
args = parser.parse_args()

graph_description, _ = get_graph(args.workflow)
graph = load_graph(graph_description)
output_path = Path("examples") / f"{args.workflow}.svg"
graph_to_svg(graph, output_path)
print(f"Wrote {output_path}")
