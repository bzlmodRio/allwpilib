
// This file is autogenerated. DO NOT EDIT
#include <robotpy_build.h>




#include <frc/kinematics/DifferentialDriveKinematics.h>


#include <units_length_type_caster.h>







#define RPYGEN_ENABLE_frc__DifferentialDriveKinematics_PROTECTED_CONSTRUCTORS
#include <rpygen/frc__DifferentialDriveKinematics.hpp>







#include <wpystruct.h>



#include <type_traits>


  using namespace frc;





struct rpybuild_DifferentialDriveKinematics_initializer {


  

  












  
  using DifferentialDriveKinematics_Trampoline = rpygen::PyTrampoline_frc__DifferentialDriveKinematics<typename frc::DifferentialDriveKinematics, typename rpygen::PyTrampolineCfg_frc__DifferentialDriveKinematics<>>;
    static_assert(std::is_abstract<DifferentialDriveKinematics_Trampoline>::value == false, "frc::DifferentialDriveKinematics " RPYBUILD_BAD_TRAMPOLINE);
  py::class_<typename frc::DifferentialDriveKinematics, DifferentialDriveKinematics_Trampoline, frc::Kinematics<DifferentialDriveWheelSpeeds, DifferentialDriveWheelPositions>> cls_DifferentialDriveKinematics;

    

    
    

  py::module &m;

  
  rpybuild_DifferentialDriveKinematics_initializer(py::module &m) :

  

  

  

  
    cls_DifferentialDriveKinematics(m, "DifferentialDriveKinematics"),

  

  
  
  

    m(m)
  {
    
    

    
    
  

    
    
  }

void finish() {





  {
  
  
  


  

  cls_DifferentialDriveKinematics.doc() =
    "Helper class that converts a chassis velocity (dx and dtheta components) to\n"
"left and right wheel velocities for a differential drive.\n"
"\n"
"Inverse kinematics converts a desired chassis speed into left and right\n"
"velocity components whereas forward kinematics converts left and right\n"
"component velocities into a linear and angular chassis speed.";

  cls_DifferentialDriveKinematics
  
    
  .def(py::init<units::meter_t>(),
      py::arg("trackWidth"), release_gil(), py::doc(
    "Constructs a differential drive kinematics object.\n"
"\n"
":param trackWidth: The track width of the drivetrain. Theoretically, this is\n"
"                   the distance between the left wheels and right wheels. However, the\n"
"                   empirical value may be larger than the physical measured value due to\n"
"                   scrubbing effects.")
  )
  
  
  
    
  .
def
("toChassisSpeeds", &frc::DifferentialDriveKinematics::ToChassisSpeeds,
      py::arg("wheelSpeeds"), release_gil(), py::doc(
    "Returns a chassis speed from left and right component velocities using\n"
"forward kinematics.\n"
"\n"
":param wheelSpeeds: The left and right velocities.\n"
"\n"
":returns: The chassis speed.")
  )
  
  
  
    
  .
def
("toWheelSpeeds", &frc::DifferentialDriveKinematics::ToWheelSpeeds,
      py::arg("chassisSpeeds"), release_gil(), py::doc(
    "Returns left and right component velocities from a chassis speed using\n"
"inverse kinematics.\n"
"\n"
":param chassisSpeeds: The linear and angular (dx and dtheta) components that\n"
"                      represent the chassis' speed.\n"
"\n"
":returns: The left and right velocities.")
  )
  
  
  
    
  .
def
("toTwist2d", static_cast<Twist2d(frc::DifferentialDriveKinematics::*)(const units::meter_t, const units::meter_t) const>(
        &frc::DifferentialDriveKinematics::ToTwist2d),
      py::arg("leftDistance"), py::arg("rightDistance"), release_gil(), py::doc(
    "Returns a twist from left and right distance deltas using\n"
"forward kinematics.\n"
"\n"
":param leftDistance:  The distance measured by the left encoder.\n"
":param rightDistance: The distance measured by the right encoder.\n"
"\n"
":returns: The resulting Twist2d.")
  )
  
  
  
    
  .
def
("toTwist2d", static_cast<Twist2d(frc::DifferentialDriveKinematics::*)(const DifferentialDriveWheelPositions&, const DifferentialDriveWheelPositions&) const>(
        &frc::DifferentialDriveKinematics::ToTwist2d),
      py::arg("start"), py::arg("end"), release_gil()
  )
  
  
  
    .def_readonly("trackWidth", &frc::DifferentialDriveKinematics::trackWidth, py::doc(
    "Differential drive trackwidth."))
  ;

  


  }







  SetupWPyStruct<frc::DifferentialDriveKinematics>(cls_DifferentialDriveKinematics);


}

}; // struct rpybuild_DifferentialDriveKinematics_initializer

static std::unique_ptr<rpybuild_DifferentialDriveKinematics_initializer> cls;

void begin_init_DifferentialDriveKinematics(py::module &m) {
  cls = std::make_unique<rpybuild_DifferentialDriveKinematics_initializer>(m);
}

void finish_init_DifferentialDriveKinematics() {
  cls->finish();
  cls.reset();
}