import pytest
import math
import numpy as np

from wpimath.kinematics import ChassisSpeeds
from wpimath.geometry import Twist2d, Pose2d, Rotation2d
from wpimath.units import (
    meters,
    radians,
    meters_per_second,
    radians_per_second,
    seconds,
)


def test_discretize():
    target = ChassisSpeeds(
        meters_per_second(1), meters_per_second(0), radians_per_second(0.5)
    )
    duration = seconds(1)
    dt = seconds(0.01)

    speeds = target.discretize(duration)
    twist = Twist2d(speeds.vx * dt, speeds.vy * dt, speeds.omega * dt)

    pose = Pose2d()
    time = seconds(0)
    while time < duration:
        pose = pose.exp(twist)
        time += dt

    assert pose.x == pytest.approx((target.vx * duration), abs=1e-9)
    assert pose.y == pytest.approx((target.vy * duration), abs=1e-9)
    assert pose.rotation().radians() == pytest.approx(
        (target.omega * duration), abs=1e-9
    )


def test_to_robot_relative():
    chassis_speeds = ChassisSpeeds(
        meters_per_second(1), meters_per_second(0), radians_per_second(0.5)).toRobotRelative(Rotation2d.fromDegrees(-90))
        

    assert chassis_speeds.vx == pytest.approx(0.0, abs=1e-9)
    assert chassis_speeds.vy == pytest.approx(1.0, abs=1e-9)
    assert chassis_speeds.omega == pytest.approx(0.5, abs=1e-9)


def test_to_field_relative():
    chassis_speeds = ChassisSpeeds(
        meters_per_second(1), meters_per_second(0), radians_per_second(0.5)).toFieldRelative(Rotation2d.fromDegrees(45))
    
    assert chassis_speeds.vx == pytest.approx(1.0 / math.sqrt(2.0), abs=1e-9)
    assert chassis_speeds.vy == pytest.approx(1.0 / math.sqrt(2.0), abs=1e-9)
    assert chassis_speeds.omega == pytest.approx(0.5, abs=1e-9)


def test_plus():
    left = ChassisSpeeds(
        meters_per_second(1.0), meters_per_second(0.5), radians_per_second(0.75)
    )
    right = ChassisSpeeds(
        meters_per_second(2.0), meters_per_second(1.5), radians_per_second(0.25)
    )

    result = left + right

    assert result.vx == pytest.approx(3.0, abs=1e-9)
    assert result.vy == pytest.approx(2.0, abs=1e-9)
    assert result.omega == pytest.approx(1.0, abs=1e-9)


def test_minus():
    left = ChassisSpeeds(
        meters_per_second(1.0), meters_per_second(0.5), radians_per_second(0.75)
    )
    right = ChassisSpeeds(
        meters_per_second(2.0), meters_per_second(0.5), radians_per_second(0.25)
    )

    result = left - right

    assert result.vx == pytest.approx(-1.0, abs=1e-9)
    assert result.vy == pytest.approx(0.0, abs=1e-9)
    assert result.omega == pytest.approx(0.5, abs=1e-9)


def test_unary_minus():
    speeds = ChassisSpeeds(
        meters_per_second(1.0), meters_per_second(0.5), radians_per_second(0.75)
    )

    result = -speeds

    assert result.vx == pytest.approx(-1.0, abs=1e-9)
    assert result.vy == pytest.approx(-0.5, abs=1e-9)
    assert result.omega == pytest.approx(-0.75, abs=1e-9)


def test_multiplication():
    speeds = ChassisSpeeds(
        meters_per_second(1.0), meters_per_second(0.5), radians_per_second(0.75)
    )

    result = speeds * 2

    assert result.vx == pytest.approx(2.0, abs=1e-9)
    assert result.vy == pytest.approx(1.0, abs=1e-9)
    assert result.omega == pytest.approx(1.5, abs=1e-9)


def test_division():
    speeds = ChassisSpeeds(
        meters_per_second(1.0), meters_per_second(0.5), radians_per_second(0.75)
    )

    result = speeds / 2

    assert result.vx == pytest.approx(0.5, abs=1e-9)
    assert result.vy == pytest.approx(0.25, abs=1e-9)
    assert result.omega == pytest.approx(0.375, abs=1e-9)