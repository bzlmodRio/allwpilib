
// This file is autogenerated. DO NOT EDIT
#include <robotpy_build.h>




#include <frc/ADXL345_I2C.h>








#define RPYGEN_ENABLE_frc__ADXL345_I2C_PROTECTED_CONSTRUCTORS
#include <rpygen/frc__ADXL345_I2C.hpp>







#include <networktables/NTSendableBuilder.h>



#include <type_traits>


  using namespace frc;





struct rpybuild_ADXL345_I2C_initializer {


  

  static constexpr auto kRange_2G = frc::ADXL345_I2C::Range::kRange_2G;
  












  
  using ADXL345_I2C_Trampoline = rpygen::PyTrampoline_frc__ADXL345_I2C<typename frc::ADXL345_I2C, typename rpygen::PyTrampolineCfg_frc__ADXL345_I2C<>>;
    static_assert(std::is_abstract<ADXL345_I2C_Trampoline>::value == false, "frc::ADXL345_I2C " RPYBUILD_BAD_TRAMPOLINE);
  py::class_<typename frc::ADXL345_I2C, ADXL345_I2C_Trampoline, nt::NTSendable> cls_ADXL345_I2C;

    
    
  py::enum_<frc::ADXL345_I2C::Range> cls_ADXL345_I2C_enum1;
    
    
  py::enum_<frc::ADXL345_I2C::Axes> cls_ADXL345_I2C_enum2;
    

    
    
    py::class_<typename frc::ADXL345_I2C::AllAxes> cls_AllAxes;

    

    
    
    

  py::module &m;

  
  rpybuild_ADXL345_I2C_initializer(py::module &m) :

  

  

  

  
    cls_ADXL345_I2C(m, "ADXL345_I2C"),

  
    cls_ADXL345_I2C_enum1
  (cls_ADXL345_I2C, "Range"
  ,
    "Accelerometer range."),
  
    cls_ADXL345_I2C_enum2
  (cls_ADXL345_I2C, "Axes"
  ,
    "Accelerometer axes."),
  

  
  
    cls_AllAxes(cls_ADXL345_I2C, "AllAxes"),

  

  
  
  
  

