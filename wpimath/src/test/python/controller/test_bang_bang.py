import pytest

from wpimath import BangBangController


def test_should_output():
    controller = BangBangController()
    assert controller.calculate(0, 1) == pytest.approx(1.0)


def test_should_not_output():
    controller = BangBangController()
    assert controller.calculate(1, 0) == pytest.approx(0.0)


def test_in_tolerance():
    controller = BangBangController(0.1)
    controller.setSetpoint(1)
    controller.calculate(1)
    assert controller.atSetpoint()


def test_out_of_tolerance():
    controller = BangBangController(0.1)
    controller.setSetpoint(1)
    controller.calculate(0)
    assert not controller.atSetpoint()
