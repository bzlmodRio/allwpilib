import pytest
import math

from wpimath.trajectory import TrajectoryGenerator, TrajectoryConfig
from wpimath.geometry import Pose2d, Rotation2d, Translation2d, Transform2d
from wpimath.units import meters, meters_per_second, meters_per_second_squared, seconds
import trajectory_generator


def assert_same_shaped_trajectory(states_a, states_b):
    """
    Helper function to check if two trajectories have the same shape.
    This is done by comparing the relative poses between consecutive states.
    """
    assert len(states_a) == len(states_b)
    
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
    config = TrajectoryConfig(meters_per_second(3), meters_per_second_squared(3))
    
    trajectory = TrajectoryGenerator.generateTrajectory(
        Pose2d(), [], Pose2d(meters(1), meters(1), Rotation2d.fromDegrees(90)), config
    )
    
    transform = Transform2d(Translation2d(meters(1), meters(2)), Rotation2d.fromDegrees(30))
    transformed_trajectory = trajectory.transformBy(transform)
    
    first_pose = transformed_trajectory.sample(seconds(0)).pose
    
    assert first_pose.x == pytest.approx(1.0, abs=1e-9)
    assert first_pose.y == pytest.approx(2.0, abs=1e-9)
    assert first_pose.rotation().degrees() == pytest.approx(30.0, abs=1e-9)
    
    assert_same_shaped_trajectory(trajectory.states(), transformed_trajectory.states())


def test_relative_to():
    config = TrajectoryConfig(meters_per_second(3), meters_per_second_squared(3))
    
    trajectory = TrajectoryGenerator.generateTrajectory(
        Pose2d(meters(1), meters(2), Rotation2d.fromDegrees(30)),
        [],
        Pose2d(meters(5), meters(7), Rotation2d.fromDegrees(90)),
        config
    )
    
    transformed_trajectory = trajectory.relativeTo(
        Pose2d(meters(1), meters(2), Rotation2d.fromDegrees(30))
    )

    first_pose = transformed_trajectory.sample(seconds(0)).pose

    assert first_pose.x == pytest.approx(0.0, abs=1e-9)
    assert first_pose.y == pytest.approx(0.0, abs=1e-9)
    assert first_pose.rotation().degrees() == pytest.approx(0.0, abs=1e-9)
    
    assert_same_shaped_trajectory(trajectory.states(), transformed_trajectory.states())