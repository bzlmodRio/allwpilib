import pytest
import math

from wpimath.kinematics import DifferentialDriveKinematics, ChassisSpeeds
from wpimath.trajectory import TrajectoryGenerator, TrajectoryConfig, Trajectory
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.units import (
    seconds,
    meters,
    meters_per_second,
    meters_per_second_squared,
    feetToMeters,
    inchesToMeters
)
from wpimath.trajectory.constraint import DifferentialDriveKinematicsConstraint


def test_constraint():
    max_velocity = feetToMeters(12)
    kinematics = DifferentialDriveKinematics(inchesToMeters(27))

    config = TrajectoryConfig(
        feetToMeters(12), feetToMeters(12)
    )
    config.addConstraint(DifferentialDriveKinematicsConstraint(kinematics, max_velocity))
    
    trajectory = TrajectoryGenerator.generateTrajectory(
        [
            Pose2d(meters(0), meters(0), Rotation2d.fromDegrees(0)),
            Pose2d(meters(5), meters(5), Rotation2d.fromDegrees(90)),
        ],
        config,
    )
    
    time = seconds(0)
    dt = seconds(0.02)
    duration = trajectory.totalTime()

    while time < duration:
        point = trajectory.sample(time)
        time += dt
        
        chassis_speeds = ChassisSpeeds(
            point.velocity, 
            meters_per_second(0), 
            point.velocity * point.curvature
        )
        
        wheel_speeds = kinematics.toWheelSpeeds(chassis_speeds)

        # The C++ test uses a small tolerance (0.05_mps) to account for floating-point inaccuracies
        # in the trajectory generation and sampling process.
        assert wheel_speeds.left < max_velocity + meters_per_second(0.05)
        assert wheel_speeds.right < max_velocity + meters_per_second(0.05)