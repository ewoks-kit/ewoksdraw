"""Link routing for the layered algorithm — kept in its own file."""

from collections import defaultdict

from ._layered_graph_model import LayeredGraph
from ._layered_graph_model import LayeredLink
from ._layered_graph_model import LayeredNode
from ._layered_graph_model import LayeredPort
from ._layout_graph_model import Point
from ._layout_graph_model import PortSide

_STUB_LENGTH = 10.0


def route_links(
    graph: LayeredGraph,
    layers: list[list[LayeredNode]],
    dummy_spacing: float,
) -> dict[str, tuple[Point, ...]]:
    links = graph.links
    lane_offsets = _compute_route_lane_offsets(links, layers, dummy_spacing)
    routes = {}

    for link in links:
        if link.is_self_loop:
            routes[link.input_id] = tuple(_self_loop_points(link.source))
            continue

        source, source_port, target, target_port = _logical_endpoints(link)
        start = _port_position(source, source_port)
        end = _port_position(target, target_port)

        # A link reversed by cycle breaking runs against the flow
        # direction; route it outside the normal layer channels instead.
        if end[0] < start[0]:
            bend_points = _route_loopback_link(
                start, end, source_port, target_port, layers
            )
        else:
            bend_points = _route_orthogonal_link(
                link, start, end, source, target, layers, lane_offsets
            )

        routes[link.input_id] = tuple(
            Point(x, y) for x, y in [start, *bend_points, end]
        )

    return routes


def _self_loop_points(node: LayeredNode) -> list[Point]:
    x, y = node.x + node.width, node.y
    stub = _STUB_LENGTH * 2
    return [
        Point(x, y),
        Point(x + stub, y),
        Point(x + stub, y + node.height),
        Point(x, y + node.height),
    ]


def _logical_endpoints(
    link: LayeredLink,
) -> tuple[LayeredNode, LayeredPort, LayeredNode, LayeredPort]:
    return link.source, link.source_port, link.target, link.target_port


def _port_position(node: LayeredNode, port: LayeredPort) -> tuple[float, float]:
    return node.x + port.offset.x, node.y + port.offset.y


def _stub_direction(side: PortSide) -> float:
    return 1.0 if side is PortSide.EAST else -1.0


def _compute_route_lane_offsets(
    links: list[LayeredLink],
    layers: list[list[LayeredNode]],
    dummy_spacing: float,
) -> dict[tuple[LayeredLink, tuple[int, int]], float]:
    """Spread parallel links crossing the same layer gap into lanes."""
    segments_by_gap: dict[tuple[int, int], list[LayeredLink]] = defaultdict(list)
    for link in links:
        if link.is_self_loop:
            continue
        source, _, target, _ = _logical_endpoints(link)
        layer_sequence = [
            source.layer,
            *(dummy.layer for dummy in _ordered_dummy_nodes(link)),
            target.layer,
        ]
        for first, second in zip(layer_sequence, layer_sequence[1:]):
            if first != second:
                gap = (min(first, second), max(first, second))
                segments_by_gap[gap].append(link)

    offsets: dict[tuple[LayeredLink, tuple[int, int]], float] = {}
    for gap, gap_links in segments_by_gap.items():
        gap_links = _sort_links_for_gap(gap_links)
        count = len(gap_links)
        if count <= 1:
            offsets[(gap_links[0], gap)] = 0.0
            continue

        max_offset = _max_lane_offset(layers, gap)
        if max_offset <= 0:
            spacing = 0.0
        else:
            spacing = min(dummy_spacing, (max_offset * 2) / (count - 1))
        for index, link in enumerate(gap_links):
            offsets[(link, gap)] = (index - (count - 1) / 2) * spacing

    return offsets


def _sort_links_for_gap(links: list[LayeredLink]) -> list[LayeredLink]:
    def cross_axis_midpoint(link: LayeredLink) -> float:
        source, source_port, target, target_port = _logical_endpoints(link)
        start = _port_position(source, source_port)
        end = _port_position(target, target_port)
        return (start[1] + end[1]) / 2

    return sorted(links, key=cross_axis_midpoint)


