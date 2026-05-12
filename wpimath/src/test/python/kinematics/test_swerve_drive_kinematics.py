import pytest
import math

from wpimath import (
    ChassisAccelerations,
    ChassisVelocities,
    Rotation2d,
    SwerveModuleAcceleration,
    SwerveModulePosition,
    SwerveModuleVelocity,
    SwerveDrive4Kinematics,
    Translation2d,
)

kEpsilon = 0.1


@pytest.fixture
def kinematics_test():
    class SwerveDriveKinematicsTest:
        def __init__(self):
            self.m_fl = Translation2d(x=12, y=12)
            self.m_fr = Translation2d(x=12, y=-12)
            self.m_bl = Translation2d(x=-12, y=12)
            self.m_br = Translation2d(x=-12, y=-12)
            self.m_kinematics = SwerveDrive4Kinematics(
                self.m_fl, self.m_fr, self.m_bl, self.m_br
            )

    return SwerveDriveKinematicsTest()


def test_straight_line_inverse_kinematics(kinematics_test):
    velocities = ChassisVelocities(vx=5.0, vy=0.0, omega=0.0)
    states = kinematics_test.m_kinematics.toSwerveModuleVelocities(velocities)

    fl, fr, bl, br = states

    assert fl.velocity == pytest.approx(5.0, abs=kEpsilon)
    assert fr.velocity == pytest.approx(5.0, abs=kEpsilon)
    assert bl.velocity == pytest.approx(5.0, abs=kEpsilon)
    assert br.velocity == pytest.approx(5.0, abs=kEpsilon)

    assert fl.angle.radians() == pytest.approx(0.0, abs=kEpsilon)
    assert fr.angle.radians() == pytest.approx(0.0, abs=kEpsilon)
    assert bl.angle.radians() == pytest.approx(0.0, abs=kEpsilon)
    assert br.angle.radians() == pytest.approx(0.0, abs=kEpsilon)


def test_straight_line_forward_kinematics(kinematics_test):
    state = SwerveModuleVelocity(velocity=5.0, angle=Rotation2d.fromDegrees(0))
    chassis_velocities = kinematics_test.m_kinematics.toChassisVelocities(
        (state, state, state, state)
    )

    assert chassis_velocities.vx == pytest.approx(5.0, abs=kEpsilon)
    assert chassis_velocities.vy == pytest.approx(0.0, abs=kEpsilon)
    assert chassis_velocities.omega == pytest.approx(0.0, abs=kEpsilon)


def test_straight_line_forward_kinematics_with_deltas(kinematics_test):
    delta = SwerveModulePosition(distance=5.0, angle=Rotation2d.fromDegrees(0))
    twist = kinematics_test.m_kinematics.toTwist2d((delta, delta, delta, delta))

    assert twist.dx == pytest.approx(5.0, abs=kEpsilon)
    assert twist.dy == pytest.approx(0.0, abs=kEpsilon)
    assert twist.dtheta == pytest.approx(0.0, abs=kEpsilon)


def test_straight_strafe_inverse_kinematics(kinematics_test):
    velocities = ChassisVelocities(vx=0, vy=5, omega=0)
    states = kinematics_test.m_kinematics.toSwerveModuleVelocities(velocities)

    fl, fr, bl, br = states

    assert fl.velocity == pytest.approx(5.0, abs=kEpsilon)
    assert fr.velocity == pytest.approx(5.0, abs=kEpsilon)
    assert bl.velocity == pytest.approx(5.0, abs=kEpsilon)
    assert br.velocity == pytest.approx(5.0, abs=kEpsilon)

    assert fl.angle.degrees() == pytest.approx(90.0, abs=kEpsilon)
    assert fr.angle.degrees() == pytest.approx(90.0, abs=kEpsilon)
    assert bl.angle.degrees() == pytest.approx(90.0, abs=kEpsilon)
    assert br.angle.degrees() == pytest.approx(90.0, abs=kEpsilon)


