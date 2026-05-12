import math
import pytest

import wpimath
from wpimath import Translation2d, Translation3d


def test_apply_deadband_unity_scale():
    assert wpimath.applyDeadband(-1.0, 0.02) == pytest.approx(-1.0)
    assert wpimath.applyDeadband(-0.03, 0.02) == pytest.approx(
        (-0.03 + 0.02) / (1.0 - 0.02)
    )
    assert wpimath.applyDeadband(-0.02, 0.02) == pytest.approx(0.0)
    assert wpimath.applyDeadband(-0.01, 0.02) == pytest.approx(0.0)
    assert wpimath.applyDeadband(0.0, 0.02) == pytest.approx(0.0)
    assert wpimath.applyDeadband(0.01, 0.02) == pytest.approx(0.0)
    assert wpimath.applyDeadband(0.02, 0.02) == pytest.approx(0.0)
    assert wpimath.applyDeadband(0.03, 0.02) == pytest.approx(
        (0.03 - 0.02) / (1.0 - 0.02)
    )
    assert wpimath.applyDeadband(1.0, 0.02) == pytest.approx(1.0)


def test_apply_deadband_arbitrary_scale():
    assert wpimath.applyDeadband(-2.5, 0.02, 2.5) == pytest.approx(-2.5)
    assert wpimath.applyDeadband(-0.02, 0.02, 2.5) == pytest.approx(0.0)
    assert wpimath.applyDeadband(-0.01, 0.02, 2.5) == pytest.approx(0.0)
    assert wpimath.applyDeadband(0.0, 0.02, 2.5) == pytest.approx(0.0)
    assert wpimath.applyDeadband(0.01, 0.02, 2.5) == pytest.approx(0.0)
    assert wpimath.applyDeadband(0.02, 0.02, 2.5) == pytest.approx(0.0)
    assert wpimath.applyDeadband(2.5, 0.02, 2.5) == pytest.approx(2.5)


def test_apply_deadband_large_max_magnitude():
    assert wpimath.applyDeadband(100.0, 20.0, math.inf) == pytest.approx(80.0)


def test_input_modulus():
    # Symmetric range
    assert wpimath.inputModulus(170.0 - (-170.0), -180.0, 180.0) == pytest.approx(-20.0)
    assert wpimath.inputModulus(170.0 + 360.0 - (-170.0), -180.0, 180.0) == pytest.approx(-20.0)
    assert wpimath.inputModulus(170.0 - (-170.0 + 360.0), -180.0, 180.0) == pytest.approx(-20.0)
    assert wpimath.inputModulus(-170.0 - 170.0, -180.0, 180.0) == pytest.approx(20.0)
    assert wpimath.inputModulus(-170.0 + 360.0 - 170.0, -180.0, 180.0) == pytest.approx(20.0)
    assert wpimath.inputModulus(-170.0 - (170.0 + 360.0), -180.0, 180.0) == pytest.approx(20.0)

    # Range starting at zero
    assert wpimath.inputModulus(170.0 - 190.0, 0.0, 360.0) == pytest.approx(340.0)
    assert wpimath.inputModulus(170.0 + 360.0 - 190.0, 0.0, 360.0) == pytest.approx(340.0)
    assert wpimath.inputModulus(170.0 - (190.0 + 360.0), 0.0, 360.0) == pytest.approx(340.0)

    # Asymmetric range not starting at zero
    assert wpimath.inputModulus(170.0 - (-170.0), -170.0, 190.0) == pytest.approx(-20.0)

    # Range with both positive endpoints
    assert wpimath.inputModulus(0.0, 1.0, 3.0) == pytest.approx(2.0)
    assert wpimath.inputModulus(1.0, 1.0, 3.0) == pytest.approx(3.0)
    assert wpimath.inputModulus(2.0, 1.0, 3.0) == pytest.approx(2.0)
    assert wpimath.inputModulus(3.0, 1.0, 3.0) == pytest.approx(3.0)
    assert wpimath.inputModulus(4.0, 1.0, 3.0) == pytest.approx(2.0)


def test_angle_modulus():
    assert wpimath.angleModulus(-2000 * math.pi / 180) == pytest.approx(
        160 * math.pi / 180, abs=1e-10
    )
    assert wpimath.angleModulus(358 * math.pi / 180) == pytest.approx(
        -2 * math.pi / 180, abs=1e-10
    )
    assert wpimath.angleModulus(2.0 * math.pi) == pytest.approx(0.0, abs=1e-10)

    assert wpimath.angleModulus(5 * math.pi) == pytest.approx(math.pi)
    assert wpimath.angleModulus(-5 * math.pi) == pytest.approx(math.pi)
    assert wpimath.angleModulus(math.pi / 2) == pytest.approx(math.pi / 2)
    assert wpimath.angleModulus(-math.pi / 2) == pytest.approx(-math.pi / 2)


def test_translation2d_slew_rate_limit_unchanged():
    translation1 = Translation2d(0.0, 0.0)
    translation2 = Translation2d(2.0, 2.0)

    result = wpimath.slewRateLimit(translation1, translation2, 1.0, 50.0)
    assert result == Translation2d(2.0, 2.0)


def test_translation2d_slew_rate_limit_changed():
    translation3 = Translation2d(1.0, 1.0)
    translation4 = Translation2d(3.0, 3.0)

    result = wpimath.slewRateLimit(translation3, translation4, 0.25, 2.0)
    expected_x = 1.0 + 0.5 * (math.sqrt(2.0) / 2.0)
    expected_y = 1.0 + 0.5 * (math.sqrt(2.0) / 2.0)
    assert result == Translation2d(expected_x, expected_y)


def test_translation3d_slew_rate_limit_unchanged():
    translation1 = Translation3d(0.0, 0.0, 0.0)
    translation2 = Translation3d(2.0, 2.0, 2.0)

    result = wpimath.slewRateLimit(translation1, translation2, 1.0, 50.0)
    assert result == Translation3d(2.0, 2.0, 2.0)


def test_translation3d_slew_rate_limit_changed():
    translation3 = Translation3d(1.0, 1.0, 1.0)
    translation4 = Translation3d(3.0, 3.0, 3.0)

    result = wpimath.slewRateLimit(translation3, translation4, 0.25, 2.0)
    inv_sqrt3 = 1.0 / math.sqrt(3.0)
    expected = Translation3d(
        1.0 + 0.5 * inv_sqrt3,
        1.0 + 0.5 * inv_sqrt3,
        1.0 + 0.5 * inv_sqrt3,
    )
    assert result == expected
