import pytest
import math

from wpimath.trajectory import TrajectoryGenerator, TrajectoryConfig, Trajectory
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.units import feetToMeters
import trajectory_generator


def test_obeys_constraints():
    config = TrajectoryConfig(feetToMeters(12), feetToMeters(12))
    trajectory = trajectory_generator.getTestTrajectory(config)

    time = 0
    dt = 0.02
    duration = trajectory.totalTime()

    while time < duration:
        point = trajectory.sample(time)
        time += dt
        
        assert abs(point.velocity) <= feetToMeters(12) + 0.01
        assert abs(point.acceleration) <= feetToMeters(12) + 0.01


def test_returns_empty_on_malformed():
    config = TrajectoryConfig(feetToMeters(12), feetToMeters(12))

    t = TrajectoryGenerator.generateTrajectory(
        [
            Pose2d(x=0, y=0, rotation=Rotation2d.fromDegrees(0)),
            Pose2d(x=1, y=0, rotation=Rotation2d.fromDegrees(180)),
        ],
        config,
    )
    
    # A malformed trajectory should return a trajectory with a single state and zero time.
    assert len(t.states()) == 1
    assert t.totalTime() == 0


def test_curvature_optimization():
    config = TrajectoryConfig(feetToMeters(12), feetToMeters(12))

    t = TrajectoryGenerator.generateTrajectory(
        [
            Pose2d(x=1, y=0, rotation=Rotation2d.fromDegrees(90)),
            Pose2d(x=0, y=1, rotation=Rotation2d.fromDegrees(180)),
            Pose2d(x=-1, y=0, rotation=Rotation2d.fromDegrees(270)),
            Pose2d(x=0, y=-1, rotation=Rotation2d.fromDegrees(0)),
            Pose2d(x=1, y=0, rotation=Rotation2d.fromDegrees(90)),
        ],
        config,
    )

    # Check that curvature is not zero for any intermediate states.
    for i in range(1, len(t.states()) - 1):
        assert t.states()[i].curvature != pytest.approx(0.0)