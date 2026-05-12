import pytest

from wpimath import Pose2d, Rotation2d, TravelingSalesman


def _is_matching_cycle(expected, actual):
    """Check if two pose lists represent the same TSP cycle (forward or reverse)."""
    n = len(expected)
    assert len(actual) == n

    # Check forward: actual == expected
    if actual == list(expected):
        return True

    # Check reverse: [actual[0], actual[n-1], ..., actual[1]]
    reversed_actual = [actual[0]] + list(reversed(actual[1:]))
    if reversed_actual == list(expected):
        return True

    return False


def test_five_length_dynamic_path_with_distance_cost():
    poses = [
        Pose2d(3, 3, Rotation2d()),
        Pose2d(11, 5, Rotation2d()),
        Pose2d(9, 2, Rotation2d()),
        Pose2d(5, 5, Rotation2d()),
        Pose2d(14, 3, Rotation2d()),
    ]

    traveler = TravelingSalesman()
    solution = traveler.solve(poses, 500)

    assert len(solution) == 5
    expected = [poses[0], poses[2], poses[4], poses[1], poses[3]]
    assert _is_matching_cycle(expected, solution)


def test_ten_length_dynamic_path_with_distance_cost():
    poses = [
        Pose2d(2, 4, Rotation2d()),
        Pose2d(10, 1, Rotation2d()),
        Pose2d(12, 1, Rotation2d()),
        Pose2d(7, 1, Rotation2d()),
        Pose2d(3, 2, Rotation2d()),
        Pose2d(9, 5, Rotation2d()),
        Pose2d(5, 1, Rotation2d()),
        Pose2d(6, 5, Rotation2d()),
        Pose2d(13, 5, Rotation2d()),
        Pose2d(14, 3, Rotation2d()),
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
    assert _is_matching_cycle(expected, solution)
