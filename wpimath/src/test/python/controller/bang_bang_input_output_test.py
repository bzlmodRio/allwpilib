import pytest
from wpimath import BangBangController

def test_should_output():
    controller = BangBangController()
    # C++: EXPECT_DOUBLE_EQ(controller.Calculate(0, 1), 1)
    assert controller.calculate(0.0, 1.0) == 1.0

def test_should_not_output():
    controller = BangBangController()
    # C++: EXPECT_DOUBLE_EQ(controller.Calculate(1, 0), 0)
    assert controller.calculate(1.0, 0.0) == 0.0
