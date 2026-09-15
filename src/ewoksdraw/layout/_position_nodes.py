"""Node placement: layer assignment, crossing minimization, coordinates."""

from collections import defaultdict

from ._layered_graph_model import LayeredGraph
from ._layered_graph_model import LayeredLink
from ._layered_graph_model import LayeredNode
from ._layout_graph_model import LayoutOptions


def position_nodes(
    graph: LayeredGraph, options: LayoutOptions
) -> list[list[LayeredNode]]:

    _break_cycles(graph)
    _rank_nodes_by_longest_path(graph)
    _insert_dummy_nodes(graph)

    layers = group_by_layer(graph.nodes)
    _minimize_crossings(graph, layers)

    dummy_spacing = max(1.0, options.link_spacing)
    _place_rank_columns_left_to_right(
        layers,
        options.node_spacing,
        options.layer_spacing,
        dummy_spacing,
        options.padding,
    )
    return layers


def _break_cycles(graph: LayeredGraph) -> None:
    nodes, links = graph.nodes, graph.links
    white, gray, black = 0, 1, 2
    color = {node: white for node in nodes}
    adjacency: dict[LayeredNode, list[LayeredLink]] = defaultdict(list)
    for link in links:
        if not link.is_self_loop:
            adjacency[link.source].append(link)

    reversed_links: list[LayeredLink] = []

    def visit(node: LayeredNode) -> None:
        color[node] = gray
        for link in adjacency[node]:
            if color[link.target] == gray:
                reversed_links.append(link)
            elif color[link.target] == white:
                visit(link.target)
        color[node] = black

    for node in nodes:
        if color[node] == white:
            visit(node)

    for link in reversed_links:
        link.path.reverse()


def _rank_nodes_by_longest_path(graph: LayeredGraph) -> None:
    """Assign each node the longest distance from a graph source."""
    incoming, outgoing = _node_neighbors(graph)
    nodes = graph.nodes
    in_degree = {node: len(incoming[node]) for node in nodes}

    queue = [node for node in nodes if in_degree[node] == 0]
    order: list[LayeredNode] = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        for target in outgoing[node]:
            in_degree[target] -= 1
            if in_degree[target] == 0:
                queue.append(target)

    remaining = set(nodes) - set(order)
    order.extend(node for node in nodes if node in remaining)

    layer_of: dict[LayeredNode, int] = {}
    for node in order:
        max_source_layer = max(
            (layer_of[source] for source in incoming[node] if source in layer_of),
            default=-1,
        )
        layer_of[node] = max_source_layer + 1

    for node in nodes:
        node.layer = layer_of[node]


def _insert_dummy_nodes(graph: LayeredGraph) -> None:
    for link in graph.links:
        if link.is_self_loop:
            continue
        source, target = link.path
        span = target.layer - source.layer
        dummy_nodes = []
        for offset in range(1, span):
            dummy = LayeredNode(
                input_id=None,
                width=0.0,
                height=0.0,
                layer=source.layer + offset,
            )
            graph.nodes.append(dummy)
            dummy_nodes.append(dummy)
        link.path[1:1] = dummy_nodes


def _node_neighbors(
    graph: LayeredGraph,
) -> tuple[
    dict[LayeredNode, list[LayeredNode]],
    dict[LayeredNode, list[LayeredNode]],
]:
    incoming: dict[LayeredNode, list[LayeredNode]] = {node: [] for node in graph.nodes}
    outgoing: dict[LayeredNode, list[LayeredNode]] = {node: [] for node in graph.nodes}
    for link in graph.links:
        if link.is_self_loop:
            continue
        for source, target in zip(link.path, link.path[1:]):
            outgoing[source].append(target)
            incoming[target].append(source)
    return incoming, outgoing


def group_by_layer(nodes: list[LayeredNode]) -> list[list[LayeredNode]]:
    max_layer = max(node.layer for node in nodes)
    layers: list[list[LayeredNode]] = [[] for _ in range(max_layer + 1)]
    for node in nodes:
        layers[node.layer].append(node)
    return layers


