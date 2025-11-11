import pytest
import math

from wpimath.geometry import Translation2d, Translation3d
from wpimath.units import (
    meters,
    meters_per_second,
    radians,
    seconds,
)
from wpimath import applyDeadband, slewRateLimit, angleModulus, inputModulus, copySignPow


def test_apply_deadband_unity_scale():
    # < 0
    assert applyDeadband(-1.0, 0.02) == pytest.approx(-1.0)
    assert applyDeadband(-0.03, 0.02) == pytest.approx((-0.03 + 0.02) / (1.0 - 0.02))
    assert applyDeadband(-0.02, 0.02) == pytest.approx(0.0)
    assert applyDeadband(-0.01, 0.02) == pytest.approx(0.0)

    # == 0
    assert applyDeadband(0.0, 0.02) == pytest.approx(0.0)

    # > 0
    assert applyDeadband(0.01, 0.02) == pytest.approx(0.0)
    assert applyDeadband(0.02, 0.02) == pytest.approx(0.0)
    assert applyDeadband(0.03, 0.02) == pytest.approx((0.03 - 0.02) / (1.0 - 0.02))
    assert applyDeadband(1.0, 0.02) == pytest.approx(1.0)

def test_apply_deadband_arbitrary_scale():
    # < 0
    assert applyDeadband(-2.5, 0.02, 2.5) == pytest.approx(-2.5)
    assert applyDeadband(-0.02, 0.02, 2.5) == pytest.approx(0.0)
    assert applyDeadband(-0.01, 0.02, 2.5) == pytest.approx(0.0)

    # == 0
    assert applyDeadband(0.0, 0.02, 2.5) == pytest.approx(0.0)

    # > 0
    assert applyDeadband(0.01, 0.02, 2.5) == pytest.approx(0.0)
    assert applyDeadband(0.02, 0.02, 2.5) == pytest.approx(0.0)
    assert applyDeadband(2.5, 0.02, 2.5) == pytest.approx(2.5)

def test_apply_deadband_units():
    # < 0
    assert applyDeadband(radians(-20), radians(1), radians(20)) == pytest.approx(-20)

def test_apply_deadband_large_max_magnitude():
    assert applyDeadband(100.0, 20.0, math.inf) == pytest.approx(80.0)

def test_copy_sign_pow():
    assert copySignPow(0.5, 1.0) == pytest.approx(0.5)
    assert copySignPow(-0.5, 1.0) == pytest.approx(-0.5)

    assert copySignPow(0.5, 2.0) == pytest.approx(0.5 * 0.5)
    assert copySignPow(-0.5, 2.0) == pytest.approx(-(0.5 * 0.5))

    assert copySignPow(0.5, 0.5) == pytest.approx(math.sqrt(0.5))
    assert copySignPow(-0.5, 0.5) == pytest.approx(-math.sqrt(0.5))

    assert copySignPow(0.0, 2.0) == pytest.approx(0.0)
    assert copySignPow(1.0, 2.0) == pytest.approx(1.0)
    assert copySignPow(-1.0, 2.0) == pytest.approx(-1.0)

    assert copySignPow(0.8, 0.3) == pytest.approx(math.pow(0.8, 0.3))
    assert copySignPow(-0.8, 0.3) == pytest.approx(-math.pow(0.8, 0.3))

def test_copy_sign_pow_with_max_magnitude():
    assert copySignPow(5.0, 1.0, 10.0) == pytest.approx(5.0)
    assert copySignPow(-5.0, 1.0, 10.0) == pytest.approx(-5.0)

    assert copySignPow(5.0, 2.0, 10.0) == pytest.approx(0.5 * 0.5 * 10)
    assert copySignPow(-5.0, 2.0, 10.0) == pytest.approx(-0.5 * 0.5 * 10)

    assert copySignPow(5.0, 0.5, 10.0) == pytest.approx(math.sqrt(0.5) * 10)
    assert copySignPow(-5.0, 0.5, 10.0) == pytest.approx(-math.sqrt(0.5) * 10)

    assert copySignPow(0.0, 2.0, 5.0) == pytest.approx(0.0)
    assert copySignPow(5.0, 2.0, 5.0) == pytest.approx(5.0)
    assert copySignPow(-5.0, 2.0, 5.0) == pytest.approx(-5.0)

    assert copySignPow(80.0, 0.3, 100.0) == pytest.approx(math.pow(0.8, 0.3) * 100)
    assert copySignPow(-80.0, 0.3, 100.0) == pytest.approx(-math.pow(0.8, 0.3) * 100)

def test_copy_sign_pow_with_units():
    assert copySignPow(meters_per_second(0), 2.0) == pytest.approx(0)
    assert copySignPow(meters_per_second(1), 2.0) == pytest.approx(1)
    assert copySignPow(meters_per_second(-1), 2.0) == pytest.approx(-1)

    assert copySignPow(meters_per_second(5), 2.0, meters_per_second(10)) == pytest.approx(0.5 * 0.5 * 10)
    assert copySignPow(meters_per_second(-5), 2.0, meters_per_second(10)) == pytest.approx(-0.5 * 0.5 * 10)

