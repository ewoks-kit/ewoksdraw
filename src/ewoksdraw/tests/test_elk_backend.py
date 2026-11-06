from typing import Any
from typing import cast

from ewoksdraw.layout.elk_backend import layout
from ewoksdraw.layout.elk_converter import ElkGraphBeforeLayout


def test_layout() -> None:
    graph: dict[str, Any] = {
        "id": "root",
        "layoutOptions": {
            "org.eclipse.elk.algorithm": "layered",
            "org.eclipse.elk.direction": "RIGHT",
            "org.eclipse.elk.edgeRouting": "ORTHOGONAL",
        },
        "children": [
            {"id": "first", "width": 30, "height": 20},
            {"id": "second", "width": 30, "height": 20},
        ],
        "edges": [
            {
                "id": "first-to-second",
                "sources": ["first"],
                "targets": ["second"],
            }
        ],
    }
    result = layout(cast(ElkGraphBeforeLayout, graph))

    assert result["width"] > 0
    assert result["height"] > 0
    assert all("x" in node and "y" in node for node in result["children"])
    assert result["edges"][0]["sections"]
