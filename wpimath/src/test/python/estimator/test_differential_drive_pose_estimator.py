import pytest
import math
import random
from typing import Callable, List, Tuple
from wpimath.kinematics import DifferentialDriveKinematics, ChassisSpeeds, DifferentialDriveWheelSpeeds
from wpimath.trajectory import TrajectoryGenerator, TrajectoryConfig, Trajectory
from wpimath.geometry import (
    Translation2d,
    Rotation2d,
    Pose2d,
    Pose3d,
    Rotation3d,
    Transform2d,
    Translation3d,
)
from wpimath.estimator import DifferentialDrivePoseEstimator3d
from wpimath.units import (
    meters,
    radians,
    seconds,
    meters_per_second,
    meters_per_second_squared,
)
import numpy as np


def run_test_follow_trajectory(
    kinematics: DifferentialDriveKinematics,
    estimator: DifferentialDrivePoseEstimator3d,
    trajectory: Trajectory,
    chassis_speeds_generator: Callable[[Trajectory.State], ChassisSpeeds],
    vision_measurement_generator: Callable[[Trajectory.State], Pose2d],
    starting_pose: Pose2d,
    ending_pose: Pose2d,
    dt: float,
    k_vision_update_rate: float,
    k_vision_update_delay: float,
    check_error: bool,
    debug: bool,
):
    left_distance = meters(0)
    right_distance = meters(0)

    estimator.resetPosition(Rotation3d(), left_distance, right_distance, Pose3d(starting_pose))

    vision_poses: List[Tuple[float, Pose2d]] = []
    vision_log: List[Tuple[float, float, Pose2d]] = []

    max_error = -float("inf")
    error_sum = 0.0

    if debug:
        print(
            "time, est_x, est_y, est_theta, true_x, true_y, true_theta, left, right"
        )

    t = seconds(0)
    while t < trajectory.totalTime():
        ground_truth_state = trajectory.sample(t)

        if not vision_poses or (vision_poses[-1][0] + k_vision_update_rate) < t:
            vision_pose = vision_measurement_generator(ground_truth_state) + Transform2d(
                Translation2d(
                    meters(random.normalvariate(0.0, 1.0) * 0.1),
                    meters(random.normalvariate(0.0, 1.0) * 0.1),
                ),
                Rotation2d(radians(random.normalvariate(0.0, 1.0) * 0.05)),
            )
            vision_poses.append((t, vision_pose))

        if vision_poses and (vision_poses[0][0] + k_vision_update_delay) < t:
            vision_entry = vision_poses.pop(0)
            estimator.addVisionMeasurement(Pose3d(vision_entry[1]), vision_entry[0])
            vision_log.append((t, vision_entry[0], vision_entry[1]))

        chassis_speeds = chassis_speeds_generator(ground_truth_state)
        wheel_speeds = kinematics.toWheelSpeeds(chassis_speeds)

        left_distance += wheel_speeds.left * dt
        right_distance += wheel_speeds.right * dt

        xhat = estimator.updateWithTime(
            t,
            Rotation3d(
                ground_truth_state.pose.rotation()
                + Rotation2d(radians(random.normalvariate(0.0, 1.0) * 0.05))
                - trajectory.initialPose().rotation()
            ),
            left_distance,
            right_distance,
        )

        if debug:
            print(
                f"{t}, {xhat.x}, {xhat.y}, {xhat.rotation().toRotation2d().radians()}, "
                f"{ground_truth_state.pose.x}, {ground_truth_state.pose.y}, {ground_truth_state.pose.rotation().radians()}, "
                f"{left_distance}, {right_distance}"
            )

        error = ground_truth_state.pose.translation().distance(
            xhat.translation().toTranslation2d()
        )

        if error > max_error:
            max_error = error
        error_sum += error

        t += dt

    if debug:
        print("apply_time, measured_time, vision_x, vision_y, vision_theta")
        for apply_time, measure_time, vision_pose in vision_log:
            print(
                f"{apply_time}, {measure_time}, {vision_pose.x}, "
                f"{vision_pose.y}, {vision_pose.rotation().radians()}"
            )

    # TODO
    # assert ending_pose.x == pytest.approx(estimator.getEstimatedPosition().x, abs=0.08)
    # assert ending_pose.y == pytest.approx(estimator.getEstimatedPosition().y, abs=0.08)
    # assert ending_pose.rotation().radians() == pytest.approx(
    #     estimator.getEstimatedPosition().rotation().toRotation2d().radians(), abs=0.15
    # )

    if check_error:
        assert error_sum / (trajectory.totalTime() / dt) < 0.05
        assert max_error < 0.2


