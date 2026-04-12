import pytest
from wpimath import BangBangController

def test_in_tolerance():
    controller = BangBangController(tolerance=0.1)
    controller.setSetpoint(1.0)
    controller.calculate(1.0)
    # C++: EXPECT_TRUE(controller.AtSetpoint())
    assert controller.atSetpoint() is True

def test_out_of_tolerance():
    controller = BangBangController(tolerance=0.1)
    controller.setSetpoint(1.0)
    controller.calculate(0.0)
    # C++: EXPECT_FALSE(controller.AtSetpoint())
    assert controller.atSetpoint() is False