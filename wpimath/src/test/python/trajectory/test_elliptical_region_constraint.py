import pytest
import math

from wpimath.trajectory import TrajectoryGenerator, TrajectoryConfig, Trajectory
from wpimath.geometry import Pose2d, Rotation2d, Translation2d, Ellipse2d
from wpimath.units import (
    meters,
    meters_per_second_squared,
    radians,
    feetToMeters
)
from wpimath.trajectory.constraint import EllipticalRegionConstraint, MaxVelocityConstraint


def test_constraint():
    max_velocity = feetToMeters(2)
    ellipse = Ellipse2d(
        Pose2d(feetToMeters(5), feetToMeters(2.5), Rotation2d.fromDegrees(180)), feetToMeters(5), feetToMeters(2.5)
    )

    config = TrajectoryConfig(feetToMeters(13), feetToMeters(13))
    config.addConstraint(EllipticalRegionConstraint(ellipse, MaxVelocityConstraint(max_velocity)))
    
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

    exceeded_constraint_outside_region = False
    for point in trajectory.states():
        if ellipse.contains(point.pose.translation()):
            assert abs(point.velocity) < max_velocity + meters_per_second_squared(0.05)
        elif abs(point.velocity) >= max_velocity + meters_per_second_squared(0.05):
            exceeded_constraint_outside_region = True
    
    assert exceeded_constraint_outside_region