def test_accuracy():
    kinematics = DifferentialDriveKinematics(meters(1.0))
    estimator = DifferentialDrivePoseEstimator3d(
        kinematics,
        Rotation3d(),
        meters(0),
        meters(0),
        Pose3d(),
        np.array([0.02, 0.02, 0.02, 0.01]),
        np.array([0.1, 0.1, 0.1, 0.1]),
    )
    trajectory = TrajectoryGenerator.generateTrajectory(
        [
            Pose2d(meters(0), meters(0), Rotation2d.fromDegrees(45)),
            Pose2d(meters(3), meters(0), Rotation2d.fromDegrees(-90)),
            Pose2d(meters(0), meters(0), Rotation2d.fromDegrees(135)),
            Pose2d(meters(-3), meters(0), Rotation2d.fromDegrees(-90)),
            Pose2d(meters(0), meters(0), Rotation2d.fromDegrees(45)),
        ],
        TrajectoryConfig(meters_per_second(2), meters_per_second_squared(2)),
    )

    run_test_follow_trajectory(
        kinematics,
        estimator,
        trajectory,
        lambda state: ChassisSpeeds(
            state.velocity,
            meters_per_second(0),
            state.velocity * state.curvature,
        ),
        lambda state: state.pose,
        trajectory.initialPose(),
        Pose2d(meters(0), meters(0), Rotation2d.fromDegrees(45)),
        seconds(0.02),
        seconds(0.1),
        seconds(0.25),
        True,
        False,
    )


def test_bad_initial_pose():
    kinematics = DifferentialDriveKinematics(meters(1.0))
    estimator = DifferentialDrivePoseEstimator3d(
        kinematics,
        Rotation3d(),
        meters(0),
        meters(0),
        Pose3d(),
        np.array([0.02, 0.02, 0.02, 0.01]),
        np.array([0.1, 0.1, 0.1, 0.1]),
    )
    trajectory = TrajectoryGenerator.generateTrajectory(
        [
            Pose2d(meters(0), meters(0), Rotation2d.fromDegrees(45)),
            Pose2d(meters(3), meters(0), Rotation2d.fromDegrees(-90)),
            Pose2d(meters(0), meters(0), Rotation2d.fromDegrees(135)),
            Pose2d(meters(-3), meters(0), Rotation2d.fromDegrees(-90)),
            Pose2d(meters(0), meters(0), Rotation2d.fromDegrees(45)),
        ],
        TrajectoryConfig(meters_per_second(2), meters_per_second_squared(2)),
    )

    for offset_direction_degs in range(0, 360, 45):
        for offset_heading_degs in range(0, 360, 45):
            pose_offset = Rotation2d.fromDegrees(offset_direction_degs)
            heading_offset = Rotation2d.fromDegrees(offset_heading_degs)
            initial_pose = trajectory.initialPose() + Transform2d(
                Translation2d(
                    meters(pose_offset.cos() * 1), meters(pose_offset.sin() * 1)
                ),
                heading_offset,
            )
            run_test_follow_trajectory(
                kinematics,
                estimator,
                trajectory,
                lambda state: ChassisSpeeds(
                    state.velocity, meters_per_second(0), state.velocity * state.curvature
                ),
                lambda state: state.pose,
                initial_pose,
                Pose2d(meters(0), meters(0), Rotation2d.fromDegrees(45)),
                seconds(0.02),
                seconds(0.1),
                seconds(0.25),
                False,
                False,
            )


