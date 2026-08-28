import pytest
from ewokscore import load_graph
from ewokscore.graph import TaskGraph
from ewokscore.tests.examples.graphs import get_graph
from ewokscore.tests.examples.graphs import graph_names
from pyelk.graph import validate_graph

from ewoksdraw import build_svg_task_group
from ewoksdraw.config.constants import ELK_LAYOUT_OPTIONS
from ewoksdraw.layout.elk_converter import LaidOutElkGraph
from ewoksdraw.layout.elk_converter import convert_ewoks_to_elk_graph
from ewoksdraw.layout.elk_converter import extract_task_positions_from_elk_graph
from ewoksdraw.svg.svg_task import TaskIOPosition
from ewoksdraw.svg.svg_task import TaskPosition
from ewoksdraw.svg.svg_task_group import TaskInputPositions
from ewoksdraw.svg.svg_task_group import TaskOutputPositions
from ewoksdraw.svg.svg_task_group import TaskSize
from ewoksdraw.svg.svg_task_group import TaskSizes

_TASK_TYPE = "ewokscore.tests.examples.tasks.sumtask.SumTask"


def _node(node_id: str) -> dict:
    return {"id": node_id, "task_type": "class", "task_identifier": _TASK_TYPE}


def _task_sizes(graph: TaskGraph) -> TaskSizes:
    return {
        node_id: TaskSize(width=10.0 * i, height=20.0 * i)
        for i, node_id in enumerate(graph.graph.nodes, start=1)
    }


def _task_input_positions(graph: TaskGraph) -> TaskInputPositions:
    return {node_id: [] for node_id in graph.graph.nodes}


def _task_output_positions(graph: TaskGraph) -> TaskOutputPositions:
    return {node_id: [] for node_id in graph.graph.nodes}


def test_extract_task_positions_from_elk_graph() -> None:
    laid_out_graph: LaidOutElkGraph = {
        "id": "root",
        "width": 100.0,
        "height": 100.0,
        "layoutOptions": {},
        "children": [
            {
                "id": "task",
                "width": 20.0,
                "height": 30.0,
                "x": 12.0,
                "y": 34.0,
                "layoutOptions": {},
                "ports": [],
            }
        ],
        "edges": [],
    }

    assert extract_task_positions_from_elk_graph(laid_out_graph) == [
        TaskPosition(name="task", x=12.0, y=34.0)
    ]


def test_top_level_structure() -> None:
    graph_description, _ = get_graph("acyclic1")
    graph = load_graph(graph_description)

    elk_graph = convert_ewoks_to_elk_graph(
        graph,
        _task_sizes(graph),
        _task_input_positions(graph),
        _task_output_positions(graph),
    )

    assert elk_graph["id"] == "__ewoksdraw_root__"
    assert elk_graph["layoutOptions"] == ELK_LAYOUT_OPTIONS
    assert "children" in elk_graph
    assert "edges" in elk_graph


def test_root_id_does_not_collide_with_task_ids() -> None:
    task_id = "__ewoksdraw_root__"
    graph_description = {
        "graph": {"id": "g", "label": "g", "schema_version": "1.1"},
        "nodes": [_node(task_id)],
        "links": [],
    }
    graph = load_graph(graph_description)

    elk_graph = convert_ewoks_to_elk_graph(
        graph,
        {task_id: TaskSize(width=1.0, height=1.0)},
        {task_id: []},
        {task_id: []},
    )

    assert elk_graph["id"] == "__ewoksdraw_root___1"
    assert elk_graph["children"][0]["id"] == task_id


def test_children_match_task_sizes() -> None:
    graph_description, _ = get_graph("acyclic1")
    graph = load_graph(graph_description)
    task_sizes = _task_sizes(graph)

    elk_graph = convert_ewoks_to_elk_graph(
        graph,
        task_sizes,
        _task_input_positions(graph),
        _task_output_positions(graph),
    )

    assert len(elk_graph["children"]) == len(task_sizes)
    for child in elk_graph["children"]:
        width, height = task_sizes[child["id"]]
        assert child["width"] == width
        assert child["height"] == height


