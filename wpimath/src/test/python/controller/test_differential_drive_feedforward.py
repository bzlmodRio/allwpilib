import numpy as np
import pytest

from wpimath import DifferentialDriveFeedforward, Models

K_V_LINEAR = 1.0
K_A_LINEAR = 1.0
K_V_ANGULAR_RAD = 1.0
K_A_ANGULAR_RAD = 1.0
K_V_ANGULAR_MPS = 1.0
K_A_ANGULAR_MPS = 1.0
TRACKWIDTH = 1.0
DT = 0.020


def test_calculate_with_trackwidth():
    ff = DifferentialDriveFeedforward(
        K_V_LINEAR, K_A_LINEAR, K_V_ANGULAR_RAD, K_A_ANGULAR_RAD, TRACKWIDTH
    )
    plant = Models.differentialDriveFromSysId(
        K_V_LINEAR, K_A_LINEAR, K_V_ANGULAR_RAD, K_A_ANGULAR_RAD, TRACKWIDTH
    )

    for current_left in range(-4, 5, 2):
        for current_right in range(-4, 5, 2):
            for next_left in range(-4, 5, 2):
                for next_right in range(-4, 5, 2):
                    voltages = ff.calculate(
                        float(current_left),
                        float(next_left),
                        float(current_right),
                        float(next_right),
                        DT,
                    )
                    next_x = plant.calculateX(
                        np.array([[float(current_left)], [float(current_right)]]),
                        np.array([[voltages.left], [voltages.right]]),
                        DT,
                    )
                    assert next_x[0] == pytest.approx(float(next_left), abs=1e-6)
                    assert next_x[1] == pytest.approx(float(next_right), abs=1e-6)


def test_calculate_without_trackwidth():
    ff = DifferentialDriveFeedforward(
        K_V_LINEAR, K_A_LINEAR, K_V_ANGULAR_MPS, K_A_ANGULAR_MPS
    )
    plant = Models.differentialDriveFromSysId(
        K_V_LINEAR, K_A_LINEAR, K_V_ANGULAR_MPS, K_A_ANGULAR_MPS
    )

    for current_left in range(-4, 5, 2):
        for current_right in range(-4, 5, 2):
            for next_left in range(-4, 5, 2):
                for next_right in range(-4, 5, 2):
                    voltages = ff.calculate(
                        float(current_left),
                        float(next_left),
                        float(current_right),
                        float(next_right),
                        DT,
                    )
                    next_x = plant.calculateX(
                        np.array([[float(current_left)], [float(current_right)]]),
                        np.array([[voltages.left], [voltages.right]]),
                        DT,
                    )
                    assert next_x[0] == pytest.approx(float(next_left), abs=1e-6)
                    assert next_x[1] == pytest.approx(float(next_right), abs=1e-6)
