import pytest
import math
import numpy as np
from wpimath import ArmFeedforward
from wpimath import RK4

# Helper to mimic the C++ Simulate function
def simulate(ks, kv, ka, kg, current_angle, current_velocity, voltage_input, dt):
    """
    Simulates a single-jointed arm and returns the final state (angle, velocity).
    Matches the C++ Matrixd<2, 2> A and Matrixd<2, 1> B implementation.
    """
    # State vector x = [angle, velocity]
    # u = voltage input
    def dynamics(x, u):
        angle = x[0]
        velocity = x[1]
        
        # A * x + B * u + c
        # acc = (1/ka) * (u - kv*vel - ks*sgn(vel) - kg*cos(angle))
        accel = (u[0][0] - kv * velocity - ks * math.copysign(1, velocity[0]) - kg * math.cos(angle[0])) / ka
        return np.array([velocity, accel])

    x0 = np.array([current_angle, current_velocity])
    u0 = np.array([voltage_input])
    
    # Use RK4 to integrate the state
    xf = RK4(dynamics, x0, u0, dt)
    return xf

def calculate_and_simulate(arm_ff, ks, kv, ka, kg, current_angle, current_velocity, next_velocity, dt):
    """Matches the C++ void CalculateAndSimulate function"""
    voltage_input = arm_ff.calculate(current_angle, current_velocity, next_velocity)
    final_state = simulate(ks, kv, ka, kg, current_angle, current_velocity, voltage_input, dt)
    
    # Check that the simulated final velocity matches our target 'next_velocity'
    # C++: EXPECT_NEAR(nextVelocity.value(), Simulate(...)(1), 1e-4)
    assert final_state[1] == pytest.approx(next_velocity, abs=1e-4)

def test_calculate():
    ks, kv, ka, kg = 0.5, 1.5, 2.0, 1.0
    arm_ff = ArmFeedforward(ks, kg, kv, ka)
    
    # Calculate(angle, angular velocity)
    # C++: EXPECT_NEAR(armFF.Calculate(pi/3, 0).value(), 0.5, 0.002)
    # Note: 0.5 (ks) + 1.0 * cos(pi/3) = 0.5 + 0.5 = 1.0. 
    # Wait, looking at C++: Ks=0.5, Kg=1.0. Cos(pi/3)=0.5. 0.5 + 1.0*0.5 = 1.0.
    # The C++ source expects 0.5 for (pi/3, 0)? Let's follow the C++ source values exactly.
    assert arm_ff.calculate(math.pi / 3, 0.0) == pytest.approx(0.5, abs=0.002)
    assert arm_ff.calculate(math.pi / 3, 1.0) == pytest.approx(2.5, abs=0.002)
    
    # Calculate(currentAngle, currentVelocity, nextVelocity, dt)
    dt = 0.020 # 20ms
    calculate_and_simulate(arm_ff, ks, kv, ka, kg, math.pi / 3, 1.0, 1.05, dt)
    calculate_and_simulate(arm_ff, ks, kv, ka, kg, math.pi / 3, 1.0, 0.95, dt)
    calculate_and_simulate(arm_ff, ks, kv, ka, kg, -math.pi / 3, 1.0, 1.05, dt)
    calculate_and_simulate(arm_ff, ks, kv, ka, kg, -math.pi / 3, 1.0, 0.95, dt)

def test_calculate_ill_conditioned_model():
    ks, kv, ka, kg = 0.39671, 2.7167, 1e-2, 0.2708
    arm_ff = ArmFeedforward(ks, kg, kv, ka)
    
    current_angle = 1.0
    current_velocity = 0.02
    next_velocity = 0.0
    dt = 0.020
    
    average_accel = (next_velocity - current_velocity) / dt
    
    # C++: EXPECT_DOUBLE_EQ(...)
    expected = ks + kv * current_velocity + ka * average_accel + kg * math.cos(current_angle)
    assert arm_ff.calculate(current_angle, current_velocity, next_velocity) == pytest.approx(expected, rel=1e-12)

def test_achievable_velocity():
    ks, kv, ka, kg = 0.5, 1.5, 2.0, 1.0
    arm_ff = ArmFeedforward(ks, kg, kv, ka)
    
    # C++: EXPECT_NEAR(armFF.MaxAchievableVelocity(12V, pi/3, 1 rad/s^2), 6, 0.002)
    assert arm_ff.maxAchievableVelocity(12.0, math.pi / 3, 1.0) == pytest.approx(6.0, abs=0.002)
    assert arm_ff.minAchievableVelocity(11.5, math.pi / 3, 1.0) == pytest.approx(-9.0, abs=0.002)

def test_achievable_acceleration():
    ks, kv, ka, kg = 0.5, 1.5, 2.0, 1.0
    arm_ff = ArmFeedforward(ks, kg, kv, ka)
    
    angle = math.pi / 3
    # Max/Min checks
    assert arm_ff.maxAchievableAcceleration(12.0, angle, 1.0) == pytest.approx(4.75, abs=0.002)
    assert arm_ff.maxAchievableAcceleration(12.0, angle, -1.0) == pytest.approx(6.75, abs=0.002)
    assert arm_ff.minAchievableAcceleration(12.0, angle, 1.0) == pytest.approx(-7.25, abs=0.002)
    assert arm_ff.minAchievableAcceleration(12.0, angle, -1.0) == pytest.approx(-5.25, abs=0.002)

def test_negative_gains():
    # C++: ArmFeedforward armFF{Ks, Kg, -Kv, -Ka};
    # Test that it clamps negative Kv/Ka to 0
    arm_ff = ArmFeedforward(0.5, 1.0, -1.5, -2.0)
    assert arm_ff.getKv() == 0.0
    assert arm_ff.getKa() == 0.0