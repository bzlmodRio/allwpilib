import pytest
import numpy as np
from wpimath import LinearPlantInversionFeedforward_2_1

def test_calculate():
    A = np.eye(2)
    B = np.array([[0], [1]])
    
    ff = LinearPlantInversionFeedforward_2_1(A, B, 0.020)
    
    r = np.array([2.0, 2.0])
    next_r = np.array([3.0, 3.0])
    
    # Calculate returns a vector of inputs
    u = ff.calculate(r, next_r)
    assert u[0] == pytest.approx(47.502599, abs=0.002)