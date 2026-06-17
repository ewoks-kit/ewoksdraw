
from ewoks import load_graph
from ewoksdraw import graph_to_svg

EDGE_MODE = "bspline"  # "orthogonal", "polyline", or "bspline"

EDGE_ROUTING_OPTIONS = {
    "orthogonal": {"org.eclipse.elk.edgeRouting": "ORTHOGONAL"},
    "polyline": {"org.eclipse.elk.edgeRouting": "POLYLINE"},
    "bspline": {
        "org.eclipse.elk.edgeRouting": "SPLINES",
        "elk.layered.edgeRouting.splines.mode": "CONSERVATIVE_SOFT",
    },
}


graph_path = "./wip_tests_scripts/optimize_geometry_loop_workflow.json"
output_svg = f"./wip_tests_scripts/optimize_geometry_loop_workflow{EDGE_MODE}.svg"
graph = load_graph(graph_path)

elk_graph = graph_to_svg(
    graph,
    {
        "elk.algorithm": "layered",
        "elk.direction": "RIGHT",
        "elk.spacing.nodeNode": 60,
        "elk.layered.spacing.nodeNodeBetweenLayers": 80,
        "elk.layered.spacing.edgeEdgeBetweenLayers": 20,
        **EDGE_ROUTING_OPTIONS[EDGE_MODE],
    },
    output_svg,
)


