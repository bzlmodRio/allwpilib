import pytest
import numpy as np
from wpimath import ControlAffinePlantInversionFeedforward_2_1

def dynamics(x, u):
    return x + np.array([0.0, u[0]])

def state_dynamics(x):
    return x

def test_calculate():
    ff = ControlAffinePlantInversionFeedforward_2_1(dynamics, 0.020)
    r = np.array([2.0, 2.0])
    next_r = np.array([3.0, 3.0])
    
    assert ff.calculate(r, next_r)[0] == pytest.approx(48, abs=1e-6)

def test_calculate_state():
    B = np.array([[0.0], [1.0]])
    ff = ControlAffinePlantInversionFeedforward_2_1(state_dynamics, B, 0.020)
    r = np.array([2.0, 2.0])
    next_r = np.array([3.0, 3.0])
    
    assert ff.calculate(r, next_r)[0] == pytest.approx(48, abs=1e-6)