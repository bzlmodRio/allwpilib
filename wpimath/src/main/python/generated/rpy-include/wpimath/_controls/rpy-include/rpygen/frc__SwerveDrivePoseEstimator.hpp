

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>



#include <frc/estimator/SwerveDrivePoseEstimator.h>


#include <frc/kinematics/SwerveModuleState.h>









#include <units_time_type_caster.h>

#include <wpi_array_type_caster.h>


namespace rpygen {


using namespace frc;




template <size_t NumModules>
struct bind_frc__SwerveDrivePoseEstimator {

    

    
  
  

    

    py::class_<typename frc::SwerveDrivePoseEstimator<NumModules>, frc::PoseEstimator<SwerveDriveWheelSpeeds<NumModules>, SwerveDriveWheelPositions<NumModules>>> cls_SwerveDrivePoseEstimator;

    

    
    

    py::module &m;
    std::string clsName;

bind_frc__SwerveDrivePoseEstimator(py::module &m, const char * clsName) :
    
    cls_SwerveDrivePoseEstimator(m, clsName),

  

  
  
    m(m),
    clsName(clsName)
{
    
  

}

void finish(const char * set_doc = NULL, const char * add_doc = NULL) {

    

  cls_SwerveDrivePoseEstimator.doc() =
    "This class wraps Swerve Drive Odometry to fuse latency-compensated\n"
"vision measurements with swerve drive encoder distance measurements. It is\n"
"intended to be a drop-in for :class:`SwerveDriveOdometry`.\n"
"\n"
":meth:`update` should be called every robot loop.\n"
"\n"
":meth:`addVisionMeasurement` can be called as infrequently as you want; if you\n"
"never call it, then this class will behave as regular encoder odometry.\n"
"\n"
"The state-space system used internally has the following states (x) and outputs (y):\n"
"\n"
":math:`x = [x, y, \\theta]^T` in the field-coordinate system\n"
"containing x position, y position, and heading.\n"
"\n"
":math:`y = [x, y, \\theta]^T` from vision containing x position, y\n"
"position, and heading; or :math:`y = [theta]^T` containing gyro\n"
"heading.\n";

  cls_SwerveDrivePoseEstimator
  
    
  .def(py::init<SwerveDriveKinematics<NumModules>&, const Rotation2d&, const wpi::array<SwerveModulePosition, NumModules>&, const Pose2d&>(),
      py::arg("kinematics"), py::arg("gyroAngle"), py::arg("modulePositions"), py::arg("initialPose"), release_gil()
    , py::keep_alive<1, 2>()
    , py::keep_alive<1, 3>()
    , py::keep_alive<1, 4>()
    , py::keep_alive<1, 5>(), py::doc(
    "Constructs a SwerveDrivePoseEstimator with default standard deviations\n"
"for the model and vision measurements.\n"
"\n"
"The default standard deviations of the model states are\n"
"0.1 meters for x, 0.1 meters for y, and 0.1 radians for heading.\n"
"The default standard deviations of the vision measurements are\n"
"0.9 meters for x, 0.9 meters for y, and 0.9 radians for heading.\n"
"\n"
":param kinematics:      A correctly-configured kinematics object for your\n"
"                        drivetrain.\n"
":param gyroAngle:       The current gyro angle.\n"
":param modulePositions: The current distance and rotation measurements of\n"
"                        the swerve modules.\n"
":param initialPose:     The starting pose estimate.")
  )
  
  
  
    
  .def(py::init<SwerveDriveKinematics<NumModules>&, const Rotation2d&, const wpi::array<SwerveModulePosition, NumModules>&, const Pose2d&, const wpi::array<double, 3>&, const wpi::array<double, 3>&>(),
      py::arg("kinematics"), py::arg("gyroAngle"), py::arg("modulePositions"), py::arg("initialPose"), py::arg("stateStdDevs"), py::arg("visionMeasurementStdDevs"), release_gil()
    , py::keep_alive<1, 2>()
    , py::keep_alive<1, 3>()
    , py::keep_alive<1, 4>()
    , py::keep_alive<1, 5>()
    , py::keep_alive<1, 6>()
    , py::keep_alive<1, 7>(), py::doc(
    "Constructs a SwerveDrivePoseEstimator.\n"
"\n"
":param kinematics:               A correctly-configured kinematics object for your\n"
"                                 drivetrain.\n"
":param gyroAngle:                The current gyro angle.\n"
":param modulePositions:          The current distance and rotation measurements of\n"
"                                 the swerve modules.\n"
":param initialPose:              The starting pose estimate.\n"
":param stateStdDevs:             Standard deviations of the pose estimate (x position in\n"
"                                 meters, y position in meters, and heading in radians). Increase these\n"
"                                 numbers to trust your state estimate less.\n"
":param visionMeasurementStdDevs: Standard deviations of the vision pose\n"
"                                 measurement (x position in meters, y position in meters, and heading in\n"
"                                 radians). Increase these numbers to trust the vision pose measurement\n"
"                                 less.")
  )
  
  
  
    
  .
def
("resetPosition", &frc::SwerveDrivePoseEstimator<NumModules>::ResetPosition,
      py::arg("gyroAngle"), py::arg("modulePositions"), py::arg("pose"), release_gil(), py::doc(
    "Resets the robot's position on the field.\n"
"\n"
"The gyroscope angle does not need to be reset in the user's robot code.\n"
"The library automatically takes care of offsetting the gyro angle.\n"
"\n"
":param gyroAngle:       The angle reported by the gyroscope.\n"
":param modulePositions: The current distance and rotation measurements of\n"
"                        the swerve modules.\n"
":param pose:            The position on the field that your robot is at.")
  )
  
  
  
    
  .
def
("update", &frc::SwerveDrivePoseEstimator<NumModules>::Update,
      py::arg("gyroAngle"), py::arg("modulePositions"), release_gil(), py::doc(
    "Updates the pose estimator with wheel encoder and gyro information. This\n"
"should be called every loop.\n"
"\n"
":param gyroAngle:       The current gyro angle.\n"
":param modulePositions: The current distance and rotation measurements of\n"
"                        the swerve modules.\n"
"\n"
":returns: The estimated robot pose in meters.")
  )
  
  
  
    
  .
def
("updateWithTime", &frc::SwerveDrivePoseEstimator<NumModules>::UpdateWithTime,
      py::arg("currentTime"), py::arg("gyroAngle"), py::arg("modulePositions"), release_gil(), py::doc(
    "Updates the pose estimator with wheel encoder and gyro information. This\n"
"should be called every loop.\n"
"\n"
":param currentTime:     Time at which this method was called, in seconds.\n"
":param gyroAngle:       The current gyro angle.\n"
":param modulePositions: The current distance traveled and rotations of\n"
"                        the swerve modules.\n"
"\n"
":returns: The estimated robot pose in meters.")
  )
  
  
  ;

  



    if (set_doc) {
        cls_SwerveDrivePoseEstimator.doc() = set_doc;
    }
    if (add_doc) {
        cls_SwerveDrivePoseEstimator.doc() = py::cast<std::string>(cls_SwerveDrivePoseEstimator.doc()) + add_doc;
    }

    
}

}; // struct bind_frc__SwerveDrivePoseEstimator

}; // namespace rpygen