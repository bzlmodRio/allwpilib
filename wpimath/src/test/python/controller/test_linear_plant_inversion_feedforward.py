import numpy as np
import pytest

from wpimath import LinearPlantInversionFeedforward_2_1


def test_calculate():
    A = np.array([[1.0, 0.0], [0.0, 1.0]])
    B = np.array([[0.0], [1.0]])

    ff = LinearPlantInversionFeedforward_2_1(A, B, 0.020)

    r = np.array([[2.0], [2.0]])
    next_r = np.array([[3.0], [3.0]])

    result = ff.calculate(r, next_r)
    assert result[0] == pytest.approx(47.502599, abs=0.002)
