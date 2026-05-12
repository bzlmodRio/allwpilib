import math
import numpy as np
import pytest

from wpimath import (
    LTVDifferentialDriveController,
    Models,
    Pose2d,
    Rotation2d,
    rkdp,
    TrajectoryConfig,
    TrajectoryGenerator,
    angle_modulus,
)

K_LINEAR_V = 3.02   # V / (m/s)
K_LINEAR_A = 0.642  # V / (m/s²)
K_ANGULAR_V = 1.382  # V / (m/s)
K_ANGULAR_A = 0.08495  # V / (m/s²)
K_TRACKWIDTH = 0.9  # m
K_DT = 0.020  # s
K_TOLERANCE = 1 / 12.0  # m
K_ANGULAR_TOLERANCE = 2.0 * math.pi / 180.0  # rad

_plant = Models.differential_drive_from_sys_id(
    K_LINEAR_V, K_LINEAR_A, K_ANGULAR_V, K_ANGULAR_A
)


def _dynamics(x, u):
    # x = [pos_x, pos_y, heading, left_vel, right_vel]
    v = (x[3, 0] + x[4, 0]) / 2.0
    xdot = np.zeros((5, 1))
    xdot[0, 0] = v * math.cos(x[2, 0])
    xdot[1, 0] = v * math.sin(x[2, 0])
    xdot[2, 0] = (x[4, 0] - x[3, 0]) / K_TRACKWIDTH
    vel_dot = _plant.A() @ x[3:5, :] + _plant.B() @ u
    xdot[3, 0] = vel_dot[0, 0]
    xdot[4, 0] = vel_dot[1, 0]
    return xdot


def test_reaches_reference():
    controller = LTVDifferentialDriveController(
        _plant,
        K_TRACKWIDTH,
        [0.0625, 0.125, 2.5, 0.95, 0.95],
        [12.0, 12.0],
        K_DT,
    )

    waypoints = [
        Pose2d(x=2.75, y=22.521, rotation=Rotation2d()),
        Pose2d(x=24.73, y=19.68, rotation=Rotation2d(5.846)),
    ]
    trajectory = TrajectoryGenerator.generate_trajectory(waypoints, TrajectoryConfig(8.8, 0.1))

    x = np.zeros((5, 1))
    x[0, 0] = 2.7
    x[1, 0] = 23.0
    x[2, 0] = 0.0

    robot_pose = Pose2d(x=x[0, 0], y=x[1, 0], rotation=Rotation2d(x[2, 0]))

    total_time = trajectory.duration()
    steps = int(total_time / K_DT)
    for i in range(steps):
        state = trajectory.sample_at(K_DT * i)
        robot_pose = Pose2d(x=x[0, 0], y=x[1, 0], rotation=Rotation2d(x[2, 0]))

        v_ref = state.forward_velocity()
        omega_ref = v_ref * state.curvature
        left_ref = v_ref - omega_ref * (K_TRACKWIDTH / 2)
        right_ref = v_ref + omega_ref * (K_TRACKWIDTH / 2)
        result = controller.calculate(
            robot_pose,
            x[3, 0],  # left velocity
            x[4, 0],  # right velocity
            state.pose,
            left_ref,
            right_ref,
        )
        left_voltage = result.left
        right_voltage = result.right

        u = np.array([[left_voltage], [right_voltage]])
        x = rkdp(_dynamics, x, u, K_DT)

    end_pose = trajectory.samples()[-1].pose
    assert end_pose.x == pytest.approx(robot_pose.x, abs=K_TOLERANCE)
    assert end_pose.y == pytest.approx(robot_pose.y, abs=K_TOLERANCE)
    assert angle_modulus(
        end_pose.rotation().radians() - robot_pose.rotation().radians()
    ) == pytest.approx(0, abs=K_ANGULAR_TOLERANCE)
