import numpy as np
import pytest

from wpimath import (
    DCMotor,
    LinearQuadraticRegulator_2_1,
    LinearQuadraticRegulator_2_2,
    Models,
)


def _elevator_plant():
    motors = DCMotor.vex775_pro(2)
    m = 5.0  # kg
    r = 0.0181864  # m
    G = 40.0 / 40.0
    return Models.elevator_from_physical_constants(motors, m, r, G).slice(0)


def _arm_plant():
    motors = DCMotor.vex775_pro(2)
    m = 4.0  # kg
    r = 0.4  # m
    G = 100.0
    J = 1.0 / 3.0 * m * r * r
    return Models.single_jointed_arm_from_physical_constants(motors, J, G).slice(0)


def _four_motor_elevator_plant():
    motors = DCMotor.vex775_pro(4)
    m = 8.0  # kg
    r = 0.75 * 0.0254  # 0.75 inches in meters
    G = 14.67
    return Models.elevator_from_physical_constants(motors, m, r, G).slice(0)


def test_elevator_gains():
    plant = _elevator_plant()
    controller = LinearQuadraticRegulator_2_1(plant, [0.02, 0.4], [12.0], 0.005)
    K = controller.K()

    assert K[0] == pytest.approx(522.87006795347486, abs=1e-6)
    assert K[1] == pytest.approx(38.239878385020411, abs=1e-6)


def test_arm_gains():
    plant = _arm_plant()
    controller = LinearQuadraticRegulator_2_1(
        plant, [0.01745, 0.08726], [12.0], 0.005
    )
    K = controller.K()

    assert K[0] == pytest.approx(19.339349883583761, abs=1e-6)
    assert K[1] == pytest.approx(3.3542559517421582, abs=1e-6)


def test_four_motor_elevator():
    plant = _four_motor_elevator_plant()
    controller = LinearQuadraticRegulator_2_1(plant, [0.1, 0.2], [12.0], 0.020)
    K = controller.K()

    assert K[0] == pytest.approx(10.38, abs=0.1)
    assert K[1] == pytest.approx(0.69, abs=0.1)


def test_matrix_overloads_single_integrator():
    A = np.zeros((2, 2))
    B = np.eye(2)
    Q = np.eye(2)
    R = np.eye(2)

    controller = LinearQuadraticRegulator_2_2(A, B, Q, R, 0.005)
    K = controller.K()

    assert K[0, 0] == pytest.approx(0.99750312499512261, abs=1e-10)
    assert K[0, 1] == pytest.approx(0.0, abs=1e-10)
    assert K[1, 0] == pytest.approx(0.0, abs=1e-10)
    assert K[1, 1] == pytest.approx(0.99750312499512261, abs=1e-10)


def test_matrix_overloads_double_integrator():
    Kv = 3.02
    Ka = 0.642
    A = np.array([[0, 1], [0, -Kv / Ka]])
    B = np.array([[0], [1.0 / Ka]])
    Q = np.array([[1, 0], [0, 0.2]])
    R = np.array([[0.25]])

    controller = LinearQuadraticRegulator_2_1(A, B, Q, R, 0.005)
    K = controller.K()

    assert K[0] == pytest.approx(1.9960017786537287, abs=1e-10)
    assert K[1] == pytest.approx(0.51182128351092726, abs=1e-10)


def test_latency_compensate():
    plant = _four_motor_elevator_plant()
    controller = LinearQuadraticRegulator_2_1(plant, [0.1, 0.2], [12.0], 0.020)
    controller.latency_compensate(plant, 0.020, 0.010)

    K = controller.K()
    assert K[0] == pytest.approx(8.97115941, abs=1e-3)
    assert K[1] == pytest.approx(0.07904881, abs=1e-3)
