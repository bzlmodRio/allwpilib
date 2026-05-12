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
    max_centripetal_accel = 7 * 0.3048  # 7 fps² in m/s²

    config = TrajectoryConfig.from_fps(12, 12)
    config.add_constraint(CentripetalAccelerationConstraint(max_centripetal_accel))
    trajectory = _get_test_trajectory(config)

    dt = 0.020
    t = 0.0
    duration = trajectory.duration()

    while t < duration:
        state = trajectory.sample_at(t)
        t += dt

        centripetal_accel = state.forward_velocity() ** 2 * state.curvature
        assert centripetal_accel < max_centripetal_accel + 0.05
