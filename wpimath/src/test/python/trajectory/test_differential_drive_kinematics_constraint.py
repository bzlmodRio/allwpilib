from wpimath import (
    ChassisVelocities,
    DifferentialDriveKinematics,
    DifferentialDriveKinematicsConstraint,
    Pose2d,
    Rotation2d,
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
    max_velocity = 12 * 0.3048  # 12 fps in m/s
    kinematics = DifferentialDriveKinematics(trackwidth=27 * 0.0254)  # 27 inches

    config = TrajectoryConfig.from_fps(12, 12)
    config.add_constraint(DifferentialDriveKinematicsConstraint(kinematics, max_velocity))
    trajectory = _get_test_trajectory(config)

    dt = 0.020
    t = 0.0
    duration = trajectory.duration()

    while t < duration:
        state = trajectory.sample_at(t)
        t += dt

        chassis_vel = ChassisVelocities(
            vx=state.forward_velocity(), vy=0, omega=state.forward_velocity() * state.curvature
        )
        wheel_vel = kinematics.to_wheel_velocities(chassis_vel)

        assert wheel_vel.left < max_velocity + 0.05
        assert wheel_vel.right < max_velocity + 0.05
