import pytest
import math

from wpimath.trajectory import TrapezoidProfile
from wpimath.units import (
    meters,
    meters_per_second,
    meters_per_second_squared,
    seconds,
)

kDt = seconds(0.01)


def test_reaches_goal():
    constraints = TrapezoidProfile.Constraints(
        meters_per_second(1.75), meters_per_second_squared(0.75)
    )
    goal = TrapezoidProfile.State(meters(3), meters_per_second(0))
    state = TrapezoidProfile.State()

    profile = TrapezoidProfile(constraints)
    for _ in range(450):
        state = profile.calculate(kDt, state, goal)

    assert state.position == pytest.approx(goal.position)
    assert state.velocity == pytest.approx(goal.velocity)


def test_pos_continuous_under_vel_change():
    constraints = TrapezoidProfile.Constraints(
        meters_per_second(1.75), meters_per_second_squared(0.75)
    )
    goal = TrapezoidProfile.State(meters(12), meters_per_second(0))

    profile = TrapezoidProfile(constraints)
    state = profile.calculate(kDt, TrapezoidProfile.State(), goal)

    last_pos = state.position
    for i in range(1600):
        if i == 400:
            constraints.maxVelocity = meters_per_second(0.75)
            profile = TrapezoidProfile(constraints)

        state = profile.calculate(kDt, state, goal)
        estimated_vel = (state.position - last_pos) / kDt

        if i >= 400:
            assert estimated_vel <= constraints.maxVelocity + 1e-4
            assert state.velocity <= constraints.maxVelocity

        last_pos = state.position

    assert state.position == pytest.approx(goal.position)
    assert state.velocity == pytest.approx(goal.velocity)


def test_backwards():
    constraints = TrapezoidProfile.Constraints(
        meters_per_second(0.75), meters_per_second_squared(0.75)
    )
    goal = TrapezoidProfile.State(meters(-2), meters_per_second(0))
    state = TrapezoidProfile.State()

    profile = TrapezoidProfile(constraints)
    for _ in range(400):
        state = profile.calculate(kDt, state, goal)

    assert state.position == pytest.approx(goal.position)
    assert state.velocity == pytest.approx(goal.velocity)


def test_switch_goal_in_middle():
    constraints = TrapezoidProfile.Constraints(
        meters_per_second(0.75), meters_per_second_squared(0.75)
    )
    goal = TrapezoidProfile.State(meters(-2), meters_per_second(0))
    state = TrapezoidProfile.State()

    profile = TrapezoidProfile(constraints)
    for _ in range(200):
        state = profile.calculate(kDt, state, goal)

    assert state.position != pytest.approx(goal.position)

    goal = TrapezoidProfile.State(meters(0), meters_per_second(0))
    profile = TrapezoidProfile(constraints)
    for _ in range(550):
        state = profile.calculate(kDt, state, goal)

    assert state.position == pytest.approx(goal.position)
    assert state.velocity == pytest.approx(goal.velocity)


def test_top_speed():
    constraints = TrapezoidProfile.Constraints(
        meters_per_second(0.75), meters_per_second_squared(0.75)
    )
    goal = TrapezoidProfile.State(meters(4), meters_per_second(0))
    state = TrapezoidProfile.State()

    profile = TrapezoidProfile(constraints)
    for _ in range(200):
        state = profile.calculate(kDt, state, goal)

    assert constraints.maxVelocity == pytest.approx(state.velocity, abs=10e-5)

    profile = TrapezoidProfile(constraints)
    for _ in range(2000):
        state = profile.calculate(kDt, state, goal)

    assert state.position == pytest.approx(goal.position)
    assert state.velocity == pytest.approx(goal.velocity)


def test_timing_to_current():
    constraints = TrapezoidProfile.Constraints(
        meters_per_second(0.75), meters_per_second_squared(0.75)
    )
    goal = TrapezoidProfile.State(meters(2), meters_per_second(0))
    state = TrapezoidProfile.State()

    profile = TrapezoidProfile(constraints)
    for _ in range(400):
        state = profile.calculate(kDt, state, goal)
        assert profile.timeLeftUntil(state.position) == pytest.approx(0.0, abs=0.02)


