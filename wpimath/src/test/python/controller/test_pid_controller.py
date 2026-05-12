import pytest

from wpimath import PIDController

K_SETPOINT = 50.0
K_RANGE = 200.0
K_TOLERANCE = 10.0


def test_continuous_input():
    controller = PIDController(0.0, 0.0, 0.0)
    controller.setP(1)

    controller.enableContinuousInput(-180, 180)
    assert controller.calculate(-179, 179) == pytest.approx(-2.0)

    controller.enableContinuousInput(0, 360)
    assert controller.calculate(1, 359) == pytest.approx(-2.0)


def test_proportional_gain_output():
    controller = PIDController(0.0, 0.0, 0.0)
    controller.setP(4)
    assert controller.calculate(0.025, 0) == pytest.approx(-0.1)


def test_integral_gain_output():
    controller = PIDController(0.0, 0.0, 0.0)
    controller.setI(4)

    out = 0.0
    for _ in range(5):
        out = controller.calculate(0.025, 0)

    assert out == pytest.approx(-0.5 * controller.getPeriod(), abs=1e-9)


def test_derivative_gain_output():
    controller = PIDController(0.0, 0.0, 0.0)
    controller.setD(4)

    controller.calculate(0, 0)
    assert controller.calculate(0.0025, 0) == pytest.approx(
        -0.01 / controller.getPeriod(), abs=1e-9
    )


def test_izone_no_output():
    controller = PIDController(0.0, 0.0, 0.0)
    controller.setI(1)
    controller.setIZone(1)

    out = controller.calculate(2, 0)
    assert out == pytest.approx(0.0)


def test_izone_output():
    controller = PIDController(0.0, 0.0, 0.0)
    controller.setI(1)
    controller.setIZone(1)

    out = controller.calculate(1, 0)
    assert out == pytest.approx(-1 * controller.getPeriod(), abs=1e-9)


def test_initial_tolerance():
    controller = PIDController(0.5, 0.0, 0.0)
    controller.enableContinuousInput(-K_RANGE / 2, K_RANGE / 2)
    assert not controller.atSetpoint()


def test_absolute_tolerance():
    controller = PIDController(0.5, 0.0, 0.0)
    controller.enableContinuousInput(-K_RANGE / 2, K_RANGE / 2)

    assert not controller.atSetpoint()

    controller.setTolerance(K_TOLERANCE)
    controller.setSetpoint(K_SETPOINT)

    assert not controller.atSetpoint()

    controller.calculate(0.0)
    assert not controller.atSetpoint()

    controller.calculate(K_SETPOINT + K_TOLERANCE / 2)
    assert controller.atSetpoint()

    controller.calculate(K_SETPOINT + 10 * K_TOLERANCE)
    assert not controller.atSetpoint()
