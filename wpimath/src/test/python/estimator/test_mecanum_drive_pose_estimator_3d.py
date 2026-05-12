import math
import random
import pytest

from wpimath import (
    ChassisVelocities,
    MecanumDrivePoseEstimator3d,
    MecanumDriveKinematics,
    MecanumDriveWheelPositions,
    Pose2d,
    Pose3d,
    Rotation2d,
    Rotation3d,
    Transform2d,
    Translation2d,
    Translation3d,
    TrajectoryConfig,
    TrajectoryGenerator,
)

K_DT = 0.02
K_VISION_UPDATE_RATE = 0.1
K_VISION_UPDATE_DELAY = 0.25


def _make_trajectory():
    return TrajectoryGenerator.generate_trajectory(
        [
            Pose2d(x=0, y=0, rotation=Rotation2d.from_degrees(45)),
            Pose2d(x=3, y=0, rotation=Rotation2d.from_degrees(-90)),
            Pose2d(x=0, y=0, rotation=Rotation2d.from_degrees(135)),
            Pose2d(x=-3, y=0, rotation=Rotation2d.from_degrees(-90)),
            Pose2d(x=0, y=0, rotation=Rotation2d.from_degrees(45)),
        ],
        TrajectoryConfig(2.0, 2.0),
    )


def _test_follow_trajectory(
    kinematics,
    estimator,
    trajectory,
    chassis_velocities_generator,
    vision_measurement_generator,
    starting_pose,
    ending_pose,
    dt,
    k_vision_update_rate,
    k_vision_update_delay,
    check_error,
):
    random.seed(0)
    fl = fr = rl = rr = 0.0

    estimator.reset_position(Rotation3d(), MecanumDriveWheelPositions(), Pose3d(starting_pose))

    t = 0.0
    vision_poses = []
    max_error = -float("inf")
    error_sum = 0.0
    num_steps = 0
    initial_rotation = trajectory.samples()[0].pose.rotation()

    while t < trajectory.duration():
        ground_truth_state = trajectory.sample_at(t)

        if not vision_poses or vision_poses[-1][0] + k_vision_update_rate < t:
            raw_vision = vision_measurement_generator(ground_truth_state)
            noise = Transform2d(
                Translation2d(random.gauss(0, 0.1), random.gauss(0, 0.1)),
                Rotation2d(random.gauss(0, 0.05)),
            )
            vision_poses.append((t, raw_vision + noise))

        if vision_poses and vision_poses[0][0] + k_vision_update_delay < t:
            vision_entry = vision_poses.pop(0)
            estimator.add_vision_measurement(Pose3d(vision_entry[1]), vision_entry[0])

        chassis_velocities = chassis_velocities_generator(ground_truth_state)
        wheel_velocities = kinematics.to_wheel_velocities(chassis_velocities)

        fl += wheel_velocities.frontLeft * dt
        fr += wheel_velocities.frontRight * dt
        rl += wheel_velocities.rearLeft * dt
        rr += wheel_velocities.rearRight * dt
        wheel_positions = MecanumDriveWheelPositions(
            frontLeft=fl, frontRight=fr, rearLeft=rl, rearRight=rr
        )

        xhat = estimator.update_with_time(
            t,
            Rotation3d(
                ground_truth_state.pose.rotation()
                + Rotation2d(random.gauss(0, 0.05))
                - initial_rotation
            ),
            wheel_positions,
        )

        error = math.hypot(
            ground_truth_state.pose.x - xhat.x,
            ground_truth_state.pose.y - xhat.y,
        )
        max_error = max(max_error, error)
        error_sum += error
        num_steps += 1

        t += dt

    est = estimator.get_estimated_position()
    assert est.x == pytest.approx(ending_pose.x, abs=0.08)
    assert est.y == pytest.approx(ending_pose.y, abs=0.08)
    assert est.rotation().to_rotation2d().radians() == pytest.approx(
        ending_pose.rotation().radians(), abs=0.15
    )

    if check_error:
        assert error_sum / num_steps < 0.051
        assert max_error < 0.2


def _make_kinematics():
    return MecanumDriveKinematics(
        Translation2d(x=1, y=1),
        Translation2d(x=1, y=-1),
        Translation2d(x=-1, y=-1),
        Translation2d(x=-1, y=1),
    )


