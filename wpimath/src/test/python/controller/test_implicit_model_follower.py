import numpy as np
import pytest

from wpimath import ImplicitModelFollower_2_2, Models


DT = 0.005  # 5 ms


def _make_plant():
    return Models.differentialDriveFromSysId(1.0, 1.0, 1.0, 1.0)


def _make_slow_ref_plant():
    return Models.differentialDriveFromSysId(1.0, 2.0, 1.0, 1.0)


def test_same_model():
    plant = _make_plant()
    imf = ImplicitModelFollower_2_2(plant, plant)

    x = np.zeros(2)
    x_imf = np.zeros(2)

    # Forward
    u = np.array([12.0, 12.0])
    for _ in range(int(3.0 / DT)):
        x = plant.calculateX(x, u, DT)
        u_imf = imf.calculate(x_imf, u)
        x_imf = plant.calculateX(x_imf, u_imf, DT)

        assert x[0] == pytest.approx(x_imf[0])
        assert x[1] == pytest.approx(x_imf[1])

    # Backward
    u = np.array([-12.0, -12.0])
    for _ in range(int(3.0 / DT)):
        x = plant.calculateX(x, u, DT)
        u_imf = imf.calculate(x_imf, u)
        x_imf = plant.calculateX(x_imf, u_imf, DT)

        assert x[0] == pytest.approx(x_imf[0])
        assert x[1] == pytest.approx(x_imf[1])

    # Rotate CCW
    u = np.array([-12.0, 12.0])
    for _ in range(int(3.0 / DT)):
        x = plant.calculateX(x, u, DT)
        u_imf = imf.calculate(x_imf, u)
        x_imf = plant.calculateX(x_imf, u_imf, DT)

        assert x[0] == pytest.approx(x_imf[0])
        assert x[1] == pytest.approx(x_imf[1])


def test_slower_ref_model():
    plant = _make_plant()
    plant_ref = _make_slow_ref_plant()
    imf = ImplicitModelFollower_2_2(plant, plant_ref)

    x = np.zeros(2)
    x_imf = np.zeros(2)

    # Forward: IMF slows down linear acceleration, so x_imf <= x
    u = np.array([12.0, 12.0])
    for _ in range(int(3.0 / DT)):
        x = plant.calculateX(x, u, DT)
        u_imf = imf.calculate(x_imf, u)
        x_imf = plant.calculateX(x_imf, u_imf, DT)

        assert x[0] >= x_imf[0]
        assert x[1] >= x_imf[1]

    # Backward: IMF slows magnitude, so x_imf >= x (both negative, IMF less negative)
    x = np.zeros(2)
    x_imf = np.zeros(2)
    u = np.array([-12.0, -12.0])
    for _ in range(int(3.0 / DT)):
        x = plant.calculateX(x, u, DT)
        u_imf = imf.calculate(x_imf, u)
        x_imf = plant.calculateX(x_imf, u_imf, DT)

        assert x[0] <= x_imf[0]
        assert x[1] <= x_imf[1]

    # Rotate CCW: angular accel the same, so values should be near equal
    x = np.zeros(2)
    x_imf = np.zeros(2)
    u = np.array([-12.0, 12.0])
    for _ in range(int(3.0 / DT)):
        x = plant.calculateX(x, u, DT)
        u_imf = imf.calculate(x_imf, u)
        x_imf = plant.calculateX(x_imf, u_imf, DT)

        assert x[0] == pytest.approx(x_imf[0], abs=1e-5)
        assert x[1] == pytest.approx(x_imf[1], abs=1e-5)
