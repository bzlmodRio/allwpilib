import numpy as np
import pytest

from wpimath import DifferentialDriveAccelerationLimiter, Models

TRACKWIDTH = 0.9
DT = 0.005  # 5 ms
MAX_A = 2.0
MAX_ALPHA = 2.0


def _make_plant():
    return Models.differential_drive_from_sys_id(1.0, 1.0, 1.0, 1.0)


def test_low_limits():
    plant = _make_plant()
    accel_limiter = DifferentialDriveAccelerationLimiter(
        plant, TRACKWIDTH, MAX_A, MAX_ALPHA
    )

    x = np.zeros(2)
    x_accel = np.zeros(2)

    A = plant.A()
    B = plant.B()

    # Verify voltage exceeds acceleration limits before limiting
    accels_fwd = A @ x_accel + B @ np.array([12.0, 12.0])
    a_fwd = (accels_fwd[0] + accels_fwd[1]) / 2.0
    assert abs(a_fwd) > MAX_A

    accels_rot = A @ x_accel + B @ np.array([-12.0, 12.0])
    alpha = (accels_rot[1] - accels_rot[0]) / TRACKWIDTH
    assert abs(alpha) > MAX_ALPHA

    # Forward
    u = np.array([12.0, 12.0])
    t = 0.0
    while t < 3.0:
        x = plant.calculate_x(x, u, DT)
        voltages = accel_limiter.calculate(x_accel[0], x_accel[1], u[0], u[1])
        x_accel = plant.calculate_x(
            x_accel, np.array([voltages.left, voltages.right]), DT
        )

        accels = A @ x_accel + B @ np.array([voltages.left, voltages.right])
        a = (accels[0] + accels[1]) / 2.0
        alpha_val = (accels[1] - accels[0]) / TRACKWIDTH
        assert abs(a) <= MAX_A + 1e-9
        assert abs(alpha_val) <= MAX_ALPHA + 1e-9
        t += DT

    # Backward
    u = np.array([-12.0, -12.0])
    t = 0.0
    while t < 3.0:
        x = plant.calculate_x(x, u, DT)
        voltages = accel_limiter.calculate(x_accel[0], x_accel[1], u[0], u[1])
        x_accel = plant.calculate_x(
            x_accel, np.array([voltages.left, voltages.right]), DT
        )

        accels = A @ x_accel + B @ np.array([voltages.left, voltages.right])
        a = (accels[0] + accels[1]) / 2.0
        alpha_val = (accels[1] - accels[0]) / TRACKWIDTH
        assert abs(a) <= MAX_A + 1e-9
        assert abs(alpha_val) <= MAX_ALPHA + 1e-9
        t += DT

    # Rotate CCW
    u = np.array([-12.0, 12.0])
    t = 0.0
    while t < 3.0:
        x = plant.calculate_x(x, u, DT)
        voltages = accel_limiter.calculate(x_accel[0], x_accel[1], u[0], u[1])
        x_accel = plant.calculate_x(
            x_accel, np.array([voltages.left, voltages.right]), DT
        )

        accels = A @ x_accel + B @ np.array([voltages.left, voltages.right])
        a = (accels[0] + accels[1]) / 2.0
        alpha_val = (accels[1] - accels[0]) / TRACKWIDTH
        assert abs(a) <= MAX_A + 1e-9
        assert abs(alpha_val) <= MAX_ALPHA + 1e-9
        t += DT


def test_high_limits():
    plant = _make_plant()
    accel_limiter = DifferentialDriveAccelerationLimiter(
        plant, TRACKWIDTH, 1e3, 1e3
    )

    x = np.zeros(2)
    x_accel = np.zeros(2)

    # Forward
    u = np.array([12.0, 12.0])
    t = 0.0
    while t < 3.0:
        x = plant.calculate_x(x, u, DT)
        voltages = accel_limiter.calculate(x_accel[0], x_accel[1], u[0], u[1])
        x_accel = plant.calculate_x(
            x_accel, np.array([voltages.left, voltages.right]), DT
        )
        assert x_accel[0] == pytest.approx(x[0])
        assert x_accel[1] == pytest.approx(x[1])
        t += DT

    # Backward
    x = np.zeros(2)
    x_accel = np.zeros(2)
    u = np.array([-12.0, -12.0])
    t = 0.0
    while t < 3.0:
        x = plant.calculate_x(x, u, DT)
        voltages = accel_limiter.calculate(x_accel[0], x_accel[1], u[0], u[1])
        x_accel = plant.calculate_x(
            x_accel, np.array([voltages.left, voltages.right]), DT
        )
        assert x_accel[0] == pytest.approx(x[0])
        assert x_accel[1] == pytest.approx(x[1])
        t += DT

    # Rotate CCW
    x = np.zeros(2)
    x_accel = np.zeros(2)
    u = np.array([-12.0, 12.0])
    t = 0.0
    while t < 3.0:
        x = plant.calculate_x(x, u, DT)
        voltages = accel_limiter.calculate(x_accel[0], x_accel[1], u[0], u[1])
        x_accel = plant.calculate_x(
            x_accel, np.array([voltages.left, voltages.right]), DT
        )
        assert x_accel[0] == pytest.approx(x[0])
        assert x_accel[1] == pytest.approx(x[1])
        t += DT


def test_separate_min_max_low_limits():
    plant = _make_plant()
    min_a = -1.0
    max_a = 2.0

    accel_limiter = DifferentialDriveAccelerationLimiter(
        plant, TRACKWIDTH, min_a, max_a, MAX_ALPHA
    )

    x = np.zeros(2)
    x_accel = np.zeros(2)

    A = plant.A()
    B = plant.B()

    # Forward
    u = np.array([12.0, 12.0])
    t = 0.0
    while t < 3.0:
        x = plant.calculate_x(x, u, DT)
        voltages = accel_limiter.calculate(x_accel[0], x_accel[1], u[0], u[1])
        x_accel = plant.calculate_x(
            x_accel, np.array([voltages.left, voltages.right]), DT
        )

        accels = A @ x_accel + B @ np.array([voltages.left, voltages.right])
        a = (accels[0] + accels[1]) / 2.0
        assert a >= min_a - 1e-9
        assert a <= max_a + 1e-9
        t += DT

    # Backward
    u = np.array([-12.0, -12.0])
    t = 0.0
    while t < 3.0:
        x = plant.calculate_x(x, u, DT)
        voltages = accel_limiter.calculate(x_accel[0], x_accel[1], u[0], u[1])
        x_accel = plant.calculate_x(
            x_accel, np.array([voltages.left, voltages.right]), DT
        )

        accels = A @ x_accel + B @ np.array([voltages.left, voltages.right])
        a = (accels[0] + accels[1]) / 2.0
        assert a >= min_a - 1e-9
        assert a <= max_a + 1e-9
        t += DT


def test_min_accel_greater_than_max_accel_raises():
    plant = _make_plant()
    with pytest.raises(Exception):
        DifferentialDriveAccelerationLimiter(plant, 1.0, 1.0, -1.0, 1.0)
