import numpy as np
import pytest

from wpimath import DCMotor, Models


def test_flywheel_from_physical_constants():
    model = Models.flywheelFromPhysicalConstants(DCMotor.NEO(2), 0.00032, 1.0)

    np.testing.assert_allclose(model.A(), np.array([-26.87032]), rtol=0.001)
    np.testing.assert_allclose(model.B(), np.array([1354.166667]), rtol=0.001)
    np.testing.assert_allclose(model.C(), np.array([1.0]), rtol=0.001)
    np.testing.assert_allclose(model.D(), np.array([0.0]), rtol=0.001)


def test_flywheel_from_sys_id():
    kv = 1.0
    ka = 0.5

    model = Models.flywheelFromSysId(kv, ka)

    np.testing.assert_allclose(model.A(), np.array([-kv / ka]), rtol=0.001)
    np.testing.assert_allclose(model.B(), np.array([1.0 / ka]), rtol=0.001)


def test_differential_drive_from_physical_constants():
    model = Models.differentialDriveFromPhysicalConstants(
        DCMotor.NEO(4), 70.0, 0.05, 0.4, 6.0, 6.0
    )

    np.testing.assert_allclose(
        model.A(),
        np.array([[-10.14132, 3.06598], [3.06598, -10.14132]]),
        rtol=0.001,
    )
    np.testing.assert_allclose(
        model.B(),
        np.array([[4.2590, -1.28762], [-1.2876, 4.2590]]),
        rtol=0.001,
    )
    np.testing.assert_allclose(
        model.C(), np.array([[1.0, 0.0], [0.0, 1.0]]), rtol=0.001
    )
    np.testing.assert_allclose(
        model.D(), np.array([[0.0, 0.0], [0.0, 0.0]]), rtol=0.001
    )


def test_elevator_from_physical_constants():
    model = Models.elevatorFromPhysicalConstants(DCMotor.NEO(2), 5.0, 0.05, 12).slice(
        0
    )

    np.testing.assert_allclose(
        model.A(), np.array([[0.0, 1.0], [0.0, -99.05473]]), rtol=0.001
    )
    np.testing.assert_allclose(
        model.B(), np.array([0.0, 20.8]), rtol=0.001
    )
    np.testing.assert_allclose(model.C(), np.array([1.0, 0.0]), rtol=0.001)
    np.testing.assert_allclose(model.D(), np.array([0.0]), rtol=0.001)


def test_elevator_from_sys_id():
    kv = 1.0
    ka = 0.5

    model = Models.elevatorFromSysId(kv, ka)

    np.testing.assert_allclose(
        model.A(), np.array([[0.0, 1.0], [0.0, -kv / ka]]), rtol=0.001
    )
    np.testing.assert_allclose(model.B(), np.array([0.0, 1.0 / ka]), rtol=0.001)


def test_single_jointed_arm_from_sys_id():
    kv = 1.0
    ka = 0.5

    model = Models.singleJointedArmFromSysId(kv, ka)

    np.testing.assert_allclose(
        model.A(), np.array([[0.0, 1.0], [0.0, -kv / ka]]), rtol=0.001
    )
    np.testing.assert_allclose(model.B(), np.array([0.0, 1.0 / ka]), rtol=0.001)
