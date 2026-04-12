import pytest
import numpy as np
from wpimath import ImplicitModelFollower_2_2, Models

def test_same_model():
    dt = 0.005
    # Kv=1, Ka=1
    plant = Models.differentialDriveFromSysId(1.0, 1.0, 1.0, 1.0)
    imf = ImplicitModelFollower_2_2(plant, plant)
    
    x = np.zeros(2)
    x_imf = np.zeros(2)
    
    # Test cases: Forward, Backward, Rotate CCW
    vectors = [np.array([12.0, 12.0]), np.array([-12.0, -12.0]), np.array([-12.0, 12.0])]
    
    for u in vectors:
        x.fill(0)
        x_imf.fill(0)
        for _ in range(int(3.0 / dt)):
            x = plant.calculateX(x, u, dt)
            u_imf = imf.calculate(x_imf, u)
            x_imf = plant.calculateX(x_imf, u_imf, dt)
            
            assert x[0] == pytest.approx(x_imf[0])
            assert x[1] == pytest.approx(x_imf[1])

def test_slower_ref_model():
    dt = 0.005
    plant = Models.differentialDriveFromSysId(1.0, 1.0, 1.0, 1.0)
    # Ref model has Ka=2 (slower acceleration)
    plant_ref = Models.differentialDriveFromSysId(1.0, 2.0, 1.0, 1.0)
    
    imf = ImplicitModelFollower_2_2(plant, plant_ref)
    
    # Forward: Plant should be faster than IMF
    x, x_imf = np.zeros(2), np.zeros(2)
    u = np.array([12.0, 12.0])
    for _ in range(int(3.0 / dt)):
        x = plant.calculateX(x, u, dt)
        x_imf = plant.calculateX(x_imf, imf.calculate(x_imf, u), dt)
        assert x[0] >= x_imf[0]
        assert x[1] >= x_imf[1]

    # Backward
    x, x_imf = np.zeros(2), np.zeros(2)
    u = np.array([-12.0, -12.0])
    for _ in range(int(3.0 / dt)):
        x = plant.calculateX(x, u, dt)
        x_imf = plant.calculateX(x_imf, imf.calculate(x_imf, u), dt)
        assert x[0] <= x_imf[0]
        assert x[1] <= x_imf[1]

    # Rotate: Angular Ka is same, so they should be nearly equal
    x, x_imf = np.zeros(2), np.zeros(2)
    u = np.array([-12.0, 12.0])
    for _ in range(int(3.0 / dt)):
        x = plant.calculateX(x, u, dt)
        x_imf = plant.calculateX(x_imf, imf.calculate(x_imf, u), dt)
        assert x[0] == pytest.approx(x_imf[0], abs=1e-5)
        assert x[1] == pytest.approx(x_imf[1], abs=1e-5)