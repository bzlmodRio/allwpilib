import pytest
import math

from wpimath.kinematics import DifferentialDriveKinematics, ChassisSpeeds
from wpimath.trajectory import TrajectoryGenerator, TrajectoryConfig, Trajectory
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.trajectory.constraint import DifferentialDriveKinematicsConstraint
from wpimath.units import feetToMeters, inchesToMeters

def test_constraint():
    max_velocity = feetToMeters(12)
    kinematics = DifferentialDriveKinematics(trackwidth=inchesToMeters(27))

    config = TrajectoryConfig(
        feetToMeters(12), feetToMeters(12)
    )
    config.addConstraint(DifferentialDriveKinematicsConstraint(kinematics, max_velocity))
    
    trajectory = TrajectoryGenerator.generateTrajectory(
        [
            Pose2d(x=0, y=0, rotation=Rotation2d.fromDegrees(0)),
            Pose2d(x=5, y=5, rotation=Rotation2d.fromDegrees(90)),
        ],
        config,
    )
    
    time = 0
    dt = 0.02
    duration = trajectory.totalTime()

    while time < duration:
        point = trajectory.sample(time)
        time += dt
        
        chassis_speeds = ChassisSpeeds(
            vx=point.velocity, 
            vy=0, 
            omega=point.velocity * point.curvature
        )
        
        wheel_speeds = kinematics.toWheelSpeeds(chassis_speeds)

        # The C++ test uses a small tolerance (0.05_mps) to account for floating-point inaccuracies
        # in the trajectory generation and sampling process.
        assert wheel_speeds.left < max_velocity + 0.05
        assert wheel_speeds.right < max_velocity + 0.05