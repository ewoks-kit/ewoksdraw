from pathlib import Path

import pytest
from defusedxml import ElementTree
from ewokscore import load_graph
from ewokscore.tests.examples.graphs import get_graph
from ewokscore.tests.examples.graphs import graph_names

from ewoksdraw import graph_to_svg


def _get_svg_groups(output_path: Path):
    tree = ElementTree.parse(output_path)
    root = tree.getroot()
    return [child for child in root if child.tag.endswith("g")]


@pytest.mark.parametrize("graph_name", graph_names())
def test_groups_are_matching_nodes(graph_name, tmp_path: Path):
    output_path = tmp_path / f"{graph_name}.svg"

    graph, _ = get_graph(graph_name)
    ewoksgraph = load_graph(graph)

    graph_to_svg(ewoksgraph, output_path)

    assert output_path.is_file()

    groups = _get_svg_groups(output_path)
    for group, node_name in zip(groups, ewoksgraph.graph.nodes.keys()):
        assert group[0].text == node_name
