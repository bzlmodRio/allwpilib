import pytest
from wpimath.geometry import Pose3d, Transform3d, Translation3d, Rotation3d
from wpimath.units import meters, degrees
from wpimath import objectToRobotPose


def test_object_to_robot_pose():
    robot = Pose3d(
        meters(1), meters(2), meters(0), Rotation3d(degrees(0), degrees(0), degrees(30))
    )
    camera_to_object = Transform3d(
        Translation3d(meters(1), meters(1), meters(1)),
        Rotation3d(degrees(0), degrees(-20), degrees(45)),
    )
    robot_to_camera = Transform3d(
        Translation3d(meters(1), meters(0), meters(2)),
        Rotation3d(degrees(0), degrees(0), degrees(25)),
    )

    object_pose = robot + robot_to_camera + camera_to_object

    assert objectToRobotPose(object_pose, camera_to_object, robot_to_camera) == pytest.approx(robot)