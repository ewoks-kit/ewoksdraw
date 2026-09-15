"""Build and run the native layered graph layout."""

from ._layered_graph_model import LayeredGraph
from ._layered_graph_model import LayeredLink
from ._layered_graph_model import LayeredNode
from ._layered_graph_model import LayeredPort
from ._layout_graph_model import LayoutGraph
from ._layout_graph_model import LayoutOptions
from ._layout_graph_model import LayoutResult
from ._layout_graph_model import Point
from ._layout_graph_model import PortRef
from ._layout_graph_model import Size
from ._position_nodes import position_nodes
from ._route_links import route_links


def compute_layout(graph: LayoutGraph, options: LayoutOptions) -> LayoutResult:
    if not graph.nodes:
        size = Size(options.padding * 2, options.padding * 2)
        return LayoutResult(size=size, node_positions={}, link_routes={})

    layered_graph = _build_layered_graph(graph)
    layers = position_nodes(layered_graph, options)
    link_routes = route_links(
        layered_graph,
        layers,
        max(1.0, options.link_spacing),
    )
    return _build_result(layered_graph, link_routes, options.padding)


def _build_layered_graph(graph: LayoutGraph) -> LayeredGraph:
    nodes: list[LayeredNode] = []
    node_by_id: dict[str, LayeredNode] = {}
    port_by_ref: dict[PortRef, tuple[LayeredNode, LayeredPort]] = {}

    for node in graph.nodes:
        if node.id in node_by_id:
            raise ValueError(f"Duplicate node id: {node.id!r}")

        layered_node = LayeredNode(
            input_id=node.id,
            width=node.size.width,
            height=node.size.height,
        )
        nodes.append(layered_node)
        node_by_id[node.id] = layered_node

        for port in node.ports:
            ref = PortRef(node.id, port.id)
            if ref in port_by_ref:
                raise ValueError(f"Duplicate port id: {port.id!r} on {node.id!r}")
            port_by_ref[ref] = (
                layered_node,
                LayeredPort(offset=port.offset, side=port.side),
            )

    links: list[LayeredLink] = []
    link_ids: set[str] = set()
    for link in graph.links:
        if link.id in link_ids:
            raise ValueError(f"Duplicate link id: {link.id!r}")
        link_ids.add(link.id)

        try:
            source, source_port = port_by_ref[link.source]
            target, target_port = port_by_ref[link.target]
        except KeyError as error:
            raise ValueError(f"Unknown port reference: {error.args[0]!r}") from None

        links.append(
            LayeredLink(
                input_id=link.id,
                source=source,
                target=target,
                source_port=source_port,
                target_port=target_port,
            )
        )

    return LayeredGraph(nodes=nodes, links=links)


def _build_result(
    graph: LayeredGraph,
    link_routes: dict[str, tuple[Point, ...]],
    padding: float,
) -> LayoutResult:
    real_nodes = [node for node in graph.nodes if not node.is_dummy]
    node_positions = {
        node.input_id: Point(node.x, node.y)
        for node in real_nodes
        if node.input_id is not None
    }

    max_x = max(node.x + node.width for node in real_nodes)
    max_y = max(node.y + node.height for node in real_nodes)
    for route in link_routes.values():
        for point in route:
            max_x = max(max_x, point.x)
            max_y = max(max_y, point.y)

    return LayoutResult(
        size=Size(max_x + padding, max_y + padding),
        node_positions=node_positions,
        link_routes=link_routes,
    )
