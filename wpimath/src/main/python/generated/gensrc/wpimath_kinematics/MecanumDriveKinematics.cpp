
// This file is autogenerated. DO NOT EDIT
#include <robotpy_build.h>




#include <frc/kinematics/MecanumDriveKinematics.h>








#define RPYGEN_ENABLE_frc__MecanumDriveKinematics_PROTECTED_CONSTRUCTORS
#include <rpygen/frc__MecanumDriveKinematics.hpp>







#include <wpystruct.h>



#include <type_traits>


  using namespace frc;





struct rpybuild_MecanumDriveKinematics_initializer {


  

  












  
  using MecanumDriveKinematics_Trampoline = rpygen::PyTrampoline_frc__MecanumDriveKinematics<typename frc::MecanumDriveKinematics, typename rpygen::PyTrampolineCfg_frc__MecanumDriveKinematics<>>;
    static_assert(std::is_abstract<MecanumDriveKinematics_Trampoline>::value == false, "frc::MecanumDriveKinematics " RPYBUILD_BAD_TRAMPOLINE);
  py::class_<typename frc::MecanumDriveKinematics, MecanumDriveKinematics_Trampoline, frc::Kinematics<MecanumDriveWheelSpeeds, MecanumDriveWheelPositions>> cls_MecanumDriveKinematics;

    

    
    

  py::module &m;

  
  rpybuild_MecanumDriveKinematics_initializer(py::module &m) :

  

  

  

  
    cls_MecanumDriveKinematics(m, "MecanumDriveKinematics"),

  

  
  
  

