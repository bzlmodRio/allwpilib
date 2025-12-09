import pytest
import math

from wpimath.controller import SimpleMotorFeedforwardMeters
from wpimath.trajectory import ExponentialProfileMeterVolts

kT = 10 * 0.001  # 10_ms
kV = 2.5629 * 1  # 2.5629_V / 1_mps
kA = 0.43277 * 1  # 0.43277_V / 1_mps_sq


def check_dynamics(profile, constraints, feedforward, current, goal):
    next_state = profile.calculate(kT, current, goal)
    signal = feedforward.calculate(current.velocity, next_state.velocity)

    assert abs(signal) <= constraints.maxInput + 1e-9

    return next_state


def test_reaches_goal():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(maxInput=12, a=-kV / kA, b=1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(0, kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(10, 0)
    state = ExponentialProfileMeterVolts.State(0, 0)

    for _ in range(450):
        state = check_dynamics(profile, constraints, feedforward, state, goal)

    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)


def test_backwards():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(maxInput=12, a=-kV / kA, b=1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(0, kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(-10, 0)
    state = ExponentialProfileMeterVolts.State(0, 0)

    for _ in range(400):
        state = check_dynamics(profile, constraints, feedforward, state, goal)

    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)


def test_switch_goal_in_middle():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(12, -kV / kA, 1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(0, kV, kA, kT)
    goal1 = ExponentialProfileMeterVolts.State(-10, 0)
    state = ExponentialProfileMeterVolts.State(0, 0)

    for _ in range(50):
        state = check_dynamics(profile, constraints, feedforward, state, goal1)
    
    assert state.position != goal1.position

    goal2 = ExponentialProfileMeterVolts.State(0, 0)
    for _ in range(100):
        state = check_dynamics(profile, constraints, feedforward, state, goal2)

    assert state.position == pytest.approx(goal2.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal2.velocity, abs=1e-3)


def test_top_speed():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(maxInput=12, a=-kV / kA, b=1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(0, kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(40, 0)
    state = ExponentialProfileMeterVolts.State(0, 0)

    max_speed = 0

    for _ in range(900):
        state = check_dynamics(profile, constraints, feedforward, state, goal)
        max_speed = max(state.velocity, max_speed)

    assert constraints.maxVelocity() == pytest.approx(max_speed, abs=1e-5)
    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)


def test_top_speed_backward():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(maxInput=12, a=-kV / kA, b=1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(0, kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(-40, 0)
    state = ExponentialProfileMeterVolts.State(0, 0)

    max_speed = 0

    for _ in range(900):
        state = check_dynamics(profile, constraints, feedforward, state, goal)
        max_speed = min(state.velocity, max_speed)

    assert -constraints.maxVelocity() == pytest.approx(max_speed, abs=1e-5)
    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)


def test_high_initial_speed():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(maxInput=12, a=-kV / kA, b=1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(0, kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(40, 0)
    state = ExponentialProfileMeterVolts.State(0, 8)

    for _ in range(900):
        state = check_dynamics(profile, constraints, feedforward, state, goal)

    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)


def test_high_initial_speed_backward():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(maxInput=12, a=-kV / kA, b=1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(0, kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(-40, 0)
    state = ExponentialProfileMeterVolts.State(0, -8)

    for _ in range(900):
        state = check_dynamics(profile, constraints, feedforward, state, goal)

    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)


def test_test_heuristic():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(maxInput=12, a=-kV / kA, b=1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)

    test_cases = [
        (ExponentialProfileMeterVolts.State(0, -4), ExponentialProfileMeterVolts.State(0.75, -4), ExponentialProfileMeterVolts.State(1.3758, 4.4304)),
        (ExponentialProfileMeterVolts.State(0, -4), ExponentialProfileMeterVolts.State(1.4103, 4), ExponentialProfileMeterVolts.State(1.3758, 4.4304)),
        (ExponentialProfileMeterVolts.State(0.6603, 4), ExponentialProfileMeterVolts.State(0.75, -4), ExponentialProfileMeterVolts.State(1.3758, 4.4304)),
        (ExponentialProfileMeterVolts.State(0.6603, 4), ExponentialProfileMeterVolts.State(1.4103, 4), ExponentialProfileMeterVolts.State(1.3758, 4.4304)),
        (ExponentialProfileMeterVolts.State(0, -4), ExponentialProfileMeterVolts.State(0.5, -2), ExponentialProfileMeterVolts.State(0.4367, 3.7217)),
        (ExponentialProfileMeterVolts.State(0, -4), ExponentialProfileMeterVolts.State(0.546, 2), ExponentialProfileMeterVolts.State(0.4367, 3.7217)),
        (ExponentialProfileMeterVolts.State(0.6603, 4), ExponentialProfileMeterVolts.State(0.5, -2), ExponentialProfileMeterVolts.State(0.5560, -2.9616)),
        (ExponentialProfileMeterVolts.State(0.6603, 4), ExponentialProfileMeterVolts.State(0.546, 2), ExponentialProfileMeterVolts.State(0.5560, -2.9616)),
        (ExponentialProfileMeterVolts.State(0, -4), ExponentialProfileMeterVolts.State(-0.75, -4), ExponentialProfileMeterVolts.State(-0.7156, -4.4304)),
        (ExponentialProfileMeterVolts.State(0, -4), ExponentialProfileMeterVolts.State(-0.0897, 4), ExponentialProfileMeterVolts.State(-0.7156, -4.4304)),
        (ExponentialProfileMeterVolts.State(0.6603, 4), ExponentialProfileMeterVolts.State(-0.75, -4), ExponentialProfileMeterVolts.State(-0.7156, -4.4304)),
        (ExponentialProfileMeterVolts.State(0.6603, 4), ExponentialProfileMeterVolts.State(-0.0897, 4), ExponentialProfileMeterVolts.State(-0.7156, -4.4304)),
        (ExponentialProfileMeterVolts.State(0, -4), ExponentialProfileMeterVolts.State(-0.5, -4.5), ExponentialProfileMeterVolts.State(1.095, 4.314)),
        (ExponentialProfileMeterVolts.State(0, -4), ExponentialProfileMeterVolts.State(1.0795, 4.5), ExponentialProfileMeterVolts.State(-0.5122, -4.351)),
        (ExponentialProfileMeterVolts.State(0.6603, 4), ExponentialProfileMeterVolts.State(-0.5, -4.5), ExponentialProfileMeterVolts.State(1.095, 4.314)),
        (ExponentialProfileMeterVolts.State(0.6603, 4), ExponentialProfileMeterVolts.State(1.0795, 4.5), ExponentialProfileMeterVolts.State(-0.5122, -4.351)),
        (ExponentialProfileMeterVolts.State(0, -8), ExponentialProfileMeterVolts.State(0, 0), ExponentialProfileMeterVolts.State(-0.1384, 3.342)),
        (ExponentialProfileMeterVolts.State(0, -8), ExponentialProfileMeterVolts.State(-1, 0), ExponentialProfileMeterVolts.State(-0.562, -6.792)),
        (ExponentialProfileMeterVolts.State(0, 8), ExponentialProfileMeterVolts.State(1, 0), ExponentialProfileMeterVolts.State(0.562, 6.792)),
        (ExponentialProfileMeterVolts.State(0, 8), ExponentialProfileMeterVolts.State(-1, 0), ExponentialProfileMeterVolts.State(-0.785, -4.346)),
    ]
    
    for initial, goal, expected_inflection in test_cases:
        inflection = profile.calculateInflectionPoint(initial, goal)
        assert inflection.position == pytest.approx(expected_inflection.position, abs=1e-3)
        assert inflection.velocity == pytest.approx(expected_inflection.velocity, abs=1e-3)


def test_timing_to_current():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(maxInput=12, a=-kV / kA, b=1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(0, kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(2, 0)
    state = ExponentialProfileMeterVolts.State(0, 0)

    for _ in range(900):
        state = check_dynamics(profile, constraints, feedforward, state, goal)
        time_left = profile.timeLeftUntil(state, state)
        assert time_left == pytest.approx(0, abs=0.02)
    
    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)


def test_timing_to_goal():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(maxInput=12, a=-kV / kA, b=1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(0, kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(2, 0)
    state = ExponentialProfileMeterVolts.State(0, 0)

    prediction = profile.timeLeftUntil(state, goal)
    reached_goal = False

    for i in range(900):
        state = check_dynamics(profile, constraints, feedforward, state, goal)
        if not reached_goal and state.position == pytest.approx(goal.position, abs=1e-3) and state.velocity == pytest.approx(goal.velocity, abs=1e-3):
            assert prediction == pytest.approx((i * 0.01), abs=0.25)
            reached_goal = True
            
    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)


def test_timing_to_negative_goal():
    constraints = ExponentialProfileMeterVolts.Constraints.fromStateSpace(maxInput=12, a=-kV / kA, b=1 / kA)
    profile = ExponentialProfileMeterVolts(constraints)
    feedforward = SimpleMotorFeedforwardMeters(0, kV, kA, kT)
    goal = ExponentialProfileMeterVolts.State(-2, 0)
    state = ExponentialProfileMeterVolts.State(0, 0)

    prediction = profile.timeLeftUntil(state, goal)
    reached_goal = False

    for i in range(900):
        state = check_dynamics(profile, constraints, feedforward, state, goal)
        if not reached_goal and state.position == pytest.approx(goal.position, abs=1e-3) and state.velocity == pytest.approx(goal.velocity, abs=1e-3):
            assert prediction == pytest.approx((i * 0.01), abs=0.25)
            reached_goal = True
            
    assert state.position == pytest.approx(goal.position, abs=1e-3)
    assert state.velocity == pytest.approx(goal.velocity, abs=1e-3)