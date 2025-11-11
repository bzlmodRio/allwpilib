import pytest
import math

from wpimath.controller import SimpleMotorFeedforwardMeters
from wpimath.trajectory import ExponentialProfileMeterVolts
from wpimath.units import (
    meters,
    meters_per_second,
    meters_per_second_squared,
    volts,
    seconds,
)

kT = 10 * 0.001  # 10_ms
kV = 2.5629 * 1  # 2.5629_V / 1_mps
kA = 0.43277 * 1  # 0.43277_V / 1_mps_sq


def check_dynamics(profile, constraints, feedforward, current, goal):
    next_state = profile.calculate(kT, current, goal)
    signal = feedforward.calculate(current.velocity, next_state.velocity)

    assert abs(signal) <= constraints.maxInput + 1e-9

    return next_state


def test_reaches_goal():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(volts(12), -kV / kA, 1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(volts(0), kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(meters(10), meters_per_second(0))
    state = ExponentialProfileMeterVolts.State(meters(0), meters_per_second(0))

    for _ in range(450):
        state = check_dynamics(profile, constraints, feedforward, state, goal)

    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)


def test_pos_continuous_under_vel_change():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(volts(12), -kV / kA, 1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(volts(0), kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(meters(10), meters_per_second(0))
    state = ExponentialProfileMeterVolts.State(meters(0), meters_per_second(0))

    for i in range(300):
        if i == 150:
            constraints.maxInput = volts(9)
            profile = ExponentialProfileMeterVolts(constraints)
        state = check_dynamics(profile, constraints, feedforward, state, goal)

    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)


def test_pos_continuous_under_vel_change_backward():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(volts(12), -kV / kA, 1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(volts(0), kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(meters(-10), meters_per_second(0))
    state = ExponentialProfileMeterVolts.State(meters(0), meters_per_second(0))

    for i in range(300):
        if i == 150:
            constraints.maxInput = volts(9)
            profile = ExponentialProfileMeterVolts(constraints)
        state = check_dynamics(profile, constraints, feedforward, state, goal)

    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)


def test_backwards():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(volts(12), -kV / kA, 1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(volts(0), kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(meters(-10), meters_per_second(0))
    state = ExponentialProfileMeterVolts.State(meters(0), meters_per_second(0))

    for _ in range(400):
        state = check_dynamics(profile, constraints, feedforward, state, goal)

    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)


def test_switch_goal_in_middle():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(volts(12), -kV / kA, 1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(volts(0), kV, kA, kT)
    goal1 = ExponentialProfileMeterVolts.State(meters(-10), meters_per_second(0))
    state = ExponentialProfileMeterVolts.State(meters(0), meters_per_second(0))

    for _ in range(50):
        state = check_dynamics(profile, constraints, feedforward, state, goal1)
    
    assert state.position != goal1.position

    goal2 = ExponentialProfileMeterVolts.State(meters(0), meters_per_second(0))
    for _ in range(100):
        state = check_dynamics(profile, constraints, feedforward, state, goal2)

    assert state.position == pytest.approx(goal2.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal2.velocity, abs=1e-3)


def test_top_speed():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(volts(12), -kV / kA, 1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(volts(0), kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(meters(40), meters_per_second(0))
    state = ExponentialProfileMeterVolts.State(meters(0), meters_per_second(0))

    max_speed = meters_per_second(0)

    for _ in range(900):
        state = check_dynamics(profile, constraints, feedforward, state, goal)
        max_speed = max(state.velocity, max_speed)

    assert constraints.maxVelocity() == pytest.approx(max_speed, abs=1e-5)
    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)


def test_top_speed_backward():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(volts(12), -kV / kA, 1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(volts(0), kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(meters(-40), meters_per_second(0))
    state = ExponentialProfileMeterVolts.State(meters(0), meters_per_second(0))

    max_speed = meters_per_second(0)

    for _ in range(900):
        state = check_dynamics(profile, constraints, feedforward, state, goal)
        max_speed = min(state.velocity, max_speed)

    assert -constraints.maxVelocity() == pytest.approx(max_speed, abs=1e-5)
    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)


def test_high_initial_speed():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(volts(12), -kV / kA, 1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(volts(0), kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(meters(40), meters_per_second(0))
    state = ExponentialProfileMeterVolts.State(meters(0), meters_per_second(8))

    for _ in range(900):
        state = check_dynamics(profile, constraints, feedforward, state, goal)

    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)


def test_high_initial_speed_backward():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(volts(12), -kV / kA, 1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(volts(0), kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(meters(-40), meters_per_second(0))
    state = ExponentialProfileMeterVolts.State(meters(0), meters_per_second(-8))

    for _ in range(900):
        state = check_dynamics(profile, constraints, feedforward, state, goal)

    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)


def test_test_heuristic():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(volts(12), -kV / kA, 1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)

    test_cases = [
        (ExponentialProfileMeterVolts.State(meters(0), meters_per_second(-4)), ExponentialProfileMeterVolts.State(meters(0.75), meters_per_second(-4)), ExponentialProfileMeterVolts.State(meters(1.3758), meters_per_second(4.4304))),
        (ExponentialProfileMeterVolts.State(meters(0), meters_per_second(-4)), ExponentialProfileMeterVolts.State(meters(1.4103), meters_per_second(4)), ExponentialProfileMeterVolts.State(meters(1.3758), meters_per_second(4.4304))),
        (ExponentialProfileMeterVolts.State(meters(0.6603), meters_per_second(4)), ExponentialProfileMeterVolts.State(meters(0.75), meters_per_second(-4)), ExponentialProfileMeterVolts.State(meters(1.3758), meters_per_second(4.4304))),
        (ExponentialProfileMeterVolts.State(meters(0.6603), meters_per_second(4)), ExponentialProfileMeterVolts.State(meters(1.4103), meters_per_second(4)), ExponentialProfileMeterVolts.State(meters(1.3758), meters_per_second(4.4304))),
        (ExponentialProfileMeterVolts.State(meters(0), meters_per_second(-4)), ExponentialProfileMeterVolts.State(meters(0.5), meters_per_second(-2)), ExponentialProfileMeterVolts.State(meters(0.4367), meters_per_second(3.7217))),
        (ExponentialProfileMeterVolts.State(meters(0), meters_per_second(-4)), ExponentialProfileMeterVolts.State(meters(0.546), meters_per_second(2)), ExponentialProfileMeterVolts.State(meters(0.4367), meters_per_second(3.7217))),
        (ExponentialProfileMeterVolts.State(meters(0.6603), meters_per_second(4)), ExponentialProfileMeterVolts.State(meters(0.5), meters_per_second(-2)), ExponentialProfileMeterVolts.State(meters(0.5560), meters_per_second(-2.9616))),
        (ExponentialProfileMeterVolts.State(meters(0.6603), meters_per_second(4)), ExponentialProfileMeterVolts.State(meters(0.546), meters_per_second(2)), ExponentialProfileMeterVolts.State(meters(0.5560), meters_per_second(-2.9616))),
        (ExponentialProfileMeterVolts.State(meters(0), meters_per_second(-4)), ExponentialProfileMeterVolts.State(meters(-0.75), meters_per_second(-4)), ExponentialProfileMeterVolts.State(meters(-0.7156), meters_per_second(-4.4304))),
        (ExponentialProfileMeterVolts.State(meters(0), meters_per_second(-4)), ExponentialProfileMeterVolts.State(meters(-0.0897), meters_per_second(4)), ExponentialProfileMeterVolts.State(meters(-0.7156), meters_per_second(-4.4304))),
        (ExponentialProfileMeterVolts.State(meters(0.6603), meters_per_second(4)), ExponentialProfileMeterVolts.State(meters(-0.75), meters_per_second(-4)), ExponentialProfileMeterVolts.State(meters(-0.7156), meters_per_second(-4.4304))),
        (ExponentialProfileMeterVolts.State(meters(0.6603), meters_per_second(4)), ExponentialProfileMeterVolts.State(meters(-0.0897), meters_per_second(4)), ExponentialProfileMeterVolts.State(meters(-0.7156), meters_per_second(-4.4304))),
        (ExponentialProfileMeterVolts.State(meters(0), meters_per_second(-4)), ExponentialProfileMeterVolts.State(meters(-0.5), meters_per_second(-4.5)), ExponentialProfileMeterVolts.State(meters(1.095), meters_per_second(4.314))),
        (ExponentialProfileMeterVolts.State(meters(0), meters_per_second(-4)), ExponentialProfileMeterVolts.State(meters(1.0795), meters_per_second(4.5)), ExponentialProfileMeterVolts.State(meters(-0.5122), meters_per_second(-4.351))),
        (ExponentialProfileMeterVolts.State(meters(0.6603), meters_per_second(4)), ExponentialProfileMeterVolts.State(meters(-0.5), meters_per_second(-4.5)), ExponentialProfileMeterVolts.State(meters(1.095), meters_per_second(4.314))),
        (ExponentialProfileMeterVolts.State(meters(0.6603), meters_per_second(4)), ExponentialProfileMeterVolts.State(meters(1.0795), meters_per_second(4.5)), ExponentialProfileMeterVolts.State(meters(-0.5122), meters_per_second(-4.351))),
        (ExponentialProfileMeterVolts.State(meters(0), meters_per_second(-8)), ExponentialProfileMeterVolts.State(meters(0), meters_per_second(0)), ExponentialProfileMeterVolts.State(meters(-0.1384), meters_per_second(3.342))),
        (ExponentialProfileMeterVolts.State(meters(0), meters_per_second(-8)), ExponentialProfileMeterVolts.State(meters(-1), meters_per_second(0)), ExponentialProfileMeterVolts.State(meters(-0.562), meters_per_second(-6.792))),
        (ExponentialProfileMeterVolts.State(meters(0), meters_per_second(8)), ExponentialProfileMeterVolts.State(meters(1), meters_per_second(0)), ExponentialProfileMeterVolts.State(meters(0.562), meters_per_second(6.792))),
        (ExponentialProfileMeterVolts.State(meters(0), meters_per_second(8)), ExponentialProfileMeterVolts.State(meters(-1), meters_per_second(0)), ExponentialProfileMeterVolts.State(meters(-0.785), meters_per_second(-4.346))),
    ]
    
    for initial, goal, expected_inflection in test_cases:
        inflection = profile.calculateInflectionPoint(initial, goal)
        assert inflection.position == pytest.approx(expected_inflection.position, abs=1e-3)
        assert inflection.velocity == pytest.approx(expected_inflection.velocity, abs=1e-3)


def test_timing_to_current():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(volts(12), -kV / kA, 1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(volts(0), kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(meters(2), meters_per_second(0))
    state = ExponentialProfileMeterVolts.State(meters(0), meters_per_second(0))

    for _ in range(900):
        state = check_dynamics(profile, constraints, feedforward, state, goal)
        time_left = profile.timeLeftUntil(state, state)
        assert time_left == pytest.approx(seconds(0), abs=0.02)
    
    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)


def test_timing_to_goal():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(volts(12), -kV / kA, 1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(volts(0), kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(meters(2), meters_per_second(0))
    state = ExponentialProfileMeterVolts.State(meters(0), meters_per_second(0))

    prediction = profile.timeLeftUntil(state, goal)
    reached_goal = False

    for i in range(900):
        state = check_dynamics(profile, constraints, feedforward, state, goal)
        if not reached_goal and state.position == pytest.approx(goal.position, abs=1e-3) and state.velocity == pytest.approx(goal.velocity, abs=1e-3):
            assert prediction == pytest.approx((i * seconds(0.01)), abs=0.25)
            reached_goal = True
            
    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)


def test_timing_to_negative_goal():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(volts(12), -kV / kA, 1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(volts(0), kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(meters(-2), meters_per_second(0))
    state = ExponentialProfileMeterVolts.State(meters(0), meters_per_second(0))

    prediction = profile.timeLeftUntil(state, goal)
    reached_goal = False

    for i in range(900):
        state = check_dynamics(profile, constraints, feedforward, state, goal)
        if not reached_goal and state.position == pytest.approx(goal.position, abs=1e-3) and state.velocity == pytest.approx(goal.velocity, abs=1e-3):
            assert prediction == pytest.approx((i * seconds(0.01)), abs=0.25)
            reached_goal = True
            
    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)