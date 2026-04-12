import pytest
import numpy as np
from wpimath import DifferentialDriveAccelerationLimiter, Models

def test_low_limits():
    trackwidth = 0.9
    dt = 0.005
    max_a, max_alpha = 2.0, 2.0
    
    plant = Models.differentialDriveFromSysId(1.0, 1.0, 1.0, 1.0)
    limiter = DifferentialDriveAccelerationLimiter(plant, trackwidth, max_a, max_alpha)
    
    # Helper to check limits
    def check_limit(u_in, x_start):
        x_sim = x_start.copy()
        for _ in range(int(3.0 / dt)):
            voltages = limiter.calculate(x_sim[0], x_sim[1], u_in[0], u_in[1])
            u_l, u_r = voltages.left, voltages.right
            x_sim = plant.calculateX(x_sim, [u_l, u_r], dt)
            
            accels = plant.A() @ x_sim + plant.B() @ np.array([u_l, u_r])
            a = (accels[0] + accels[1]) / 2.0
            alpha = (accels[1] - accels[0]) / trackwidth
            assert abs(a) <= max_a + 1e-7
            assert abs(alpha) <= max_alpha + 1e-7

    check_limit([12.0, 12.0], np.zeros(2))  # Forward
    check_limit([-12.0, -12.0], np.zeros(2)) # Backward
    check_limit([-12.0, 12.0], np.zeros(2))  # Rotate

def test_high_limits():
    plant = Models.differentialDriveFromSysId(1.0, 1.0, 1.0, 1.0)
    limiter = DifferentialDriveAccelerationLimiter(plant, 0.9, 1e3, 1e3)
    
    # Should match unconstrained plant
    x, x_lim = np.zeros(2), np.zeros(2)
    u = np.array([12.0, 12.0])
    for _ in range(int(3.0 / 0.005)):
        x = plant.calculateX(x, u, 0.005)
        voltages = limiter.calculate(x_lim[0], x_lim[1], u[0], u[1])
        ul, ur = voltages.left, voltages.right
        x_lim = plant.calculateX(x_lim, [ul, ur], 0.005)
        assert x[0] == pytest.approx(x_lim[0])
        assert x[1] == pytest.approx(x_lim[1])

def test_separate_min_max():
    min_a, max_a = -1.0, 2.0
    plant = Models.differentialDriveFromSysId(1.0, 1.0, 1.0, 1.0)
    limiter = DifferentialDriveAccelerationLimiter(plant, 0.9, min_a, max_a, 2.0)
    
    x = np.zeros(2)
    u = np.array([12.0, 12.0])
    for _ in range(int(3.0 / 0.005)):
        voltages = limiter.calculate(x[0], x[1], u[0], u[1])
        ul, ur = voltages.left, voltages.right
        x = plant.calculateX(x, [ul, ur], 0.005)
        accels = plant.A() @ x + plant.B() @ np.array([ul, ur])
        a = (accels[0] + accels[1]) / 2.0
        assert a >= min_a - 1e-7
        assert a <= max_a + 1e-7