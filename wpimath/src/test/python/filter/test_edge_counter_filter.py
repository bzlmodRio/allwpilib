import pytest

from wpimath import EdgeCounterFilter


def test_params():
    f = EdgeCounterFilter(2, 0.2)

    assert f.getRequiredEdges() == 2
    assert f.getWindowTime() == pytest.approx(0.2, abs=1e-9)

    f.setRequiredEdges(3)
    assert f.getRequiredEdges() == 3

    f.setWindowTime(0.5)
    assert f.getWindowTime() == pytest.approx(0.5, abs=1e-9)
