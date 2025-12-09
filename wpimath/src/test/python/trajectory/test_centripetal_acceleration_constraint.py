import pytest
import math

from wpimath.kinematics import ChassisSpeeds
from wpimath.trajectory import TrajectoryGenerator, TrajectoryConfig, Trajectory
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.units import feetToMeters
from wpimath.trajectory.constraint import CentripetalAccelerationConstraint


def test_constraint():
    max_centripetal_acceleration = feetToMeters(7)
    config = TrajectoryConfig(maxVelocity=feetToMeters(12), maxAcceleration=feetToMeters(12))
    config.addConstraint(CentripetalAccelerationConstraint(max_centripetal_acceleration))

    # The test trajectory
    # fmt: off
    trajectory = TrajectoryGenerator.generateTrajectory(
        [
            Pose2d(x=0, y=0, rotation=Rotation2d.fromDegrees(0)),
            Pose2d(x=5, y=5, rotation=Rotation2d.fromDegrees(90)),
        ],
        config,
    )
    # fmt: on

    time = 0
    dt = 0.02
    duration = trajectory.totalTime()

    while time < duration:
        point = trajectory.sample(time)
        time += dt
        centripetal_acceleration = (
            point.velocity**2 * abs(point.curvature)
        )
        assert centripetal_acceleration < max_centripetal_acceleration + 0.05