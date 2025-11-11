import pytest
import math

from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.spline import SplineParameterizer, SplineHelper, Spline3
from wpimath.units import meters, radians, seconds, inchesToMeters


kMaxDx = inchesToMeters(5)
kMaxDy = inchesToMeters(0.05)
kMaxDtheta = 0.0872

def run(a, waypoints, b):
    # Generate and parameterize the spline.
    start_cv, end_cv = SplineHelper.cubicControlVectorsFromWaypoints(a, waypoints, b)
    splines = SplineHelper.cubicSplinesFromControlVectors(start_cv, waypoints, end_cv)
    
    print(splines[0].getPoint(0.0))
    poses = [splines[0].getPoint(0.0)]

    for spline in splines:
        poses.extend(SplineParameterizer.parameterize(spline))

    for i in range(len(poses) - 1):
        p0 = poses[i]
        p1 = poses[i + 1]

        # Make sure the twist is under the tolerance defined by the Spline class.
        twist = p0[0].log(p1[0])
        assert abs(twist.dx) < kMaxDx
        assert abs(twist.dy) < kMaxDy
        assert abs(twist.dtheta) < kMaxDtheta

    # Check first point.
    assert poses[0][0].x == pytest.approx(a.x, abs=1e-9)
    assert poses[0][0].y == pytest.approx(a.y, abs=1e-9)
    assert poses[0][0].rotation().radians() == pytest.approx(a.rotation().radians(), abs=1e-9)
    
    # Check interior waypoints.
    interiors_good = True
    for waypoint in waypoints:
        found = False
        for state in poses:
            if abs(waypoint.distance(state[0].translation())) < 1e-9:
                found = True
        interiors_good &= found

    assert interiors_good

    # Check last point.
    assert poses[-1][0].x == pytest.approx(b.x, abs=1e-9)
    assert poses[-1][0].y == pytest.approx(b.y, abs=1e-9)
    assert poses[-1][0].rotation().radians() == pytest.approx(b.rotation().radians(), abs=1e-9)


def test_straight_line():
    run(Pose2d(), [], Pose2d(meters(3), meters(0), 0))


def test_s_curve():
    start = Pose2d(meters(0), meters(0), Rotation2d.fromDegrees(90))
    waypoints = [Translation2d(meters(1), meters(1)), Translation2d(meters(2), meters(-1))]
    end = Pose2d(meters(3), meters(0), Rotation2d.fromDegrees(90))
    run(start, waypoints, end)


def test_one_interior():
    start = Pose2d(meters(0), meters(0), radians(0))
    waypoints = [Translation2d(meters(2), meters(0))]
    end = Pose2d(meters(4), meters(0), radians(0))
    run(start, waypoints, end)


def test_throws_on_malformed():
    with pytest.raises(RuntimeError):
        run(Pose2d(meters(0), meters(0), Rotation2d.fromDegrees(0)), [], Pose2d(meters(1), meters(0), Rotation2d.fromDegrees(180)))
    with pytest.raises(RuntimeError):
        run(Pose2d(meters(10), meters(10), Rotation2d.fromDegrees(90)), [], Pose2d(meters(10), meters(11), Rotation2d.fromDegrees(-90)))