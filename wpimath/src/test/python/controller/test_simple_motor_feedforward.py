import pytest

from wpimath import SimpleMotorFeedforwardMeters

KS = 0.5
KV = 3.0
KA = 0.6
DT = 0.02


def test_calculate():
    ff = SimpleMotorFeedforwardMeters(KS, KV, KA)

    assert ff.calculate(2.0, 3.0) == pytest.approx(37.524995834325161 + KS, abs=0.002)


def test_negative_gains():
    ff = SimpleMotorFeedforwardMeters(KS, -KV, -KA, 0.0)
    assert ff.getKv() == pytest.approx(0.0)
    assert ff.getKa() == pytest.approx(0.0)
    assert ff.getDt() == pytest.approx(DT, abs=1e-9)
