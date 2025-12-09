import pytest
import math

from wpimath.trajectory import TrajectoryGenerator, TrajectoryConfig
from wpimath.geometry import Pose2d, Rotation2d, Translation2d


def test_states():
    config = TrajectoryConfig(maxVelocity=2, maxAcceleration=2)

    t1 = TrajectoryGenerator.generateTrajectory(
        Pose2d(x=0, y=0, rotation=Rotation2d.fromDegrees(0)),
        [],
        Pose2d(x=1, y=1, rotation=Rotation2d.fromDegrees(0)),
        config
    )
    t2 = TrajectoryGenerator.generateTrajectory(
        Pose2d(x=1, y=1, rotation=Rotation2d.fromDegrees(0)),
        [],
        Pose2d(x=2, y=2, rotation=Rotation2d.fromDegrees(45)),
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