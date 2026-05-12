import math
import pytest

from wpimath import (
    Pose2d,
    Rotation2d,
    SplineHelper,
    SplineParameterizer,
    Translation2d,
)

# SplineParameterizer tolerance constants (from C++ source)
K_MAX_DX = 0.127  # meters
K_MAX_DY = 0.00127  # meters
K_MAX_DTHETA = 0.0872  # radians


def _run_cubic(start, waypoints, end):
    start_cv, end_cv = SplineHelper.cubic_control_vectors_from_waypoints(
        start, waypoints, end
    )
    splines = SplineHelper.cubic_splines_from_control_vectors(start_cv, waypoints, end_cv)

    poses = []
    first_point = splines[0].get_point(0.0)
    if first_point is not None:
        poses.append(first_point)

    for spline in splines:
        pts = SplineParameterizer.parameterize(spline)
        poses.extend(pts[1:])

    for i in range(len(poses) - 1):
        p0 = poses[i]
        p1 = poses[i + 1]
        twist = (p1[0] - p0[0]).log()
        assert abs(twist.dx) < K_MAX_DX
        assert abs(twist.dy) < K_MAX_DY
        assert abs(twist.dtheta) < K_MAX_DTHETA

    # Check first point
    assert poses[0][0].x == pytest.approx(start.x, abs=1e-9)
    assert poses[0][0].y == pytest.approx(start.y, abs=1e-9)
    assert poses[0][0].rotation().radians() == pytest.approx(
        start.rotation().radians(), abs=1e-9
    )

    # Check interior waypoints
    for waypoint in waypoints:
        found = any(
            abs(waypoint.distance(state[0].translation())) < 1e-9
            for state in poses
        )
        assert found

    # Check last point
    assert poses[-1][0].x == pytest.approx(end.x, abs=1e-9)
    assert poses[-1][0].y == pytest.approx(end.y, abs=1e-9)
    assert poses[-1][0].rotation().radians() == pytest.approx(
        end.rotation().radians(), abs=1e-9
    )


def _run_quintic(start, end):
    spline = SplineHelper.quintic_splines_from_waypoints([start, end])[0]
    poses = SplineParameterizer.parameterize(spline)

    for i in range(len(poses) - 1):
        p0 = poses[i]
        p1 = poses[i + 1]
        twist = (p1[0] - p0[0]).log()
        assert abs(twist.dx) < K_MAX_DX
        assert abs(twist.dy) < K_MAX_DY
        assert abs(twist.dtheta) < K_MAX_DTHETA

    # Check first point
    assert poses[0][0].x == pytest.approx(start.x, abs=1e-9)
    assert poses[0][0].y == pytest.approx(start.y, abs=1e-9)
    assert poses[0][0].rotation().radians() == pytest.approx(
        start.rotation().radians(), abs=1e-9
    )

    # Check last point
    assert poses[-1][0].x == pytest.approx(end.x, abs=1e-9)
    assert poses[-1][0].y == pytest.approx(end.y, abs=1e-9)
    assert poses[-1][0].rotation().radians() == pytest.approx(
        end.rotation().radians(), abs=1e-9
    )


# Cubic Hermite spline tests


def test_cubic_straight_line():
    _run_cubic(
        Pose2d(0, 0, Rotation2d()),
        [],
        Pose2d(3, 0, Rotation2d()),
    )


def test_cubic_s_curve():
    start = Pose2d(0, 0, Rotation2d.from_degrees(90))
    waypoints = [Translation2d(1, 1), Translation2d(2, -1)]
    end = Pose2d(3, 0, Rotation2d.from_degrees(90))
    _run_cubic(start, waypoints, end)


def test_cubic_one_interior():
    start = Pose2d(0, 0, Rotation2d())
    waypoints = [Translation2d(2, 0)]
    end = Pose2d(4, 0, Rotation2d())
    _run_cubic(start, waypoints, end)


def test_cubic_throws_on_malformed():
    with pytest.raises(Exception):
        _run_cubic(
            Pose2d(0, 0, Rotation2d()),
            [],
            Pose2d(1, 0, Rotation2d.from_degrees(180)),
        )

    with pytest.raises(Exception):
        _run_cubic(
            Pose2d(10, 10, Rotation2d.from_degrees(90)),
            [],
            Pose2d(10, 11, Rotation2d.from_degrees(-90)),
        )


# Quintic Hermite spline tests


def test_quintic_straight_line():
    _run_quintic(Pose2d(0, 0, Rotation2d()), Pose2d(3, 0, Rotation2d()))


def test_quintic_simple_s_curve():
    _run_quintic(Pose2d(0, 0, Rotation2d()), Pose2d(1, 1, Rotation2d()))


def test_quintic_squiggly_curve():
    _run_quintic(
        Pose2d(0, 0, Rotation2d.from_degrees(90)),
        Pose2d(-1, 0, Rotation2d.from_degrees(90)),
    )


def test_quintic_throws_on_malformed():
    with pytest.raises(Exception):
        _run_quintic(
            Pose2d(0, 0, Rotation2d()),
            Pose2d(1, 0, Rotation2d.from_degrees(180)),
        )

    with pytest.raises(Exception):
        _run_quintic(
            Pose2d(10, 10, Rotation2d.from_degrees(90)),
            Pose2d(10, 11, Rotation2d.from_degrees(-90)),
        )
