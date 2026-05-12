import math
import pytest

from wpimath import (
    Pose2d,
    Rotation2d,
    TrajectoryConfig,
    TrajectoryGenerator,
    Transform2d,
    Translation2d,
)


def _generate_simple_trajectory():
    config = TrajectoryConfig(3, 3)
    return TrajectoryGenerator.generateTrajectory(
        Pose2d(), [], Pose2d(x=1, y=1, rotation=Rotation2d.fromDegrees(90)), config
    )


def _assert_same_shaped(states_a, states_b):
    for i in range(len(states_a) - 1):
        a1 = states_a[i].pose
        a2 = states_a[i + 1].pose
        b1 = states_b[i].pose
        b2 = states_b[i + 1].pose

        a = a2.relativeTo(a1)
        b = b2.relativeTo(b1)

        assert a.x == pytest.approx(b.x, abs=1e-9)
        assert a.y == pytest.approx(b.y, abs=1e-9)
        assert a.rotation().radians() == pytest.approx(b.rotation().radians(), abs=1e-9)


def test_transform_by():
    trajectory = _generate_simple_trajectory()
    transformed = trajectory.transformBy(
        Transform2d(Translation2d(1, 2), Rotation2d.fromDegrees(30))
    )

    first_pose = transformed.sample(0).pose
    assert first_pose.x == pytest.approx(1.0, abs=1e-9)
    assert first_pose.y == pytest.approx(2.0, abs=1e-9)
    assert first_pose.rotation().degrees() == pytest.approx(30.0, abs=1e-9)

    _assert_same_shaped(trajectory.states(), transformed.states())


def test_relative_to():
    config = TrajectoryConfig(3, 3)
    trajectory = TrajectoryGenerator.generateTrajectory(
        Pose2d(x=1, y=2, rotation=Rotation2d.fromDegrees(30)),
        [],
        Pose2d(x=5, y=7, rotation=Rotation2d.fromDegrees(90)),
        config,
    )

    transformed = trajectory.relativeTo(Pose2d(x=1, y=2, rotation=Rotation2d.fromDegrees(30)))

    first_pose = transformed.sample(0).pose
    assert first_pose.x == pytest.approx(0, abs=1e-9)
    assert first_pose.y == pytest.approx(0, abs=1e-9)
    assert first_pose.rotation().degrees() == pytest.approx(0, abs=1e-9)

    _assert_same_shaped(trajectory.states(), transformed.states())
