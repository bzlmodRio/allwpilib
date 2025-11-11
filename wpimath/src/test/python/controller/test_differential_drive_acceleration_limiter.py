import pytest
import numpy as np

from wpimath.controller import DifferentialDriveAccelerationLimiter
from wpimath.system.plant import LinearSystemId
from wpimath.units import (
    meters,
    meters_per_second,
    meters_per_second_squared,
    radians,
    radians_per_second,
    radians_per_second_squared,
    seconds,
    volts,
    # per_meter,
    # per_meter_squared,
)

per_meter = float
per_meter_squared = float

def test_low_limits():
    trackwidth = meters(0.9)
    dt = seconds(0.005)
    max_a = meters_per_second_squared(2)
    max_alpha = radians_per_second_squared(2)

    plant = LinearSystemId.identifyDrivetrainSystem(
        volts(1) / meters_per_second(1),
        volts(1) / meters_per_second_squared(1),
        volts(1) / meters_per_second(1),
        volts(1) / meters_per_second_squared(1),
    )

    accel_limiter = DifferentialDriveAccelerationLimiter(
        plant, trackwidth, max_a, max_alpha
    )

    x = np.array([0.0, 0.0])
    x_accel_limiter = np.array([0.0, 0.0])

    # Ensure voltage exceeds acceleration before limiting
    accels = plant.A() @ x_accel_limiter + plant.B() @ np.array([12.0, 12.0])
    a = meters_per_second_squared((accels[0] + accels[1]) / 2.0)
    assert abs(a) > max_a

    accels = plant.A() @ x_accel_limiter + plant.B() @ np.array([-12.0, 12.0])
    alpha = radians_per_second_squared((accels[1] - accels[0]) / trackwidth)
    assert abs(alpha) > max_alpha

    # Forward
    u = np.array([12.0, 12.0])
    for t in np.arange(0, 3, dt):
        x = plant.calculateX(x, u, dt)
        wheel_voltages = accel_limiter.calculate(
            meters_per_second(x_accel_limiter[0]),
            meters_per_second(x_accel_limiter[1]),
            volts(u[0]),
            volts(u[1]),
        )
        x_accel_limiter = plant.calculateX(
            x_accel_limiter, np.array([wheel_voltages.left, wheel_voltages.right]), dt
        )

        accels = plant.A() @ x_accel_limiter + plant.B() @ np.array([wheel_voltages.left, wheel_voltages.right])
        a = meters_per_second_squared((accels[0] + accels[1]) / 2.0)
        alpha = radians_per_second_squared((accels[1] - accels[0]) / trackwidth)

        assert abs(a) <= max_a
        assert abs(alpha) <= max_alpha

    # Backward
    u = np.array([-12.0, -12.0])
    for t in np.arange(0, 3, dt):
        x = plant.calculateX(x, u, dt)
        wheel_voltages = accel_limiter.calculate(
            meters_per_second(x_accel_limiter[0]),
            meters_per_second(x_accel_limiter[1]),
            volts(u[0]),
            volts(u[1]),
        )
        x_accel_limiter = plant.calculateX(
            x_accel_limiter, np.array([wheel_voltages.left, wheel_voltages.right]), dt
        )

        accels = plant.A() @ x_accel_limiter + plant.B() @ np.array([wheel_voltages.left, wheel_voltages.right])
        a = meters_per_second_squared((accels[0] + accels[1]) / 2.0)
        alpha = radians_per_second_squared((accels[1] - accels[0]) / trackwidth)

        assert abs(a) <= max_a
        assert abs(alpha) <= max_alpha

    # Rotate CCW
    u = np.array([-12.0, 12.0])
    for t in np.arange(0, 3, dt):
        x = plant.calculateX(x, u, dt)
        wheel_voltages = accel_limiter.calculate(
            meters_per_second(x_accel_limiter[0]),
            meters_per_second(x_accel_limiter[1]),
            volts(u[0]),
            volts(u[1]),
        )
        x_accel_limiter = plant.calculateX(
            x_accel_limiter, np.array([wheel_voltages.left, wheel_voltages.right]), dt
        )

        accels = plant.A() @ x_accel_limiter + plant.B() @ np.array([wheel_voltages.left, wheel_voltages.right])
        a = meters_per_second_squared((accels[0] + accels[1]) / 2.0)
        alpha = radians_per_second_squared((accels[1] - accels[0]) / trackwidth)

        assert abs(a) <= max_a
        assert abs(alpha) <= max_alpha


