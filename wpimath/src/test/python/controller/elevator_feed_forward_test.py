import pytest
import numpy as np
from wpimath import ElevatorFeedforward, LinearPlantInversionFeedforward_1_1

# Constants from C++
KS, KV, KA, KG = 0.5, 1.5, 2.0, 1.0

def test_elevator_calculate():
    eff = ElevatorFeedforward(KS, KG, KV, KA)
    
    # C++: EXPECT_NEAR(elevatorFF.Calculate(0).value(), Kg.value(), 0.002)
    assert eff.calculate(0.0) == pytest.approx(KG, abs=0.002)
    assert eff.calculate(2.0) == pytest.approx(4.5, abs=0.002)

    # Comparison with LinearPlantInversion
    a = np.array([[-KV / KA]])
    b = np.array([[1.0 / KA]])
    dt = 0.020
    plant_inversion = LinearPlantInversionFeedforward_1_1(a, b, dt)
    
    r = np.array([2.0])
    next_r = np.array([3.0])
    # C++ logic: plantInversion.Calculate + Ks + Kg
    expected = plant_inversion.calculate(r, next_r)[0] + KS + KG
    assert eff.calculate(2.0, 3.0) == pytest.approx(expected, abs=0.002)

def test_elevator_achievable_velocity():
    eff = ElevatorFeedforward(KS, KG, KV, KA)
    assert eff.maxAchievableVelocity(11.0, 1.0) == pytest.approx(5.0, abs=0.002)
    assert eff.minAchievableVelocity(11.0, 1.0) == pytest.approx(-9.0, abs=0.002)

def test_elevator_negative_gains():
    eff = ElevatorFeedforward(KS, KG, -KV, -KA)
    assert eff.getKv() == 0.0
    assert eff.getKa() == 0.0