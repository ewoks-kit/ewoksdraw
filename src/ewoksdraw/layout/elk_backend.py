import json
from typing import Any

from ewoksdraw import _elk_rs


def layout(
    graph: dict[str, Any], options: dict[str, Any] | None = None
) -> dict[str, Any]:
    result = _elk_rs.layout_json(json.dumps(graph), json.dumps(options or {}))
    return json.loads(result)