def test_accuracy():
    kinematics = _make_kinematics()
    estimator = MecanumDrivePoseEstimator3d(
        kinematics,
        Rotation3d(),
        MecanumDriveWheelPositions(),
        Pose3d(),
        [0.1, 0.1, 0.1, 0.1],
        [0.45, 0.45, 0.45, 0.45],
    )
    trajectory = _make_trajectory()
    initial_pose = trajectory.samples()[0].pose

    _test_follow_trajectory(
        kinematics,
        estimator,
        trajectory,
        lambda state: ChassisVelocities(
            vx=state.forward_velocity(), vy=0.0, omega=state.forward_velocity() * state.curvature
        ),
        lambda state: state.pose,
        initial_pose,
        Pose2d(x=0, y=0, rotation=Rotation2d.from_degrees(45)),
        K_DT,
        K_VISION_UPDATE_RATE,
        K_VISION_UPDATE_DELAY,
        True,
    )


def test_bad_initial_pose():
    kinematics = _make_kinematics()
    estimator = MecanumDrivePoseEstimator3d(
        kinematics,
        Rotation3d(),
        MecanumDriveWheelPositions(),
        Pose3d(),
        [0.1, 0.1, 0.1, 0.1],
        [0.45, 0.45, 0.45, 0.1],
    )
    trajectory = _make_trajectory()
    initial_pose = trajectory.samples()[0].pose
    ending_pose = Pose2d(x=0, y=0, rotation=Rotation2d.from_degrees(45))

    for direction_deg in range(0, 360, 45):
        for heading_deg in range(0, 360, 45):
            pose_offset = Rotation2d.from_degrees(direction_deg)
            heading_offset = Rotation2d.from_degrees(heading_deg)

            offset_initial = initial_pose + Transform2d(
                Translation2d(pose_offset.cos(), pose_offset.sin()), heading_offset
            )

            _test_follow_trajectory(
                kinematics,
                estimator,
                trajectory,
                lambda state: ChassisVelocities(
                    vx=state.forward_velocity(), vy=0.0, omega=state.forward_velocity() * state.curvature
                ),
                lambda state: state.pose,
                offset_initial,
                ending_pose,
                K_DT,
                K_VISION_UPDATE_RATE,
                K_VISION_UPDATE_DELAY,
                False,
            )


def test_simultaneous_vision_measurements():
    kinematics = _make_kinematics()
    estimator = MecanumDrivePoseEstimator3d(
        kinematics,
        Rotation3d(),
        MecanumDriveWheelPositions(),
        Pose3d(x=1, y=2, z=0, rotation=Rotation3d.from_degrees(0, 0, 270)),
        [0.1, 0.1, 0.1, 0.1],
        [0.45, 0.45, 0.45, 0.1],
    )

    estimator.update_with_time(0.0, Rotation3d(), MecanumDriveWheelPositions())

    for _ in range(1000):
        estimator.add_vision_measurement(
            Pose3d(x=0, y=0, z=0, rotation=Rotation3d.from_degrees(0, 0, 0)), 0.0
        )
        estimator.add_vision_measurement(
            Pose3d(x=3, y=1, z=0, rotation=Rotation3d.from_degrees(0, 0, 90)), 0.0
        )
        estimator.add_vision_measurement(
            Pose3d(x=2, y=4, z=0, rotation=Rotation3d.from_degrees(0, 0, 180)), 0.0
        )

    pose = estimator.get_estimated_position()

    assert not (abs(pose.x) < 0.08 and abs(pose.y) < 0.08)
    assert not (abs(pose.x - 3) < 0.08 and abs(pose.y - 1) < 0.08)
    assert not (abs(pose.x - 2) < 0.08 and abs(pose.y - 4) < 0.08)


def test_discard_stale_vision_measurements():
    kinematics = _make_kinematics()
    estimator = MecanumDrivePoseEstimator3d(
        kinematics,
        Rotation3d(),
        MecanumDriveWheelPositions(),
        Pose3d(),
        [0.1, 0.1, 0.1, 0.1],
        [0.45, 0.45, 0.45, 0.45],
    )

    t = 0.0
    while t < 4.0:
        estimator.update_with_time(t, Rotation3d(), MecanumDriveWheelPositions())
        t += 0.02

    odometry_pose = estimator.get_estimated_position()

    estimator.add_vision_measurement(
        Pose3d(x=10, y=10, z=0, rotation=Rotation3d(0, 0, 0.1)),
        1.0,
        [0.1, 0.1, 0.1, 0.1],
    )

    est = estimator.get_estimated_position()
    assert est.x == pytest.approx(odometry_pose.x, abs=1e-6)
    assert est.y == pytest.approx(odometry_pose.y, abs=1e-6)
    assert est.z == pytest.approx(odometry_pose.z, abs=1e-6)