def test_high_limits():
    trackwidth = meters(0.9)
    dt = seconds(0.005)

    plant = LinearSystemId.identifyDrivetrainSystem(
        volts(1) / meters_per_second(1),
        volts(1) / meters_per_second_squared(1),
        volts(1) / meters_per_second(1),
        volts(1) / meters_per_second_squared(1),
    )

    # Limits are so high, they don't get hit, so states of constrained and
    # unconstrained systems should match
    accel_limiter = DifferentialDriveAccelerationLimiter(
        plant, trackwidth, meters_per_second_squared(1e3), radians_per_second_squared(1e3)
    )

    x = np.array([0.0, 0.0])
    x_accel_limiter = np.array([0.0, 0.0])

    # Forward
    u = np.array([12.0, 12.0])
    for t in np.arange(0, 3, dt):
        x = plant.calculateX(x, u, dt)
        wheel_voltages = accel_limiter.calculate(
            meters_per_second(x_accel_limiter[0]),
            meters_per_second(x_accel_limiter[1]),
            volts(u[0]),
            volts(u[1]),
        )
        x_accel_limiter = plant.calculateX(
            x_accel_limiter, np.array([wheel_voltages.left, wheel_voltages.right]), dt
        )

        assert x[0] == pytest.approx(x_accel_limiter[0])
        assert x[1] == pytest.approx(x_accel_limiter[1])

    # Backward
    x = np.array([0.0, 0.0])
    x_accel_limiter = np.array([0.0, 0.0])
    u = np.array([-12.0, -12.0])
    for t in np.arange(0, 3, dt):
        x = plant.calculateX(x, u, dt)
        wheel_voltages = accel_limiter.calculate(
            meters_per_second(x_accel_limiter[0]),
            meters_per_second(x_accel_limiter[1]),
            volts(u[0]),
            volts(u[1]),
        )
        x_accel_limiter = plant.calculateX(
            x_accel_limiter, np.array([wheel_voltages.left, wheel_voltages.right]), dt
        )

        assert x[0] == pytest.approx(x_accel_limiter[0])
        assert x[1] == pytest.approx(x_accel_limiter[1])

    # Rotate CCW
    x = np.array([0.0, 0.0])
    x_accel_limiter = np.array([0.0, 0.0])
    u = np.array([-12.0, 12.0])
    for t in np.arange(0, 3, dt):
        x = plant.calculateX(x, u, dt)
        wheel_voltages = accel_limiter.calculate(
            meters_per_second(x_accel_limiter[0]),
            meters_per_second(x_accel_limiter[1]),
            volts(u[0]),
            volts(u[1]),
        )
        x_accel_limiter = plant.calculateX(
            x_accel_limiter, np.array([wheel_voltages.left, wheel_voltages.right]), dt
        )

        assert x[0] == pytest.approx(x_accel_limiter[0])
        assert x[1] == pytest.approx(x_accel_limiter[1])


def test_separate_min_max_low_limits():
    trackwidth = meters(0.9)
    dt = seconds(0.005)
    min_a = meters_per_second_squared(-1)
    max_a = meters_per_second_squared(2)
    max_alpha = radians_per_second_squared(2)

    plant = LinearSystemId.identifyDrivetrainSystem(
        volts(1) / meters_per_second(1),
        volts(1) / meters_per_second_squared(1),
        volts(1) / meters_per_second(1),
        volts(1) / meters_per_second_squared(1),
    )

    accel_limiter = DifferentialDriveAccelerationLimiter(
        plant, trackwidth, min_a, max_a, max_alpha
    )

    x = np.array([0.0, 0.0])
    x_accel_limiter = np.array([0.0, 0.0])

    # Ensure voltage exceeds acceleration before limiting
    accels = plant.A() @ x_accel_limiter + plant.B() @ np.array([12.0, 12.0])
    a = meters_per_second_squared((accels[0] + accels[1]) / 2.0)
    assert abs(a) > max_a
    assert abs(a) > -min_a

    # a should always be within [minA, maxA]
    # Forward
    u = np.array([12.0, 12.0])
    for t in np.arange(0, 3, dt):
        x = plant.calculateX(x, u, dt)
        wheel_voltages = accel_limiter.calculate(
            meters_per_second(x_accel_limiter[0]),
            meters_per_second(x_accel_limiter[1]),
            volts(u[0]),
            volts(u[1]),
        )
        x_accel_limiter = plant.calculateX(
            x_accel_limiter, np.array([wheel_voltages.left, wheel_voltages.right]), dt
        )

        accels = plant.A() @ x_accel_limiter + plant.B() @ np.array([wheel_voltages.left, wheel_voltages.right])
        a = meters_per_second_squared((accels[0] + accels[1]) / 2.0)
        assert a >= min_a
        assert a <= max_a

    # Backward
    u = np.array([-12.0, -12.0])
    for t in np.arange(0, 3, dt):
        x = plant.calculateX(x, u, dt)
        wheel_voltages = accel_limiter.calculate(
            meters_per_second(x_accel_limiter[0]),
            meters_per_second(x_accel_limiter[1]),
            volts(u[0]),
            volts(u[1]),
        )
        x_accel_limiter = plant.calculateX(
            x_accel_limiter, np.array([wheel_voltages.left, wheel_voltages.right]), dt
        )

        accels = plant.A() @ x_accel_limiter + plant.B() @ np.array([wheel_voltages.left, wheel_voltages.right])
        a = meters_per_second_squared((accels[0] + accels[1]) / 2.0)
        assert a >= min_a
        assert a <= max_a


def test_min_accel_greater_than_max_accel():
    plant = LinearSystemId.identifyDrivetrainSystem(
        volts(1) / meters_per_second(1),
        volts(1) / meters_per_second_squared(1),
        volts(1) / meters_per_second(1),
        volts(1) / meters_per_second_squared(1),
    )

    with pytest.raises(ValueError):
        DifferentialDriveAccelerationLimiter(
            plant,
            meters(1),
            meters_per_second_squared(1),
            meters_per_second_squared(-1),
            radians_per_second_squared(1),
        )