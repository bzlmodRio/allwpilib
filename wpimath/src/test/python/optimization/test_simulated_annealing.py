import math
import random
import pytest

from wpimath.optimization import SimulatedAnnealing


def test_double_function_optimization_heart_beat():
    def function(x):
        return -(x + math.sin(x)) * math.exp(-x * x) + 1

    step_size = 10.0

    def next_state(x):
        return max(-3.0, min(3.0, x + (random.random() - 0.5) * step_size))

    simulated_annealing = SimulatedAnnealing(2.0, next_state, function)
    solution = simulated_annealing.solve(-1.0, 5000)

    assert solution == pytest.approx(0.68, abs=1e-1)


def test_double_function_optimization_multimodal():
    def function(x):
        return math.sin(x) + math.sin((10.0 / 3.0) * x)

    step_size = 10.0

    def next_state(x):
        return max(0.0, min(7.0, x + (random.random() - 0.5) * step_size))

    simulated_annealing = SimulatedAnnealing(2.0, next_state, function)
    solution = simulated_annealing.solve(-1.0, 5000)

    assert solution == pytest.approx(5.146, abs=1e-1)