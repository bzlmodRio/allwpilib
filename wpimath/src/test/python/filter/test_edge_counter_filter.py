import pytest

from wpimath import EdgeCounterFilter


def test_params():
    f = EdgeCounterFilter(2, 0.2)

    assert f.get_required_edges() == 2
    assert f.get_window_time() == pytest.approx(0.2, abs=1e-9)

    f.set_required_edges(3)
    assert f.get_required_edges() == 3

    f.set_window_time(0.5)
    assert f.get_window_time() == pytest.approx(0.5, abs=1e-9)
