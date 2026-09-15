"""Mutable working data used by the layered layout algorithm."""

from dataclasses import dataclass
from dataclasses import field

from ._layout_graph_model import Point
from ._layout_graph_model import PortSide


@dataclass(frozen=True)
class LayeredPort:
    offset: Point
    side: PortSide


@dataclass(eq=False)
class LayeredNode:
    input_id: str | None
    width: float
    height: float
    layer: int = -1
    x: float = 0.0
    y: float = 0.0

    @property
    def is_dummy(self) -> bool:
        return self.input_id is None


@dataclass(eq=False)
class LayeredLink:
    input_id: str
    source: LayeredNode
    target: LayeredNode
    source_port: LayeredPort
    target_port: LayeredPort
    path: list[LayeredNode] = field(init=False)

    def __post_init__(self) -> None:
        self.path = [self.source, self.target]

    @property
    def is_self_loop(self) -> bool:
        return self.source is self.target

    @property
    def is_reversed(self) -> bool:
        return not self.is_self_loop and self.path[0] is self.target


@dataclass
class LayeredGraph:
    nodes: list[LayeredNode]
    links: list[LayeredLink]
