import pytest

from wpimath.controller import BangBangController


def test_in_tolerance():
    controller = BangBangController(tolerance=0.1)
    controller.setSetpoint(1)
    controller.calculate(1)
    assert controller.atSetpoint()


def test_out_of_tolerance():
    controller = BangBangController(tolerance=0.1)
    controller.setSetpoint(1)
    controller.calculate(0)
    assert not controller.atSetpoint()