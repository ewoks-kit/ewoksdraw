from pathlib import Path
from xml.etree.ElementTree import Element

import pytest
from defusedxml import ElementTree
from ewokscore import load_graph
from ewokscore.tests.examples.graphs import get_graph
from ewokscore.tests.examples.graphs import graph_names

from ewoksdraw import graph_to_svg


def _find_svg_group(parent: Element, group_id: str) -> Element:
    return next(
        child
        for child in parent
        if child.tag.endswith("g") and child.get("id") == group_id
    )


@pytest.mark.parametrize("graph_name", graph_names())
def test_groups_are_matching_nodes(graph_name: str, tmp_path: Path) -> None:
    output_path = tmp_path / f"{graph_name}.svg"

    graph, _ = get_graph(graph_name)
    ewoksgraph = load_graph(graph)

    graph_to_svg(ewoksgraph, output_path)

    assert output_path.is_file()

    tree = ElementTree.parse(output_path)
    task_group = _find_svg_group(tree.getroot(), str(ewoksgraph.graph_id))
    for node_name in ewoksgraph.graph.nodes:
        svg_task = _find_svg_group(task_group, str(node_name))
        assert svg_task[0].text == node_name