def _minimize_crossings(graph: LayeredGraph, layers: list[list[LayeredNode]]) -> None:
    """Reorder nodes within each layer using the barycenter heuristic."""
    incoming, outgoing = _node_neighbors(graph)
    for index in range(1, len(layers)):
        _sort_layer_by_barycenter(layers[index], layers[index - 1], incoming)
    for index in range(len(layers) - 2, -1, -1):
        _sort_layer_by_barycenter(layers[index], layers[index + 1], outgoing)


def _sort_layer_by_barycenter(
    layer: list[LayeredNode],
    reference: list[LayeredNode],
    neighbors: dict[LayeredNode, list[LayeredNode]],
) -> None:
    reference_position = {node: index for index, node in enumerate(reference)}

    barycenters: dict[LayeredNode, float] = {}
    for node in layer:
        positions = [
            reference_position[neighbor]
            for neighbor in neighbors[node]
            if neighbor in reference_position
        ]
        if positions:
            barycenters[node] = sum(positions) / len(positions)
        else:
            barycenters[node] = float("inf")

    layer.sort(key=lambda node: barycenters[node])


def _place_rank_columns_left_to_right(
    layers: list[list[LayeredNode]],
    node_spacing: float,
    layer_spacing: float,
    dummy_spacing: float,
    padding: float,
) -> None:
    layer_heights = [
        _layer_extent(layer, node_spacing, dummy_spacing) for layer in layers
    ]
    max_height = max(layer_heights)

    x = padding
    for layer, height in zip(layers, layer_heights):
        y = padding + (max_height - height) / 2
        _place_layer(layer, x, y, node_spacing, dummy_spacing)
        x += max(node.width for node in layer) + layer_spacing


def _layer_extent(
    layer: list[LayeredNode], node_spacing: float, dummy_spacing: float
) -> float:
    real_nodes = [node for node in layer if not node.is_dummy]
    if not real_nodes:
        return dummy_spacing * max(len(layer) - 1, 0)

    extent = 0.0
    pending_dummies = 0
    seen_real = False
    for node in layer:
        if node.is_dummy:
            pending_dummies += 1
            continue
        if seen_real:
            extent += max(node_spacing, (pending_dummies + 1) * dummy_spacing)
        else:
            extent += pending_dummies * dummy_spacing
        extent += node.height
        pending_dummies = 0
        seen_real = True

    return extent + pending_dummies * dummy_spacing


def _place_layer(
    layer: list[LayeredNode],
    x: float,
    y: float,
    node_spacing: float,
    dummy_spacing: float,
) -> None:
    real_nodes = [node for node in layer if not node.is_dummy]
    if not real_nodes:
        for index, node in enumerate(layer):
            node.x, node.y = x, y + index * dummy_spacing
        return

    pending_dummies: list[LayeredNode] = []
    previous_real: LayeredNode | None = None
    current_y = y

    for node in layer:
        if node.is_dummy:
            pending_dummies.append(node)
            continue

        if previous_real is None:
            _place_dummy_run(pending_dummies, x, current_y, dummy_spacing)
            current_y += len(pending_dummies) * dummy_spacing
        else:
            gap = max(node_spacing, (len(pending_dummies) + 1) * dummy_spacing)
            gap_start = previous_real.y + previous_real.height
            slot = gap / (len(pending_dummies) + 1)
            _place_dummy_run(pending_dummies, x, gap_start + slot, slot)
            current_y = gap_start + gap

        node.x, node.y = x, current_y
        current_y += node.height
        previous_real = node
        pending_dummies = []

    if pending_dummies:
        _place_dummy_run(pending_dummies, x, current_y + dummy_spacing, dummy_spacing)


def _place_dummy_run(
    dummies: list[LayeredNode], x: float, first_y: float, spacing: float
) -> None:
    for index, dummy in enumerate(dummies):
        dummy.x, dummy.y = x, first_y + index * spacing
