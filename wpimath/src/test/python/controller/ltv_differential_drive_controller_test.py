import pytest
import numpy as np
import math
from wpimath import Models, LTVDifferentialDriveController, Pose2d, Rotation2d, TrajectoryConfig, TrajectoryGenerator, RKDP, angleModulus

# Constants
KLV, KLA = 3.02, 0.642
KAV, KAA = 1.382, 0.08495
TRACKWIDTH = 0.9
PLANT = Models.differentialDriveFromSysId(KLV, KLA, KAV, KAA)

def dynamics(x, u):
    # x = [x, y, heading, v_left, v_right]
    v = (x[3] + x[4]) / 2.0
    xdot = np.zeros(5)
    xdot[0] = v[0] * math.cos(x[2][0])
    xdot[1] = v[0] * math.sin(x[2][0])
    xdot[2] = (x[4][0] - x[3][0]) / TRACKWIDTH

    motor_dynamics = PLANT.A() @ x[3:5] + PLANT.B() @ u
    xdot[3] = motor_dynamics[0][0]
    xdot[4] = motor_dynamics[1][0]
    return xdot

def test_reaches_reference():
    dt = 0.020
    # Costs: [x, y, heading, v_l, v_r], [u_l, u_r]
    controller = LTVDifferentialDriveController(
        PLANT, TRACKWIDTH, [0.0625, 0.125, 2.5, 0.95, 0.95], [12.0, 12.0], dt
    )
    
    start_pose = Pose2d(2.7, 23.0, Rotation2d(0))
    waypoints = [Pose2d(2.75, 22.521, 0), Pose2d(24.73, 19.68, 5.846)]
    config = TrajectoryConfig(8.8, 0.1)
    trajectory = TrajectoryGenerator.generateTrajectory(waypoints, config)
    
    x = np.zeros(5)
    x[0], x[1], x[2] = start_pose.X(), start_pose.Y(), start_pose.rotation().radians()
    
    total_time = trajectory.totalTime()
    for i in range(int(total_time / dt)):
        state = trajectory.sample(dt * i)
        robot_pose = Pose2d(x[0], x[1], Rotation2d(x[2]))
        
        voltages = controller.calculate(robot_pose, x[3], x[4], state)
        u_l, u_r = voltages.left, voltages.right
        x = RKDP(dynamics, x, [u_l, u_r], dt)[:, 0]

    end_state = trajectory.states()[-1].pose
    assert end_state.X() == pytest.approx(x[0], abs=1/12.0)
    assert end_state.Y() == pytest.approx(x[1], abs=1/12.0)
    error_angle = angleModulus(end_state.rotation().radians() - x[2])
    assert abs(error_angle) <= math.radians(2.0)