
// This file is autogenerated. DO NOT EDIT
#include <robotpy_build.h>




#include <frc/DutyCycleEncoder.h>


#include <units_angle_type_caster.h>







#define RPYGEN_ENABLE_frc__DutyCycleEncoder_PROTECTED_CONSTRUCTORS
#include <rpygen/frc__DutyCycleEncoder.hpp>







#include <wpi/sendable/SendableBuilder.h>

#include <frc/DutyCycle.h>

#include <frc/DigitalSource.h>



#include <type_traits>


  using namespace frc;





struct rpybuild_DutyCycleEncoder_initializer {


  

  












  
  using DutyCycleEncoder_Trampoline = rpygen::PyTrampoline_frc__DutyCycleEncoder<typename frc::DutyCycleEncoder, typename rpygen::PyTrampolineCfg_frc__DutyCycleEncoder<>>;
    static_assert(std::is_abstract<DutyCycleEncoder_Trampoline>::value == false, "frc::DutyCycleEncoder " RPYBUILD_BAD_TRAMPOLINE);
  py::class_<typename frc::DutyCycleEncoder, DutyCycleEncoder_Trampoline, wpi::Sendable> cls_DutyCycleEncoder;

    

    
    

  py::module &m;

  
  rpybuild_DutyCycleEncoder_initializer(py::module &m) :

  

  

  

  
    cls_DutyCycleEncoder(m, "DutyCycleEncoder"),

  

  
  
  

