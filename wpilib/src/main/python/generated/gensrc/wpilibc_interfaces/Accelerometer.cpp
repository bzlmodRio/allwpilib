
// This file is autogenerated. DO NOT EDIT
#include <robotpy_build.h>




#include <frc/interfaces/Accelerometer.h>








#define RPYGEN_ENABLE_frc__Accelerometer_PROTECTED_CONSTRUCTORS
#include <rpygen/frc__Accelerometer.hpp>









#include <type_traits>


  using namespace frc;





struct rpybuild_Accelerometer_initializer {


  

  












  
  using Accelerometer_Trampoline = rpygen::PyTrampoline_frc__Accelerometer<typename frc::Accelerometer, typename rpygen::PyTrampolineCfg_frc__Accelerometer<>>;
    static_assert(std::is_abstract<Accelerometer_Trampoline>::value == false, "frc::Accelerometer " RPYBUILD_BAD_TRAMPOLINE);
  py::class_<typename frc::Accelerometer, Accelerometer_Trampoline> cls_Accelerometer;

    
    
  py::enum_<frc::Accelerometer::Range> cls_Accelerometer_enum1;
    

    
    

  py::module &m;

  
  rpybuild_Accelerometer_initializer(py::module &m) :

  

  

  

  
    cls_Accelerometer(m, "Accelerometer"),

  
    cls_Accelerometer_enum1
  (cls_Accelerometer, "Range"
  ,
    "Accelerometer range."),
  

  
  
  

    m(m)
  {
    
    

    
    
  
    cls_Accelerometer_enum1
  
    .value("kRange_2G", frc::Accelerometer::Range::kRange_2G,
      "2 Gs max.")
  
    .value("kRange_4G", frc::Accelerometer::Range::kRange_4G,
      "4 Gs max.")
  
    .value("kRange_8G", frc::Accelerometer::Range::kRange_8G,
      "8 Gs max.")
  
    .value("kRange_16G", frc::Accelerometer::Range::kRange_16G,
      "16 Gs max.")
  ;

  

    
    
  }

void finish() {





  {
  
  
  using Range [[maybe_unused]] = typename frc::Accelerometer::Range;
  
  


  

  cls_Accelerometer.doc() =
    "Interface for 3-axis accelerometers.\n"
"\n"
":deprecated: This interface is being removed with no replacement.";

  cls_Accelerometer
  
    
  .def(py::init<>(), release_gil()
  )
  
  
  
    
  .
def
("setRange", &frc::Accelerometer::SetRange,
      py::arg("range"), release_gil(), py::doc(
    "Common interface for setting the measuring range of an accelerometer.\n"
"\n"
":param range: The maximum acceleration, positive or negative, that the\n"
"              accelerometer will measure. Not all accelerometers support all\n"
"              ranges.")
  )
  
  
  
    
  .
def
("getX", &frc::Accelerometer::GetX, release_gil(), py::doc(
    "Common interface for getting the x axis acceleration.\n"
"\n"
":returns: The acceleration along the x axis in g-forces")
  )
  
  
  
    
  .
def
("getY", &frc::Accelerometer::GetY, release_gil(), py::doc(
    "Common interface for getting the y axis acceleration.\n"
"\n"
":returns: The acceleration along the y axis in g-forces")
  )
  
  
  
    
  .
def
("getZ", &frc::Accelerometer::GetZ, release_gil(), py::doc(
    "Common interface for getting the z axis acceleration.\n"
"\n"
":returns: The acceleration along the z axis in g-forces")
  )
  
  
  ;

  


  }






}

}; // struct rpybuild_Accelerometer_initializer

static std::unique_ptr<rpybuild_Accelerometer_initializer> cls;

void begin_init_Accelerometer(py::module &m) {
  cls = std::make_unique<rpybuild_Accelerometer_initializer>(m);
}

void finish_init_Accelerometer() {
  cls->finish();
  cls.reset();
}