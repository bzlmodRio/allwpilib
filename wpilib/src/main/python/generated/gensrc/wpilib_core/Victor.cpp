
// This file is autogenerated. DO NOT EDIT
#include <robotpy_build.h>




#include <frc/motorcontrol/Victor.h>








#define RPYGEN_ENABLE_frc__Victor_PROTECTED_CONSTRUCTORS
#include <rpygen/frc__Victor.hpp>







#include <wpi/sendable/SendableBuilder.h>



#include <type_traits>


  using namespace frc;





struct rpybuild_Victor_initializer {


  

  












  
  using Victor_Trampoline = rpygen::PyTrampoline_frc__Victor<typename frc::Victor, typename rpygen::PyTrampolineCfg_frc__Victor<>>;
    static_assert(std::is_abstract<Victor_Trampoline>::value == false, "frc::Victor " RPYBUILD_BAD_TRAMPOLINE);
  py::class_<typename frc::Victor, Victor_Trampoline, frc::PWMMotorController> cls_Victor;

    

    
    

  py::module &m;

  
  rpybuild_Victor_initializer(py::module &m) :

  

  

  

  
    cls_Victor(m, "Victor"),

  

  
  
  

    m(m)
  {
    
    

    
    
  

    
    
  }

void finish() {





  {
  
  
  


  

  cls_Victor.doc() =
    "Vex Robotics %Victor 888 Motor %Controller.\n"
"\n"
"The Vex Robotics %Victor 884 Motor %Controller can also be used with this\n"
"class but may need to be calibrated per the Victor 884 user manual.\n"
"\n"
"Note that the %Victor uses the following bounds for PWM values.  These\n"
"values were determined empirically and optimized for the %Victor 888. These\n"
"values should work reasonably well for %Victor 884 controllers as well but\n"
"if users experience issues such as asymmetric behavior around the deadband\n"
"or inability to saturate the controller in either direction, calibration is\n"
"recommended. The calibration procedure can be found in the %Victor 884 User\n"
"Manual available from Vex.\n"
"\n"
"- 2.027ms = full \"forward\"\n"
"- 1.525ms = the \"high end\" of the deadband range\n"
"- 1.507ms = center of the deadband range (off)\n"
"- 1.490ms = the \"low end\" of the deadband range\n"
"- 1.026ms = full \"reverse\"";

  cls_Victor
  
    
  .def(py::init<int>(),
      py::arg("channel"), release_gil(), py::doc(
    "Constructor for a %Victor.\n"
"\n"
":param channel: The PWM channel number that the %Victor is attached to. 0-9\n"
"                are on-board, 10-19 are on the MXP port")
  )
  
  
  ;

  


  }






}

}; // struct rpybuild_Victor_initializer

static std::unique_ptr<rpybuild_Victor_initializer> cls;

void begin_init_Victor(py::module &m) {
  cls = std::make_unique<rpybuild_Victor_initializer>(m);
}

void finish_init_Victor() {
  cls->finish();
  cls.reset();
}