def test_simultaneous_vision_measurements():
    kinematics = DifferentialDriveKinematics(meters(1.0))
    estimator = DifferentialDrivePoseEstimator3d(
        kinematics,
        Rotation3d(),
        meters(0),
        meters(0),
        Pose3d(meters(1), meters(2), meters(0), Rotation3d.fromDegrees(0, 0, 270)),
        np.array([0.02, 0.02, 0.02, 0.01]),
        np.array([0.1, 0.1, 0.1, 0.1]),
    )

    estimator.updateWithTime(seconds(0), Rotation3d(), meters(0), meters(0))

    for _ in range(1000):
        estimator.addVisionMeasurement(Pose3d(meters(0), meters(0), meters(0), Rotation3d.fromDegrees(0, 0, 0)), seconds(0))
        estimator.addVisionMeasurement(Pose3d(meters(3), meters(1), meters(0), Rotation3d.fromDegrees(0, 0, 90)), seconds(0))
        estimator.addVisionMeasurement(Pose3d(meters(2), meters(4), meters(0), Rotation3d.fromDegrees(0, 0, 180)), seconds(0))

    dx_1 = abs(estimator.getEstimatedPosition().x - meters(0))
    dy_1 = abs(estimator.getEstimatedPosition().y - meters(0))
    dtheta_1 = abs(
        estimator.getEstimatedPosition().rotation().toRotation2d().radians() - radians(0)
    )

    assert dx_1 > 0.08 or dy_1 > 0.08 or dtheta_1 > 0.08

    dx_2 = abs(estimator.getEstimatedPosition().x - meters(3))
    dy_2 = abs(estimator.getEstimatedPosition().y - meters(1))
    dtheta_2 = abs(
        estimator.getEstimatedPosition().rotation().toRotation2d().radians() - math.radians(90)
    )

    assert dx_2 > 0.08 or dy_2 > 0.08 or dtheta_2 > 0.08

    dx_3 = abs(estimator.getEstimatedPosition().x - meters(2))
    dy_3 = abs(estimator.getEstimatedPosition().y - meters(4))
    dtheta_3 = abs(
        estimator.getEstimatedPosition().rotation().toRotation2d().radians() - math.radians(180)
    )

    assert dx_3 > 0.08 or dy_3 > 0.08 or dtheta_3 > 0.08


# TODO
# def test_discard_stale_vision_measurements():
#     kinematics = DifferentialDriveKinematics(meters(1))
#     estimator = DifferentialDrivePoseEstimator3d(
#         kinematics,
#         Rotation3d(),
#         meters(0),
#         meters(0),
#         Pose3d(),
#         np.array([0.1, 0.1, 0.1, 0.1]),
#         np.array([0.45, 0.45, 0.45, 0.45]),
#     )

#     for time in np.arange(0, 4, 0.02):
#         estimator.updateWithTime(seconds(time), Rotation3d(), meters(0), meters(0))

#     odometry_pose = estimator.getEstimatedPosition()

#     estimator.addVisionMeasurement(
#         Pose3d(meters(10), meters(10), meters(0), Rotation3d(0, 0, radians(0.1))),
#         seconds(1),
#         np.array([0.1, 0.1, 0.1, 0.1]),
#     )

#     estimated_pose = estimator.getEstimatedPosition()
#     assert estimated_pose.x == pytest.approx(odometry_pose.x, abs=1e-6)
#     assert estimated_pose.y == pytest.approx(odometry_pose.y, abs=1e-6)
#     assert estimated_pose.z == pytest.approx(odometry_pose.z, abs=1e-6)
#     assert estimated_pose.rotation().x == pytest.approx(odometry_pose.rotation().x, abs=1e-6)
#     assert estimated_pose.rotation().y == pytest.approx(odometry_pose.rotation().y, abs=1e-6)
#     assert estimated_pose.rotation().z == pytest.approx(odometry_pose.rotation().z, abs=1e-6)


