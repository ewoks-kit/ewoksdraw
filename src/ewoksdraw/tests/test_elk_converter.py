import pytest
from ewokscore import load_graph
from ewokscore.tests.examples.graphs import get_graph
from ewokscore.tests.examples.graphs import graph_names

from ewoksdraw.layout.elk_converter import LAYOUT_OPTIONS
from ewoksdraw.layout.elk_converter import convert_ewoks_to_elk_graph

_TASK_TYPE = "ewokscore.tests.examples.tasks.sumtask.SumTask"


def _node(node_id: str) -> dict:
    return {"id": node_id, "task_type": "class", "task_identifier": _TASK_TYPE}


def _task_sizes(graph) -> dict[str, tuple[float, float]]:
    return {
        node_id: (10.0 * i, 20.0 * i)
        for i, node_id in enumerate(graph.graph.nodes, start=1)
    }


def test_top_level_structure():
    graph_description, _ = get_graph("acyclic1")
    graph = load_graph(graph_description)

    elk_graph = convert_ewoks_to_elk_graph(graph, _task_sizes(graph))

    assert elk_graph["id"] == "root"
    assert elk_graph["layoutOptions"] == LAYOUT_OPTIONS
    assert "children" in elk_graph
    assert "edges" in elk_graph


def test_children_match_task_sizes():
    graph_description, _ = get_graph("acyclic1")
    graph = load_graph(graph_description)
    task_sizes = _task_sizes(graph)

    elk_graph = convert_ewoks_to_elk_graph(graph, task_sizes)

    assert len(elk_graph["children"]) == len(task_sizes)
    for child in elk_graph["children"]:
        width, height = task_sizes[child["id"]]
        assert child["width"] == width
        assert child["height"] == height


def test_link_without_data_mapping_produces_one_elk_edge():
    graph_description = {
        "graph": {"id": "g", "label": "g", "schema_version": "1.1"},
        "nodes": [_node("a"), _node("b")],
        "links": [{"source": "a", "target": "b"}],
    }
    graph = load_graph(graph_description)

    elk_graph = convert_ewoks_to_elk_graph(graph, {"a": (1.0, 1.0), "b": (1.0, 1.0)})

    assert elk_graph["edges"] == [
        {"id": "edge_a_b_0", "sources": ["a"], "targets": ["b"]}
    ]


def test_link_with_multiple_data_mappings_produces_one_elk_edge_per_mapping():
    graph_description = {
        "graph": {"id": "g", "label": "g", "schema_version": "1.1"},
        "nodes": [_node("a"), _node("b")],
        "links": [
            {
                "source": "a",
                "target": "b",
                "data_mapping": [
                    {"source_output": "result", "target_input": "a"},
                    {"source_output": "result", "target_input": "b"},
                ],
            }
        ],
    }
    graph = load_graph(graph_description)

    elk_graph = convert_ewoks_to_elk_graph(graph, {"a": (1.0, 1.0), "b": (1.0, 1.0)})

    assert elk_graph["edges"] == [
        {"id": "edge_a_b_0", "sources": ["a"], "targets": ["b"]},
        {"id": "edge_a_b_1", "sources": ["a"], "targets": ["b"]},
    ]


def test_graph_without_link():
    graph_description, _ = get_graph("empty")
    graph = load_graph(graph_description)

    elk_graph = convert_ewoks_to_elk_graph(graph, {})

    assert elk_graph["children"] == []
    assert elk_graph["edges"] == []


@pytest.mark.parametrize("graph_name", graph_names())
def test_children_and_edges_count_across_example_graphs(graph_name):
    graph_description, _ = get_graph(graph_name)
    graph = load_graph(graph_description)
    task_sizes = _task_sizes(graph)

    elk_graph = convert_ewoks_to_elk_graph(graph, task_sizes)

    assert len(elk_graph["children"]) == graph.graph.number_of_nodes()

    expected_edge_count = sum(
        len(link_attrs.get("data_mapping") or []) or 1
        for _, _, link_attrs in graph.graph.edges(data=True)
    )
    assert len(elk_graph["edges"]) == expected_edge_count


def test_task_sizes_missing_a_node_raises():
    graph_description, _ = get_graph("acyclic1")
    graph = load_graph(graph_description)

    with pytest.raises(ValueError):
        convert_ewoks_to_elk_graph(graph, {"task1": (10.0, 20.0)})


def test_task_sizes_with_extra_task_id_raises():
    graph_description, _ = get_graph("acyclic1")
    graph = load_graph(graph_description)
    task_sizes = _task_sizes(graph)
    task_sizes["not_a_node"] = (1.0, 1.0)

    with pytest.raises(ValueError):
        convert_ewoks_to_elk_graph(graph, task_sizes)
