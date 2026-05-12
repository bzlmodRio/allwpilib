import math
import numpy as np
import pytest

import wpimath
from wpimath import ArmFeedforward

KS = 0.5
KG = 1.0
KV = 1.5
KA = 2.0


def _simulate_arm(Ks, Kv, Ka, Kg, current_angle, current_velocity, input_voltage, dt):
    A = np.array([[0.0, 1.0], [0.0, -Kv / Ka]])
    B = np.array([[0.0], [1.0 / Ka]])

    def f(x, u):
        vel = x[1, 0]
        sign_vel = 1.0 if vel > 0 else (-1.0 if vel < 0 else 0.0)
        c = np.array(
            [[0.0], [-Ks / Ka * sign_vel - Kg / Ka * math.cos(x[0, 0])]]
        )
        return A @ x + B @ u + c

    x0 = np.array([[current_angle], [current_velocity]])
    u = np.array([[input_voltage]])
    return wpimath.RK4(f, x0, u, dt)


def _calculate_and_simulate(
    arm_ff, Ks, Kv, Ka, Kg, current_angle, current_velocity, next_velocity, dt
):
    input_voltage = arm_ff.calculate(current_angle, current_velocity, next_velocity)
    result = _simulate_arm(Ks, Kv, Ka, Kg, current_angle, current_velocity, input_voltage, dt)
    assert result[1, 0] == pytest.approx(next_velocity, abs=1e-4)


def test_calculate():
    ff = ArmFeedforward(KS, KG, KV, KA)

    assert ff.calculate(math.pi / 3, 0.0) == pytest.approx(0.5, abs=0.002)
    assert ff.calculate(math.pi / 3, 1.0) == pytest.approx(2.5, abs=0.002)

    dt = 0.020
    _calculate_and_simulate(ff, KS, KV, KA, KG, math.pi / 3, 1.0, 1.05, dt)
    _calculate_and_simulate(ff, KS, KV, KA, KG, math.pi / 3, 1.0, 0.95, dt)
    _calculate_and_simulate(ff, KS, KV, KA, KG, -math.pi / 3, 1.0, 1.05, dt)
    _calculate_and_simulate(ff, KS, KV, KA, KG, -math.pi / 3, 1.0, 0.95, dt)


def test_calculate_ill_conditioned_model():
    Ks = 0.39671
    Kv = 2.7167
    Ka = 1e-2
    Kg = 0.2708
    ff = ArmFeedforward(Ks, Kg, Kv, Ka)

    current_angle = 1.0
    current_velocity = 0.02
    next_velocity = 0.0
    dt = 0.020

    average_accel = (next_velocity - current_velocity) / dt

    expected = Ks + Kv * current_velocity + Ka * average_accel + Kg * math.cos(current_angle)
    assert ff.calculate(current_angle, current_velocity, next_velocity) == pytest.approx(
        expected, abs=1e-9
    )


def test_calculate_ill_conditioned_gradient():
    Ks = 0.39671
    Kv = 2.7167
    Ka = 0.50799
    Kg = 0.2708
    ff = ArmFeedforward(Ks, Kg, Kv, Ka)

    _calculate_and_simulate(ff, Ks, Kv, Ka, Kg, 1.0, 0.02, 0.0, 0.020)


def test_achievable_velocity():
    ff = ArmFeedforward(KS, KG, KV, KA)

    assert ff.maxAchievableVelocity(12.0, math.pi / 3, 1.0) == pytest.approx(6.0, abs=0.002)
    assert ff.minAchievableVelocity(11.5, math.pi / 3, 1.0) == pytest.approx(-9.0, abs=0.002)


def test_achievable_acceleration():
    ff = ArmFeedforward(KS, KG, KV, KA)

    assert ff.maxAchievableAcceleration(12.0, math.pi / 3, 1.0) == pytest.approx(4.75, abs=0.002)
    assert ff.maxAchievableAcceleration(12.0, math.pi / 3, -1.0) == pytest.approx(6.75, abs=0.002)
    assert ff.minAchievableAcceleration(12.0, math.pi / 3, 1.0) == pytest.approx(-7.25, abs=0.002)
    assert ff.minAchievableAcceleration(12.0, math.pi / 3, -1.0) == pytest.approx(-5.25, abs=0.002)


def test_negative_gains():
    ff = ArmFeedforward(KS, KG, -KV, -KA)
    assert ff.getKv() == pytest.approx(0.0)
    assert ff.getKa() == pytest.approx(0.0)
