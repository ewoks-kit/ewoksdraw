import subprocess
from pathlib import Path
from xml.etree import ElementTree

from ewokscore import load_graph


def _get_svg_groups(output_path: Path):
    tree = ElementTree.parse(output_path)
    root = tree.getroot()
    return [child for child in root if child.tag.endswith("g")]


def test_groups_are_matching_nodes(tmp_path: Path):
    output_path = tmp_path / "test.svg"
    subprocess.run(
        ("ewoksdraw", "demo", "--test", "--output_svg", output_path), check=True
    )

    assert output_path.is_file()

    groups = _get_svg_groups(output_path)
    demo_graph = load_graph("demo", representation="test_core").graph
    for group, node_name in zip(groups, demo_graph.nodes.keys()):
        assert group[0].text == node_name
