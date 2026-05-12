import pytest

from wpimath import ElevatorFeedforward

KS = 0.5
KG = 1.0
KV = 1.5
KA = 2.0


def test_calculate():
    ff = ElevatorFeedforward(KS, KG, KV, KA)

    assert ff.calculate(0.0) == pytest.approx(KG, abs=0.002)
    assert ff.calculate(2.0) == pytest.approx(4.5, abs=0.002)


def test_achievable_velocity():
    ff = ElevatorFeedforward(KS, KG, KV, KA)

    assert ff.max_achievable_velocity(11.0, 1.0) == pytest.approx(5.0, abs=0.002)
    assert ff.min_achievable_velocity(11.0, 1.0) == pytest.approx(-9.0, abs=0.002)


def test_achievable_acceleration():
    ff = ElevatorFeedforward(KS, KG, KV, KA)

    assert ff.max_achievable_acceleration(12.0, 2.0) == pytest.approx(3.75, abs=0.002)
    assert ff.max_achievable_acceleration(12.0, -2.0) == pytest.approx(7.25, abs=0.002)
    assert ff.min_achievable_acceleration(12.0, 2.0) == pytest.approx(-8.25, abs=0.002)
    assert ff.min_achievable_acceleration(12.0, -2.0) == pytest.approx(-4.75, abs=0.002)


def test_negative_gains():
    ff = ElevatorFeedforward(KS, KG, -KV, -KA)
    assert ff.get_kv() == pytest.approx(0.0)
    assert ff.get_ka() == pytest.approx(0.0)
