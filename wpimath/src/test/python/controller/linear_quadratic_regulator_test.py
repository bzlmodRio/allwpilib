import pytest
import numpy as np
from wpimath import LinearQuadraticRegulator_2_1, LinearQuadraticRegulator_2_2, DCMotor, Models


def test_elevator_gains():
    # Setup plant
    motors = DCMotor.vex775Pro(2)
    m = 5.0 # kg
    r = 0.0181864 # meters
    G = 1.0 # Gear ratio
    
    plant = Models.elevatorFromPhysicalConstants(motors, m, r, G).slice(0)
    
    # LQR with state costs [0.02, 0.4], effort cost [12.0], dt 5ms
    lqr = LinearQuadraticRegulator_2_1(plant, [0.02, 0.4], [12.0], 0.005)
    k = lqr.K()
    
    assert k[0] == pytest.approx(522.87006795347486, abs=1e-6)
    assert k[1] == pytest.approx(38.239878385020411, abs=1e-6)

def test_arm_gains():
    motors = DCMotor.vex775Pro(2)
    m = 4.0 # kg
    r = 0.4 # meters
    G = 100.0
    
    # J = 1/3 * m * r^2
    j = 1.0 / 3.0 * m * r * r
    plant = Models.singleJointedArmFromPhysicalConstants(motors, j, G).slice(0)
    
    # State costs: 1 deg (0.01745 rad), 5 deg/s (0.08726 rad/s)
    lqr = LinearQuadraticRegulator_2_1(plant, [0.01745, 0.08726], [12.0], 0.005)
    k = lqr.K()
    
    assert k[0] == pytest.approx(19.339349883583761, abs=1e-6)
    assert k[1] == pytest.approx(3.3542559517421582, abs=1e-6)

def test_four_motor_elevator():
    motors = DCMotor.vex775Pro(4)
    m = 8.0 # kg
    r = 0.01905 # 0.75 inches
    G = 14.67
    
    plant = Models.elevatorFromPhysicalConstants(motors, m, r, G).slice(0)
    lqr = LinearQuadraticRegulator_2_1(plant, [0.1, 0.2], [12.0], 0.020)
    k = lqr.K()
    
    assert k[0] == pytest.approx(10.38, abs=1e-1)
    assert k[1] == pytest.approx(0.69, abs=1e-1)

def test_matrix_overloads_single_integrator():
    A = np.zeros((2, 2))
    B = np.eye(2)
    Q = np.eye(2)
    R = np.eye(2)
    
    # QR overload
    lqr_qr = LinearQuadraticRegulator_2_2(A, B, Q, R, 0.005)
    k_qr = lqr_qr.K()
    assert k_qr[0, 0] == pytest.approx(0.99750312499512261, abs=1e-10)
    assert k_qr[0, 1] == pytest.approx(0.0, abs=1e-10)
    assert k_qr[1, 0] == pytest.approx(0.0, abs=1e-10)
    assert k_qr[1, 1] == pytest.approx(0.99750312499512261, abs=1e-10)

    # QRN overload
    N = np.eye(2)
    lqr_qrn = LinearQuadraticRegulator_2_2(A, B, Q, R, N, 0.005)
    k_qrn = lqr_qrn.K()
    assert k_qrn[0, 0] == pytest.approx(1.0, abs=1e-10)
    assert k_qrn[1, 1] == pytest.approx(1.0, abs=1e-10)

def test_latency_compensate():
    motors = DCMotor.vex775Pro(4)
    m, r, g = 8.0, 0.01905, 14.67
    plant = Models.elevatorFromPhysicalConstants(motors, m, r, g).slice(0)
    
    controller = LinearQuadraticRegulator_2_1(plant, [0.1, 0.2], [12.0], 0.020)
    controller.latencyCompensate(plant, 0.020, 0.010)
    
    k = controller.K()
    assert k[0] == pytest.approx(8.97115941, abs=1e-3)
    assert k[1] == pytest.approx(0.07904881, abs=1e-3)