def test_sample_at():
    kinematics = DifferentialDriveKinematics(meters(1))
    estimator = DifferentialDrivePoseEstimator3d(
        kinematics,
        Rotation3d(),
        meters(0),
        meters(0),
        Pose3d(),
        np.array([1.0, 1.0, 1.0, 1.0]),
        np.array([1.0, 1.0, 1.0, 1.0]),
    )

    assert estimator.sampleAt(seconds(1)) is None

    for time in np.arange(1, 2 + 1e-9, 0.02):
        estimator.updateWithTime(
            seconds(time), Rotation3d(), meters(time), meters(time)
        )

    assert estimator.sampleAt(seconds(1.02)) == Pose3d(meters(1.02), meters(0), meters(0), Rotation3d())
    assert estimator.sampleAt(seconds(1.01)) == Pose3d(meters(1.01), meters(0), meters(0), Rotation3d())
    assert estimator.sampleAt(seconds(0.5)) == Pose3d(meters(1), meters(0), meters(0), Rotation3d())
    assert estimator.sampleAt(seconds(2.5)) == Pose3d(meters(2), meters(0), meters(0), Rotation3d())

    estimator.addVisionMeasurement(
        Pose3d(meters(2), meters(0), meters(0), Rotation3d(0, 0, radians(1))), seconds(2.2)
    )

    assert estimator.sampleAt(seconds(1.02)) == Pose3d(meters(1.02), meters(0), meters(0), Rotation3d())
    assert estimator.sampleAt(seconds(1.01)) == Pose3d(meters(1.01), meters(0), meters(0), Rotation3d())
    assert estimator.sampleAt(seconds(0.5)) == Pose3d(meters(1), meters(0), meters(0), Rotation3d())
    
    estimator.addVisionMeasurement(
        Pose3d(meters(1), meters(0.2), meters(0), Rotation3d()), seconds(0.9)
    )

    assert estimator.sampleAt(seconds(1.02)) == Pose3d(meters(1.02), meters(0.1), meters(0), Rotation3d())
    assert estimator.sampleAt(seconds(1.01)) == Pose3d(meters(1.01), meters(0.1), meters(0), Rotation3d())
    assert estimator.sampleAt(seconds(0.5)) == Pose3d(meters(1), meters(0.1), meters(0), Rotation3d())
    assert estimator.sampleAt(seconds(2.5)) == Pose3d(meters(2), meters(0.1), meters(0), Rotation3d())


def test_reset():
    kinematics = DifferentialDriveKinematics(meters(1))
    estimator = DifferentialDrivePoseEstimator3d(
        kinematics,
        Rotation3d(),
        meters(0),
        meters(0),
        Pose3d(meters(-1), meters(-1), meters(-1), Rotation3d(0.0, 0.0, 1.0)),
        np.array([1.0, 1.0, 1.0, 1.0]),
        np.array([1.0, 1.0, 1.0, 1.0]),
    )

    assert estimator.getEstimatedPosition().x == pytest.approx(-1.0)
    assert estimator.getEstimatedPosition().y == pytest.approx(-1.0)
    assert estimator.getEstimatedPosition().z == pytest.approx(-1.0)
    assert estimator.getEstimatedPosition().rotation().x == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().y == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().z == pytest.approx(1.0)

    estimator.resetPosition(Rotation3d(), meters(1), meters(1), Pose3d(meters(1), meters(0), meters(0), Rotation3d()))

    assert estimator.getEstimatedPosition().x == pytest.approx(1.0)
    assert estimator.getEstimatedPosition().y == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().z == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().x == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().y == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().z == pytest.approx(0.0)

    estimator.update(Rotation3d(), meters(2), meters(2))

    assert estimator.getEstimatedPosition().x == pytest.approx(2.0)
    assert estimator.getEstimatedPosition().y == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().z == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().x == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().y == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().z == pytest.approx(0.0)

    estimator.resetRotation(Rotation3d.fromDegrees(0, 0, 90))

    assert estimator.getEstimatedPosition().x == pytest.approx(2.0)
    assert estimator.getEstimatedPosition().y == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().z == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().x == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().y == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().z == pytest.approx(math.pi / 2)

    estimator.update(Rotation3d(), meters(3), meters(3))

    assert estimator.getEstimatedPosition().x == pytest.approx(2.0)
    assert estimator.getEstimatedPosition().y == pytest.approx(1.0)
    assert estimator.getEstimatedPosition().z == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().x == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().y == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().z == pytest.approx(math.pi / 2)

    estimator.resetTranslation(Translation3d(meters(-1), meters(-1), meters(-1)))

    assert estimator.getEstimatedPosition().x == pytest.approx(-1.0)
    assert estimator.getEstimatedPosition().y == pytest.approx(-1.0)
    assert estimator.getEstimatedPosition().z == pytest.approx(-1.0)
    assert estimator.getEstimatedPosition().rotation().x == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().y == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().z == pytest.approx(math.pi / 2)

    estimator.resetPose(Pose3d())

    assert estimator.getEstimatedPosition().x == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().y == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().z == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().x == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().y == pytest.approx(0.0)
    assert estimator.getEstimatedPosition().rotation().z == pytest.approx(0.0)