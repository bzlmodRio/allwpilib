import math
import pytest

from wpimath import ProfiledPIDController, TrapezoidProfile


def test_continuous_input1():
    controller = ProfiledPIDController(
        0.0, 0.0, 0.0, TrapezoidProfile.Constraints(360.0, 180.0)
    )
    controller.set_p(1)
    controller.enable_continuous_input(-180.0, 180.0)

    k_setpoint = -179.0
    k_measurement = -179.0
    k_goal = 179.0

    controller.reset(k_setpoint)
    assert controller.calculate(k_measurement, k_goal) < 0.0
    assert abs(controller.get_setpoint().position - k_measurement) < 180.0


def test_continuous_input2():
    controller = ProfiledPIDController(
        0.0,
        0.0,
        0.0,
        TrapezoidProfile.Constraints(2.0 * math.pi, math.pi),
    )
    controller.set_p(1)
    controller.enable_continuous_input(-math.pi, math.pi)

    k_setpoint = -3.4826633343199735
    k_measurement = -3.1352207333939606
    k_goal = -3.534162788601621

    controller.reset(k_setpoint)
    assert controller.calculate(k_measurement, k_goal) < 0.0
    assert abs(controller.get_setpoint().position - k_measurement) < math.pi


def test_continuous_input3():
    controller = ProfiledPIDController(
        0.0,
        0.0,
        0.0,
        TrapezoidProfile.Constraints(2.0 * math.pi, math.pi),
    )
    controller.set_p(1)
    controller.enable_continuous_input(-math.pi, math.pi)

    k_setpoint = -3.5176604690006377
    k_measurement = 3.1191729343822456
    k_goal = 2.709680418117445

    controller.reset(k_setpoint)
    assert controller.calculate(k_measurement, k_goal) < 0.0
    assert abs(controller.get_setpoint().position - k_measurement) < math.pi


def test_continuous_input4():
    controller = ProfiledPIDController(
        0.0,
        0.0,
        0.0,
        TrapezoidProfile.Constraints(2.0 * math.pi, math.pi),
    )
    controller.set_p(1)
    controller.enable_continuous_input(0.0, 2.0 * math.pi)

    k_setpoint = 2.78
    k_measurement = 3.12
    k_goal = 2.71

    controller.reset(k_setpoint)
    assert controller.calculate(k_measurement, k_goal) < 0.0
    assert abs(controller.get_setpoint().position - k_measurement) < math.pi


def test_proportional_gain_output():
    controller = ProfiledPIDController(
        0.0, 0.0, 0.0, TrapezoidProfile.Constraints(360.0, 180.0)
    )
    controller.set_p(4)
    assert controller.calculate(0.025, 0.0) == pytest.approx(-0.1)


def test_integral_gain_output():
    controller = ProfiledPIDController(
        0.0, 0.0, 0.0, TrapezoidProfile.Constraints(360.0, 180.0)
    )
    controller.set_i(4)

    out = 0.0
    for _ in range(5):
        out = controller.calculate(0.025, 0.0)

    assert out == pytest.approx(-0.5 * controller.get_period(), abs=1e-9)


def test_derivative_gain_output():
    controller = ProfiledPIDController(
        0.0, 0.0, 0.0, TrapezoidProfile.Constraints(360.0, 180.0)
    )
    controller.set_d(4)

    controller.calculate(0.0, 0.0)
    assert controller.calculate(0.0025, 0.0) == pytest.approx(
        -0.01 / controller.get_period(), abs=1e-9
    )
