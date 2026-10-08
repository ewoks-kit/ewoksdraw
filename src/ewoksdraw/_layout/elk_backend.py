import json
from typing import cast

from ewoksdraw import _elk_rs
from ewoksdraw._config.constants import ELK_LAYOUT_OPTIONS

from .elk_converter import ElkGraph
from .elk_converter import ElkGraphBeforeLayout


class ElkLayoutError(Exception):
    """Raised when the Rust ELK backend fails to lay out a graph."""


def layout(graph: ElkGraphBeforeLayout) -> ElkGraph:
    """Lay out an ELK graph for SVG rendering using orthogonal edge routing.

    Layout options are read from ``graph["layoutOptions"]``.
    Unsupported edge routing raises ``ValueError`` before layout.
    """
    routing = graph["layoutOptions"].get(
        "org.eclipse.elk.edgeRouting", ELK_LAYOUT_OPTIONS["org.eclipse.elk.edgeRouting"]
    )
    if routing != "ORTHOGONAL":
        raise ValueError(
            "SVG rendering currently supports only ORTHOGONAL edge routing."
        )

    try:
        result = _elk_rs.layout_json(json.dumps(graph))
    except RuntimeError as e:
        raise ElkLayoutError(str(e)) from e
    return cast(ElkGraph, json.loads(result))
