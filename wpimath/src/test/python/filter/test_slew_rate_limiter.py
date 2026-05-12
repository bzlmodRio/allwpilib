import pytest
import wpiutil

from wpimath import SlewRateLimiter

_now_us = 0


def _now_getter():
    return int(_now_us)


@pytest.fixture(autouse=True)
def mock_time():
    global _now_us
    _now_us = 0
    wpiutil.set_now_impl(_now_getter)
    yield
    wpiutil.set_now_impl(None)


def test_slew_rate_limit():
    global _now_us
    limiter = SlewRateLimiter(1.0)
    _now_us = 1_000_000  # 1 second in microseconds
    assert limiter.calculate(2.0) < 2.0


def test_slew_rate_no_limit():
    global _now_us
    limiter = SlewRateLimiter(1.0)
    _now_us = 1_000_000
    assert limiter.calculate(0.5) == pytest.approx(0.5)


def test_slew_rate_positive_negative_limit():
    global _now_us
    limiter = SlewRateLimiter(1.0, -0.5, 0.0)
    _now_us = 1_000_000
    assert limiter.calculate(2.0) == pytest.approx(1.0)
    _now_us = 2_000_000
    assert limiter.calculate(0.0) == pytest.approx(0.5)
