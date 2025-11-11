import pytest
import math
import numpy as np

from wpimath.controller import LinearQuadraticRegulator_2_1, LinearQuadraticRegulator_2_2
from wpimath.system import LinearSystem_2_1_1
from wpimath.system.plant import DCMotor, LinearSystemId
from wpimath.units import (
    meters,
    volts,
    kilograms,
    seconds,
    inches,
    inchesToMeters,
    radians,
    radians_per_second,
    radians_per_second_squared,
)


def test_elevator_gains():
    motors = DCMotor.vex775Pro(2)
    m = kilograms(5)
    r = meters(0.0181864)
    G = 40.0 / 40.0

    plant = LinearSystemId.elevatorSystem(motors, m, r, G)

    K = LinearQuadraticRegulator_2_1(
        plant, np.array([0.02, 0.4]), np.array([12.0]), seconds(0.00505)
    ).K()

    assert K[0] == pytest.approx(522.15314269, abs=1e-6)
    assert K[1] == pytest.approx(38.20138596, abs=1e-6)


def test_arm_gains():
    motors = DCMotor.vex775Pro(2)
    m = kilograms(4)
    r = meters(0.4)
    G = 100.0

    J = 1.0 / 3.0 * m * r * r
    plant = LinearSystemId.singleJointedArmSystem(motors, J, G)

    K = LinearQuadraticRegulator_2_1(
        plant, np.array([0.01745, 0.08726]), np.array([12.0]), seconds(0.00505)
    ).K()

    assert K[0] == pytest.approx(19.16, abs=1e-1)
    assert K[1] == pytest.approx(3.32, abs=1e-1)


def test_four_motor_elevator():
    motors = DCMotor.vex775Pro(4)
    m = kilograms(8)
    r = inchesToMeters(0.75)
    G = 14.67

    plant = LinearSystemId.elevatorSystem(motors, m, r, G)

    K = LinearQuadraticRegulator_2_1(
        plant, np.array([0.1, 0.2]), np.array([12.0]), seconds(0.02)
    ).K()

    print("Hello...")
    print(K)

    assert K[0] == pytest.approx(10.38, abs=1e-1)
    assert K[1] == pytest.approx(0.69, abs=1e-1)


def test_matrix_overloads_with_single_integrator():
    A = np.zeros((2, 2))
    B = np.identity(2)
    Q = np.identity(2)
    R = np.identity(2)

    # QR overload
    K = LinearQuadraticRegulator_2_2(A, B, Q, R, seconds(0.005)).K()
    assert K[0, 0] == pytest.approx(0.99750312499512261, abs=1e-10)
    assert K[0, 1] == pytest.approx(0.0, abs=1e-10)
    assert K[1, 0] == pytest.approx(0.0, abs=1e-10)
    assert K[1, 1] == pytest.approx(0.99750312499512261, abs=1e-10)

    # QRN overload
    N = np.identity(2)
    K_imf = LinearQuadraticRegulator_2_2(A, B, Q, R, N, seconds(0.005)).K()
    assert K_imf[0, 0] == pytest.approx(1.0, abs=1e-10)
    assert K_imf[0, 1] == pytest.approx(0.0, abs=1e-10)
    assert K_imf[1, 0] == pytest.approx(0.0, abs=1e-10)
    assert K_imf[1, 1] == pytest.approx(1.0, abs=1e-10)


def test_latency_compensate():
    motors = DCMotor.vex775Pro(4)
    m = kilograms(8)
    r = inchesToMeters(0.75)
    G = 14.67

    plant = LinearSystemId.elevatorSystem(motors, m, r, G)

    controller = LinearQuadraticRegulator_2_1(
        plant, np.array([0.1, 0.2]), np.array([12.0]), seconds(0.02)
    )

    controller.latencyCompensate(plant, seconds(0.02), seconds(0.01))

    assert controller.K()[0] == pytest.approx(8.97115941, abs=1e-3)
    assert controller.K()[1] == pytest.approx(0.07904881, abs=1e-3)