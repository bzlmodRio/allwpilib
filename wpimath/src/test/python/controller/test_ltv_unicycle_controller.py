import math
import pytest

from wpimath import (
    LTVUnicycleController,
    angleModulus,
    Pose2d,
    Rotation2d,
    TrajectoryConfig,
    TrajectoryGenerator,
    Twist2d,
)

K_TOLERANCE = 1 / 12.0  # meters
K_ANGULAR_TOLERANCE = 2.0 * math.pi / 180.0  # radians
K_DT = 0.020  # seconds


def test_reaches_reference():
    controller = LTVUnicycleController([0.0625, 0.125, 2.5], [4.0, 4.0], K_DT)
    robot_pose = Pose2d(x=2.7, y=23, rotation=Rotation2d())

    waypoints = [
        Pose2d(x=2.75, y=22.521, rotation=Rotation2d()),
        Pose2d(x=24.73, y=19.68, rotation=Rotation2d(5.846)),
    ]
    trajectory = TrajectoryGenerator.generateTrajectory(waypoints, TrajectoryConfig(8.8, 0.1))

    total_time = trajectory.totalTime()
    steps = int(total_time / K_DT)
    for i in range(steps):
        state = trajectory.sample(K_DT * i)
        result = controller.calculate(robot_pose, state)

        vx = result.vx
        omega = result.omega

        robot_pose = robot_pose + Twist2d(dx=vx * K_DT, dy=0, dtheta=omega * K_DT).exp()

    end_pose = trajectory.states()[-1].pose
    assert end_pose.x == pytest.approx(robot_pose.x, abs=K_TOLERANCE)
    assert end_pose.y == pytest.approx(robot_pose.y, abs=K_TOLERANCE)
    assert angleModulus(
        end_pose.rotation().radians() - robot_pose.rotation().radians()
    ) == pytest.approx(0, abs=K_ANGULAR_TOLERANCE)