def test_straight_strafe_forward_kinematics(kinematics_test):
    state = SwerveModuleVelocity(velocity=5, angle=Rotation2d.fromDegrees(90))
    chassis_velocities = kinematics_test.m_kinematics.toChassisVelocities(
        (state, state, state, state)
    )

    assert chassis_velocities.vx == pytest.approx(0.0, abs=kEpsilon)
    assert chassis_velocities.vy == pytest.approx(5.0, abs=kEpsilon)
    assert chassis_velocities.omega == pytest.approx(0.0, abs=kEpsilon)


def test_straight_strafe_forward_kinematics_with_deltas(kinematics_test):
    delta = SwerveModulePosition(distance=5, angle=Rotation2d.fromDegrees(90))
    twist = kinematics_test.m_kinematics.toTwist2d((delta, delta, delta, delta))

    assert twist.dx == pytest.approx(0.0, abs=kEpsilon)
    assert twist.dy == pytest.approx(5.0, abs=kEpsilon)
    assert twist.dtheta == pytest.approx(0.0, abs=kEpsilon)


def test_turn_in_place_inverse_kinematics(kinematics_test):
    velocities = ChassisVelocities(vx=0, vy=0, omega=2 * math.pi)
    states = kinematics_test.m_kinematics.toSwerveModuleVelocities(velocities)

    fl, fr, bl, br = states

    assert fl.velocity == pytest.approx(106.63, abs=kEpsilon)
    assert fr.velocity == pytest.approx(106.63, abs=kEpsilon)
    assert bl.velocity == pytest.approx(106.63, abs=kEpsilon)
    assert br.velocity == pytest.approx(106.63, abs=kEpsilon)

    assert fl.angle.degrees() == pytest.approx(135.0, abs=kEpsilon)
    assert fr.angle.degrees() == pytest.approx(45.0, abs=kEpsilon)
    assert bl.angle.degrees() == pytest.approx(-135.0, abs=kEpsilon)
    assert br.angle.degrees() == pytest.approx(-45.0, abs=kEpsilon)


def test_conserve_wheel_angle(kinematics_test):
    velocities = ChassisVelocities(vx=0, vy=0, omega=2 * math.pi)
    kinematics_test.m_kinematics.toSwerveModuleVelocities(velocities)
    states = kinematics_test.m_kinematics.toSwerveModuleVelocities(ChassisVelocities())

    fl, fr, bl, br = states

    assert fl.velocity == pytest.approx(0.0, abs=kEpsilon)
    assert fr.velocity == pytest.approx(0.0, abs=kEpsilon)
    assert bl.velocity == pytest.approx(0.0, abs=kEpsilon)
    assert br.velocity == pytest.approx(0.0, abs=kEpsilon)

    assert fl.angle.degrees() == pytest.approx(135.0, abs=kEpsilon)
    assert fr.angle.degrees() == pytest.approx(45.0, abs=kEpsilon)
    assert bl.angle.degrees() == pytest.approx(-135.0, abs=kEpsilon)
    assert br.angle.degrees() == pytest.approx(-45.0, abs=kEpsilon)


def test_reset_wheel_angle(kinematics_test):
    fl_angle = Rotation2d.fromDegrees(0)
    fr_angle = Rotation2d.fromDegrees(90)
    bl_angle = Rotation2d.fromDegrees(180)
    br_angle = Rotation2d.fromDegrees(270)
    kinematics_test.m_kinematics.resetHeadings((fl_angle, fr_angle, bl_angle, br_angle))
    states = kinematics_test.m_kinematics.toSwerveModuleVelocities(ChassisVelocities())

    fl_mod, fr_mod, bl_mod, br_mod = states

    assert fl_mod.velocity == pytest.approx(0.0, abs=kEpsilon)
    assert fr_mod.velocity == pytest.approx(0.0, abs=kEpsilon)
    assert bl_mod.velocity == pytest.approx(0.0, abs=kEpsilon)
    assert br_mod.velocity == pytest.approx(0.0, abs=kEpsilon)

    assert fl_mod.angle.degrees() == pytest.approx(0.0, abs=kEpsilon)
    assert fr_mod.angle.degrees() == pytest.approx(90.0, abs=kEpsilon)
    assert bl_mod.angle.degrees() == pytest.approx(180.0, abs=kEpsilon)
    assert br_mod.angle.degrees() == pytest.approx(-90.0, abs=kEpsilon)


