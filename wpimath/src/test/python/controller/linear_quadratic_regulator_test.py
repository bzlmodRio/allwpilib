import pytest
import numpy as np
from wpimath import LinearQuadraticRegulator_2_1, LinearQuadraticRegulator_2_2, DCMotor, Models
from wpimath.units import inchesToMeters

def test_elevator_gains():
    motors = DCMotor.vex775Pro(2)
    m, r, g = 5.0, 0.0181864, 1.0
    
    # Slice(0) in C++ takes the first output. 
    # RobotPy handles the system generation via LinearSystemId
    plant = Models.elevatorFromPhysicalConstants(motors, m, r, g)
    
    # qelms = [0.02, 0.4], relms = [12.0], dt = 0.005
    lqr = LinearQuadraticRegulator_2_1(plant, [0.02, 0.4], [12.0], 0.005)
    k = lqr.K()
    
    assert k[0] == pytest.approx(522.870067, abs=1e-6)
    assert k[1] == pytest.approx(38.239878, abs=1e-6)

def test_matrix_overloads():
    a = np.zeros((2, 2))
    b = np.eye(2)
    q = np.eye(2)
    r = np.eye(2)
    
    lqr = LinearQuadraticRegulator_2_2(a, b, q, r, 0.005)
    k = lqr.K()
    assert k[0, 0] == pytest.approx(0.997503, abs=1e-6)
    assert k[1, 1] == pytest.approx(0.997503, abs=1e-6)

# This didn't convert everything