def _max_lane_offset(layers: list[list[LayeredNode]], gap: tuple[int, int]) -> float:
    first_layer, second_layer = gap
    if first_layer < 0 or second_layer >= len(layers):
        return 0.0
    first_nodes, second_nodes = layers[first_layer], layers[second_layer]
    if not first_nodes or not second_nodes:
        return 0.0

    first_end = max(node.x + node.width for node in first_nodes)
    second_start = min(node.x for node in second_nodes)
    return max(0.0, (second_start - first_end) / 2 - _STUB_LENGTH)


def _ordered_dummy_nodes(link: LayeredLink) -> list[LayeredNode]:
    path = link.path if not link.is_reversed else reversed(link.path)
    return list(path)[1:-1]


def _route_orthogonal_link(
    link: LayeredLink,
    start: tuple[float, float],
    end: tuple[float, float],
    source: LayeredNode,
    target: LayeredNode,
    layers: list[list[LayeredNode]],
    lane_offsets: dict[tuple[LayeredLink, tuple[int, int]], float],
) -> list[tuple[float, float]]:
    _, source_port, _, target_port = _logical_endpoints(link)
    start_out = (start[0] + _stub_direction(source_port.side) * _STUB_LENGTH, start[1])
    end_out = (end[0] + _stub_direction(target_port.side) * _STUB_LENGTH, end[1])

    if len(link.path) > 2:
        return _route_long_link(
            link, start, end, start_out, end_out, source, target, layers, lane_offsets
        )

    bend_points = [start_out]
    channel = _layer_channel_between(layers, source.layer, target.layer)
    gap = (min(source.layer, target.layer), max(source.layer, target.layer))
    channel += lane_offsets.get((link, gap), 0.0)
    bend_points.append((channel, start_out[1]))
    bend_points.append((channel, end_out[1]))

    bend_points.append(end_out)
    return _clean_bend_points(bend_points, start, end)


def _route_long_link(
    link: LayeredLink,
    start: tuple[float, float],
    end: tuple[float, float],
    start_out: tuple[float, float],
    end_out: tuple[float, float],
    source: LayeredNode,
    target: LayeredNode,
    layers: list[list[LayeredNode]],
    lane_offsets: dict[tuple[LayeredLink, tuple[int, int]], float],
) -> list[tuple[float, float]]:
    """Route a multi-layer link without following dummy-node y slots."""
    layer_sequence = [
        source.layer,
        *(dummy.layer for dummy in _ordered_dummy_nodes(link)),
        target.layer,
    ]

    channels = []
    for first, second in zip(layer_sequence, layer_sequence[1:]):
        channel = _layer_channel_between(layers, first, second)
        gap = (min(first, second), max(first, second))
        channels.append(channel + lane_offsets.get((link, gap), 0.0))

    track_y = _long_link_track_y(
        start_out[1], end_out[1], layers, source.layer, target.layer
    )

    bend_points = [start_out, (channels[0], start_out[1]), (channels[0], track_y)]
    bend_points.extend((channel, track_y) for channel in channels[1:])
    bend_points.append((channels[-1], end_out[1]))
    bend_points.append(end_out)
    return _clean_bend_points(bend_points, start, end)