def test_sample_at():
    kinematics = _make_kinematics()
    estimator = MecanumDrivePoseEstimator3d(
        kinematics,
        Rotation3d(),
        MecanumDriveWheelPositions(),
        Pose3d(),
        [1.0, 1.0, 1.0, 1.0],
        [1.0, 1.0, 1.0, 1.0],
    )

    assert estimator.sample_at(1.0) is None

    time = 1.0
    while time <= 2.0 + 1e-9:
        positions = MecanumDriveWheelPositions(
            frontLeft=time, frontRight=time, rearLeft=time, rearRight=time
        )
        estimator.update_with_time(time, Rotation3d(), positions)
        time += 0.02

    result = estimator.sample_at(1.02)
    assert result is not None
    assert result.x == pytest.approx(1.02, abs=1e-9)
    assert result.y == pytest.approx(0.0, abs=1e-9)

    assert estimator.sample_at(0.5).x == pytest.approx(1.0, abs=1e-9)
    assert estimator.sample_at(2.5).x == pytest.approx(2.0, abs=1e-9)

    estimator.add_vision_measurement(
        Pose3d(x=2, y=0, z=0, rotation=Rotation3d(0, 0, 1.0)), 2.2
    )

    assert estimator.sample_at(1.02).x == pytest.approx(1.02, abs=1e-9)

    estimator.add_vision_measurement(
        Pose3d(x=1, y=0.2, z=0, rotation=Rotation3d()), 0.9
    )

    assert estimator.sample_at(1.02).y == pytest.approx(0.1, abs=1e-9)
    assert estimator.sample_at(0.5).y == pytest.approx(0.1, abs=1e-9)
    assert estimator.sample_at(2.5).y == pytest.approx(0.1, abs=1e-9)


def test_reset():
    kinematics = _make_kinematics()
    estimator = MecanumDrivePoseEstimator3d(
        kinematics,
        Rotation3d(),
        MecanumDriveWheelPositions(),
        Pose3d(x=-1, y=-1, z=0, rotation=Rotation3d(0, 0, 1.0)),
        [1.0, 1.0, 1.0, 1.0],
        [1.0, 1.0, 1.0, 1.0],
    )

    assert estimator.get_estimated_position().x == pytest.approx(-1.0)
    assert estimator.get_estimated_position().y == pytest.approx(-1.0)
    assert estimator.get_estimated_position().rotation().z == pytest.approx(1.0)

    estimator.reset_position(
        Rotation3d(),
        MecanumDriveWheelPositions(frontLeft=1, frontRight=1, rearLeft=1, rearRight=1),
        Pose3d(x=1, y=0, z=0, rotation=Rotation3d()),
    )

    assert estimator.get_estimated_position().x == pytest.approx(1.0)
    assert estimator.get_estimated_position().y == pytest.approx(0.0)

    estimator.update(
        Rotation3d(),
        MecanumDriveWheelPositions(frontLeft=2, frontRight=2, rearLeft=2, rearRight=2),
    )

    assert estimator.get_estimated_position().x == pytest.approx(2.0)

    estimator.reset_rotation(Rotation3d.from_degrees(0, 0, 90))

    assert estimator.get_estimated_position().rotation().z == pytest.approx(math.pi / 2)

    estimator.update(
        Rotation3d(),
        MecanumDriveWheelPositions(frontLeft=3, frontRight=3, rearLeft=3, rearRight=3),
    )

    assert estimator.get_estimated_position().x == pytest.approx(2.0)
    assert estimator.get_estimated_position().y == pytest.approx(1.0)

    estimator.reset_translation(Translation3d(x=-1, y=-1, z=-1))

    assert estimator.get_estimated_position().x == pytest.approx(-1.0)
    assert estimator.get_estimated_position().y == pytest.approx(-1.0)

    estimator.reset_pose(Pose3d())

    assert estimator.get_estimated_position().x == pytest.approx(0.0)
    assert estimator.get_estimated_position().y == pytest.approx(0.0)
    assert estimator.get_estimated_position().rotation().z == pytest.approx(0.0)
