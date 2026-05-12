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
    side_start = Pose2d.fromFeet(1.54, 23.23, Rotation2d.fromDegrees(180))
    cross_scale = Pose2d.fromFeet(23.7, 6.8, Rotation2d.fromDegrees(-160))
    config.setReversed(True)
    waypoints = [
        (side_start + Transform2d(Translation2d.fromFeet(-13, 0), Rotation2d())).translation(),
        (
            side_start
            + Transform2d(Translation2d.fromFeet(-19.5, 5.0), Rotation2d.fromDegrees(-90))
        ).translation(),
    ]
    return TrajectoryGenerator.generateTrajectory(side_start, waypoints, cross_scale, config)


def test_constraint():
    max_velocity = 12 * 0.3048  # 12 fps in m/s
    kinematics = DifferentialDriveKinematics(trackwidth=27 * 0.0254)  # 27 inches

    config = TrajectoryConfig.fromFps(12, 12)
    config.addConstraint(DifferentialDriveKinematicsConstraint(kinematics, max_velocity))
    trajectory = _get_test_trajectory(config)

    dt = 0.020
    t = 0.0
    duration = trajectory.totalTime()

    while t < duration:
        state = trajectory.sample(t)
        t += dt

        chassis_vel = ChassisVelocities(
            vx=state.velocity, vy=0, omega=state.velocity * state.curvature
        )
        wheel_vel = kinematics.toWheelVelocities(chassis_vel)

        assert wheel_vel.left < max_velocity + 0.05
        assert wheel_vel.right < max_velocity + 0.05
