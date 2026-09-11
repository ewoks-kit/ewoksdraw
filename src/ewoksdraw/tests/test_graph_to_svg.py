import logging
from pathlib import Path
from xml.etree.ElementTree import Element

import pytest
from defusedxml import ElementTree
from ewokscore import load_graph
from ewokscore.graph import TaskGraph
from ewokscore.tests.examples.graphs import get_graph
from ewokscore.tests.examples.graphs import graph_names
from pytest import LogCaptureFixture

from ewoksdraw import graph_to_svg

pytestmark = pytest.mark.filterwarnings("ignore:.*uses 'map_all_data'.*:UserWarning")


@pytest.fixture(params=graph_names(), ids=graph_names())
def ewoks_graph(request: pytest.FixtureRequest) -> TaskGraph:
    graph_description, _ = get_graph(request.param)
    return load_graph(graph_description)


def _find_svg_group(parent: Element, group_id: str) -> Element:
    return next(
        child
        for child in parent
        if child.tag.endswith("g") and child.get("id") == group_id
    )


def _translation(group: Element) -> tuple[float, float]:
    transform = group.attrib["transform"]
    coordinates = transform.removeprefix("translate(").removesuffix(")").split(",")
    return float(coordinates[0]), float(coordinates[1])


def test_groups_are_matching_nodes(ewoks_graph: TaskGraph, tmp_path: Path) -> None:
    output_path = tmp_path / f"{ewoks_graph.graph_id}.svg"
    graph_to_svg(ewoks_graph, output_path)

    assert output_path.is_file()

    tree = ElementTree.parse(output_path)
    task_group = _find_svg_group(tree.getroot(), str(ewoks_graph.graph_id))
    for node_name in ewoks_graph.graph.nodes:
        svg_task = _find_svg_group(task_group, str(node_name))
        assert svg_task[0].text == node_name


def test_elk_positions_data_mapped_tasks(
    ewoks_graph: TaskGraph, tmp_path: Path
) -> None:
    """Testing Elk computed layout give left->right connected tasks position"""
    if ewoks_graph.is_cyclic:
        pytest.skip("Left-to-right edge ordering does not apply to cyclic workflows")

    output_path = tmp_path / f"{ewoks_graph.graph_id}.svg"
    graph_to_svg(ewoks_graph, output_path)

    # SVG
    root = ElementTree.parse(output_path).getroot()
    task_group = _find_svg_group(root, str(ewoks_graph.graph_id))
    positions: dict[str, tuple[float, float]] = {}

    # Ewoks Graph
    for task_id in ewoks_graph.graph.nodes:
        svg_task = _find_svg_group(task_group, task_id)
        task_position = _translation(svg_task)
        positions[task_id] = task_position

    for source, target, attributes in ewoks_graph.graph.edges(data=True):
        if not attributes.get("data_mapping"):
            continue

        assert positions[source][0] < positions[target][0]


def test_elk_links_are_rendered(ewoks_graph: TaskGraph, tmp_path: Path) -> None:
    output_path = tmp_path / f"{ewoks_graph.graph_id}.svg"
    graph_to_svg(ewoks_graph, output_path)

    # SVG
    root = ElementTree.parse(output_path).getroot()
    link_group = _find_svg_group(root, f"{ewoks_graph.graph_id}-links")
    links = [element for element in link_group if element.tag.endswith("path")]

    # Ewoks Graph
    expected_link_count = sum(
        len(attributes.get("data_mapping", []))
        for _, _, attributes in ewoks_graph.graph.edges(data=True)
    )
    assert len(links) == expected_link_count
    assert all(link.get("class") == "link_cubic_bezier" for link in links)
    assert all((link.get("d") or "").startswith("M ") for link in links)


def test_workflow_with_non_importable_task(
    tmp_path: Path, caplog: LogCaptureFixture
) -> None:
    output_path = tmp_path / "workflow1.svg"

    ewoksgraph = load_graph(Path(__file__).parent / "resources" / "workflow1.json")

    with caplog.at_level(logging.WARNING):
        graph_to_svg(ewoksgraph, output_path)

    assert "Cannot import 'not.a.task': No module named 'not'" in caplog.text
    assert output_path.is_file()

    tree = ElementTree.parse(output_path)
    task_group = _find_svg_group(tree.getroot(), str(ewoksgraph.graph_id))
    for node_name in ewoksgraph.graph.nodes:
        svg_task = _find_svg_group(task_group, str(node_name))
        assert svg_task[0].text == node_name
