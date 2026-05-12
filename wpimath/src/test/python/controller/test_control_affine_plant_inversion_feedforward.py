import numpy as np
import pytest

from wpimath import ControlAffinePlantInversionFeedforward_2_1


def _dynamics(x, u):
    A = np.array([[1.0, 0.0], [0.0, 1.0]])
    B = np.array([[0.0], [1.0]])
    return A @ x + B @ u


def _state_dynamics(x):
    A = np.array([[1.0, 0.0], [0.0, 1.0]])
    return A @ x


def test_calculate():
    ff = ControlAffinePlantInversionFeedforward_2_1(_dynamics, 0.020)

    r = np.array([[2.0], [2.0]])
    next_r = np.array([[3.0], [3.0]])

    result = ff.calculate(r, next_r)
    assert result[0] == pytest.approx(48, abs=1e-6)


def test_calculate_state():
    B = np.array([[0.0], [1.0]])
    ff = ControlAffinePlantInversionFeedforward_2_1(_state_dynamics, B, 0.020)

    r = np.array([[2.0], [2.0]])
    next_r = np.array([[3.0], [3.0]])

    result = ff.calculate(r, next_r)
    assert result[0] == pytest.approx(48, abs=1e-6)
