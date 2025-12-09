import pytest
import math

from wpimath.trajectory import TrajectoryGenerator, TrajectoryConfig, Trajectory
from wpimath.geometry import Pose2d, Rotation2d, Translation2d, Ellipse2d
from wpimath.trajectory.constraint import EllipticalRegionConstraint, MaxVelocityConstraint
from wpimath.units import feetToMeters

def test_constraint():
    max_velocity = feetToMeters(2)
    ellipse = Ellipse2d(
        Pose2d(x=feetToMeters(5), y=feetToMeters(2.5), rotation=Rotation2d.fromDegrees(180)), feetToMeters(5), feetToMeters(2.5)
    )

    config = TrajectoryConfig(maxVelocity=feetToMeters(13), maxAcceleration=feetToMeters(13))
    config.addConstraint(EllipticalRegionConstraint(ellipse, MaxVelocityConstraint(max_velocity)))
    
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

    exceeded_constraint_outside_region = False
    for point in trajectory.states():
        if ellipse.contains(point.pose.translation()):
            assert abs(point.velocity) < max_velocity + 0.05
        elif abs(point.velocity) >= max_velocity + 0.05:
            exceeded_constraint_outside_region = True
    
    assert exceeded_constraint_outside_region