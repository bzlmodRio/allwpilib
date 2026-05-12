import pytest

from wpimath import PIDController

K_SETPOINT = 50.0
K_RANGE = 200.0
K_TOLERANCE = 10.0


def test_continuous_input():
    controller = PIDController(0.0, 0.0, 0.0)
    controller.set_p(1)

    controller.enable_continuous_input(-180, 180)
    assert controller.calculate(-179, 179) == pytest.approx(-2.0)

    controller.enable_continuous_input(0, 360)
    assert controller.calculate(1, 359) == pytest.approx(-2.0)


def test_proportional_gain_output():
    controller = PIDController(0.0, 0.0, 0.0)
    controller.set_p(4)
    assert controller.calculate(0.025, 0) == pytest.approx(-0.1)


def test_integral_gain_output():
    controller = PIDController(0.0, 0.0, 0.0)
    controller.set_i(4)

    out = 0.0
    for _ in range(5):
        out = controller.calculate(0.025, 0)

    assert out == pytest.approx(-0.5 * controller.get_period(), abs=1e-9)


def test_derivative_gain_output():
    controller = PIDController(0.0, 0.0, 0.0)
    controller.set_d(4)

    controller.calculate(0, 0)
    assert controller.calculate(0.0025, 0) == pytest.approx(
        -0.01 / controller.get_period(), abs=1e-9
    )


def test_izone_no_output():
    controller = PIDController(0.0, 0.0, 0.0)
    controller.set_i(1)
    controller.set_i_zone(1)

    out = controller.calculate(2, 0)
    assert out == pytest.approx(0.0)


def test_izone_output():
    controller = PIDController(0.0, 0.0, 0.0)
    controller.set_i(1)
    controller.set_i_zone(1)

    out = controller.calculate(1, 0)
    assert out == pytest.approx(-1 * controller.get_period(), abs=1e-9)


def test_initial_tolerance():
    controller = PIDController(0.5, 0.0, 0.0)
    controller.enable_continuous_input(-K_RANGE / 2, K_RANGE / 2)
    assert not controller.at_setpoint()


def test_absolute_tolerance():
    controller = PIDController(0.5, 0.0, 0.0)
    controller.enable_continuous_input(-K_RANGE / 2, K_RANGE / 2)

    assert not controller.at_setpoint()

    controller.set_tolerance(K_TOLERANCE)
    controller.set_setpoint(K_SETPOINT)

    assert not controller.at_setpoint()

    controller.calculate(0.0)
    assert not controller.at_setpoint()

    controller.calculate(K_SETPOINT + K_TOLERANCE / 2)
    assert controller.at_setpoint()

    controller.calculate(K_SETPOINT + 10 * K_TOLERANCE)
    assert not controller.at_setpoint()