    m(m)
  {
    
    

    
    
  

    
    
  }

void finish() {





  {
  
  
  


  

  cls_DutyCycleEncoder.doc() =
    "Class for supporting duty cycle/PWM encoders, such as the US Digital MA3 with\n"
"PWM Output, the CTRE Mag Encoder, the Rev Hex Encoder, and the AM Mag\n"
"Encoder.";

  cls_DutyCycleEncoder
  
    
  .def(py::init<int>(),
      py::arg("channel"), release_gil(), py::doc(
    "Construct a new DutyCycleEncoder on a specific channel.\n"
"\n"
":param channel: the channel to attach to")
  )
  
  
  
    
  .def(py::init<std::shared_ptr<DutyCycle>>(),
      py::arg("dutyCycle"), release_gil(), py::doc(
    "Construct a new DutyCycleEncoder attached to an existing DutyCycle object.\n"
"\n"
":param dutyCycle: the duty cycle to attach to")
  )
  
  
  
    
  .def(py::init<std::shared_ptr<DigitalSource>>(),
      py::arg("digitalSource"), release_gil(), py::doc(
    "Construct a new DutyCycleEncoder attached to a DigitalSource object.\n"
"\n"
":param digitalSource: the digital source to attach to")
  )
  
  
  
    
  .
def
("getFrequency", &frc::DutyCycleEncoder::GetFrequency, release_gil(), py::doc(
    "Get the frequency in Hz of the duty cycle signal from the encoder.\n"
"\n"
":returns: duty cycle frequency in Hz")
  )
  
  
  
    
  .
def
("isConnected", &frc::DutyCycleEncoder::IsConnected, release_gil(), py::doc(
    "Get if the sensor is connected\n"
"\n"
"This uses the duty cycle frequency to determine if the sensor is connected.\n"
"By default, a value of 100 Hz is used as the threshold, and this value can\n"
"be changed with SetConnectedFrequencyThreshold.\n"
"\n"
":returns: true if the sensor is connected")
  )
  
  
  
    
  .
def
("setConnectedFrequencyThreshold", &frc::DutyCycleEncoder::SetConnectedFrequencyThreshold,
      py::arg("frequency"), release_gil(), py::doc(
    "Change the frequency threshold for detecting connection used by\n"
"IsConnected.\n"
"\n"
":param frequency: the minimum frequency in Hz.")
  )
  
  
  
    
  .
def
("reset", &frc::DutyCycleEncoder::Reset, release_gil(), py::doc(
    "Reset the Encoder distance to zero.")
  )
  
  
  
    
  .
def
("get", &frc::DutyCycleEncoder::Get, release_gil(), py::doc(
    "Get the encoder value since the last reset.\n"
"\n"
"This is reported in rotations since the last reset.\n"
"\n"
":returns: the encoder value in rotations")
  )
  
  
  
    
  .
def
("getAbsolutePosition", &frc::DutyCycleEncoder::GetAbsolutePosition, release_gil(), py::doc(
    "Get the absolute position of the duty cycle encoder encoder.\n"
"\n"
"GetAbsolutePosition() - GetPositionOffset() will give an encoder\n"
"absolute position relative to the last reset. This could potentially be\n"
"negative, which needs to be accounted for.\n"
"\n"
"This will not account for rollovers, and will always be just the raw\n"
"absolute position.\n"
"\n"
":returns: the absolute position")
  )
  
  
  
    
  .
def
("getPositionOffset", &frc::DutyCycleEncoder::GetPositionOffset, release_gil(), py::doc(
    "Get the offset of position relative to the last reset.\n"
"\n"
"GetAbsolutePosition() - GetPositionOffset() will give an encoder absolute\n"
"position relative to the last reset. This could potentially be negative,\n"
"which needs to be accounted for.\n"
"\n"
":returns: the position offset")
  )
  
  
  
    
  .
def
("setPositionOffset", &frc::DutyCycleEncoder::SetPositionOffset,
      py::arg("offset"), release_gil(), py::doc(
    "Set the position offset.\n"
"\n"
"This must be in the range of 0-1.\n"
"\n"
":param offset: the offset")
  )
  
  
  
    
  .
def
("setDutyCycleRange", &frc::DutyCycleEncoder::SetDutyCycleRange,
      py::arg("min"), py::arg("max"), release_gil(), py::doc(
    "Set the encoder duty cycle range. As the encoder needs to maintain a duty\n"
"cycle, the duty cycle cannot go all the way to 0% or all the way to 100%.\n"
"For example, an encoder with a 4096 us period might have a minimum duty\n"
"cycle of 1 us / 4096 us and a maximum duty cycle of 4095 / 4096 us. Setting\n"
"the range will result in an encoder duty cycle less than or equal to the\n"
"minimum being output as 0 rotation, the duty cycle greater than or equal to\n"
"the maximum being output as 1 rotation, and values in between linearly\n"
"scaled from 0 to 1.\n"
"\n"
":param min: minimum duty cycle (0-1 range)\n"
":param max: maximum duty cycle (0-1 range)")
  )
  
  
  
    
  .
def
("setDistancePerRotation", &frc::DutyCycleEncoder::SetDistancePerRotation,
      py::arg("distancePerRotation"), release_gil(), py::doc(
    "Set the distance per rotation of the encoder. This sets the multiplier used\n"
"to determine the distance driven based on the rotation value from the\n"
"encoder. Set this value based on the how far the mechanism travels in 1\n"
"rotation of the encoder, and factor in gearing reductions following the\n"
"encoder shaft. This distance can be in any units you like, linear or\n"
"angular.\n"
"\n"
":param distancePerRotation: the distance per rotation of the encoder")
  )
  
  
  
    
  .
def
("getDistancePerRotation", &frc::DutyCycleEncoder::GetDistancePerRotation, release_gil(), py::doc(
    "Get the distance per rotation for this encoder.\n"
"\n"
":returns: The scale factor that will be used to convert rotation to useful\n"
"          units.")
  )
  
  
  
    
  .
def
("getDistance", &frc::DutyCycleEncoder::GetDistance, release_gil(), py::doc(
    "Get the distance the sensor has driven since the last reset as scaled by\n"
"the value from SetDistancePerRotation.\n"
"\n"
":returns: The distance driven since the last reset")
  )
  
  
  
    
  .
def
("getFPGAIndex", &frc::DutyCycleEncoder::GetFPGAIndex, release_gil(), py::doc(
    "Get the FPGA index for the DutyCycleEncoder.\n"
"\n"
":returns: the FPGA index")
  )
  
  
  
    
  .
def
("getSourceChannel", &frc::DutyCycleEncoder::GetSourceChannel, release_gil(), py::doc(
    "Get the channel of the source.\n"
"\n"
":returns: the source channel")
  )
  
  
  
    
  .
def
("initSendable", &frc::DutyCycleEncoder::InitSendable,
      py::arg("builder"), release_gil()
  )
  
  
  ;

  


  }







  cls_DutyCycleEncoder
  .def("__repr__", [](const DutyCycleEncoder &self) {
    return py::str("<DutyCycleEncoder {}>").format(self.GetSourceChannel());
  });


}

}; // struct rpybuild_DutyCycleEncoder_initializer

static std::unique_ptr<rpybuild_DutyCycleEncoder_initializer> cls;

void begin_init_DutyCycleEncoder(py::module &m) {
  cls = std::make_unique<rpybuild_DutyCycleEncoder_initializer>(m);
}

void finish_init_DutyCycleEncoder() {
  cls->finish();
  cls.reset();
}