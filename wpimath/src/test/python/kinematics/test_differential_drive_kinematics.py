import pytest
import math
import numpy as np

from wpimath import (
    ChassisAccelerations,
    ChassisVelocities,
    DifferentialDriveKinematics,
    DifferentialDriveWheelAccelerations,
    DifferentialDriveWheelVelocities,
    Rotation2d,
)


def test_inverse_kinematics_from_zero():
    kinematics = DifferentialDriveKinematics(trackwidth=0.381 * 2)
    chassis_velocities = ChassisVelocities()
    wheel_velocities = kinematics.toWheelVelocities(chassis_velocities)

    assert wheel_velocities.left == pytest.approx(0, abs=1e-9)
    assert wheel_velocities.right == pytest.approx(0, abs=1e-9)


def test_forward_kinematics_from_zero():
    kinematics = DifferentialDriveKinematics(trackwidth=0.381 * 2)
    wheel_velocities = DifferentialDriveWheelVelocities()
    chassis_velocities = kinematics.toChassisVelocities(wheel_velocities)

    assert chassis_velocities.vx == pytest.approx(0, abs=1e-9)
    assert chassis_velocities.vy == pytest.approx(0, abs=1e-9)
    assert chassis_velocities.omega == pytest.approx(0, abs=1e-9)


def test_inverse_kinematics_for_straight_line():
    kinematics = DifferentialDriveKinematics(trackwidth=(0.381 * 2))
    chassis_velocities = ChassisVelocities(vx=3.0, vy=0, omega=0)
    wheel_velocities = kinematics.toWheelVelocities(chassis_velocities)

    assert wheel_velocities.left == pytest.approx(3, abs=1e-9)
    assert wheel_velocities.right == pytest.approx(3, abs=1e-9)


def test_forward_kinematics_for_straight_line():
    kinematics = DifferentialDriveKinematics(trackwidth=0.381 * 2)
    wheel_velocities = DifferentialDriveWheelVelocities(left=3.0, right=3.0)
    chassis_velocities = kinematics.toChassisVelocities(wheel_velocities)

    assert chassis_velocities.vx == pytest.approx(3, abs=1e-9)
    assert chassis_velocities.vy == pytest.approx(0, abs=1e-9)
    assert chassis_velocities.omega == pytest.approx(0, abs=1e-9)


def test_inverse_kinematics_for_rotate_in_place():
    kinematics = DifferentialDriveKinematics(trackwidth=0.381 * 2)
    chassis_velocities = ChassisVelocities(vx=0.0, vy=0.0, omega=math.pi)
    wheel_velocities = kinematics.toWheelVelocities(chassis_velocities)

    assert wheel_velocities.left == pytest.approx(-0.381 * math.pi, abs=1e-9)
    assert wheel_velocities.right == pytest.approx(0.381 * math.pi, abs=1e-9)


def test_forward_kinematics_for_rotate_in_place():
    kinematics = DifferentialDriveKinematics(trackwidth=0.381 * 2)
    wheel_velocities = DifferentialDriveWheelVelocities(
        left=0.381 * math.pi, right=-0.381 * math.pi
    )
    chassis_velocities = kinematics.toChassisVelocities(wheel_velocities)

    assert chassis_velocities.vx == pytest.approx(0, abs=1e-9)
    assert chassis_velocities.vy == pytest.approx(0, abs=1e-9)
    assert chassis_velocities.omega == pytest.approx(-math.pi, abs=1e-9)


def test_inverse_accelerations_for_zeros():
    kinematics = DifferentialDriveKinematics(trackwidth=0.381 * 2)
    chassis_accelerations = ChassisAccelerations()
    wheel_accelerations = kinematics.toWheelAccelerations(chassis_accelerations)

    assert wheel_accelerations.left == pytest.approx(0, abs=1e-9)
    assert wheel_accelerations.right == pytest.approx(0, abs=1e-9)


def test_forward_accelerations_for_zeros():
    kinematics = DifferentialDriveKinematics(trackwidth=0.381 * 2)
    wheel_accelerations = DifferentialDriveWheelAccelerations()
    chassis_accelerations = kinematics.toChassisAccelerations(wheel_accelerations)

    assert chassis_accelerations.ax == pytest.approx(0, abs=1e-9)
    assert chassis_accelerations.ay == pytest.approx(0, abs=1e-9)
    assert chassis_accelerations.alpha == pytest.approx(0, abs=1e-9)


def test_inverse_accelerations_for_straight_line():
    kinematics = DifferentialDriveKinematics(trackwidth=0.381 * 2)
    chassis_accelerations = ChassisAccelerations(ax=3.0, ay=0, alpha=0)
    wheel_accelerations = kinematics.toWheelAccelerations(chassis_accelerations)

    assert wheel_accelerations.left == pytest.approx(3, abs=1e-9)
    assert wheel_accelerations.right == pytest.approx(3, abs=1e-9)


def test_forward_accelerations_for_straight_line():
    kinematics = DifferentialDriveKinematics(trackwidth=0.381 * 2)
    wheel_accelerations = DifferentialDriveWheelAccelerations(left=3.0, right=3.0)
    chassis_accelerations = kinematics.toChassisAccelerations(wheel_accelerations)

    assert chassis_accelerations.ax == pytest.approx(3, abs=1e-9)
    assert chassis_accelerations.ay == pytest.approx(0, abs=1e-9)
    assert chassis_accelerations.alpha == pytest.approx(0, abs=1e-9)


def test_inverse_accelerations_for_rotate_in_place():
    kinematics = DifferentialDriveKinematics(trackwidth=0.381 * 2)
    chassis_accelerations = ChassisAccelerations(ax=0.0, ay=0.0, alpha=math.pi)
    wheel_accelerations = kinematics.toWheelAccelerations(chassis_accelerations)

    assert wheel_accelerations.left == pytest.approx(-0.381 * math.pi, abs=1e-9)
    assert wheel_accelerations.right == pytest.approx(0.381 * math.pi, abs=1e-9)


def test_forward_accelerations_for_rotate_in_place():
    kinematics = DifferentialDriveKinematics(trackwidth=0.381 * 2)
    wheel_accelerations = DifferentialDriveWheelAccelerations(
        left=0.381 * math.pi, right=-0.381 * math.pi
    )
    chassis_accelerations = kinematics.toChassisAccelerations(wheel_accelerations)

    assert chassis_accelerations.ax == pytest.approx(0, abs=1e-9)
    assert chassis_accelerations.ay == pytest.approx(0, abs=1e-9)
    assert chassis_accelerations.alpha == pytest.approx(-math.pi, abs=1e-9)
