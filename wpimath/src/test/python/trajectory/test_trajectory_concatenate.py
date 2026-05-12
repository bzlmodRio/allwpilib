import pytest

from wpimath import (
    Pose2d,
    Rotation2d,
    SplineTrajectory,
    TrajectoryConfig,
    TrajectoryGenerator,
)


def test_states():
    t1 = TrajectoryGenerator.generate_trajectory(
        Pose2d(), [], Pose2d(x=1, y=1, rotation=Rotation2d()), TrajectoryConfig(2, 2)
    )
    t2 = TrajectoryGenerator.generate_trajectory(
        Pose2d(x=1, y=1, rotation=Rotation2d()),
        [],
        Pose2d(x=2, y=2, rotation=Rotation2d.from_degrees(45)),
        TrajectoryConfig(2, 2),
    )

    t = SplineTrajectory(t1.concatenate_samples(t2.samples()))
    states = t.samples()

    time = -1.0
    for i, state in enumerate(states):
        # Timestamps must be strictly increasing
        assert state.timestamp > time
        time = state.timestamp

        # States from t1 match directly; states from t2 have adjusted time
        t1_states = t1.samples()
        t2_states = t2.samples()
        if i < len(t1_states):
            assert state.pose.x == pytest.approx(t1_states[i].pose.x, abs=1e-9)
            assert state.pose.y == pytest.approx(t1_states[i].pose.y, abs=1e-9)
            assert state.timestamp == pytest.approx(t1_states[i].timestamp, abs=1e-9)
        else:
            j = i - len(t1_states) + 1
            expected_t = t2_states[j].timestamp + t1.duration()
            assert state.timestamp == pytest.approx(expected_t, abs=1e-9)
            assert state.pose.x == pytest.approx(t2_states[j].pose.x, abs=1e-9)
            assert state.pose.y == pytest.approx(t2_states[j].pose.y, abs=1e-9)