def test_timing_to_goal():
    constraints = TrapezoidProfile.Constraints(
        meters_per_second(0.75), meters_per_second_squared(0.75)
    )
    goal = TrapezoidProfile.State(meters(2), meters_per_second(0))

    profile = TrapezoidProfile(constraints)
    state = profile.calculate(kDt, goal, TrapezoidProfile.State())

    predicted_time_left = profile.timeLeftUntil(goal.position)
    reached_goal = False
    for i in range(400):
        state = profile.calculate(kDt, state, goal)
        if not reached_goal and state.position == pytest.approx(goal.position):
            assert predicted_time_left == pytest.approx(i / 100.0, abs=0.25)
            reached_goal = True


def test_timing_before_goal():
    constraints = TrapezoidProfile.Constraints(
        meters_per_second(0.75), meters_per_second_squared(0.75)
    )
    goal = TrapezoidProfile.State(meters(2), meters_per_second(0))

    profile = TrapezoidProfile(constraints)
    state = profile.calculate(kDt, goal, TrapezoidProfile.State())

    predicted_time_left = profile.timeLeftUntil(meters(1))
    reached_goal = False
    for i in range(400):
        state = profile.calculate(kDt, state, goal)
        if not reached_goal and abs(state.velocity - meters_per_second(1)) < 10e-5:
            assert predicted_time_left == pytest.approx(i / 100.0, abs=0.02)
            reached_goal = True


def test_timing_to_negative_goal():
    constraints = TrapezoidProfile.Constraints(
        meters_per_second(0.75), meters_per_second_squared(0.75)
    )
    goal = TrapezoidProfile.State(meters(-2), meters_per_second(0))

    profile = TrapezoidProfile(constraints)
    state = profile.calculate(kDt, goal, TrapezoidProfile.State())

    predicted_time_left = profile.timeLeftUntil(goal.position)
    reached_goal = False
    for i in range(400):
        state = profile.calculate(kDt, state, goal)
        if not reached_goal and state.position == pytest.approx(goal.position):
            assert predicted_time_left == pytest.approx(i / 100.0, abs=0.25)
            reached_goal = True


def test_timing_before_negative_goal():
    constraints = TrapezoidProfile.Constraints(
        meters_per_second(0.75), meters_per_second_squared(0.75)
    )
    goal = TrapezoidProfile.State(meters(-2), meters_per_second(0))

    profile = TrapezoidProfile(constraints)
    state = profile.calculate(kDt, goal, TrapezoidProfile.State())

    predicted_time_left = profile.timeLeftUntil(meters(-1))
    reached_goal = False
    for i in range(400):
        state = profile.calculate(kDt, state, goal)
        if not reached_goal and abs(state.velocity - -meters_per_second(1)) < 10e-5:
            assert predicted_time_left == pytest.approx(i / 100.0, abs=0.02)
            reached_goal = True


def test_initalization_of_current_state():
    constraints = TrapezoidProfile.Constraints(
        meters_per_second(1), meters_per_second_squared(1)
    )
    profile = TrapezoidProfile(constraints)
    assert profile.timeLeftUntil(meters(0)) == pytest.approx(0.0, abs=1e-10)
    assert profile.totalTime() == pytest.approx(0.0, abs=1e-10)


def test_initial_velocity_constraints():
    constraints = TrapezoidProfile.Constraints(
        meters_per_second(0.75), meters_per_second_squared(0.75)
    )
    goal = TrapezoidProfile.State(meters(10), meters_per_second(0))
    state = TrapezoidProfile.State(meters(0), meters_per_second(-10))

    profile = TrapezoidProfile(constraints)

    for _ in range(200):
        state = profile.calculate(kDt, state, goal)
        assert abs(state.velocity) <= abs(constraints.maxVelocity)


def test_goal_velocity_constraints():
    constraints = TrapezoidProfile.Constraints(
        meters_per_second(0.75), meters_per_second_squared(0.75)
    )
    goal = TrapezoidProfile.State(meters(10), meters_per_second(5))
    state = TrapezoidProfile.State(meters(0), meters_per_second(0.75))

    profile = TrapezoidProfile(constraints)

    for _ in range(200):
        state = profile.calculate(kDt, state, goal)
        assert abs(state.velocity) <= abs(constraints.maxVelocity)


def test_negative_goal_velocity_constraints():
    constraints = TrapezoidProfile.Constraints(
        meters_per_second(0.75), meters_per_second_squared(0.75)
    )
    goal = TrapezoidProfile.State(meters(10), meters_per_second(-5))
    state = TrapezoidProfile.State(meters(0), meters_per_second(0.75))

    profile = TrapezoidProfile(constraints)

    for _ in range(200):
        state = profile.calculate(kDt, state, goal)
        assert abs(state.velocity) <= abs(constraints.maxVelocity)