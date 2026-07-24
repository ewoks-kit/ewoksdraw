import sys
from dataclasses import dataclass
from typing import Sequence

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

Point = tuple[float, float]
Vector = tuple[float, float]


@dataclass(frozen=True)
class CubicBezierSegment:
    control1: Point
    control2: Point
    end: Point


@dataclass(frozen=True)
class CubicBezierPath:
    start: Point
    segments: Sequence[CubicBezierSegment]

    @classmethod
    def from_points(cls, points: Sequence[Point], radius: float) -> Self:
        """
        Create a rounded cubic Bezier path from horizontal and vertical points.

        :param points: The polyline points to convert.
        :param radius: The turn radius around each intermediate point.
        """

        segments = []
        current = points[0]

        for index in range(1, len(points) - 1):
            previous_point = points[index - 1]
            corner_point = points[index]
            next_point = points[index + 1]

            previous_direction = _direction(previous_point, corner_point)
            next_direction = _direction(corner_point, next_point)

            # we might not have the space to turn if distance is too small
            turn_radius = min(
                radius,
                _l1_distance(previous_point, corner_point) / 2,
                _l1_distance(corner_point, next_point) / 2,
            )

            corner_start = _move(corner_point, previous_direction, -turn_radius)
            corner_end = _move(corner_point, next_direction, turn_radius)

            segments.append(_straight_segment(current, corner_start))
            segments.append(
                CubicBezierSegment(
                    control1=_move(corner_start, previous_direction, turn_radius / 2),
                    control2=_move(corner_end, next_direction, -turn_radius / 2),
                    end=corner_end,
                )
            )
            current = corner_end

        segments.append(_straight_segment(current, points[-1]))
        return cls(start=points[0], segments=segments)


def _straight_segment(start: Point, end: Point) -> CubicBezierSegment:
    """Create a cubic Bezier segment that renders as a straight line."""
    start_x, start_y = start
    end_x, end_y = end

    # Control points are set to 1/2; 2/3 arbitrarly so they are not combine with
    # start and end points.
    return CubicBezierSegment(
        control1=(start_x + (end_x - start_x) / 3, start_y + (end_y - start_y) / 3),
        control2=(
            start_x + 2 * (end_x - start_x) / 3,
            start_y + 2 * (end_y - start_y) / 3,
        ),
        end=end,
    )


def _direction(start: Point, end: Point) -> Vector:
    """
    Return the horizontal or vertical direction from start to end.
    Example : (1, 0) right; (-1, 0) left ...
    """
    if start[0] == end[0]:
        return (0, 1 if end[1] > start[1] else -1)
    return (1 if end[0] > start[0] else -1, 0)


def _l1_distance(start: Point, end: Point) -> float:
    return abs(end[0] - start[0]) + abs(end[1] - start[1])


def _move(point: Point, direction: Vector, distance: float) -> Point:
    """Move a point along a direction by a distance."""
    return (point[0] + direction[0] * distance, point[1] + direction[1] * distance)
