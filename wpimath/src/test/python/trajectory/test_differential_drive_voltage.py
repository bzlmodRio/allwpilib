import pytest
import math

from wpimath.controller import SimpleMotorFeedforwardMeters
from wpimath.kinematics import DifferentialDriveKinematics, ChassisSpeeds
from wpimath.trajectory import TrajectoryGenerator, TrajectoryConfig, Trajectory
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.trajectory.constraint import DifferentialDriveVoltageConstraint
from wpimath.units import feetToMeters

def test_constraint():
    # Pick an unreasonably large kA to ensure the constraint has to do some work
    feedforward = SimpleMotorFeedforwardMeters(
        1, 1, 3
    )
    kinematics = DifferentialDriveKinematics(trackwidth=0.5)
    max_voltage = 10

    config = TrajectoryConfig(
        maxVelocity=feetToMeters(12), maxAcceleration=feetToMeters(12)
    )
    config.addConstraint(DifferentialDriveVoltageConstraint(feedforward, kinematics, max_voltage))

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
        
        chassis_speeds = ChassisSpeeds(point.velocity, 0,
                                        point.velocity * point.curvature)

        wheel_speeds = kinematics.toWheelSpeeds(chassis_speeds)
        left = wheel_speeds.left
        right = wheel_speeds.right
        acceleration = point.acceleration

        # Not really a strictly-correct test as we're using the chassis accel
        # instead of the wheel accel, but much easier than doing it "properly" and
        # a reasonable check anyway
        assert feedforward.calculate(
            left, left + acceleration * dt
        ) < max_voltage + 0.05
        assert feedforward.calculate(
            left, left + acceleration * dt
        ) > -max_voltage - 0.05
        assert feedforward.calculate(
            right, right + acceleration * dt
        ) < max_voltage + 0.05
        assert feedforward.calculate(
            right, right + acceleration * dt
        ) > -max_voltage - 0.05


def test_high_curvature():
    feedforward = SimpleMotorFeedforwardMeters(
        1, 1, 3
    )
    # Large trackwidth - need to test with radius of curvature less than half of
    # trackwidth
    kinematics = DifferentialDriveKinematics(3)
    max_voltage = 10

    config = TrajectoryConfig(
        maxVelocity=feetToMeters(12), maxAcceleration=feetToMeters(12)
    )
    config.addConstraint(DifferentialDriveVoltageConstraint(feedforward, kinematics, max_voltage))

    TrajectoryGenerator.generateTrajectory(
        Pose2d(x=1, y=0, rotation=Rotation2d.fromDegrees(90)),
        [],
        Pose2d(x=0, y=1, rotation=Rotation2d.fromDegrees(180)),
        config,
    )

    config.setReversed(True)

    TrajectoryGenerator.generateTrajectory(
        Pose2d(x=0, y=1, rotation=Rotation2d.fromDegrees(180)),
        [],
        Pose2d(x=1, y=0, rotation=Rotation2d.fromDegrees(90)),
        config,
    )