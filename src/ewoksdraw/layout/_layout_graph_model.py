"""Input and output data for the native graph layout."""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum


class PortSide(Enum):
    WEST = "WEST"
    EAST = "EAST"


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class Size:
    width: float
    height: float


@dataclass(frozen=True)
class LayoutPort:
    id: str
    offset: Point
    side: PortSide


@dataclass(frozen=True)
class PortRef:
    node_id: str
    port_id: str


@dataclass(frozen=True)
class LayoutNode:
    id: str
    size: Size
    ports: tuple[LayoutPort, ...] = ()


@dataclass(frozen=True)
class LayoutLink:
    id: str
    source: PortRef
    target: PortRef


@dataclass(frozen=True)
class LayoutGraph:
    nodes: tuple[LayoutNode, ...] = ()
    links: tuple[LayoutLink, ...] = ()


@dataclass(frozen=True)
class LayoutResult:
    size: Size
    node_positions: Mapping[str, Point]
    link_routes: Mapping[str, tuple[Point, ...]]


@dataclass(frozen=True)
class LayoutOptions:
    node_spacing: float = 20.0
    layer_spacing: float = 20.0
    link_spacing: float = 10.0
    padding: float = 12.0