def test_turn_in_place_forward_kinematics(kinematics_test):
    fl = SwerveModuleVelocity(velocity=106.629, angle=Rotation2d.fromDegrees(135))
    fr = SwerveModuleVelocity(velocity=106.629, angle=Rotation2d.fromDegrees(45))
    bl = SwerveModuleVelocity(velocity=106.629, angle=Rotation2d.fromDegrees(-135))
    br = SwerveModuleVelocity(velocity=106.629, angle=Rotation2d.fromDegrees(-45))

    chassis_velocities = kinematics_test.m_kinematics.toChassisVelocities(
        (fl, fr, bl, br)
    )

    assert chassis_velocities.vx == pytest.approx(0.0, abs=kEpsilon)
    assert chassis_velocities.vy == pytest.approx(0.0, abs=kEpsilon)
    assert chassis_velocities.omega == pytest.approx(2 * math.pi, abs=kEpsilon)


def test_turn_in_place_forward_kinematics_with_deltas(kinematics_test):
    fl = SwerveModulePosition(distance=106.629, angle=Rotation2d.fromDegrees(135))
    fr = SwerveModulePosition(distance=106.629, angle=Rotation2d.fromDegrees(45))
    bl = SwerveModulePosition(distance=106.629, angle=Rotation2d.fromDegrees(-135))
    br = SwerveModulePosition(distance=106.629, angle=Rotation2d.fromDegrees(-45))

    twist = kinematics_test.m_kinematics.toTwist2d((fl, fr, bl, br))

    assert twist.dx == pytest.approx(0.0, abs=kEpsilon)
    assert twist.dy == pytest.approx(0.0, abs=kEpsilon)
    assert twist.dtheta == pytest.approx(2 * math.pi, abs=kEpsilon)


def test_off_center_cor_rotation_inverse_kinematics(kinematics_test):
    velocities = ChassisVelocities(0, 0, 2 * math.pi)
    states = kinematics_test.m_kinematics.toSwerveModuleVelocities(
        velocities, kinematics_test.m_fl
    )

    fl, fr, bl, br = states

    assert fl.velocity == pytest.approx(0.0, abs=kEpsilon)
    assert fr.velocity == pytest.approx(150.796, abs=kEpsilon)
    assert bl.velocity == pytest.approx(150.796, abs=kEpsilon)
    assert br.velocity == pytest.approx(213.258, abs=kEpsilon)

    assert fl.angle.degrees() == pytest.approx(0.0, abs=kEpsilon)
    assert fr.angle.degrees() == pytest.approx(0.0, abs=kEpsilon)
    assert bl.angle.degrees() == pytest.approx(-90.0, abs=kEpsilon)
    assert br.angle.degrees() == pytest.approx(-45.0, abs=kEpsilon)


def test_off_center_cor_rotation_forward_kinematics(kinematics_test):
    fl = SwerveModuleVelocity(velocity=0.0, angle=Rotation2d.fromDegrees(0))
    fr = SwerveModuleVelocity(velocity=150.796, angle=Rotation2d.fromDegrees(0))
    bl = SwerveModuleVelocity(velocity=150.796, angle=Rotation2d.fromDegrees(-90))
    br = SwerveModuleVelocity(velocity=213.258, angle=Rotation2d.fromDegrees(-45))

    chassis_velocities = kinematics_test.m_kinematics.toChassisVelocities(
        (fl, fr, bl, br)
    )

    assert chassis_velocities.vx == pytest.approx(75.398, abs=kEpsilon)
    assert chassis_velocities.vy == pytest.approx(-75.398, abs=kEpsilon)
    assert chassis_velocities.omega == pytest.approx(2 * math.pi, abs=kEpsilon)


