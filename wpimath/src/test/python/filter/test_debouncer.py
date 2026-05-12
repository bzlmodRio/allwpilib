import pytest

from wpimath import Debouncer


def test_params():
    debouncer = Debouncer(0.020, Debouncer.DebounceType.kBoth)

    assert debouncer.getDebounceTime() == pytest.approx(0.020, abs=1e-9)
    assert debouncer.getDebounceType() == Debouncer.DebounceType.kBoth

    debouncer.setDebounceTime(0.100)
    assert debouncer.getDebounceTime() == pytest.approx(0.100, abs=1e-9)

    debouncer.setDebounceType(Debouncer.DebounceType.kFalling)
    assert debouncer.getDebounceType() == Debouncer.DebounceType.kFalling


def test_default_type_is_rising():
    debouncer = Debouncer(0.020)
    assert debouncer.getDebounceType() == Debouncer.DebounceType.kRising
