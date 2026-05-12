import pytest

from wpimath import Debouncer


def test_params():
    debouncer = Debouncer(0.020, Debouncer.DebounceType.BOTH)

    assert debouncer.get_debounce_time() == pytest.approx(0.020, abs=1e-9)
    assert debouncer.get_debounce_type() == Debouncer.DebounceType.BOTH

    debouncer.set_debounce_time(0.100)
    assert debouncer.get_debounce_time() == pytest.approx(0.100, abs=1e-9)

    debouncer.set_debounce_type(Debouncer.DebounceType.FALLING)
    assert debouncer.get_debounce_type() == Debouncer.DebounceType.FALLING


def test_default_type_is_rising():
    debouncer = Debouncer(0.020)
    assert debouncer.get_debounce_type() == Debouncer.DebounceType.RISING