def test_off_center_cor_rotation_forward_kinematics_with_deltas(kinematics_test):
    fl = SwerveModulePosition(distance=0.0, angle=Rotation2d.fromDegrees(0))
    fr = SwerveModulePosition(distance=150.796, angle=Rotation2d.fromDegrees(0))
    bl = SwerveModulePosition(distance=150.796, angle=Rotation2d.fromDegrees(-90))
    br = SwerveModulePosition(distance=213.258, angle=Rotation2d.fromDegrees(-45))

    twist = kinematics_test.m_kinematics.toTwist2d((fl, fr, bl, br))

    assert twist.dx == pytest.approx(75.398, abs=kEpsilon)
    assert twist.dy == pytest.approx(-75.398, abs=kEpsilon)
    assert twist.dtheta == pytest.approx(2 * math.pi, abs=kEpsilon)


def test_off_center_cor_rotation_and_translation_inverse_kinematics(kinematics_test):
    velocities = ChassisVelocities(0, 3.0, 1.5)
    states = kinematics_test.m_kinematics.toSwerveModuleVelocities(
        velocities, Translation2d(x=24, y=0)
    )

    fl, fr, bl, br = states

    assert fl.velocity == pytest.approx(23.43, abs=kEpsilon)
    assert fr.velocity == pytest.approx(23.43, abs=kEpsilon)
    assert bl.velocity == pytest.approx(54.08, abs=kEpsilon)
    assert br.velocity == pytest.approx(54.08, abs=kEpsilon)

    assert fl.angle.degrees() == pytest.approx(-140.19, abs=kEpsilon)
    assert fr.angle.degrees() == pytest.approx(-39.81, abs=kEpsilon)
    assert bl.angle.degrees() == pytest.approx(-109.44, abs=kEpsilon)
    assert br.angle.degrees() == pytest.approx(-70.56, abs=kEpsilon)


def test_off_center_cor_rotation_and_translation_forward_kinematics(kinematics_test):
    fl = SwerveModuleVelocity(velocity=23.43, angle=Rotation2d.fromDegrees(-140.19))
    fr = SwerveModuleVelocity(velocity=23.43, angle=Rotation2d.fromDegrees(-39.81))
    bl = SwerveModuleVelocity(velocity=54.08, angle=Rotation2d.fromDegrees(-109.44))
    br = SwerveModuleVelocity(velocity=54.08, angle=Rotation2d.fromDegrees(-70.56))

    chassis_velocities = kinematics_test.m_kinematics.toChassisVelocities(
        (fl, fr, bl, br)
    )

    assert chassis_velocities.vx == pytest.approx(0.0, abs=kEpsilon)
    assert chassis_velocities.vy == pytest.approx(-33.0, abs=kEpsilon)
    assert chassis_velocities.omega == pytest.approx(1.5, abs=kEpsilon)


def test_off_center_cor_rotation_and_translation_forward_kinematics_with_deltas(
    kinematics_test,
):
    fl = SwerveModulePosition(distance=23.43, angle=Rotation2d.fromDegrees(-140.19))
    fr = SwerveModulePosition(distance=23.43, angle=Rotation2d.fromDegrees(-39.81))
    bl = SwerveModulePosition(distance=54.08, angle=Rotation2d.fromDegrees(-109.44))
    br = SwerveModulePosition(distance=54.08, angle=Rotation2d.fromDegrees(-70.56))

    twist = kinematics_test.m_kinematics.toTwist2d((fl, fr, bl, br))

    assert twist.dx == pytest.approx(0.0, abs=kEpsilon)
    assert twist.dy == pytest.approx(-33.0, abs=kEpsilon)
    assert twist.dtheta == pytest.approx(1.5, abs=kEpsilon)


def test_desaturate(kinematics_test):
    state1 = SwerveModuleVelocity(velocity=5.0, angle=Rotation2d.fromDegrees(0))
    state2 = SwerveModuleVelocity(velocity=6.0, angle=Rotation2d.fromDegrees(0))
    state3 = SwerveModuleVelocity(velocity=4.0, angle=Rotation2d.fromDegrees(0))
    state4 = SwerveModuleVelocity(velocity=7.0, angle=Rotation2d.fromDegrees(0))

    arr = [state1, state2, state3, state4]
    arr = kinematics_test.m_kinematics.desaturateWheelVelocities(arr, 5.5)

    k_factor = 5.5 / 7.0

    assert arr[0].velocity == pytest.approx(5.0 * k_factor, abs=kEpsilon)
    assert arr[1].velocity == pytest.approx(6.0 * k_factor, abs=kEpsilon)
    assert arr[2].velocity == pytest.approx(4.0 * k_factor, abs=kEpsilon)
    assert arr[3].velocity == pytest.approx(7.0 * k_factor, abs=kEpsilon)


