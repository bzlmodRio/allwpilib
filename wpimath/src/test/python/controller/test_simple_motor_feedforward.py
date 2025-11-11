import pytest
import math
import numpy as np

from wpimath.controller import SimpleMotorFeedforwardMeters, LinearPlantInversionFeedforward_1_1
from wpimath.units import (
    meters_per_second,
    meters_per_second_squared,
    volts,
    seconds,
)


def test_calculate():
    ks = volts(0.5)
    kv = volts(3) / meters_per_second(1)
    ka = volts(0.6) / meters_per_second_squared(1)
    dt = seconds(0.02)

    A = np.array([[-kv / ka]])
    B = np.array([[1.0 / ka]])

    plant_inversion = LinearPlantInversionFeedforward_1_1(A, B, dt)
    simple_motor = SimpleMotorFeedforwardMeters(ks, kv, ka)

    r = np.array([[2.0]])
    next_r = np.array([[3.0]])

    assert simple_motor.calculate(
        meters_per_second(2), meters_per_second(3)
    ) == pytest.approx(
        (volts(37.524995834325161) + ks), abs=0.002
    )
    assert simple_motor.calculate(
        meters_per_second(2), meters_per_second(3)
    ) == pytest.approx(
        plant_inversion.calculate(r, next_r)[0] + ks, abs=0.002
    )

    # These won't match exactly. It's just an approximation to make sure they're
    # in the same ballpark.
    assert simple_motor.calculate(
        meters_per_second(2), meters_per_second(3)
    ) == pytest.approx(
        plant_inversion.calculate(r, next_r)[0] + ks, abs=2.0
    )


def test_negative_gains():
    ks = volts(0.5)
    kv = volts(-3) / meters_per_second(1)
    ka = volts(-0.6) / meters_per_second_squared(1)
    dt = seconds(0)
    simple_motor = SimpleMotorFeedforwardMeters(ks, kv, ka, dt)
    assert simple_motor.getKv() == pytest.approx(0)
    assert simple_motor.getKa() == pytest.approx(0)
    assert simple_motor.getDt() == pytest.approx(0.02)