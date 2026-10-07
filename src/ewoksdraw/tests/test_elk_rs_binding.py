import math
from typing import Any
from typing import Literal
from typing import cast

import pytest

from ewoksdraw import _elk_rs
from ewoksdraw.layout.elk_backend import ElkLayoutError
from ewoksdraw.layout.elk_backend import layout
from ewoksdraw.layout.elk_converter import ElkGraph
from ewoksdraw.layout.elk_converter import ElkGraphBeforeLayout

NODE_WIDTH = 100
NODE_HEIGHT = 60
INPUT_Y = (20, 40)
OUTPUT_Y = (30,)


def _node(node_id: str) -> dict[str, Any]:
    ports = [
        {
            "id": f"{node_id}.in{i}",
            "x": 0,
            "y": y,
            "width": 0,
            "height": 0,
            "layoutOptions": {
                "org.eclipse.elk.port.side": "WEST",
                "org.eclipse.elk.port.index": i,
                "org.eclipse.elk.port.borderOffset": 0,
            },
        }
        for i, y in enumerate(INPUT_Y)
    ]
    ports += [
        {
            "id": f"{node_id}.out{i}",
            "x": NODE_WIDTH,
            "y": y,
            "width": 0,
            "height": 0,
            "layoutOptions": {
                "org.eclipse.elk.port.side": "EAST",
                "org.eclipse.elk.port.index": i,
                "org.eclipse.elk.port.borderOffset": 0,
            },
        }
        for i, y in enumerate(OUTPUT_Y)
    ]
    return {
        "id": node_id,
        "width": NODE_WIDTH,
        "height": NODE_HEIGHT,
        "layoutOptions": {"org.eclipse.elk.portConstraints": "FIXED_POS"},
        "ports": ports,
    }


def _graph(
    node_ids: list[str], links: list[tuple[str, str]], routing: str = "ORTHOGONAL"
) -> ElkGraphBeforeLayout:
    return cast(
        ElkGraphBeforeLayout,
        {
            "id": "root",
            "layoutOptions": {
                "org.eclipse.elk.algorithm": "layered",
                "org.eclipse.elk.direction": "RIGHT",
                "org.eclipse.elk.edgeRouting": routing,
            },
            "children": [_node(node_id) for node_id in node_ids],
            "edges": [
                {
                    "id": f"{source}->{target}",
                    "sources": [f"{source}.out0"],
                    "targets": [f"{target}.in0"],
                }
                for source, target in links
            ],
        },
    )


def _absolute_ports(result: ElkGraph) -> dict[str, tuple[float, float]]:
    return {
        port["id"]: (node["x"] + port["x"], node["y"] + port["y"])
        for node in result["children"]
        for port in node["ports"]
    }


@pytest.mark.parametrize(
    "node_ids, links",
    [
        (["a", "b"], [("a", "b")]),
        (["a", "b", "c"], [("a", "b"), ("a", "c")]),  # branching
        (["a", "b", "c"], [("a", "b")]),  # disconnected node
        (["a", "b"], [("a", "b"), ("b", "a")]),  # cycle
        (["a"], [("a", "a")]),  # self-loop
    ],
)
def test_orthogonal_layout_contract(
    node_ids: list[str], links: list[tuple[str, str]]
) -> None:
    result = layout(_graph(node_ids, links))

    assert result["width"] > 0 and result["height"] > 0

    # Nodes are placed and fixed ports are kept at their input offsets.
    assert [node["id"] for node in result["children"]] == node_ids
    for node in result["children"]:
        assert math.isfinite(node["x"]) and math.isfinite(node["y"])
        assert {port["id"]: port["y"] for port in node["ports"]} == {
            f"{node['id']}.in0": INPUT_Y[0],
            f"{node['id']}.in1": INPUT_Y[1],
            f"{node['id']}.out0": OUTPUT_Y[0],
        }

    # Every edge has sections that start/end on its ports and are orthogonal.
    ports = _absolute_ports(result)
    assert len(result["edges"]) == len(links)
    for edge in result["edges"]:
        assert edge["sections"]
        for section in edge["sections"]:
            points = [
                section["startPoint"],
                *section.get("bendPoints", []),
                section["endPoint"],
            ]
            for p, q in zip(points, points[1:]):
                assert p["x"] == pytest.approx(q["x"]) or p["y"] == pytest.approx(
                    q["y"]
                ), f"diagonal segment in {edge['id']}: {p} -> {q}"
        start = edge["sections"][0]["startPoint"]
        end = edge["sections"][-1]["endPoint"]
        assert (start["x"], start["y"]) == pytest.approx(ports[edge["sources"][0]])
        assert (end["x"], end["y"]) == pytest.approx(ports[edge["targets"][0]])


