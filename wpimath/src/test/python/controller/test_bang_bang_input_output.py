import pytest

from wpimath.controller import BangBangController


def test_should_output():
    controller = BangBangController()
    assert controller.calculate(0, 1) == pytest.approx(1)


def test_should_not_output():
    controller = BangBangController()
    assert controller.calculate(1, 0) == pytest.approx(0)