import pytest
import numpy as np
from wpimath import DifferentialDriveFeedforward, Models

def test_calculate_with_trackwidth():
    kv_lin, ka_lin = 1.0, 1.0
    kv_ang, ka_ang = 1.0, 1.0
    trackwidth = 1.0
    dt = 0.020
    
    ff = DifferentialDriveFeedforward(kv_lin, ka_lin, kv_ang, ka_ang, trackwidth)
    plant = Models.differentialDriveFromSysId(kv_lin, ka_lin, kv_ang, ka_ang, trackwidth)
    
    # Nested loops covering -4 to 4 m/s in 2 m/s steps
    velocities = range(-4, 5, 2)
    for v_l in velocities:
        for v_r in velocities:
            for next_v_l in velocities:
                for next_v_r in velocities:
                    voltages = ff.calculate(v_l, next_v_l, v_r, next_v_r, dt)
                    u_l = voltages.left
                    u_r = voltages.right
                    next_x = plant.calculateX([v_l, v_r], [u_l, u_r], dt)
                    assert next_x[0] == pytest.approx(next_v_l, abs=1e-6)
                    assert next_x[1] == pytest.approx(next_v_r, abs=1e-6)

def test_calculate_without_trackwidth():
    kv_lin, ka_lin = 1.0, 1.0
    kv_ang, ka_ang = 1.0, 1.0
    dt = 0.020
    
    ff = DifferentialDriveFeedforward(kv_lin, ka_lin, kv_ang, ka_ang)
    plant = Models.differentialDriveFromSysId(kv_lin, ka_lin, kv_ang, ka_ang)
    
    velocities = range(-4, 5, 2)
    for v_l in velocities:
        for v_r in velocities:
            for next_v_l in velocities:
                for next_v_r in velocities:
                    voltages = ff.calculate(v_l, next_v_l, v_r, next_v_r, dt)
                    u_l = voltages.left
                    u_r = voltages.right
                    next_x = plant.calculateX([v_l, v_r], [u_l, u_r], dt)
                    assert next_x[0] == pytest.approx(next_v_l, abs=1e-6)
                    assert next_x[1] == pytest.approx(next_v_r, abs=1e-6)