    m(m)
  {
    
    

    
    
  

    
    
  }

void finish() {





  {
  
  
  


  

  cls_MecanumDriveKinematics.doc() =
    "Helper class that converts a chassis velocity (dx, dy, and dtheta components)\n"
"into individual wheel speeds.\n"
"\n"
"The inverse kinematics (converting from a desired chassis velocity to\n"
"individual wheel speeds) uses the relative locations of the wheels with\n"
"respect to the center of rotation. The center of rotation for inverse\n"
"kinematics is also variable. This means that you can set your set your center\n"
"of rotation in a corner of the robot to perform special evasion maneuvers.\n"
"\n"
"Forward kinematics (converting an array of wheel speeds into the overall\n"
"chassis motion) is performs the exact opposite of what inverse kinematics\n"
"does. Since this is an overdetermined system (more equations than variables),\n"
"we use a least-squares approximation.\n"
"\n"
"The inverse kinematics: [wheelSpeeds] = [wheelLocations] * [chassisSpeeds]\n"
"We take the Moore-Penrose pseudoinverse of [wheelLocations] and then\n"
"multiply by [wheelSpeeds] to get our chassis speeds.\n"
"\n"
"Forward kinematics is also used for odometry -- determining the position of\n"
"the robot on the field using encoders and a gyro.";

  cls_MecanumDriveKinematics
  
    
  .def(py::init<Translation2d, Translation2d, Translation2d, Translation2d>(),
      py::arg("frontLeftWheel"), py::arg("frontRightWheel"), py::arg("rearLeftWheel"), py::arg("rearRightWheel"), release_gil(), py::doc(
    "Constructs a mecanum drive kinematics object.\n"
"\n"
":param frontLeftWheel:  The location of the front-left wheel relative to the\n"
"                        physical center of the robot.\n"
":param frontRightWheel: The location of the front-right wheel relative to\n"
"                        the physical center of the robot.\n"
":param rearLeftWheel:   The location of the rear-left wheel relative to the\n"
"                        physical center of the robot.\n"
":param rearRightWheel:  The location of the rear-right wheel relative to the\n"
"                        physical center of the robot.")
  )
  
  
  
    
  .
def
("toWheelSpeeds", static_cast<MecanumDriveWheelSpeeds(frc::MecanumDriveKinematics::*)(const ChassisSpeeds&, const Translation2d&) const>(
        &frc::MecanumDriveKinematics::ToWheelSpeeds),
      py::arg("chassisSpeeds"), py::arg("centerOfRotation"), release_gil(), py::doc(
    "Performs inverse kinematics to return the wheel speeds from a desired\n"
"chassis velocity. This method is often used to convert joystick values into\n"
"wheel speeds.\n"
"\n"
"This function also supports variable centers of rotation. During normal\n"
"operations, the center of rotation is usually the same as the physical\n"
"center of the robot; therefore, the argument is defaulted to that use case.\n"
"However, if you wish to change the center of rotation for evasive\n"
"maneuvers, vision alignment, or for any other use case, you can do so.\n"
"\n"
":param chassisSpeeds:    The desired chassis speed.\n"
":param centerOfRotation: The center of rotation. For example, if you set the\n"
"                         center of rotation at one corner of the robot and\n"
"                         provide a chassis speed that only has a dtheta\n"
"                         component, the robot will rotate around that\n"
"                         corner.\n"
"\n"
":returns: The wheel speeds. Use caution because they are not normalized.\n"
"          Sometimes, a user input may cause one of the wheel speeds to go\n"
"          above the attainable max velocity. Use the\n"
"          :meth:`MecanumDriveWheelSpeeds.normalize` method to rectify\n"
"          this issue. In addition, you can use Python unpacking syntax\n"
"          to directly assign the wheel speeds to variables::\n"
"\n"
"            fl, fr, bl, br = kinematics.toWheelSpeeds(chassisSpeeds)\n")
  )
  
  
  
    
  .
def
("toWheelSpeeds", static_cast<MecanumDriveWheelSpeeds(frc::MecanumDriveKinematics::*)(const ChassisSpeeds&) const>(
        &frc::MecanumDriveKinematics::ToWheelSpeeds),
      py::arg("chassisSpeeds"), release_gil(), py::doc(
    "Performs inverse kinematics to return the wheel speeds from a desired\n"
"chassis velocity. This method is often used to convert joystick values into\n"
"wheel speeds.\n"
"\n"
"This function also supports variable centers of rotation. During normal\n"
"operations, the center of rotation is usually the same as the physical\n"
"center of the robot; therefore, the argument is defaulted to that use case.\n"
"However, if you wish to change the center of rotation for evasive\n"
"maneuvers, vision alignment, or for any other use case, you can do so.\n"
"\n"
":param chassisSpeeds:    The desired chassis speed.\n"
":param centerOfRotation: The center of rotation. For example, if you set the\n"
"                         center of rotation at one corner of the robot and\n"
"                         provide a chassis speed that only has a dtheta\n"
"                         component, the robot will rotate around that\n"
"                         corner.\n"
"\n"
":returns: The wheel speeds. Use caution because they are not normalized.\n"
"          Sometimes, a user input may cause one of the wheel speeds to go\n"
"          above the attainable max velocity. Use the\n"
"          :meth:`MecanumDriveWheelSpeeds.normalize` method to rectify\n"
"          this issue. In addition, you can use Python unpacking syntax\n"
"          to directly assign the wheel speeds to variables::\n"
"\n"
"            fl, fr, bl, br = kinematics.toWheelSpeeds(chassisSpeeds)\n")
  )
  
  
  
    
  .
def
("toChassisSpeeds", &frc::MecanumDriveKinematics::ToChassisSpeeds,
      py::arg("wheelSpeeds"), release_gil(), py::doc(
    "Performs forward kinematics to return the resulting chassis state from the\n"
"given wheel speeds. This method is often used for odometry -- determining\n"
"the robot's position on the field using data from the real-world speed of\n"
"each wheel on the robot.\n"
"\n"
":param wheelSpeeds: The current mecanum drive wheel speeds.\n"
"\n"
":returns: The resulting chassis speed.")
  )
  
  
  
    
  .
def
("toTwist2d", static_cast<Twist2d(frc::MecanumDriveKinematics::*)(const MecanumDriveWheelPositions&, const MecanumDriveWheelPositions&) const>(
        &frc::MecanumDriveKinematics::ToTwist2d),
      py::arg("start"), py::arg("end"), release_gil()
  )
  
  
  
    
  .
def
("toTwist2d", static_cast<Twist2d(frc::MecanumDriveKinematics::*)(const MecanumDriveWheelPositions&) const>(
        &frc::MecanumDriveKinematics::ToTwist2d),
      py::arg("wheelDeltas"), release_gil(), py::doc(
    "Performs forward kinematics to return the resulting Twist2d from the\n"
"given wheel position deltas. This method is often used for odometry --\n"
"determining the robot's position on the field using data from the\n"
"distance driven by each wheel on the robot.\n"
"\n"
":param wheelDeltas: The change in distance driven by each wheel.\n"
"\n"
":returns: The resulting chassis speed.")
  )
  
  
  
    
  .
def
("getFrontLeft", &frc::MecanumDriveKinematics::GetFrontLeft, release_gil(), py::doc(
    "Returns the front-left wheel translation.\n"
"\n"
":returns: The front-left wheel translation.")
  )
  
  
  
    
  .
def
("getFrontRight", &frc::MecanumDriveKinematics::GetFrontRight, release_gil(), py::doc(
    "Returns the front-right wheel translation.\n"
"\n"
":returns: The front-right wheel translation.")
  )
  
  
  
    
  .
def
("getRearLeft", &frc::MecanumDriveKinematics::GetRearLeft, release_gil(), py::doc(
    "Returns the rear-left wheel translation.\n"
"\n"
":returns: The rear-left wheel translation.")
  )
  
  
  
    
  .
def
("getRearRight", &frc::MecanumDriveKinematics::GetRearRight, release_gil(), py::doc(
    "Returns the rear-right wheel translation.\n"
"\n"
":returns: The rear-right wheel translation.")
  )
  
  
  ;

  


  }







  SetupWPyStruct<frc::MecanumDriveKinematics>(cls_MecanumDriveKinematics);


}

}; // struct rpybuild_MecanumDriveKinematics_initializer

static std::unique_ptr<rpybuild_MecanumDriveKinematics_initializer> cls;

void begin_init_MecanumDriveKinematics(py::module &m) {
  cls = std::make_unique<rpybuild_MecanumDriveKinematics_initializer>(m);
}

void finish_init_MecanumDriveKinematics() {
  cls->finish();
  cls.reset();
}