import pytest

from ewoksdraw.geometry.cubic_bezier_path import CubicBezierPath
from ewoksdraw.geometry.cubic_bezier_path import Point
from ewoksdraw.geometry.cubic_bezier_path import Vector
from ewoksdraw.geometry.cubic_bezier_path import _direction
from ewoksdraw.geometry.cubic_bezier_path import _l1_distance
from ewoksdraw.geometry.cubic_bezier_path import _move
from ewoksdraw.geometry.cubic_bezier_path import _straight_segment


def _point(x: float, y: float) -> Point:
    return {"x": x, "y": y}


def test_straight_segment() -> None:
    segment = _straight_segment(_point(0, 0), _point(9, 0))
    assert segment.control1 == pytest.approx(_point(3, 0))
    assert segment.control2 == pytest.approx(_point(6, 0))
    assert segment.end == _point(9, 0)


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (_point(0, 0), _point(5, 0), (1, 0)),
        (_point(5, 0), _point(0, 0), (-1, 0)),
        (_point(0, 0), _point(0, 5), (0, 1)),
        (_point(0, 5), _point(0, 0), (0, -1)),
    ],
)
def test_direction(start: Point, end: Point, expected: Vector) -> None:
    assert _direction(start, end) == expected


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (_point(0, 0), _point(3, 4), 7),
        (_point(0, 0), _point(0, 0), 0),
        (_point(-1, -1), _point(1, 1), 4),
    ],
)
def test_distance(start: Point, end: Point, expected: float) -> None:
    assert _l1_distance(start, end) == expected


@pytest.mark.parametrize(
    "point, direction, distance, expected",
    [
        (_point(0, 0), (1, 0), 5, _point(5, 0)),
        (_point(0, 0), (-1, 0), 5, _point(-5, 0)),
        (_point(0, 0), (0, 1), 5, _point(0, 5)),
        (_point(0, 0), (0, 1), -5, _point(0, -5)),
    ],
)
def test_move(
    point: Point, direction: Vector, distance: float, expected: Point
) -> None:
    assert _move(point, direction, distance) == expected


def test_from_points_two_points_is_a_single_straight_segment() -> None:
    path = CubicBezierPath.from_points(points=[_point(0, 0), _point(10, 0)], radius=2)

    assert path.start == _point(0, 0)
    assert len(path.segments) == 1
    assert path.segments[0].end == _point(10, 0)


def test_from_points_single_corner_produces_three_segments() -> None:
    path = CubicBezierPath.from_points(
        points=[_point(0, 0), _point(10, 0), _point(10, 10)], radius=2
    )

    assert path.start == _point(0, 0)
    assert len(path.segments) == 3

    straight_before, corner, straight_after = path.segments
    assert straight_before.end == _point(8, 0)
    assert corner.end == _point(10, 2)
    assert straight_after.end == _point(10, 10)


def test_from_points_radius_clamped_to_half_shorter_adjacent_segment() -> None:
    path = CubicBezierPath.from_points(
        points=[_point(0, 0), _point(2, 0), _point(2, 10)], radius=100
    )

    _, corner, _ = path.segments
    assert corner.end == _point(2, 1)


def test_from_points_zero_radius_collapses_corner_to_point() -> None:
    path = CubicBezierPath.from_points(
        points=[_point(0, 0), _point(10, 0), _point(10, 10)], radius=0
    )

    straight_before, corner, straight_after = path.segments
    assert straight_before.end == _point(10, 0)
    assert corner.end == _point(10, 0)
    assert straight_after.end == _point(10, 10)
