import pytest
import math
import numpy as np

from wpimath.controller import DifferentialDriveFeedforward, LinearPlantInversionFeedforward_1_1
from wpimath.system.plant import LinearSystemId
from wpimath.units import (
    meters,
    meters_per_second,
    meters_per_second_squared,
    radians_per_second,
    radians_per_second_squared,
    volts,
    seconds,
)


def test_calculate_with_trackwidth():
    kv_linear = volts(1) / meters_per_second(1)
    ka_linear = volts(1) / meters_per_second_squared(1)
    kv_angular = volts(1) / radians_per_second(1)
    ka_angular = volts(1) / radians_per_second_squared(1)
    trackwidth = meters(1)
    dt = seconds(0.02)

    differential_drive_feedforward = DifferentialDriveFeedforward(
        kv_linear, ka_linear, kv_angular, ka_angular, trackwidth
    )
    plant = LinearSystemId.identifyDrivetrainSystem(
        kv_linear, ka_linear, kv_angular, ka_angular, trackwidth
    )

    for current_left_velocity in np.arange(-4, 4 + 2, 2):
        for current_right_velocity in np.arange(-4, 4 + 2, 2):
            for next_left_velocity in np.arange(-4, 4 + 2, 2):
                for next_right_velocity in np.arange(-4, 4 + 2, 2):
                    wheel_voltages = differential_drive_feedforward.calculate(
                        meters_per_second(current_left_velocity),
                        meters_per_second(next_left_velocity),
                        meters_per_second(current_right_velocity),
                        meters_per_second(next_right_velocity),
                        dt,
                    )
                    next_x = plant.calculateX(
                        np.array([current_left_velocity, current_right_velocity]),
                        np.array([wheel_voltages.left, wheel_voltages.right]),
                        dt,
                    )
                    assert next_x[0] == pytest.approx(next_left_velocity, abs=1e-6)
                    assert next_x[1] == pytest.approx(next_right_velocity, abs=1e-6)


def test_calculate_without_trackwidth():
    kv_linear = volts(1) / meters_per_second(1)
    ka_linear = volts(1) / meters_per_second_squared(1)
    kv_angular = volts(1) / meters_per_second(1)
    ka_angular = volts(1) / meters_per_second_squared(1)
    dt = seconds(0.02)

    differential_drive_feedforward = DifferentialDriveFeedforward(
        kv_linear, ka_linear, kv_angular, ka_angular
    )
    plant = LinearSystemId.identifyDrivetrainSystem(
        kv_linear, ka_linear, kv_angular, ka_angular
    )

    for current_left_velocity in np.arange(-4, 4 + 2, 2):
        for current_right_velocity in np.arange(-4, 4 + 2, 2):
            for next_left_velocity in np.arange(-4, 4 + 2, 2):
                for next_right_velocity in np.arange(-4, 4 + 2, 2):
                    wheel_voltages = differential_drive_feedforward.calculate(
                        meters_per_second(current_left_velocity),
                        meters_per_second(next_left_velocity),
                        meters_per_second(current_right_velocity),
                        meters_per_second(next_right_velocity),
                        dt,
                    )
                    next_x = plant.calculateX(
                        np.array([[current_left_velocity], [current_right_velocity]]),
                        np.array([[wheel_voltages.left], [wheel_voltages.right]]),
                        dt,
                    )
                    assert next_x[0] == pytest.approx(next_left_velocity, abs=1e-6)
                    assert next_x[1] == pytest.approx(next_right_velocity, abs=1e-6)