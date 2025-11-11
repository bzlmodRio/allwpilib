import pytest
import math
import numpy as np

from wpimath.controller import ElevatorFeedforward, LinearPlantInversionFeedforward_1_1
from wpimath.units import (
    meters,
    meters_per_second,
    meters_per_second_squared,
    volts,
    seconds,
)


def test_calculate():
    ks = volts(0.5)
    kv = volts(1.5) / meters_per_second(1)
    ka = volts(2) / meters_per_second_squared(1)
    kg = volts(1)
    elevator_ff = ElevatorFeedforward(ks, kg, kv, ka)

    assert elevator_ff.calculate(meters_per_second(0)) == pytest.approx(kg, abs=0.002)
    assert elevator_ff.calculate(meters_per_second(2)) == pytest.approx(4.5, abs=0.002)

    A = np.array([[-kv / ka]])
    B = np.array([[1.0 / ka]])
    dt = seconds(0.02)
    plant_inversion = LinearPlantInversionFeedforward_1_1(A, B, dt)

    r = np.array([[2.0]])
    next_r = np.array([[3.0]])
    calculated_value = plant_inversion.calculate(r, next_r)[0] + ks + kg
    assert calculated_value == pytest.approx(
        elevator_ff.calculate(meters_per_second(2), meters_per_second(3)), abs=0.002
    )


def test_achievable_velocity():
    ks = volts(0.5)
    kv = volts(1.5) / meters_per_second(1)
    ka = volts(2) / meters_per_second_squared(1)
    kg = volts(1)
    elevator_ff = ElevatorFeedforward(ks, kg, kv, ka)
    
    assert elevator_ff.maxAchievableVelocity(
        volts(11), meters_per_second_squared(1)
    ) == pytest.approx(5, abs=0.002)
    assert elevator_ff.minAchievableVelocity(
        volts(11), meters_per_second_squared(1)
    ) == pytest.approx(-9, abs=0.002)


def test_achievable_acceleration():
    ks = volts(0.5)
    kv = volts(1.5) / meters_per_second(1)
    ka = volts(2) / meters_per_second_squared(1)
    kg = volts(1)
    elevator_ff = ElevatorFeedforward(ks, kg, kv, ka)

    assert elevator_ff.maxAchievableAcceleration(
        volts(12), meters_per_second(2)
    ) == pytest.approx(3.75, abs=0.002)
    assert elevator_ff.maxAchievableAcceleration(
        volts(12), meters_per_second(-2)
    ) == pytest.approx(7.25, abs=0.002)
    assert elevator_ff.minAchievableAcceleration(
        volts(12), meters_per_second(2)
    ) == pytest.approx(-8.25, abs=0.002)
    assert elevator_ff.minAchievableAcceleration(
        volts(12), meters_per_second(-2)
    ) == pytest.approx(-4.75, abs=0.002)


def test_negative_gains():
    ks = volts(0.5)
    kv = volts(1.5) / meters_per_second(1)
    ka = volts(2) / meters_per_second_squared(1)
    kg = volts(1)
    elevator_ff = ElevatorFeedforward(ks, kg, -kv, -ka)
    assert elevator_ff.getKv() == pytest.approx(0)
    assert elevator_ff.getKa() == pytest.approx(0)