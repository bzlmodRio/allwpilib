import math
import pytest
import numpy as np

from wpimath import Pose3d, Rotation3d, Transform3d, Translation3d, Twist3d


def test_straight_x():
    straight = Twist3d(dx=5, dy=0, dz=0, rx=0, ry=0, rz=0)
    result = straight.exp()

    expected = Transform3d(x=5, y=0, z=0, rotation=Rotation3d())
    assert result == expected


def test_straight_y():
    straight = Twist3d(dx=0, dy=5, dz=0, rx=0, ry=0, rz=0)
    result = straight.exp()

    expected = Transform3d(x=0, y=5, z=0, rotation=Rotation3d())
    assert result == expected


def test_straight_z():
    straight = Twist3d(dx=0, dy=0, dz=5, rx=0, ry=0, rz=0)
    result = straight.exp()

    expected = Transform3d(x=0, y=0, z=5, rotation=Rotation3d())
    assert result == expected


def test_quarter_circle():
    z_axis = np.array([0.0, 0.0, 1.0])

    quarter_circle = Twist3d(
        dx=5 / 2.0 * math.pi, dy=0, dz=0, rx=0, ry=0, rz=math.pi / 2.0
    )
    result = quarter_circle.exp()

    expected = Transform3d(x=5, y=5, z=0, rotation=Rotation3d(z_axis, math.pi / 2.0))
    assert result == expected


def test_diagonal_no_dtheta():
    diagonal = Twist3d(dx=2, dy=2, dz=0, rx=0, ry=0, rz=0)
    result = diagonal.exp()

    expected = Transform3d(x=2, y=2, z=0, rotation=Rotation3d())
    assert result == expected


def test_equality():
    one = Twist3d(dx=5, dy=1, dz=0, rx=0, ry=0, rz=3)
    two = Twist3d(dx=5, dy=1, dz=0, rx=0, ry=0, rz=3)
    assert one == two


def test_inequality():
    one = Twist3d(dx=5, dy=1, dz=0, rx=0, ry=0, rz=3)
    two = Twist3d(dx=5, dy=1.2, dz=0, rx=0, ry=0, rz=3)
    assert one != two


def test_pose3d_log_x():
    end = Pose3d(x=0, y=5, z=5, rotation=Rotation3d.fromDegrees(90, 0, 0))
    start = Pose3d()

    twist = (end - start).log()

    expected = Twist3d(
        dx=0,
        dy=5.0 / 2.0 * math.pi,
        dz=0,
        rx=math.radians(90),
        ry=0,
        rz=0,
    )
    assert expected == twist

    reapplied = start + twist.exp()
    assert end == reapplied


def test_pose3d_log_y():
    end = Pose3d(x=5, y=0, z=5, rotation=Rotation3d.fromDegrees(0, 90, 0))
    start = Pose3d()

    twist = (end - start).log()

    expected = Twist3d(
        dx=0,
        dy=0,
        dz=5.0 / 2.0 * math.pi,
        rx=0,
        ry=math.radians(90),
        rz=0,
    )
    assert expected == twist

    reapplied = start + twist.exp()
    assert end == reapplied


def test_pose3d_log_z():
    end = Pose3d(x=5, y=5, z=0, rotation=Rotation3d.fromDegrees(0, 0, 90))
    start = Pose3d()

    twist = (end - start).log()

    expected = Twist3d(
        dx=5.0 / 2.0 * math.pi,
        dy=0,
        dz=0,
        rx=0,
        ry=0,
        rz=math.radians(90),
    )
    assert expected == twist

    reapplied = start + twist.exp()
    assert end == reapplied