def test_desaturate_smooth(kinematics_test):
    state1 = SwerveModuleVelocity(velocity=5.0, angle=Rotation2d(0))
    state2 = SwerveModuleVelocity(velocity=6.0, angle=Rotation2d(0))
    state3 = SwerveModuleVelocity(velocity=4.0, angle=Rotation2d(0))
    state4 = SwerveModuleVelocity(velocity=7.0, angle=Rotation2d(0))

    arr = [state1, state2, state3, state4]
    chassis_velocities = kinematics_test.m_kinematics.toChassisVelocities(
        (arr[0], arr[1], arr[2], arr[3])
    )
    arr = kinematics_test.m_kinematics.desaturateWheelVelocities(
        arr, chassis_velocities, 5.5, 5.5, 3.5
    )

    k_factor = 5.5 / 7.0

    assert arr[0].velocity == pytest.approx(5.0 * k_factor, abs=kEpsilon)
    assert arr[1].velocity == pytest.approx(6.0 * k_factor, abs=kEpsilon)
    assert arr[2].velocity == pytest.approx(4.0 * k_factor, abs=kEpsilon)
    assert arr[3].velocity == pytest.approx(7.0 * k_factor, abs=kEpsilon)


def test_desaturate_negative_velocity(kinematics_test):
    state1 = SwerveModuleVelocity(velocity=1.0, angle=Rotation2d(0))
    state2 = SwerveModuleVelocity(velocity=1.0, angle=Rotation2d(0))
    state3 = SwerveModuleVelocity(velocity=-2.0, angle=Rotation2d(0))
    state4 = SwerveModuleVelocity(velocity=-2.0, angle=Rotation2d(0))

    arr = [state1, state2, state3, state4]
    arr = kinematics_test.m_kinematics.desaturateWheelVelocities(arr, 1.0)

    assert arr[0].velocity == pytest.approx(0.5, abs=kEpsilon)
    assert arr[1].velocity == pytest.approx(0.5, abs=kEpsilon)
    assert arr[2].velocity == pytest.approx(-1.0, abs=kEpsilon)
    assert arr[3].velocity == pytest.approx(-1.0, abs=kEpsilon)


def test_turn_in_place_inverse_accelerations(kinematics_test):
    accelerations = ChassisAccelerations(ax=0, ay=0, alpha=2 * math.pi)
    angular_velocity = 2 * math.pi
    fl_accel, fr_accel, bl_accel, br_accel = (
        kinematics_test.m_kinematics.toSwerveModuleAccelerations(
            accelerations, angular_velocity
        )
    )

    modules = kinematics_test.m_kinematics.getModules()

    center_radius = modules[0].norm()
    tangential_accel = center_radius * accelerations.alpha
    centripetal_accel = center_radius * angular_velocity**2
    total_accel = math.hypot(tangential_accel, centripetal_accel)

    expected_angles = []
    for module in modules:
        radius_angle = module.angle()
        tangential_dir = Rotation2d(
            radius_angle.cos() * 0 - radius_angle.sin() * 1,
            radius_angle.sin() * 0 + radius_angle.cos() * 1,
        )
        tangential_x = tangential_accel * tangential_dir.cos()
        tangential_y = tangential_accel * tangential_dir.sin()

        centripetal_x = centripetal_accel * (-radius_angle.cos())
        centripetal_y = centripetal_accel * (-radius_angle.sin())

        total_x = tangential_x + centripetal_x
        total_y = tangential_y + centripetal_y
        expected_angles.append(Rotation2d(total_x, total_y))

    assert fl_accel.acceleration == pytest.approx(total_accel, abs=1e-9)
    assert fr_accel.acceleration == pytest.approx(total_accel, abs=1e-9)
    assert bl_accel.acceleration == pytest.approx(total_accel, abs=1e-9)
    assert br_accel.acceleration == pytest.approx(total_accel, abs=1e-9)
    assert fl_accel.angle.degrees() == pytest.approx(
        expected_angles[0].degrees(), abs=1e-9
    )
    assert fr_accel.angle.degrees() == pytest.approx(
        expected_angles[1].degrees(), abs=1e-9
    )
    assert bl_accel.angle.degrees() == pytest.approx(
        expected_angles[2].degrees(), abs=1e-9
    )
    assert br_accel.angle.degrees() == pytest.approx(
        expected_angles[3].degrees(), abs=1e-9
    )


