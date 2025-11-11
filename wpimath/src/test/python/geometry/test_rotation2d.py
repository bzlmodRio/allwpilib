import pytest
import math
import numpy as np

from wpimath.geometry import Rotation2d
from wpimath.units import radians


def test_radians_to_degrees():
    rot1 = Rotation2d(radians(math.pi / 3.0))
    rot2 = Rotation2d(radians(math.pi / 4.0))

    assert rot1.degrees() == pytest.approx(60.0)
    assert rot2.degrees() == pytest.approx(45.0)


def test_degrees_to_radians():
    rot1 = Rotation2d(math.radians(45))
    rot2 = Rotation2d(math.radians(30))

    assert rot1.radians() == pytest.approx(math.pi / 4.0)
    assert rot2.radians() == pytest.approx(math.pi / 6.0)


def test_rotate_by_from_zero():
    zero = Rotation2d()
    rotated = zero + Rotation2d(math.radians(90))

    assert rotated.radians() == pytest.approx(math.pi / 2.0)
    assert rotated.degrees() == pytest.approx(90.0)


def test_rotate_by_non_zero():
    rot = Rotation2d(math.radians(90))
    rot = rot + Rotation2d(math.radians(30))

    assert rot.degrees() == pytest.approx(120.0)


def test_minus():
    rot1 = Rotation2d(math.radians(70))
    rot2 = Rotation2d(math.radians(30))

    assert (rot1 - rot2).degrees() == pytest.approx(40.0)


def test_unary_minus():
    rot = Rotation2d(math.radians(20))

    assert (-rot).degrees() == pytest.approx(-20.0)


def test_multiply():
    rot = Rotation2d(math.radians(10))

    assert (rot * 3.0).degrees() == pytest.approx(30.0)
    # The C++ test has an odd multiplication where it expects 10*41 to result in 50.
    # WPILib's Python multiplication does not have this behavior. The test is changed to
    # expect the correct multiplication.
    # WPILib's C++ code normalizes the angle to be between [-180, 180] before returning the.
    # Therefore, 10 * 41 = 410, and 410 - 360 = 50.
    # Python returns 410 which is equivalent to 50.
    assert (rot * 41.0).degrees() == pytest.approx(50.0)


def test_equality():
    rot1 = Rotation2d(math.radians(43))
    rot2 = Rotation2d(math.radians(43))
    assert rot1 == rot2

    rot1 = Rotation2d(math.radians(-180))
    rot2 = Rotation2d(math.radians(180))
    assert rot1 == rot2


def test_inequality():
    rot1 = Rotation2d(math.radians(43))
    rot2 = Rotation2d(math.radians(43.5))
    assert rot1 != rot2


def test_to_matrix():
    before = Rotation2d(math.radians(20))
    after = Rotation2d.fromMatrix(before.toMatrix())

    assert before == after
