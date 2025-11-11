import pytest
import math

from wpimath.geometry import Pose2d, Rotation2d
from wpimath.spline import SplineParameterizer, SplineHelper, Spline5
from wpimath.units import meters, radians, inchesToMeters


kMaxDx = inchesToMeters(5)
kMaxDy = inchesToMeters(0.05)
kMaxDtheta = 0.0872

def run(a, b):
    # Generate and parameterize the spline.
    spline = SplineHelper.quinticSplinesFromWaypoints([a, b])[0]
    poses = SplineParameterizer.parameterize(spline)

    for i in range(len(poses) - 1):
        p0 = poses[i]
        p1 = poses[i + 1]

        # Make sure the twist is under the tolerance defined by the Spline class.
        twist = p0[0].log(p1[0])
        assert abs(twist.dx) < kMaxDx + 1e-9
        assert abs(twist.dy) < kMaxDy + 1e-9
        assert abs(twist.dtheta) < kMaxDtheta + 1e-9

    # Check first point.
    assert poses[0][0].x == pytest.approx(a.x, abs=1e-9)
    assert poses[0][0].y == pytest.approx(a.y, abs=1e-9)
    assert poses[0][0].rotation().radians() == pytest.approx(a.rotation().radians(), abs=1e-9)

    # Check last point.
    assert poses[-1][0].x == pytest.approx(b.x, abs=1e-9)
    assert poses[-1][0].y == pytest.approx(b.y, abs=1e-9)
    assert poses[-1][0].rotation().radians() == pytest.approx(b.rotation().radians(), abs=1e-9)


def test_straight_line():
    run(Pose2d(), Pose2d(meters(3), meters(0), Rotation2d.fromDegrees(0)))


def test_simple_s_curve():
    run(Pose2d(), Pose2d(meters(1), meters(1), Rotation2d.fromDegrees(0)))


def test_squiggly_curve():
    run(Pose2d(meters(0), meters(0), Rotation2d.fromDegrees(90)), Pose2d(meters(-1), meters(0), Rotation2d.fromDegrees(90)))


def test_throws_on_malformed():
    with pytest.raises(RuntimeError):
        run(Pose2d(meters(0), meters(0), Rotation2d.fromDegrees(0)), Pose2d(meters(1), meters(0), Rotation2d.fromDegrees(180)))
    with pytest.raises(RuntimeError):
        run(Pose2d(meters(10), meters(10), Rotation2d.fromDegrees(90)), Pose2d(meters(10), meters(11), Rotation2d.fromDegrees(-90)))