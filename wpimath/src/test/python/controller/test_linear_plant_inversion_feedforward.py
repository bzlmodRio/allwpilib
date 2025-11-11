import pytest
import math
import numpy as np

from wpimath.controller import LinearPlantInversionFeedforward_2_1
from wpimath.units import seconds


def test_calculate():
    A = np.array([[1, 0], [0, 1]])
    B = np.array([[0], [1]])

    feedforward = LinearPlantInversionFeedforward_2_1(A, B, seconds(0.02))

    r = np.array([[2.0], [2.0]])
    next_r = np.array([[3.0], [3.0]])

    assert feedforward.calculate(r, next_r)[0] == pytest.approx(47.502599, abs=0.002)