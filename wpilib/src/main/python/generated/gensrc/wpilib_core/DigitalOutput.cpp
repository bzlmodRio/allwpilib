
// This file is autogenerated. DO NOT EDIT
#include <robotpy_build.h>




#include <frc/DigitalOutput.h>


#include <units_time_type_caster.h>







#define RPYGEN_ENABLE_frc__DigitalOutput_PROTECTED_CONSTRUCTORS
#include <rpygen/frc__DigitalOutput.hpp>







#include <wpi/sendable/SendableBuilder.h>



#include <type_traits>


  using namespace frc;





struct rpybuild_DigitalOutput_initializer {


  

  












  
  using DigitalOutput_Trampoline = rpygen::PyTrampoline_frc__DigitalOutput<typename frc::DigitalOutput, typename rpygen::PyTrampolineCfg_frc__DigitalOutput<>>;
    static_assert(std::is_abstract<DigitalOutput_Trampoline>::value == false, "frc::DigitalOutput " RPYBUILD_BAD_TRAMPOLINE);
  py::class_<typename frc::DigitalOutput, DigitalOutput_Trampoline, frc::DigitalSource, wpi::Sendable> cls_DigitalOutput;

    

    
    

  py::module &m;

  
  rpybuild_DigitalOutput_initializer(py::module &m) :

  

  

  

  
    cls_DigitalOutput(m, "DigitalOutput"),

  

  
  
  

    m(m)
  {
    
    

    
    
  

    
    
  }

void finish() {





  {
  
  
  


  

  cls_DigitalOutput.doc() =
    "Class to write to digital outputs.\n"
"\n"
"Write values to the digital output channels. Other devices implemented\n"
"elsewhere will allocate channels automatically so for those devices it\n"
"shouldn't be done here.";

  cls_DigitalOutput
  
    
  .def(py::init<int>(),
      py::arg("channel"), release_gil(), py::doc(
    "Create an instance of a digital output.\n"
"\n"
"Create a digital output given a channel.\n"
"\n"
":param channel: The digital channel 0-9 are on-board, 10-25 are on the MXP\n"
"                port")
  )
  
  
  
    
  .
def
("set", &frc::DigitalOutput::Set,
      py::arg("value"), release_gil(), py::doc(
    "Set the value of a digital output.\n"
"\n"
"Set the value of a digital output to either one (true) or zero (false).\n"
"\n"
":param value: 1 (true) for high, 0 (false) for disabled")
  )
  
  
  
    
  .
def
("get", &frc::DigitalOutput::Get, release_gil(), py::doc(
    "Gets the value being output from the Digital Output.\n"
"\n"
":returns: the state of the digital output.")
  )
  
  
  
    
  .
def
("getPortHandleForRouting", &frc::DigitalOutput::GetPortHandleForRouting, release_gil(), py::doc(
    "\n"
"\n"
":returns: The HAL Handle to the specified source.")
  )
  
  
  
    
  .
def
("getAnalogTriggerTypeForRouting", &frc::DigitalOutput::GetAnalogTriggerTypeForRouting, release_gil(), py::doc(
    "\n"
"\n"
":returns: The type of analog trigger output to be used. 0 for Digitals")
  )
  
  
  
    
  .
def
("isAnalogTrigger", &frc::DigitalOutput::IsAnalogTrigger, release_gil(), py::doc(
    "Is source an AnalogTrigger")
  )
  
  
  
    
  .
def
("getChannel", &frc::DigitalOutput::GetChannel, release_gil(), py::doc(
    "\n"
"\n"
":returns: The GPIO channel number that this object represents.")
  )
  
  
  
    
  .
def
("pulse", &frc::DigitalOutput::Pulse,
      py::arg("pulseLength"), release_gil(), py::doc(
    "Output a single pulse on the digital output line.\n"
"\n"
"Send a single pulse on the digital output line where the pulse duration is\n"
"specified in seconds. Maximum of 65535 microseconds.\n"
"\n"
":param pulseLength: The pulse length in seconds")
  )
  
  
  
    
  .
def
("isPulsing", &frc::DigitalOutput::IsPulsing, release_gil(), py::doc(
    "Determine if the pulse is still going.\n"
"\n"
"Determine if a previously started pulse is still going.")
  )
  
  
  
    
  .
def
("setPWMRate", &frc::DigitalOutput::SetPWMRate,
      py::arg("rate"), release_gil(), py::doc(
    "Change the PWM frequency of the PWM output on a Digital Output line.\n"
"\n"
"The valid range is from 0.6 Hz to 19 kHz.  The frequency resolution is\n"
"logarithmic.\n"
"\n"
"There is only one PWM frequency for all digital channels.\n"
"\n"
":param rate: The frequency to output all digital output PWM signals.")
  )
  
  
  
    
  .
def
("enablePPS", &frc::DigitalOutput::EnablePPS,
      py::arg("dutyCycle"), release_gil(), py::doc(
    "Enable a PWM PPS (Pulse Per Second) Output on this line.\n"
"\n"
"Allocate one of the 6 DO PWM generator resources from this module.\n"
"\n"
"Supply the duty-cycle to output.\n"
"\n"
"The resolution of the duty cycle is 8-bit.\n"
"\n"
":param dutyCycle: The duty-cycle to start generating. [0..1]")
  )
  
  
  
    
  .
def
("enablePWM", &frc::DigitalOutput::EnablePWM,
      py::arg("initialDutyCycle"), release_gil(), py::doc(
    "Enable a PWM Output on this line.\n"
"\n"
"Allocate one of the 6 DO PWM generator resources from this module.\n"
"\n"
"Supply the initial duty-cycle to output so as to avoid a glitch when first\n"
"starting.\n"
"\n"
"The resolution of the duty cycle is 8-bit for low frequencies (1kHz or\n"
"less) but is reduced the higher the frequency of the PWM signal is.\n"
"\n"
":param initialDutyCycle: The duty-cycle to start generating. [0..1]")
  )
  
  
  
    
  .
def
("disablePWM", &frc::DigitalOutput::DisablePWM, release_gil(), py::doc(
    "Change this line from a PWM output back to a static Digital Output line.\n"
"\n"
"Free up one of the 6 DO PWM generator resources that were in use.")
  )
  
  
  
    
  .
def
("updateDutyCycle", &frc::DigitalOutput::UpdateDutyCycle,
      py::arg("dutyCycle"), release_gil(), py::doc(
    "Change the duty-cycle that is being generated on the line.\n"
"\n"
"The resolution of the duty cycle is 8-bit for low frequencies (1kHz or\n"
"less) but is reduced the higher the frequency of the PWM signal is.\n"
"\n"
":param dutyCycle: The duty-cycle to change to. [0..1]")
  )
  
  
  
    
  .
def
("setSimDevice", &frc::DigitalOutput::SetSimDevice,
      py::arg("device"), release_gil(), py::doc(
    "Indicates this output is used by a simulated device.\n"
"\n"
":param device: simulated device handle")
  )
  
  
  
    
  .
def
("initSendable", &frc::DigitalOutput::InitSendable,
      py::arg("builder"), release_gil()
  )
  
  
  ;

  


  }






}

}; // struct rpybuild_DigitalOutput_initializer

static std::unique_ptr<rpybuild_DigitalOutput_initializer> cls;

void begin_init_DigitalOutput(py::module &m) {
  cls = std::make_unique<rpybuild_DigitalOutput_initializer>(m);
}

void finish_init_DigitalOutput() {
  cls->finish();
  cls.reset();
}