def test_children_include_io_positions_as_elk_ports() -> None:
    graph_description = {
        "graph": {"id": "g", "label": "g", "schema_version": "1.1"},
        "nodes": [_node("task")],
        "links": [],
    }
    graph = load_graph(graph_description)
    input_positions = {"task": [TaskIOPosition(name="value", x=0.0, y=10.0)]}
    output_positions = {"task": [TaskIOPosition(name="result", x=20.0, y=15.0)]}

    elk_graph = convert_ewoks_to_elk_graph(
        graph,
        {"task": TaskSize(width=20.0, height=30.0)},
        input_positions,
        output_positions,
    )

    assert elk_graph["children"][0]["ports"] == [
        {
            "id": "task.input.value",
            "x": 0.0,
            "y": 10.0,
            "width": 0,
            "height": 0,
            "layoutOptions": {
                "org.eclipse.elk.port.side": "WEST",
                "org.eclipse.elk.port.index": 0,
                "org.eclipse.elk.port.borderOffset": 0,
            },
        },
        {
            "id": "task.output.result",
            "x": 20.0,
            "y": 15.0,
            "width": 0,
            "height": 0,
            "layoutOptions": {
                "org.eclipse.elk.port.side": "EAST",
                "org.eclipse.elk.port.index": 0,
                "org.eclipse.elk.port.borderOffset": 0,
            },
        },
    ]


def test_link_without_data_mapping_produces_no_elk_edge() -> None:
    graph_description = {
        "graph": {"id": "g", "label": "g", "schema_version": "1.1"},
        "nodes": [_node("a"), _node("b")],
        "links": [{"source": "a", "target": "b"}],
    }
    graph = load_graph(graph_description)

    size = TaskSize(width=1.0, height=1.0)
    elk_graph = convert_ewoks_to_elk_graph(
        graph,
        {"a": size, "b": size},
        {"a": [], "b": []},
        {"a": [], "b": []},
    )

    assert elk_graph["edges"] == []


def test_link_with_map_all_data_produces_no_elk_edge() -> None:
    graph_description = {
        "graph": {"id": "g", "label": "g", "schema_version": "1.1"},
        "nodes": [_node("a"), _node("b")],
        "links": [{"source": "a", "target": "b", "map_all_data": True}],
    }
    graph = load_graph(graph_description)

    size = TaskSize(width=1.0, height=1.0)
    with pytest.warns(
        UserWarning,
        match=(
            r"Ewoks link 'a' -> 'b' uses 'map_all_data', which is not yet supported\."
        ),
    ):
        elk_graph = convert_ewoks_to_elk_graph(
            graph,
            {"a": size, "b": size},
            {"a": [], "b": []},
            {"a": [], "b": []},
        )

    assert elk_graph["edges"] == []


def test_data_mapping_without_source_output_is_not_drawn() -> None:
    graph_description = {
        "graph": {"id": "g", "label": "g", "schema_version": "1.1"},
        "nodes": [_node("a"), _node("b")],
        "links": [
            {
                "source": "a",
                "target": "b",
                "data_mapping": [
                    {"target_input": "all_results"},
                    {"source_output": "result", "target_input": "value"},
                ],
            }
        ],
    }
    graph = load_graph(graph_description)
    size = TaskSize(width=1.0, height=1.0)
    input_positions = {
        "a": [],
        "b": [
            TaskIOPosition(name="all_results", x=0.0, y=0.25),
            TaskIOPosition(name="value", x=0.0, y=0.75),
        ],
    }
    output_positions = {
        "a": [TaskIOPosition(name="result", x=1.0, y=0.5)],
        "b": [],
    }

    with pytest.warns(
        UserWarning,
        match=(
            r"Data mapping on Ewoks link 'a' -> 'b' has no 'source_output', "
            r"which is not yet supported\."
        ),
    ):
        elk_graph = convert_ewoks_to_elk_graph(
            graph,
            {"a": size, "b": size},
            input_positions,
            output_positions,
        )

    assert elk_graph["edges"] == [
        {
            "id": "edge_0_a_b",
            "sources": ["a.output.result"],
            "targets": ["b.input.value"],
        }
    ]


def test_link_with_multiple_data_mappings_produces_one_elk_edge_per_mapping() -> None:
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

    size = TaskSize(width=1.0, height=1.0)
    input_positions = {
        "a": [],
        "b": [
            TaskIOPosition(name="a", x=0.0, y=0.25),
            TaskIOPosition(name="b", x=0.0, y=0.75),
        ],
    }
    output_positions = {
        "a": [TaskIOPosition(name="result", x=1.0, y=0.5)],
        "b": [],
    }
    elk_graph = convert_ewoks_to_elk_graph(
        graph,
        {"a": size, "b": size},
        input_positions,
        output_positions,
    )

    assert elk_graph["edges"] == [
        {
            "id": "edge_0_a_b",
            "sources": ["a.output.result"],
            "targets": ["b.input.a"],
        },
        {
            "id": "edge_1_a_b",
            "sources": ["a.output.result"],
            "targets": ["b.input.b"],
        },
    ]


