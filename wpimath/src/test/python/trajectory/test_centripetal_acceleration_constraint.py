import math

from wpimath import (
    CentripetalAccelerationConstraint,
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
    max_centripetal_accel = 7 * 0.3048  # 7 fps² in m/s²

    config = TrajectoryConfig.fromFps(12, 12)
    config.addConstraint(CentripetalAccelerationConstraint(max_centripetal_accel))
    trajectory = _get_test_trajectory(config)

    dt = 0.020
    t = 0.0
    duration = trajectory.totalTime()

    while t < duration:
        state = trajectory.sample(t)
        t += dt

        centripetal_accel = state.velocity ** 2 * state.curvature
        assert centripetal_accel < max_centripetal_accel + 0.05
