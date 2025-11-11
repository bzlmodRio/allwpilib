import pytest
import numpy as np

from wpimath.controller import ControlAffinePlantInversionFeedforward_2_1
from wpimath.units import seconds


def _dynamics(x, u):
    """
    C++ Dynamics function equivalent.
    """
    A = np.array([[1.0, 0.0], [0.0, 1.0]])
    B = np.array([[0.0], [1.0]])
    return A @ x + B @ u


def _state_dynamics(x):
    """
    C++ StateDynamics function equivalent.
    """
    A = np.array([[1.0, 0.0], [0.0, 1.0]])
    return A @ x


def test_calculate():
    feedforward = ControlAffinePlantInversionFeedforward_2_1(_dynamics, seconds(0.02))

    r = np.array([[2.0], [2.0]])
    next_r = np.array([[3.0], [3.0]])

    assert feedforward.calculate(r, next_r) == pytest.approx(48, abs=1e-6)


def test_calculate_state():
    B = np.array([[0.0], [1.0]])
    feedforward = ControlAffinePlantInversionFeedforward_2_1(_state_dynamics, B, seconds(0.02))

    r = np.array([[2.0], [2.0]])
    next_r = np.array([[3.0], [3.0]])

    assert feedforward.calculate(r, next_r) == pytest.approx(48, abs=1e-6)