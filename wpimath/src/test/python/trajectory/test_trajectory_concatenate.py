import pytest
import math

from wpimath.trajectory import TrajectoryGenerator, TrajectoryConfig
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.units import meters, degrees, meters_per_second, meters_per_second_squared, seconds


def test_states():
    config = TrajectoryConfig(meters_per_second(2), meters_per_second_squared(2))

    t1 = TrajectoryGenerator.generateTrajectory(
        Pose2d(meters(0), meters(0), Rotation2d.fromDegrees(0)),
        [],
        Pose2d(meters(1), meters(1), Rotation2d.fromDegrees(0)),
        config
    )
    t2 = TrajectoryGenerator.generateTrajectory(
        Pose2d(meters(1), meters(1), Rotation2d.fromDegrees(0)),
        [],
        Pose2d(meters(2), meters(2), Rotation2d.fromDegrees(45)),
        config
    )
    
    t = t1 + t2

    time = -1.0
    for i, state in enumerate(t.states()):
        # Make sure that the timestamps are strictly increasing.
        assert state.t > time
        time = state.t

        # Ensure that the states in t are the same as those in t1 and t2.
        if i < len(t1.states()):
            assert state == t1.states()[i]
        else:
            st = t2.states()[i - len(t1.states()) + 1]
            st.t += t1.totalTime()
            assert state == st