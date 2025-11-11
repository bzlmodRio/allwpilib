import pytest
import math
import numpy as np

from wpimath.controller import PIDController
from wpimath.units import seconds, milliseconds


def test_continuous_input():
    controller = PIDController(0.0, 0.0, 0.0)

    controller.setP(1)
    controller.enableContinuousInput(-180, 180)
    assert controller.calculate(-179, 179) == pytest.approx(-2)

    controller.enableContinuousInput(0, 360)
    assert controller.calculate(1, 359) == pytest.approx(-2)


def test_proportional_gain_output():
    controller = PIDController(0.0, 0.0, 0.0)

    controller.setP(4)

    assert controller.calculate(0.025, 0) == pytest.approx(-0.1)


def test_integral_gain_output():
    controller = PIDController(0.0, 0.0, 0.0)

    controller.setI(4)

    out = 0

    for i in range(5):
        out = controller.calculate(0.025, 0)

    assert out == pytest.approx(-0.5 * controller.getPeriod())


def test_derivative_gain_output():
    controller = PIDController(0.0, 0.0, 0.0)

    controller.setD(4)

    controller.calculate(0, 0)

    assert controller.calculate(0.0025, 0) == pytest.approx(
        -seconds(10 * 1e-3) / controller.getPeriod()
    )


def test_izone_no_output():
    controller = PIDController(0.0, 0.0, 0.0)

    controller.setI(1)
    controller.setIZone(1)

    out = controller.calculate(2, 0)

    assert out == pytest.approx(0)


def test_izone_output():
    controller = PIDController(0.0, 0.0, 0.0)

    controller.setI(1)
    controller.setIZone(1)

    out = controller.calculate(1, 0)

    assert out == pytest.approx(-1 * controller.getPeriod())