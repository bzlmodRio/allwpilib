from wpimath import (
    DifferentialDriveKinematics,
    DifferentialDriveVoltageConstraint,
    Pose2d,
    Rotation2d,
    SimpleMotorFeedforwardMeters,
    Transform2d,
    Translation2d,
    TrajectoryConfig,
    TrajectoryGenerator,
)


def _get_test_trajectory(config):
    side_start = Pose2d.from_feet(1.54, 23.23, Rotation2d.from_degrees(180))
    cross_scale = Pose2d.from_feet(23.7, 6.8, Rotation2d.from_degrees(-160))
    config.set_reversed(True)
    waypoints = [
        (side_start + Transform2d(Translation2d.from_feet(-13, 0), Rotation2d())).translation(),
        (
            side_start
            + Transform2d(Translation2d.from_feet(-19.5, 5.0), Rotation2d.from_degrees(-90))
        ).translation(),
    ]
    return TrajectoryGenerator.generate_trajectory(side_start, waypoints, cross_scale, config)


def test_constraint():
    # Large kA to ensure constraint has to do work
    feedforward = SimpleMotorFeedforwardMeters(kS=1, kV=1, kA=3)
    kinematics = DifferentialDriveKinematics(trackwidth=0.5)
    max_voltage = 10.0
    dt = 0.020

    config = TrajectoryConfig.from_fps(12, 12)
    config.add_constraint(DifferentialDriveVoltageConstraint(feedforward, kinematics, max_voltage))
    trajectory = _get_test_trajectory(config)

    t = 0.0
    duration = trajectory.duration()

    while t < duration:
        state = trajectory.sample_at(t)
        t += dt

        from wpimath import ChassisVelocities
        chassis_vel = ChassisVelocities(
            vx=state.forward_velocity(), vy=0, omega=state.forward_velocity() * state.curvature
        )
        wheel_vel = kinematics.to_wheel_velocities(chassis_vel)
        accel = state.forward_acceleration()

        assert feedforward.calculate(wheel_vel.left, wheel_vel.left + accel * dt) < max_voltage + 0.05
        assert feedforward.calculate(wheel_vel.left, wheel_vel.left + accel * dt) > -max_voltage - 0.05
        assert feedforward.calculate(wheel_vel.right, wheel_vel.right + accel * dt) < max_voltage + 0.05
        assert feedforward.calculate(wheel_vel.right, wheel_vel.right + accel * dt) > -max_voltage - 0.05


def test_high_curvature():
    feedforward = SimpleMotorFeedforwardMeters(kS=1, kV=1, kA=3)
    kinematics = DifferentialDriveKinematics(trackwidth=3.0)
    max_voltage = 10.0

    config = TrajectoryConfig.from_fps(12, 12)
    config.add_constraint(DifferentialDriveVoltageConstraint(feedforward, kinematics, max_voltage))

    # Should not raise
    TrajectoryGenerator.generate_trajectory(
        Pose2d(x=1, y=0, rotation=Rotation2d.from_degrees(90)),
        [],
        Pose2d(x=0, y=1, rotation=Rotation2d.from_degrees(180)),
        config,
    )

    config.set_reversed(True)
    TrajectoryGenerator.generate_trajectory(
        Pose2d(x=0, y=1, rotation=Rotation2d.from_degrees(180)),
        [],
        Pose2d(x=1, y=0, rotation=Rotation2d.from_degrees(90)),
        config,
    )