def test_input_modulus():
    # These tests check error wrapping. That is, the result of wrapping the
    # result of an angle reference minus the measurement.

    # Test symmetric range
    assert inputModulus(170.0 - (-170.0), -180.0, 180.0) == pytest.approx(-20.0)
    assert inputModulus(170.0 + 360.0 - (-170.0), -180.0, 180.0) == pytest.approx(-20.0)
    assert inputModulus(170.0 - (-170.0 + 360.0), -180.0, 180.0) == pytest.approx(-20.0)
    assert inputModulus(-170.0 - 170.0, -180.0, 180.0) == pytest.approx(20.0)
    assert inputModulus(-170.0 + 360.0 - 170.0, -180.0, 180.0) == pytest.approx(20.0)
    assert inputModulus(-170.0 - (170.0 + 360.0), -180.0, 180.0) == pytest.approx(20.0)

    # Test range starting at zero
    assert inputModulus(170.0 - 190.0, 0.0, 360.0) == pytest.approx(340.0)
    assert inputModulus(170.0 + 360.0 - 190.0, 0.0, 360.0) == pytest.approx(340.0)
    assert inputModulus(170.0 - (190.0 + 360.0), 0.0, 360.0) == pytest.approx(340.0)

    # Test asymmetric range that doesn't start at zero
    assert inputModulus(170.0 - (-170.0), -170.0, 190.0) == pytest.approx(-20.0)

    # Test range with both positive endpoints
    assert inputModulus(0.0, 1.0, 3.0) == pytest.approx(2.0)
    assert inputModulus(1.0, 1.0, 3.0) == pytest.approx(3.0)
    assert inputModulus(2.0, 1.0, 3.0) == pytest.approx(2.0)
    assert inputModulus(3.0, 1.0, 3.0) == pytest.approx(3.0)
    assert inputModulus(4.0, 1.0, 3.0) == pytest.approx(2.0)

    # Test all supported types
    assert inputModulus(170.0 - (-170.0), -170.0, 190.0) == pytest.approx(-20.0)
    assert inputModulus(170 - (-170), -170, 190) == pytest.approx(-20)

def test_angle_modulus():
    assert angleModulus(radians(-2000 * math.pi / 180)) == pytest.approx(160 * math.pi / 180, abs=1e-10)
    assert angleModulus(radians(358 * math.pi / 180)) == pytest.approx(-2 * math.pi / 180, abs=1e-10)
    assert angleModulus(radians(2.0 * math.pi)) == pytest.approx(0.0, abs=1e-10)

    assert angleModulus(radians(5 * math.pi)) == pytest.approx(math.pi)
    assert angleModulus(radians(-5 * math.pi)) == pytest.approx(math.pi)
    assert angleModulus(radians(math.pi / 2)) == pytest.approx(math.pi / 2)
    assert angleModulus(radians(-math.pi / 2)) == pytest.approx(-math.pi / 2)


def test_translation2d_slew_rate_limit_unchanged():
    translation1 = Translation2d(meters(0), meters(0))
    translation2 = Translation2d(meters(2), meters(2))

    result1 = slewRateLimit(translation1, translation2, seconds(1), meters_per_second(50))

    expected1 = Translation2d(meters(2), meters(2))

    assert result1.x == pytest.approx(expected1.x)
    assert result1.y == pytest.approx(expected1.y)

def test_translation2d_slew_rate_limit_changed():
    translation3 = Translation2d(meters(1), meters(1))
    translation4 = Translation2d(meters(3), meters(3))

    result2 = slewRateLimit(translation3, translation4, seconds(0.25), meters_per_second(2))

    expected2 = Translation2d(
        meters(1.0 + 0.5 * (math.sqrt(2) / 2)),
        meters(1.0 + 0.5 * (math.sqrt(2) / 2)),
    )

    assert result2.x == pytest.approx(expected2.x)
    assert result2.y == pytest.approx(expected2.y)

def test_translation3d_slew_rate_limit_unchanged():
    translation1 = Translation3d(meters(0), meters(0), meters(0))
    translation2 = Translation3d(meters(2), meters(2), meters(2))

    result1 = slewRateLimit(translation1, translation2, seconds(1), meters_per_second(50.0))

    expected1 = Translation3d(meters(2), meters(2), meters(2))

    assert result1.x == pytest.approx(expected1.x)
    assert result1.y == pytest.approx(expected1.y)
    assert result1.z == pytest.approx(expected1.z)

def test_translation3d_slew_rate_limit_changed():
    translation3 = Translation3d(meters(1), meters(1), meters(1))
    translation4 = Translation3d(meters(3), meters(3), meters(3))

    result2 = slewRateLimit(translation3, translation4, seconds(0.25), meters_per_second(2.0))

    expected2 = Translation3d(
        meters(1.0 + 0.5 * (1 / math.sqrt(3))),
        meters(1.0 + 0.5 * (1 / math.sqrt(3))),
        meters(1.0 + 0.5 * (1 / math.sqrt(3))),
    )

    assert result2.x == pytest.approx(expected2.x)
    assert result2.y == pytest.approx(expected2.y)
    assert result2.z == pytest.approx(expected2.z)