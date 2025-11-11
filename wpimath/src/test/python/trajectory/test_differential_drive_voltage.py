import pytest
import math

from wpimath.controller import SimpleMotorFeedforwardMeters
from wpimath.kinematics import DifferentialDriveKinematics, ChassisSpeeds
from wpimath.trajectory import TrajectoryGenerator, TrajectoryConfig, Trajectory
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.units import (
    meters,
    volts,
    meters_per_second,
    meters_per_second_squared,
    seconds,
    feetToMeters,
)
from wpimath.trajectory.constraint import DifferentialDriveVoltageConstraint


def test_constraint():
    # Pick an unreasonably large kA to ensure the constraint has to do some work
    feedforward = SimpleMotorFeedforwardMeters(
        volts(1), 1, 3
    )
    kinematics = DifferentialDriveKinematics(meters(0.5))
    max_voltage = volts(10)

    config = TrajectoryConfig(
        feetToMeters(12), feetToMeters(12)
    )
    config.addConstraint(DifferentialDriveVoltageConstraint(feedforward, kinematics, max_voltage))

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
        ) < max_voltage + volts(0.05)
        assert feedforward.calculate(
            left, left + acceleration * dt
        ) > -max_voltage - volts(0.05)
        assert feedforward.calculate(
            right, right + acceleration * dt
        ) < max_voltage + volts(0.05)
        assert feedforward.calculate(
            right, right + acceleration * dt
        ) > -max_voltage - volts(0.05)


def test_high_curvature():
    feedforward = SimpleMotorFeedforwardMeters(
        volts(1), 1, 3
    )
    # Large trackwidth - need to test with radius of curvature less than half of
    # trackwidth
    kinematics = DifferentialDriveKinematics(meters(3))
    max_voltage = volts(10)

    config = TrajectoryConfig(
        feetToMeters(12), feetToMeters(12)
    )
    config.addConstraint(DifferentialDriveVoltageConstraint(feedforward, kinematics, max_voltage))

    TrajectoryGenerator.generateTrajectory(
        Pose2d(meters(1), meters(0), Rotation2d.fromDegrees(90)),
        [],
        Pose2d(meters(0), meters(1), Rotation2d.fromDegrees(180)),
        config,
    )

    config.setReversed(True)

    TrajectoryGenerator.generateTrajectory(
        Pose2d(meters(0), meters(1), Rotation2d.fromDegrees(180)),
        [],
        Pose2d(meters(1), meters(0), Rotation2d.fromDegrees(90)),
        config,
    )