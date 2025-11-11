import pytest
import math

from wpimath.kinematics import ChassisSpeeds
from wpimath.trajectory import TrajectoryGenerator, TrajectoryConfig, Trajectory
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.units import (
    meters_per_second_squared,
    seconds,
    meters,
    radians,
    feetToMeters
)
from wpimath.trajectory.constraint import CentripetalAccelerationConstraint


def test_constraint():
    max_centripetal_acceleration = feetToMeters(7)
    config = TrajectoryConfig(feetToMeters(12), feetToMeters(12))
    config.addConstraint(CentripetalAccelerationConstraint(max_centripetal_acceleration))

    # The test trajectory
    # fmt: off
    trajectory = TrajectoryGenerator.generateTrajectory(
        [
            Pose2d(meters(0), meters(0), Rotation2d.fromDegrees(0)),
            Pose2d(meters(5), meters(5), Rotation2d.fromDegrees(90)),
        ],
        config,
    )
    # fmt: on

    time = seconds(0)
    dt = seconds(0.02)
    duration = trajectory.totalTime()

    while time < duration:
        point = trajectory.sample(time)
        time += dt
        centripetal_acceleration = (
            point.velocity**2 * abs(point.curvature)
        )
        assert centripetal_acceleration < max_centripetal_acceleration + meters_per_second_squared(0.05)