def test_edge_points_within_canvas() -> None:
    result = layout(_graph(["a", "b", "c"], [("a", "b"), ("a", "c"), ("b", "c")]))

    for edge in result["edges"]:
        for section in edge["sections"]:
            for point in [
                section["startPoint"],
                *section.get("bendPoints", []),
                section["endPoint"],
            ]:
                assert 0 <= point["x"] <= result["width"]
                assert 0 <= point["y"] <= result["height"]


def test_empty_graph() -> None:
    result = layout({"id": "root", "layoutOptions": {}, "children": [], "edges": []})

    assert result["width"] == 0 and result["height"] == 0
    assert result["children"] == []


@pytest.mark.parametrize(
    "graph_json, message",
    [
        ("{not json", "Failed to parse graph JSON"),
        ("[]", "must be a json object"),
        ("{}", "Every element must have an id"),
    ],
)
def test_invalid_graph_raises(graph_json: str, message: str) -> None:
    with pytest.raises(RuntimeError, match=message):
        _elk_rs.layout_json(graph_json)


def test_invalid_options_raises() -> None:
    with pytest.raises(RuntimeError, match="Failed to parse options JSON"):
        _elk_rs.layout_json('{"id": "root"}', "{bad")


def test_unknown_port_raises() -> None:
    graph = _graph(["a"], [])
    graph["edges"] = [{"id": "e", "sources": ["a.out0"], "targets": ["missing"]}]

    with pytest.raises(ElkLayoutError, match="Referenced shape does not exist"):
        layout(graph)


def test_unknown_algorithm_raises() -> None:
    graph = _graph(["a"], [])
    graph["layoutOptions"]["org.eclipse.elk.algorithm"] = "nope"

    with pytest.raises(ElkLayoutError, match="Layout algorithm 'nope' not found"):
        layout(graph)


def _with_options(graph: ElkGraphBeforeLayout, **options: Any) -> ElkGraphBeforeLayout:
    graph["layoutOptions"].update(options)
    return graph


@pytest.mark.parametrize(
    "option, size_key",
    [
        ("org.eclipse.elk.spacing.nodeNode", "height"),
        ("org.eclipse.elk.layered.spacing.nodeNodeBetweenLayers", "width"),
    ],
)
def test_spacing_options_are_applied(
    option: str, size_key: Literal["width", "height"]
) -> None:
    links = [("a", "b"), ("a", "c")]
    small = layout(_with_options(_graph(["a", "b", "c"], links), **{option: 10}))
    large = layout(_with_options(_graph(["a", "b", "c"], links), **{option: 200}))

    assert large[size_key] > small[size_key]


def test_edges_have_a_single_section_and_optional_bend_points() -> None:
    result = layout(_graph(["a", "b", "c"], [("a", "b"), ("a", "c")]))

    sections = [edge["sections"] for edge in result["edges"]]
    assert all(len(edge_sections) == 1 for edge_sections in sections)
    # Straight edges have no "bendPoints" key at all.
    assert any("bendPoints" not in s[0] for s in sections)


def test_back_edges_route_around_nodes() -> None:
    result = layout(_graph(["a", "b"], [("a", "b"), ("b", "a")]))

    sections = [edge["sections"][0] for edge in result["edges"]]
    back_sections = [s for s in sections if s["endPoint"]["x"] < s["startPoint"]["x"]]
    assert len(back_sections) == 1
    assert len(back_sections[0]["bendPoints"]) >= 2


@pytest.mark.parametrize("routing", ["SPLINES", "POLYLINE"])
def test_unsupported_edge_routing_raises(routing: str) -> None:
    with pytest.raises(
        ValueError,
        match="SVG rendering currently supports only ORTHOGONAL edge routing",
    ):
        layout(_graph(["a", "b"], [("a", "b")], routing))
