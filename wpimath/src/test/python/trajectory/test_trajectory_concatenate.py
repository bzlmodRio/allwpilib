import pytest

from wpimath import (
    Pose2d,
    Rotation2d,
    TrajectoryConfig,
    TrajectoryGenerator,
)


def test_states():
    t1 = TrajectoryGenerator.generateTrajectory(
        Pose2d(), [], Pose2d(x=1, y=1, rotation=Rotation2d()), TrajectoryConfig(2, 2)
    )
    t2 = TrajectoryGenerator.generateTrajectory(
        Pose2d(x=1, y=1, rotation=Rotation2d()),
        [],
        Pose2d(x=2, y=2, rotation=Rotation2d.fromDegrees(45)),
        TrajectoryConfig(2, 2),
    )

    t = t1 + t2
    states = t.states()

    time = -1.0
    for i, state in enumerate(states):
        # Timestamps must be strictly increasing
        assert state.t > time
        time = state.t

        # States from t1 match directly; states from t2 have adjusted time
        t1_states = t1.states()
        t2_states = t2.states()
        if i < len(t1_states):
            assert state.pose.x == pytest.approx(t1_states[i].pose.x, abs=1e-9)
            assert state.pose.y == pytest.approx(t1_states[i].pose.y, abs=1e-9)
            assert state.t == pytest.approx(t1_states[i].t, abs=1e-9)
        else:
            j = i - len(t1_states) + 1
            expected_t = t2_states[j].t + t1.totalTime()
            assert state.t == pytest.approx(expected_t, abs=1e-9)
            assert state.pose.x == pytest.approx(t2_states[j].pose.x, abs=1e-9)
            assert state.pose.y == pytest.approx(t2_states[j].pose.y, abs=1e-9)
