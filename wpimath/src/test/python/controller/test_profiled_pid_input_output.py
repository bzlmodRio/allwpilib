import pytest
import math
import numpy as np

from wpimath.controller import ProfiledPIDController
from wpimath.trajectory import TrapezoidProfile
from wpimath.units import (
    degrees,
    degrees_per_second,
    degrees_per_second_squared,
    radians,
    radians_per_second,
    radians_per_second_squared,
    seconds,
    milliseconds,
)


def test_continuous_input1():
    controller = ProfiledPIDController(
        0.0,
        0.0,
        0.0,
        TrapezoidProfile.Constraints(degrees_per_second(360), degrees_per_second_squared(180)),
    )

    controller.setP(1)
    controller.enableContinuousInput(degrees(-180), degrees(180))

    k_setpoint = degrees(-179.0)
    k_measurement = degrees(-179.0)
    k_goal = degrees(179.0)

    controller.reset(k_setpoint)
    assert controller.calculate(k_measurement, k_goal) < 0.0

    # Error must be less than half the input range at all times
    assert abs(controller.getSetpoint().position - k_measurement) < degrees(180)


def test_continuous_input2():
    controller = ProfiledPIDController(
        0.0,
        0.0,
        0.0,
        TrapezoidProfile.Constraints(degrees_per_second(360), degrees_per_second_squared(180)),
    )

    controller.setP(1)
    controller.enableContinuousInput(radians(-math.pi), radians(math.pi))

    k_setpoint = radians(-3.4826633343199735)
    k_measurement = radians(-3.1352207333939606)
    k_goal = radians(-3.534162788601621)

    controller.reset(k_setpoint)
    assert controller.calculate(k_measurement, k_goal) < 0.0

    # Error must be less than half the input range at all times
    assert abs(controller.getSetpoint().position - k_measurement) < radians(math.pi)


def test_continuous_input3():
    controller = ProfiledPIDController(
        0.0,
        0.0,
        0.0,
        TrapezoidProfile.Constraints(degrees_per_second(360), degrees_per_second_squared(180)),
    )

    controller.setP(1)
    controller.enableContinuousInput(radians(-math.pi), radians(math.pi))

    k_setpoint = radians(-3.5176604690006377)
    k_measurement = radians(3.1191729343822456)
    k_goal = radians(2.709680418117445)

    controller.reset(k_setpoint)
    assert controller.calculate(k_measurement, k_goal) < 0.0

    # Error must be less than half the input range at all times
    assert abs(controller.getSetpoint().position - k_measurement) < radians(math.pi)


def test_continuous_input4():
    controller = ProfiledPIDController(
        0.0,
        0.0,
        0.0,
        TrapezoidProfile.Constraints(degrees_per_second(360), degrees_per_second_squared(180)),
    )

    controller.setP(1)
    controller.enableContinuousInput(radians(0), radians(2.0 * math.pi))

    k_setpoint = radians(2.78)
    k_measurement = radians(3.12)
    k_goal = radians(2.71)

    controller.reset(k_setpoint)
    assert controller.calculate(k_measurement, k_goal) < 0.0

    # Error must be less than half the input range at all times
    assert abs(controller.getSetpoint().position - k_measurement) < radians(math.pi)


def test_proportional_gain_output():
    controller = ProfiledPIDController(
        0.0,
        0.0,
        0.0,
        TrapezoidProfile.Constraints(degrees_per_second(360), degrees_per_second_squared(180)),
    )

    controller.setP(4)

    assert controller.calculate(degrees(0.025), degrees(0)) == pytest.approx(-0.1)


def test_integral_gain_output():
    controller = ProfiledPIDController(
        0.0,
        0.0,
        0.0,
        TrapezoidProfile.Constraints(degrees_per_second(360), degrees_per_second_squared(180)),
    )

    controller.setI(4)

    out = 0

    for i in range(5):
        out = controller.calculate(degrees(0.025), degrees(0))

    assert out == pytest.approx(-0.5 * controller.getPeriod())


def test_derivative_gain_output():
    controller = ProfiledPIDController(
        0.0,
        0.0,
        0.0,
        TrapezoidProfile.Constraints(degrees_per_second(360), degrees_per_second_squared(180)),
    )

    controller.setD(4)

    controller.calculate(degrees(0), degrees(0))

    assert controller.calculate(degrees(0.0025), degrees(0)) == pytest.approx(
        -seconds(10 * 1e-3) / controller.getPeriod()
    )