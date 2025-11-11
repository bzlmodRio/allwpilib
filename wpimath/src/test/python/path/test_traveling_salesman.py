import pytest
import math

from typing import List
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.path import TravelingSalesman
from wpimath.units import meters, radians

def is_matching_cycle(expected: List[Pose2d], actual: List[Pose2d]) -> bool:
    assert len(expected) == len(actual)

    # Check for a forward match.
    try:
        start_index = actual.index(expected[0])
    except ValueError:
        return False
        
    actual_rotated = actual[start_index:] + actual[:start_index]
    matches_forward = all(
        a.x == pytest.approx(b.x, abs=1e-9) and
        a.y == pytest.approx(b.y, abs=1e-9)
        for a, b in zip(expected, actual_rotated)
    )

    # Check for a reverse match.
    actual_reversed = list(reversed(actual))
    try:
        start_index_reversed = actual_reversed.index(expected[0])
    except ValueError:
        pass # If expected[0] wasn't in actual, matches_forward is already false
    else:
        actual_rotated_reversed = actual_reversed[start_index_reversed:] + actual_reversed[:start_index_reversed]
        matches_reverse = all(
            a.x == pytest.approx(b.x, abs=1e-9) and
            a.y == pytest.approx(b.y, abs=1e-9)
            for a, b in zip(expected, actual_rotated_reversed)
        )

        return matches_forward or matches_reverse

    return matches_forward


def test_five_length_static_path_with_distance_cost():
    # ...................
    # ........2..........
    # ..0..........4.....
    # ...................
    # ....3.....1........
    # ...................
    poses = [
        Pose2d(meters(3), meters(3), radians(0)),
        Pose2d(meters(11), meters(5), radians(0)),
        Pose2d(meters(9), meters(2), radians(0)),
        Pose2d(meters(5), meters(5), radians(0)),
        Pose2d(meters(14), meters(3), radians(0)),
    ]

    traveler = TravelingSalesman()
    solution = traveler.solve(poses, 500)

    expected = [poses[0], poses[2], poses[4], poses[1], poses[3]]

    assert is_matching_cycle(expected, solution)


def test_five_length_dynamic_path_with_distance_cost():
    # ...................
    # ........2..........
    # ..0..........4.....
    # ...................
    # ....3.....1........
    # ...................
    poses = [
        Pose2d(meters(3), meters(3), radians(0)),
        Pose2d(meters(11), meters(5), radians(0)),
        Pose2d(meters(9), meters(2), radians(0)),
        Pose2d(meters(5), meters(5), radians(0)),
        Pose2d(meters(14), meters(3), radians(0)),
    ]

    traveler = TravelingSalesman()
    solution = traveler.solve(poses, 500)

    assert len(solution) == 5
    expected = [poses[0], poses[2], poses[4], poses[1], poses[3]]

    assert is_matching_cycle(expected, solution)


def test_ten_length_static_path_with_distance_cost():
    # ....6.3..1.2.......
    # ..4................
    # .............9.....
    # .0.................
    # .....7..5...8......
    # ...................
    poses = [
        Pose2d(meters(2), meters(4), radians(0)),
        Pose2d(meters(10), meters(1), radians(0)),
        Pose2d(meters(12), meters(1), radians(0)),
        Pose2d(meters(7), meters(1), radians(0)),
        Pose2d(meters(3), meters(2), radians(0)),
        Pose2d(meters(9), meters(5), radians(0)),
        Pose2d(meters(5), meters(1), radians(0)),
        Pose2d(meters(6), meters(5), radians(0)),
        Pose2d(meters(13), meters(5), radians(0)),
        Pose2d(meters(14), meters(3), radians(0)),
    ]

    traveler = TravelingSalesman()
    solution = traveler.solve(poses, 500)

    expected = [
        poses[0],
        poses[4],
        poses[6],
        poses[3],
        poses[1],
        poses[2],
        poses[9],
        poses[8],
        poses[5],
        poses[7],
    ]

    assert is_matching_cycle(expected, solution)


def test_ten_length_dynamic_path_with_distance_cost():
    # ....6.3..1.2.......
    # ..4................
    # .............9.....
    # .0.................
    # .....7..5...8......
    # ...................
    poses = [
        Pose2d(meters(2), meters(4), radians(0)),
        Pose2d(meters(10), meters(1), radians(0)),
        Pose2d(meters(12), meters(1), radians(0)),
        Pose2d(meters(7), meters(1), radians(0)),
        Pose2d(meters(3), meters(2), radians(0)),
        Pose2d(meters(9), meters(5), radians(0)),
        Pose2d(meters(5), meters(1), radians(0)),
        Pose2d(meters(6), meters(5), radians(0)),
        Pose2d(meters(13), meters(5), radians(0)),
        Pose2d(meters(14), meters(3), radians(0)),
    ]

    traveler = TravelingSalesman()
    solution = traveler.solve(poses, 500)

    assert len(solution) == 10
    expected = [
        poses[0],
        poses[4],
        poses[6],
        poses[3],
        poses[1],
        poses[2],
        poses[9],
        poses[8],
        poses[5],
        poses[7],
    ]

    assert is_matching_cycle(expected, solution)