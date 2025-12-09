from wpimath.geometry import (
    Ellipse2d,
    Pose2d,
    Rectangle2d,
    Rotation2d,
    Transform2d,
    Translation2d,
)
from typing import List
from wpimath.spline import CubicHermiteSpline, SplineHelper
from wpimath.trajectory import (
    Trajectory,
    TrajectoryConfig,
    TrajectoryGenerator,
    TrajectoryParameterizer,
)
from wpimath.trajectory.constraint import (
    EllipticalRegionConstraint,
    MaxVelocityConstraint,
    RectangularRegionConstraint,
    TrajectoryConstraint,
)

def getTestTrajectory(config: TrajectoryConfig) -> Trajectory:
    # 2018 cross scale auto waypoints
    side_start = Pose2d.fromFeet(1.54, 23.23, Rotation2d.fromDegrees(180))
    cross_scale = Pose2d.fromFeet(23.7, 6.8, Rotation2d.fromDegrees(-160))

    config.setReversed(True)

    vector = [
        (side_start + Transform2d(Translation2d.fromFeet(-13, 0), Rotation2d.fromDegrees(0))).translation(),
        (side_start + Transform2d(Translation2d.fromFeet(-19.5, 5), Rotation2d.fromDegrees(-90))).translation(),
    ]

    return TrajectoryGenerator.generateTrajectory(side_start, vector, cross_scale, config)