def test_edge_id_does_not_collide_with_task_ids() -> None:
    colliding_task_id = "edge_0_a_b"
    graph_description = {
        "graph": {"id": "g", "label": "g", "schema_version": "1.1"},
        "nodes": [_node("a"), _node("b"), _node(colliding_task_id)],
        "links": [
            {
                "source": "a",
                "target": "b",
                "data_mapping": [{"source_output": "result", "target_input": "value"}],
            }
        ],
    }
    graph = load_graph(graph_description)
    size = TaskSize(width=1.0, height=1.0)
    input_positions = {
        "a": [],
        "b": [TaskIOPosition(name="value", x=0.0, y=0.5)],
        colliding_task_id: [],
    }
    output_positions = {
        "a": [TaskIOPosition(name="result", x=1.0, y=0.5)],
        "b": [],
        colliding_task_id: [],
    }

    elk_graph = convert_ewoks_to_elk_graph(
        graph,
        {"a": size, "b": size, colliding_task_id: size},
        input_positions,
        output_positions,
    )

    assert elk_graph["edges"][0]["id"] == "edge_0_a_b_1"


def test_graph_without_link() -> None:
    graph_description, _ = get_graph("empty")
    graph = load_graph(graph_description)

    elk_graph = convert_ewoks_to_elk_graph(graph, {}, {}, {})

    assert elk_graph["children"] == []
    assert elk_graph["edges"] == []


@pytest.mark.parametrize("graph_name", graph_names())
@pytest.mark.filterwarnings("ignore:.*uses 'map_all_data'.*:UserWarning")
def test_children_and_edges_count_across_example_graphs(graph_name: str) -> None:
    graph_description, _ = get_graph(graph_name)
    graph = load_graph(graph_description)
    task_sizes = _task_sizes(graph)

    elk_graph = convert_ewoks_to_elk_graph(
        graph,
        task_sizes,
        _task_input_positions(graph),
        _task_output_positions(graph),
    )

    assert len(elk_graph["children"]) == graph.graph.number_of_nodes()

    expected_edge_count = sum(
        len(link_attrs.get("data_mapping") or [])
        for _, _, link_attrs in graph.graph.edges(data=True)
    )
    assert len(elk_graph["edges"]) == expected_edge_count


def test_task_sizes_missing_a_node_raises() -> None:
    graph_description, _ = get_graph("acyclic1")
    graph = load_graph(graph_description)

    with pytest.raises(ValueError):
        convert_ewoks_to_elk_graph(
            graph,
            {"task1": TaskSize(width=10.0, height=20.0)},
            _task_input_positions(graph),
            _task_output_positions(graph),
        )


def test_task_sizes_with_extra_task_id_raises() -> None:
    graph_description, _ = get_graph("acyclic1")
    graph = load_graph(graph_description)
    task_sizes = _task_sizes(graph)
    task_sizes["not_a_node"] = TaskSize(width=1.0, height=1.0)

    with pytest.raises(ValueError):
        convert_ewoks_to_elk_graph(
            graph,
            task_sizes,
            _task_input_positions(graph),
            _task_output_positions(graph),
        )


def test_task_input_positions_missing_a_node_raises() -> None:
    graph_description, _ = get_graph("acyclic1")
    graph = load_graph(graph_description)

    with pytest.raises(ValueError, match="task_input_positions"):
        convert_ewoks_to_elk_graph(
            graph,
            _task_sizes(graph),
            {"task1": []},
            _task_output_positions(graph),
        )


def test_task_output_positions_missing_a_node_raises() -> None:
    graph_description, _ = get_graph("acyclic1")
    graph = load_graph(graph_description)

    with pytest.raises(ValueError, match="task_output_positions"):
        convert_ewoks_to_elk_graph(
            graph,
            _task_sizes(graph),
            _task_input_positions(graph),
            {"task1": []},
        )


@pytest.mark.parametrize("graph_name", graph_names())
@pytest.mark.filterwarnings("ignore:.*uses 'map_all_data'.*:UserWarning")
def test_output_is_a_valid_pyelk_graph(graph_name: str) -> None:
    """Check graph validation from pyelk"""

    graph_description, _ = get_graph(graph_name)
    graph = load_graph(graph_description)
    task_group = build_svg_task_group(graph)

    elk_graph = convert_ewoks_to_elk_graph(
        graph,
        task_group.extract_task_sizes(),
        task_group.extract_input_positions(),
        task_group.extract_output_positions(),
    )

    validate_graph(elk_graph)
