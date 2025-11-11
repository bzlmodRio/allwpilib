import pytest
import math
import numpy as np

from wpimath.controller import ImplicitModelFollower_2_2
from wpimath.system.plant import LinearSystemId
from wpimath.units import (
    meters,
    meters_per_second,
    meters_per_second_squared,
    radians_per_second,
    radians_per_second_squared,
    volts,
    seconds,
)


def test_same_model():
    dt = seconds(0.005)

    plant = LinearSystemId.identifyDrivetrainSystem(
        volts(1) / meters_per_second(1),
        volts(1) / meters_per_second_squared(1),
        volts(1) / meters_per_second(1),
        volts(1) / meters_per_second_squared(1),
    )

    imf = ImplicitModelFollower_2_2(plant, plant)

    x = np.array([[0.0], [0.0]])
    x_imf = np.array([[0.0], [0.0]])

    # Forward
    u = np.array([[12.0], [12.0]])
    for t in np.arange(0, 3, dt):
        x = plant.calculateX(x, u, dt)
        x_imf = plant.calculateX(x_imf, imf.calculate(x_imf, u), dt)

        assert x[0] == pytest.approx(x_imf[0])
        assert x[1] == pytest.approx(x_imf[1])

    # Backward
    x = np.array([[0.0], [0.0]])
    x_imf = np.array([[0.0], [0.0]])
    u = np.array([[-12.0], [-12.0]])
    for t in np.arange(0, 3, dt):
        x = plant.calculateX(x, u, dt)
        x_imf = plant.calculateX(x_imf, imf.calculate(x_imf, u), dt)

        assert x[0] == pytest.approx(x_imf[0])
        assert x[1] == pytest.approx(x_imf[1])

    # Rotate CCW
    x = np.array([[0.0], [0.0]])
    x_imf = np.array([[0.0], [0.0]])
    u = np.array([[-12.0], [12.0]])
    for t in np.arange(0, 3, dt):
        x = plant.calculateX(x, u, dt)
        x_imf = plant.calculateX(x_imf, imf.calculate(x_imf, u), dt)

        assert x[0] == pytest.approx(x_imf[0])
        assert x[1] == pytest.approx(x_imf[1])


def test_slower_ref_model():
    dt = seconds(0.005)

    plant = LinearSystemId.identifyDrivetrainSystem(
        volts(1) / meters_per_second(1),
        volts(1) / meters_per_second_squared(1),
        volts(1) / meters_per_second(1),
        volts(1) / meters_per_second_squared(1),
    )

    # Linear acceleration is slower, but angular acceleration is the same
    plant_ref = LinearSystemId.identifyDrivetrainSystem(
        volts(1) / meters_per_second(1),
        volts(2) / meters_per_second_squared(1),
        volts(1) / meters_per_second(1),
        volts(1) / meters_per_second_squared(1),
    )

    imf = ImplicitModelFollower_2_2(plant, plant_ref)

    x = np.array([[0.0], [0.0]])
    x_imf = np.array([[0.0], [0.0]])

    # Forward
    u = np.array([[12.0], [12.0]])
    for t in np.arange(0, 3, dt):
        x = plant.calculateX(x, u, dt)
        x_imf = plant.calculateX(x_imf, imf.calculate(x_imf, u), dt)

        assert x[0] >= x_imf[0]
        assert x[1] >= x_imf[1]

    # Backward
    x = np.array([[0.0], [0.0]])
    x_imf = np.array([[0.0], [0.0]])
    u = np.array([[-12.0], [-12.0]])
    for t in np.arange(0, 3, dt):
        x = plant.calculateX(x, u, dt)
        x_imf = plant.calculateX(x_imf, imf.calculate(x_imf, u), dt)

        assert x[0] <= x_imf[0]
        assert x[1] <= x_imf[1]

    # Rotate CCW
    x = np.array([[0.0], [0.0]])
    x_imf = np.array([[0.0], [0.0]])
    u = np.array([[-12.0], [12.0]])
    for t in np.arange(0, 3, dt):
        x = plant.calculateX(x, u, dt)
        x_imf = plant.calculateX(x_imf, imf.calculate(x_imf, u), dt)

        assert x[0] == pytest.approx(x_imf[0], abs=1e-5)
        assert x[1] == pytest.approx(x_imf[1], abs=1e-5)