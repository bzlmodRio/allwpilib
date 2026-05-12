import math
import pytest

from wpimath import ChassisAccelerations, Rotation2d


def test_default_constructor():
    accelerations = ChassisAccelerations()

    assert accelerations.ax == pytest.approx(0.0, abs=1e-9)
    assert accelerations.ay == pytest.approx(0.0, abs=1e-9)
    assert accelerations.alpha == pytest.approx(0.0, abs=1e-9)


def test_parameterized_constructor():
    accelerations = ChassisAccelerations(ax=1.0, ay=2.0, alpha=3.0)

    assert accelerations.ax == pytest.approx(1.0, abs=1e-9)
    assert accelerations.ay == pytest.approx(2.0, abs=1e-9)
    assert accelerations.alpha == pytest.approx(3.0, abs=1e-9)


def test_to_robot_relative():
    chassis_accelerations = ChassisAccelerations(
        ax=1.0, ay=0.0, alpha=0.5
    ).toRobotRelative(Rotation2d.fromDegrees(-90))

    assert chassis_accelerations.ax == pytest.approx(0.0, abs=1e-9)
    assert chassis_accelerations.ay == pytest.approx(1.0, abs=1e-9)
    assert chassis_accelerations.alpha == pytest.approx(0.5, abs=1e-9)


def test_to_field_relative():
    chassis_accelerations = ChassisAccelerations(
        ax=1.0, ay=0.0, alpha=0.5
    ).toFieldRelative(Rotation2d.fromDegrees(45))

    assert chassis_accelerations.ax == pytest.approx(1.0 / math.sqrt(2.0), abs=1e-9)
    assert chassis_accelerations.ay == pytest.approx(1.0 / math.sqrt(2.0), abs=1e-9)
    assert chassis_accelerations.alpha == pytest.approx(0.5, abs=1e-9)


def test_plus():
    left = ChassisAccelerations(ax=1.0, ay=0.5, alpha=0.75)
    right = ChassisAccelerations(ax=2.0, ay=1.5, alpha=0.25)

    result = left + right

    assert result.ax == pytest.approx(3.0, abs=1e-9)
    assert result.ay == pytest.approx(2.0, abs=1e-9)
    assert result.alpha == pytest.approx(1.0, abs=1e-9)


def test_minus():
    left = ChassisAccelerations(ax=1.0, ay=0.5, alpha=0.75)
    right = ChassisAccelerations(ax=2.0, ay=0.5, alpha=0.25)

    result = left - right

    assert result.ax == pytest.approx(-1.0, abs=1e-9)
    assert result.ay == pytest.approx(0.0, abs=1e-9)
    assert result.alpha == pytest.approx(0.5, abs=1e-9)


def test_unary_minus():
    result = -ChassisAccelerations(ax=1.0, ay=0.5, alpha=0.75)

    assert result.ax == pytest.approx(-1.0, abs=1e-9)
    assert result.ay == pytest.approx(-0.5, abs=1e-9)
    assert result.alpha == pytest.approx(-0.75, abs=1e-9)


def test_multiplication():
    result = ChassisAccelerations(ax=1.0, ay=0.5, alpha=0.75) * 2.0

    assert result.ax == pytest.approx(2.0, abs=1e-9)
    assert result.ay == pytest.approx(1.0, abs=1e-9)
    assert result.alpha == pytest.approx(1.5, abs=1e-9)


def test_division():
    result = ChassisAccelerations(ax=2.0, ay=1.0, alpha=1.5) / 2.0

    assert result.ax == pytest.approx(1.0, abs=1e-9)
    assert result.ay == pytest.approx(0.5, abs=1e-9)
    assert result.alpha == pytest.approx(0.75, abs=1e-9)