def test_turn_in_place_forward_accelerations(kinematics_test):
    fl_accel = SwerveModuleAcceleration(106.629, Rotation2d.fromDegrees(135))
    fr_accel = SwerveModuleAcceleration(106.629, Rotation2d.fromDegrees(45))
    bl_accel = SwerveModuleAcceleration(106.629, Rotation2d.fromDegrees(-135))
    br_accel = SwerveModuleAcceleration(106.629, Rotation2d.fromDegrees(-45))

    chassis_accelerations = kinematics_test.m_kinematics.toChassisAccelerations(
        (fl_accel, fr_accel, bl_accel, br_accel)
    )

    assert chassis_accelerations.ax == pytest.approx(0.0, abs=kEpsilon)
    assert chassis_accelerations.ay == pytest.approx(0.0, abs=kEpsilon)
    assert chassis_accelerations.alpha == pytest.approx(2 * math.pi, abs=kEpsilon)


def test_off_center_rotation_inverse_accelerations(kinematics_test):
    accelerations = ChassisAccelerations(ax=0, ay=0, alpha=1)
    angular_velocity = 1.0
    fl_accel, fr_accel, bl_accel, br_accel = (
        kinematics_test.m_kinematics.toSwerveModuleAccelerations(
            accelerations, angular_velocity, kinematics_test.m_fl
        )
    )

    modules = kinematics_test.m_kinematics.getModules()

    expected_accels = []
    expected_angles = []
    for module in modules:
        relative_pos = module - kinematics_test.m_fl
        r = relative_pos.norm()

        if r < 1e-9:
            expected_accels.append(0.0)
            expected_angles.append(Rotation2d())
        else:
            tangential_accel = r * accelerations.alpha
            centripetal_accel = r * angular_velocity**2
            expected_accels.append(math.hypot(tangential_accel, centripetal_accel))

            radius_angle = Rotation2d(relative_pos.x, relative_pos.y)

            tangential_x = tangential_accel * (
                radius_angle.cos() * 0 - radius_angle.sin() * 1
            )
            tangential_y = tangential_accel * (
                radius_angle.sin() * 0 + radius_angle.cos() * 1
            )

            centripetal_x = centripetal_accel * (-radius_angle.cos())
            centripetal_y = centripetal_accel * (-radius_angle.sin())

            total_x = tangential_x + centripetal_x
            total_y = tangential_y + centripetal_y
            expected_angles.append(Rotation2d(total_x, total_y))

    assert fl_accel.acceleration == pytest.approx(expected_accels[0], abs=1e-9)
    assert fr_accel.acceleration == pytest.approx(expected_accels[1], abs=1e-9)
    assert bl_accel.acceleration == pytest.approx(expected_accels[2], abs=1e-9)
    assert br_accel.acceleration == pytest.approx(expected_accels[3], abs=1e-9)
    assert fl_accel.angle.degrees() == pytest.approx(
        expected_angles[0].degrees(), abs=1e-9
    )
    assert fr_accel.angle.degrees() == pytest.approx(
        expected_angles[1].degrees(), abs=1e-9
    )
    assert bl_accel.angle.degrees() == pytest.approx(
        expected_angles[2].degrees(), abs=1e-9
    )
    assert br_accel.angle.degrees() == pytest.approx(
        expected_angles[3].degrees(), abs=1e-9
    )
