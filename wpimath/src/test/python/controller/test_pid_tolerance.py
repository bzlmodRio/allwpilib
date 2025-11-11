import pytest
import math
import numpy as np

from wpimath.controller import PIDController
from wpimath.units import seconds


def test_initial_tolerance():
    controller = PIDController(0.5, 0.0, 0.0)
    controller.enableContinuousInput(-200 / 2, 200 / 2)

    assert not controller.atSetpoint()


def test_absolute_tolerance():
    setpoint = 50.0
    tolerance = 10.0
    range_ = 200

    controller = PIDController(0.5, 0.0, 0.0)
    controller.enableContinuousInput(-range_ / 2, range_ / 2)

    assert not controller.atSetpoint()

    controller.setTolerance(tolerance)
    controller.setSetpoint(setpoint)

    assert not controller.atSetpoint()

    controller.calculate(0.0)

    assert not controller.atSetpoint()

    controller.calculate(setpoint + tolerance / 2)

    assert controller.atSetpoint()

    controller.calculate(setpoint + 10 * tolerance)

    assert not controller.atSetpoint()