
// This file is autogenerated. DO NOT EDIT
#include <robotpy_build.h>




#include <hal/DutyCycle.h>
















#include <type_traits>






struct rpybuild_DutyCycle_initializer {













  py::module &m;

  
  rpybuild_DutyCycle_initializer(py::module &m) :

  

  

  

  

    m(m)
  {
    
    

    
  }

void finish() {







m
  .
def
("initializeDutyCycle", [](HAL_Handle digitalSourceHandle, HAL_AnalogTriggerType triggerType) {
                    int32_t status;
          auto __ret =::HAL_InitializeDutyCycle(std::move(digitalSourceHandle), std::move(triggerType), &status);
          return std::make_tuple(__ret,status);
        },
      py::arg("digitalSourceHandle"), py::arg("triggerType"), release_gil(), py::doc(
    "Initialize a DutyCycle input.\n"
"\n"
":param in:  digitalSourceHandle the digital source to use (either a\n"
"            HAL_DigitalHandle or a\n"
"            HAL_AnalogTriggerHandle)\n"
":param in:  triggerType the analog trigger type of the source if it is\n"
"            an analog trigger\n"
":param out: status Error status variable. 0 on success.\n"
"\n"
":returns: the created duty cycle handle")
  )
  
  ;
m
  .
def
("freeDutyCycle", &::HAL_FreeDutyCycle,
      py::arg("dutyCycleHandle"), release_gil(), py::doc(
    "Free a DutyCycle.\n"
"\n"
":param dutyCycleHandle: the duty cycle handle")
  )
  
  ;
m
  

  #ifndef __FRC_ROBORIO__
  .
def
("setDutyCycleSimDevice", &::HAL_SetDutyCycleSimDevice,
      py::arg("handle"), py::arg("device"), release_gil(), py::doc(
    "Indicates the duty cycle is used by a simulated device.\n"
"\n"
":param handle: the duty cycle handle\n"
":param device: simulated device handle")
  )
  
  
  #endif // __FRC_ROBORIO__
  ;
m
  .
def
("getDutyCycleFrequency", [](HAL_DutyCycleHandle dutyCycleHandle) {
                    int32_t status;
          auto __ret =::HAL_GetDutyCycleFrequency(std::move(dutyCycleHandle), &status);
          return std::make_tuple(__ret,status);
        },
      py::arg("dutyCycleHandle"), release_gil(), py::doc(
    "Get the frequency of the duty cycle signal.\n"
"\n"
":param in:  dutyCycleHandle the duty cycle handle\n"
":param out: status Error status variable. 0 on success.\n"
"\n"
":returns: frequency in Hertz")
  )
  
  ;
m
  .
def
("getDutyCycleOutput", [](HAL_DutyCycleHandle dutyCycleHandle) {
                    int32_t status;
          auto __ret =::HAL_GetDutyCycleOutput(std::move(dutyCycleHandle), &status);
          return std::make_tuple(__ret,status);
        },
      py::arg("dutyCycleHandle"), release_gil(), py::doc(
    "Get the output ratio of the duty cycle signal.\n"
"\n"
"0 means always low, 1 means always high.\n"
"\n"
":param in:  dutyCycleHandle the duty cycle handle\n"
":param out: status Error status variable. 0 on success.\n"
"\n"
":returns: output ratio between 0 and 1")
  )
  
  ;
m
  .
def
("getDutyCycleHighTime", [](HAL_DutyCycleHandle dutyCycleHandle) {
                    int32_t status;
          auto __ret =::HAL_GetDutyCycleHighTime(std::move(dutyCycleHandle), &status);
          return std::make_tuple(__ret,status);
        },
      py::arg("dutyCycleHandle"), release_gil(), py::doc(
    "Get the raw high time of the duty cycle signal.\n"
"\n"
":param in:  dutyCycleHandle the duty cycle handle\n"
":param out: status Error status variable. 0 on success.\n"
"\n"
":returns: high time of last pulse in nanoseconds")
  )
  
  ;
m
  .
def
("getDutyCycleOutputScaleFactor", [](HAL_DutyCycleHandle dutyCycleHandle) {
                    int32_t status;
          auto __ret =::HAL_GetDutyCycleOutputScaleFactor(std::move(dutyCycleHandle), &status);
          return std::make_tuple(__ret,status);
        },
      py::arg("dutyCycleHandle"), release_gil(), py::doc(
    "Get the scale factor of the output.\n"
"\n"
"An output equal to this value is always high, and then linearly scales\n"
"down to 0. Divide a raw result by this in order to get the\n"
"percentage between 0 and 1. Used by DMA.\n"
"\n"
":param in:  dutyCycleHandle the duty cycle handle\n"
":param out: status Error status variable. 0 on success.\n"
"\n"
":returns: the output scale factor")
  )
  
  ;
m
  .
def
("getDutyCycleFPGAIndex", [](HAL_DutyCycleHandle dutyCycleHandle) {
                    int32_t status;
          auto __ret =::HAL_GetDutyCycleFPGAIndex(std::move(dutyCycleHandle), &status);
          return std::make_tuple(__ret,status);
        },
      py::arg("dutyCycleHandle"), release_gil(), py::doc(
    "Get the FPGA index for the DutyCycle.\n"
"\n"
":param in:  dutyCycleHandle the duty cycle handle\n"
":param out: status Error status variable. 0 on success.\n"
"\n"
":returns: the FPGA index")
  )
  
  ;



}

}; // struct rpybuild_DutyCycle_initializer

static std::unique_ptr<rpybuild_DutyCycle_initializer> cls;

void begin_init_DutyCycle(py::module &m) {
  cls = std::make_unique<rpybuild_DutyCycle_initializer>(m);
}

void finish_init_DutyCycle() {
  cls->finish();
  cls.reset();
}