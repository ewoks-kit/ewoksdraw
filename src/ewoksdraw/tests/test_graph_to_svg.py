from xml.etree import ElementTree

import pytest
from ewokscore import load_graph
from ewokscore.tests.examples.graphs import get_graph
from ewokscore.tests.examples.graphs import graph_names

from ewoksdraw import graph_to_svg


def _get_svg_groups(svg: str):
    root = ElementTree.fromstring(svg)
    return [child for child in root if child.tag.endswith("g")]


def _translation(group):
    transform = group.get("transform")
    assert transform is not None
    coordinates = transform.removeprefix("translate(").removesuffix(")").split(",")
    return tuple(float(coordinate) for coordinate in coordinates)


@pytest.mark.parametrize("graph_name", graph_names())
def test_groups_are_matching_nodes(graph_name):
    graph, _ = get_graph(graph_name)
    ewoksgraph = load_graph(graph)

    svg = graph_to_svg(ewoksgraph)

    groups = _get_svg_groups(svg)
    for group, node_name in zip(groups, ewoksgraph.graph.nodes.keys()):
        assert group[0].text == node_name
        assert group.get("id") == node_name
        assert group.get("class") == "ewoks-task"
        assert group.get("data-ewoks-node-id") == node_name


def test_svg_includes_packaged_styles(monkeypatch, tmp_path):
    graph, _ = get_graph("acyclic1")
    ewoksgraph = load_graph(graph)
    monkeypatch.chdir(tmp_path)

    svg = graph_to_svg(ewoksgraph)

    assert ".task_box" in svg
    assert ".link" in svg


def test_default_layout_separates_connected_tasks():
    graph, _ = get_graph("acyclic1")
    ewoksgraph = load_graph(graph)

    svg = graph_to_svg(ewoksgraph)
    groups = _get_svg_groups(svg)
    positions = {group.get("id"): _translation(group) for group in groups}

    for source, target in ewoksgraph.graph.edges:
        source_group = next(group for group in groups if group.get("id") == source)
        source_box = next(child for child in source_group if child.tag.endswith("rect"))
        source_right = positions[source][0] + float(source_box.get("width"))
        assert source_right < positions[target][0]


def test_links_use_spline_routing_by_default():
    graph, _ = get_graph("acyclic1")
    root = ElementTree.fromstring(graph_to_svg(load_graph(graph)))
    links = [child for child in root if child.get("class") == "link"]

    assert links
    assert all(" C " in (link.get("d") or "") for link in links)


def test_svg_has_scalable_view_box():
    graph, _ = get_graph("acyclic1")
    root = ElementTree.fromstring(graph_to_svg(load_graph(graph)))

    assert root.get("viewBox") == f"0 0 {root.get('width')} {root.get('height')}"


def test_svg_exposes_semantic_ports_and_links():
    graph, _ = get_graph("acyclic1")
    root = ElementTree.fromstring(graph_to_svg(load_graph(graph)))

    ports = [element for element in root.iter() if element.get("class") == "ewoks-port"]
    output_port = next(
        port
        for port in ports
        if port.get("data-ewoks-node-id") == "task1"
        and port.get("data-ewoks-port-kind") == "output"
        and port.get("data-ewoks-port-name") == "result"
    )
    assert output_port is not None

    links = [child for child in root if child.get("class") == "link"]
    link = next(
        item
        for item in links
        if item.get("data-ewoks-source-node-id") == "task1"
        and item.get("data-ewoks-target-node-id") == "task3"
    )
    assert link.get("data-ewoks-link-id") == "edge_task1_task3_0"
    assert link.get("data-ewoks-source-output") == "result"
    assert link.get("data-ewoks-target-input") == "a"