    m(m)
  {
    
    

    
    
  
    cls_ADXL345_I2C_enum1
  
    .value("kRange_2G", frc::ADXL345_I2C::Range::kRange_2G,
      "2 Gs max.")
  
    .value("kRange_4G", frc::ADXL345_I2C::Range::kRange_4G,
      "4 Gs max.")
  
    .value("kRange_8G", frc::ADXL345_I2C::Range::kRange_8G,
      "8 Gs max.")
  
    .value("kRange_16G", frc::ADXL345_I2C::Range::kRange_16G,
      "16 Gs max.")
  ;

  
    cls_ADXL345_I2C_enum2
  
    .value("kAxis_X", frc::ADXL345_I2C::Axes::kAxis_X,
      "X axis.")
  
    .value("kAxis_Y", frc::ADXL345_I2C::Axes::kAxis_Y,
      "Y axis.")
  
    .value("kAxis_Z", frc::ADXL345_I2C::Axes::kAxis_Z,
      "Z axis.")
  ;

  

    
    
  

    
    
  }

void finish() {





  {
  
  using AllAxes [[maybe_unused]] = typename frc::ADXL345_I2C::AllAxes;
  
  
  using Range [[maybe_unused]] = typename frc::ADXL345_I2C::Range;
  
  using Axes [[maybe_unused]] = typename frc::ADXL345_I2C::Axes;
  
  
    static constexpr auto kAddress [[maybe_unused]] = frc::ADXL345_I2C::kAddress;
  


  

  cls_ADXL345_I2C.doc() =
    "ADXL345 Accelerometer on I2C.\n"
"\n"
"This class allows access to a Analog Devices ADXL345 3-axis accelerometer on\n"
"an I2C bus. This class assumes the default (not alternate) sensor address of\n"
"0x1D (7-bit address).\n"
"\n"
"The Onboard I2C port is subject to system lockups. See <a\n"
"href=\"https://docs.wpilib.org/en/stable/docs/yearly-overview/known-issues.html#onboard-i2c-causing-system-lockups\">\n"
"WPILib Known Issues</a> page for details.";

  cls_ADXL345_I2C
  
    
  .def(py::init<I2C::Port, Range, int>(),
      py::arg("port"), py::arg("range") = kRange_2G, py::arg("deviceAddress") = kAddress, release_gil(), py::doc(
    "Constructs the ADXL345 Accelerometer over I2C.\n"
"\n"
":param port:          The I2C port the accelerometer is attached to\n"
":param range:         The range (+ or -) that the accelerometer will measure\n"
":param deviceAddress: The I2C address of the accelerometer (0x1D or 0x53)")
  )
  
  
  
    
  .
def
("getI2CPort", &frc::ADXL345_I2C::GetI2CPort, release_gil()
  )
  
  
  
    
  .
def
("getI2CDeviceAddress", &frc::ADXL345_I2C::GetI2CDeviceAddress, release_gil()
  )
  
  
  
    
  .
def
("setRange", &frc::ADXL345_I2C::SetRange,
      py::arg("range"), release_gil(), py::doc(
    "Set the measuring range of the accelerometer.\n"
"\n"
":param range: The maximum acceleration, positive or negative, that the\n"
"              accelerometer will measure.")
  )
  
  
  
    
  .
def
("getX", &frc::ADXL345_I2C::GetX, release_gil(), py::doc(
    "Returns the acceleration along the X axis in g-forces.\n"
"\n"
":returns: The acceleration along the X axis in g-forces.")
  )
  
  
  
    
  .
def
("getY", &frc::ADXL345_I2C::GetY, release_gil(), py::doc(
    "Returns the acceleration along the Y axis in g-forces.\n"
"\n"
":returns: The acceleration along the Y axis in g-forces.")
  )
  
  
  
    
  .
def
("getZ", &frc::ADXL345_I2C::GetZ, release_gil(), py::doc(
    "Returns the acceleration along the Z axis in g-forces.\n"
"\n"
":returns: The acceleration along the Z axis in g-forces.")
  )
  
  
  
    
  .
def
("getAcceleration", &frc::ADXL345_I2C::GetAcceleration,
      py::arg("axis"), release_gil(), py::doc(
    "Get the acceleration of one axis in Gs.\n"
"\n"
":param axis: The axis to read from.\n"
"\n"
":returns: Acceleration of the ADXL345 in Gs.")
  )
  
  
  
    
  .
def
("getAccelerations", &frc::ADXL345_I2C::GetAccelerations, release_gil(), py::doc(
    "Get the acceleration of all axes in Gs.\n"
"\n"
":returns: An object containing the acceleration measured on each axis of the\n"
"          ADXL345 in Gs.")
  )
  
  
  
    
  .
def
("initSendable", &frc::ADXL345_I2C::InitSendable,
      py::arg("builder"), release_gil()
  )
  
  
  
    .def_readonly_static("kAddress", &frc::ADXL345_I2C::kAddress, py::doc(
    "Default I2C device address."))
  ;

  


  

  cls_AllAxes.doc() =
    "Container type for accelerations from all axes.";

  cls_AllAxes
  
    .def(py::init<>(), release_gil())
  
    .def_readwrite("XAxis", &frc::ADXL345_I2C::AllAxes::XAxis, py::doc(
    "Acceleration along the X axis in g-forces."))
  
    .def_readwrite("YAxis", &frc::ADXL345_I2C::AllAxes::YAxis, py::doc(
    "Acceleration along the Y axis in g-forces."))
  
    .def_readwrite("ZAxis", &frc::ADXL345_I2C::AllAxes::ZAxis, py::doc(
    "Acceleration along the Z axis in g-forces."))
  ;

  


  
  }






}

}; // struct rpybuild_ADXL345_I2C_initializer

static std::unique_ptr<rpybuild_ADXL345_I2C_initializer> cls;

void begin_init_ADXL345_I2C(py::module &m) {
  cls = std::make_unique<rpybuild_ADXL345_I2C_initializer>(m);
}

void finish_init_ADXL345_I2C() {
  cls->finish();
  cls.reset();
}