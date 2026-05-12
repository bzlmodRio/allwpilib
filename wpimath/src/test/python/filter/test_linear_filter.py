import math
import random
import pytest

from wpimath import LinearFilter

K_FILTER_STEP = 0.005  # 5 ms in seconds
K_FILTER_TIME = 2.0  # 2 s
K_SINGLE_POLE_IIR_TIME_CONSTANT = 0.015915
K_SINGLE_POLE_IIR_EXPECTED_OUTPUT = -3.2172003
K_HIGH_PASS_TIME_CONSTANT = 0.006631
K_HIGH_PASS_EXPECTED_OUTPUT = 10.074717
K_MOV_AVG_TAPS = 6
K_MOV_AVG_EXPECTED_OUTPUT = -10.191644


def get_data(t):
    return 100.0 * math.sin(2.0 * math.pi * t) + 20.0 * math.cos(50.0 * math.pi * t)


def get_pulse_data(t):
    if abs(t - 1.0) < 0.001:
        return 1.0
    return 0.0


def run_filter_output(f, data_fn, expected_output):
    filter_output = 0.0
    t = 0.0
    while t < K_FILTER_TIME:
        filter_output = f.calculate(data_fn(t))
        t += K_FILTER_STEP
    assert filter_output == pytest.approx(expected_output, abs=1e-5)


def test_single_pole_iir_output():
    f = LinearFilter.single_pole_iir(K_SINGLE_POLE_IIR_TIME_CONSTANT, K_FILTER_STEP)
    run_filter_output(f, get_data, K_SINGLE_POLE_IIR_EXPECTED_OUTPUT)


def test_high_pass_output():
    f = LinearFilter.high_pass(K_HIGH_PASS_TIME_CONSTANT, K_FILTER_STEP)
    run_filter_output(f, get_data, K_HIGH_PASS_EXPECTED_OUTPUT)


def test_moving_average_output():
    f = LinearFilter.moving_average(K_MOV_AVG_TAPS)
    run_filter_output(f, get_data, K_MOV_AVG_EXPECTED_OUTPUT)


def test_pulse_output():
    f = LinearFilter.moving_average(K_MOV_AVG_TAPS)
    run_filter_output(f, get_pulse_data, 0.0)


def run_noise_reduce(f):
    noise_gen_error = 0.0
    filter_error = 0.0

    random.seed(42)

    def get_signal(t):
        return 100.0 * math.sin(2.0 * math.pi * t)

    t = 0.0
    while t < K_FILTER_TIME:
        theory = get_signal(t)
        noise = random.gauss(0.0, 10.0)
        filter_error += abs(f.calculate(theory + noise) - theory)
        noise_gen_error += abs(noise - theory)
        t += K_FILTER_STEP

    assert noise_gen_error > filter_error, (
        "Filter should have reduced noise accumulation but failed"
    )


def test_single_pole_iir_noise_reduce():
    f = LinearFilter.single_pole_iir(K_SINGLE_POLE_IIR_TIME_CONSTANT, K_FILTER_STEP)
    run_noise_reduce(f)


def test_moving_average_noise_reduce():
    f = LinearFilter.moving_average(K_MOV_AVG_TAPS)
    run_noise_reduce(f)
