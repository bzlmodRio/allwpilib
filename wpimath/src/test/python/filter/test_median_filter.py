import pytest

from wpimath import MedianFilter


def test_not_full_even():
    f = MedianFilter(10)

    f.calculate(3)
    f.calculate(0)
    f.calculate(4)

    assert f.calculate(1000) == pytest.approx(3.5)


def test_not_full_odd():
    f = MedianFilter(10)

    f.calculate(3)
    f.calculate(0)
    f.calculate(4)
    f.calculate(7)

    assert f.calculate(1000) == pytest.approx(4)


def test_full_even():
    f = MedianFilter(6)

    f.calculate(3)
    f.calculate(0)
    f.calculate(0)
    f.calculate(5)
    f.calculate(4)
    f.calculate(1000)

    assert f.calculate(99) == pytest.approx(4.5)


def test_full_odd():
    f = MedianFilter(5)

    f.calculate(3)
    f.calculate(0)
    f.calculate(5)
    f.calculate(4)
    f.calculate(1000)

    assert f.calculate(99) == pytest.approx(5)