def _long_link_track_y(
    start_y: float,
    end_y: float,
    layers: list[list[LayeredNode]],
    source_layer: int,
    target_layer: int,
) -> float:
    """Choose a compact y-track that avoids real nodes in spanned layers."""
    lower = min(source_layer, target_layer) + 1
    upper = max(source_layer, target_layer)
    obstacles = [
        node for layer in layers[lower:upper] for node in layer if not node.is_dummy
    ]
    if not obstacles:
        return end_y

    for candidate in (end_y, start_y, (start_y + end_y) / 2):
        if _track_y_is_clear(candidate, obstacles):
            return candidate

    intervals = sorted((node.y, node.y + node.height) for node in obstacles)
    merged: list[list[float]] = []
    for low, high in intervals:
        if not merged or low > merged[-1][1]:
            merged.append([low, high])
        else:
            merged[-1][1] = max(merged[-1][1], high)

    candidates = []
    for index, (low, high) in enumerate(merged):
        if low - _STUB_LENGTH >= 0:
            candidates.append(low - _STUB_LENGTH)
        candidates.append(high + _STUB_LENGTH)
        if index + 1 < len(merged):
            next_low = merged[index + 1][0]
            if next_low - high > _STUB_LENGTH * 2:
                candidates.append((high + next_low) / 2)

    clear = [c for c in candidates if c >= 0 and _track_y_is_clear(c, obstacles)]
    if not clear:
        return max(node.y + node.height for node in obstacles) + _STUB_LENGTH

    return min(clear, key=lambda c: (abs(c - end_y), abs(c - start_y)))


def _track_y_is_clear(y: float, obstacles: list[LayeredNode]) -> bool:
    eps = 1e-9
    return all(
        not (node.y + eps < y < node.y + node.height - eps) for node in obstacles
    )


def _layer_channel_between(
    layers: list[list[LayeredNode]], first_layer: int, second_layer: int
) -> float:
    left, right = min(first_layer, second_layer), max(first_layer, second_layer)
    lower, upper = layers[left], layers[right]
    lower_end = max(node.x + node.width for node in lower)
    upper_start = min(node.x for node in upper)
    return (lower_end + upper_start) / 2


def _route_loopback_link(
    start: tuple[float, float],
    end: tuple[float, float],
    source_port: LayeredPort,
    target_port: LayeredPort,
    layers: list[list[LayeredNode]],
) -> list[tuple[float, float]]:
    start_out = (start[0] + _stub_direction(source_port.side) * _STUB_LENGTH, start[1])
    end_out = (end[0] + _stub_direction(target_port.side) * _STUB_LENGTH, end[1])

    minimum, maximum = _loopback_obstacle_bounds(layers, start_out, end_out)
    loop_y = _loopback_axis_position(
        start_out[1], end_out[1], minimum, maximum, _STUB_LENGTH
    )

    bend_points = [start_out, (start_out[0], loop_y), (end_out[0], loop_y), end_out]
    return _clean_bend_points(bend_points, start, end)


def _loopback_axis_position(
    start: float, end: float, minimum: float, maximum: float, margin: float
) -> float:
    """Choose the nearer outside lane, keeping the coordinate non-negative."""
    before = minimum - margin
    after = maximum + margin
    before_detour = abs(start - before) + abs(end - before)
    after_detour = abs(start - after) + abs(end - after)
    if before >= 0 and before_detour < after_detour:
        return before
    return after


def _loopback_obstacle_bounds(
    layers: list[list[LayeredNode]],
    start: tuple[float, float],
    end: tuple[float, float],
) -> tuple[float, float]:
    real_nodes = [node for layer in layers for node in layer if not node.is_dummy]
    start_x, end_x = sorted((start[0], end[0]))
    obstacles = [
        node
        for node in real_nodes
        if node.x <= end_x and node.x + node.width >= start_x
    ]
    if not obstacles:
        obstacles = real_nodes
    return (
        min(node.y for node in obstacles),
        max(node.y + node.height for node in obstacles),
    )


def _clean_bend_points(
    points: list[tuple[float, float]],
    start: tuple[float, float],
    end: tuple[float, float],
) -> list[tuple[float, float]]:
    cleaned: list[tuple[float, float]] = []
    for point in points:
        if _same_point(point, start) or _same_point(point, end):
            continue
        if cleaned and _same_point(cleaned[-1], point):
            continue
        cleaned.append(point)
    return cleaned


def _same_point(first: tuple[float, float], second: tuple[float, float]) -> bool:
    return abs(first[0] - second[0]) < 1e-9 and abs(first[1] - second[1]) < 1e-9
