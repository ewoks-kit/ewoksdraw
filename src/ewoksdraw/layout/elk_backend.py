import json
from typing import cast

from ewoksdraw import _elk_rs

from .elk_converter import ElkGraph
from .elk_converter import ElkGraphBeforeLayout


class ElkLayoutError(Exception):
    """Raised when the Rust ELK backend fails to lay out a graph."""


def layout(graph: ElkGraphBeforeLayout) -> ElkGraph:
    """Lay out an ELK graph. Layout options are read from ``graph["layoutOptions"]``."""
    try:
        result = _elk_rs.layout_json(json.dumps(graph))
    except RuntimeError as e:
        raise ElkLayoutError(str(e)) from e
    return cast(ElkGraph, json.loads(result))
