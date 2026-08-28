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


def _translation(group: Element) -> tuple[float, float]:
    transform = group.get("transform")
    assert transform is not None
    coordinates = transform.removeprefix("translate(").removesuffix(")").split(",")
    return float(coordinates[0]), float(coordinates[1])


@pytest.mark.parametrize("graph_name", graph_names())
@pytest.mark.filterwarnings("ignore:.*uses 'map_all_data'.*:UserWarning")
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


def test_elk_positions_connected_tasks(tmp_path: Path) -> None:
    """Testing Elk computed layout give left->right connected tasks position"""
    output_path = tmp_path / "acyclic1.svg"
    graph_description, _ = get_graph("acyclic1")
    graph = load_graph(graph_description)

    graph_to_svg(graph, output_path)

    root = ElementTree.parse(output_path).getroot()
    task_group = _find_svg_group(root, str(graph.graph_id))
    positions = {
        task_id: _translation(_find_svg_group(task_group, task_id))
        for task_id in graph.graph.nodes
    }
    for source, target in graph.graph.edges:
        assert positions[source][0] < positions[target][0]


def test_elk_links_are_rendered(tmp_path: Path) -> None:
    output_path = tmp_path / "acyclic1.svg"
    graph_description, _ = get_graph("acyclic1")
    graph = load_graph(graph_description)

    graph_to_svg(graph, output_path)

    root = ElementTree.parse(output_path).getroot()
    link_group = _find_svg_group(root, f"{graph.graph_id}-links")
    links = [element for element in link_group if element.tag.endswith("path")]

    expected_link_count = sum(
        len(attributes.get("data_mapping", []))
        for _, _, attributes in graph.graph.edges(data=True)
    )
    assert len(links) == expected_link_count
    assert all(link.get("class") == "link_cubic_bezier" for link in links)
    assert all((link.get("d") or "").startswith("M ") for link in links)
