import pytest
import math
import numpy as np

from wpimath.controller import ArmFeedforward
from wpimath.system.numerical_integration import *
from wpimath.units import (
    meters,
    volts,
    radians_per_second,
    radians_per_second_squared,
    radians,
    seconds,
)


def _simulate(ks, kv, ka, kg, current_angle, current_velocity, input_voltage, dt):
    """
    Simulates a single-jointed arm and returns the final state.
    """
    A = np.array([[0.0, 1.0], [0.0, -kv / ka]])
    B = np.array([[0.0], [1.0 / ka]])

    def func(x, u):
        c = np.array(
            [
                [0.0],
                [
                    -ks / ka * math.copysign(1.0, x[1])
                    - kg / ka * math.cos(x[0])
                ],
            ]
        )
        return np.dot(A, x) + np.dot(B, u) + c

    x0 = np.array([[current_angle], [current_velocity]])
    u0 = np.array([[input_voltage]])

    return rk4_x_u_dt(func, x0, u0, dt)


def _calculate_and_simulate(
    arm_ff, ks, kv, ka, kg, current_angle, current_velocity, next_velocity, dt
):
    """
    Helper to calculate feedforward and then simulate the arm.
    """
    input_voltage = arm_ff.calculate(current_angle, current_velocity, next_velocity)
    simulated_velocity = _simulate(
        ks, kv, ka, kg, current_angle, current_velocity, input_voltage, dt
    )[1]
    assert simulated_velocity == pytest.approx(next_velocity, abs=1e-4)


def test_calculate():
    ks = volts(0.5)
    kv = volts(1.5) / radians_per_second(1)
    ka = volts(2) / radians_per_second_squared(1)
    kg = volts(1)
    arm_ff = ArmFeedforward(ks, kg, kv, ka)

    # Calculate(angle, angular velocity)
    assert arm_ff.calculate(radians(math.pi / 3), radians_per_second(0)) == pytest.approx(0.5, abs=0.002)
    assert arm_ff.calculate(radians(math.pi / 3), radians_per_second(1)) == pytest.approx(2.5, abs=0.002)

    # Calculate(currentAngle, currentVelocity, nextAngle, dt)
    _calculate_and_simulate(
        arm_ff,
        ks,
        kv,
        ka,
        kg,
        radians(math.pi / 3),
        radians_per_second(1),
        radians_per_second(1.05),
        seconds(0.02),
    )
    _calculate_and_simulate(
        arm_ff,
        ks,
        kv,
        ka,
        kg,
        radians(math.pi / 3),
        radians_per_second(1),
        radians_per_second(0.95),
        seconds(0.02),
    )
    _calculate_and_simulate(
        arm_ff,
        ks,
        kv,
        ka,
        kg,
        radians(-math.pi / 3),
        radians_per_second(1),
        radians_per_second(1.05),
        seconds(0.02),
    )
    _calculate_and_simulate(
        arm_ff,
        ks,
        kv,
        ka,
        kg,
        radians(-math.pi / 3),
        radians_per_second(1),
        radians_per_second(0.95),
        seconds(0.02),
    )


def test_calculate_ill_conditioned_model():
    ks = volts(0.39671)
    kv = volts(2.7167) / radians_per_second(1)
    ka = volts(1e-2) / radians_per_second_squared(1)
    kg = volts(0.2708)
    arm_ff = ArmFeedforward(ks, kg, kv, ka)

    current_angle = radians(1)
    current_velocity = radians_per_second(0.02)
    next_velocity = radians_per_second(0)

    average_accel = (next_velocity - current_velocity) / seconds(0.02)

    expected_value = (
        ks + kv * current_velocity + ka * average_accel + kg * math.cos(current_angle)
    )
    assert arm_ff.calculate(current_angle, current_velocity, next_velocity) == pytest.approx(
        expected_value
    )


def test_calculate_ill_conditioned_gradient():
    ks = volts(0.39671)
    kv = volts(2.7167) / radians_per_second(1)
    ka = volts(0.50799) / radians_per_second_squared(1)
    kg = volts(0.2708)
    arm_ff = ArmFeedforward(ks, kg, kv, ka)

    _calculate_and_simulate(
        arm_ff,
        ks,
        kv,
        ka,
        kg,
        radians(1),
        radians_per_second(0.02),
        radians_per_second(0),
        seconds(0.02),
    )


def test_achievable_velocity():
    ks = volts(0.5)
    kv = volts(1.5) / radians_per_second(1)
    ka = volts(2) / radians_per_second_squared(1)
    kg = volts(1)
    arm_ff = ArmFeedforward(ks, kg, kv, ka)

    assert arm_ff.maxAchievableVelocity(
        volts(12), radians(math.pi / 3), radians_per_second_squared(1)
    ) == pytest.approx(6, abs=0.002)
    assert arm_ff.minAchievableVelocity(
        volts(11.5), radians(math.pi / 3), radians_per_second_squared(1)
    ) == pytest.approx(-9, abs=0.002)


def test_achievable_acceleration():
    ks = volts(0.5)
    kv = volts(1.5) / radians_per_second(1)
    ka = volts(2) / radians_per_second_squared(1)
    kg = volts(1)
    arm_ff = ArmFeedforward(ks, kg, kv, ka)

    assert arm_ff.maxAchievableAcceleration(
        volts(12), radians(math.pi / 3), radians_per_second(1)
    ) == pytest.approx(4.75, abs=0.002)
    assert arm_ff.maxAchievableAcceleration(
        volts(12), radians(math.pi / 3), radians_per_second(-1)
    ) == pytest.approx(6.75, abs=0.002)
    assert arm_ff.minAchievableAcceleration(
        volts(12), radians(math.pi / 3), radians_per_second(1)
    ) == pytest.approx(-7.25, abs=0.002)
    assert arm_ff.minAchievableAcceleration(
        volts(12), radians(math.pi / 3), radians_per_second(-1)
    ) == pytest.approx(-5.25, abs=0.002)


def test_negative_gains():
    ks = volts(0.5)
    kv = volts(1.5) / radians_per_second(1)
    ka = volts(2) / radians_per_second_squared(1)
    kg = volts(1)
    arm_ff = ArmFeedforward(ks, kg, -kv, -ka)

    assert arm_ff.getKv() == pytest.approx(0)
    assert arm_ff.getKa() == pytest.approx(0)