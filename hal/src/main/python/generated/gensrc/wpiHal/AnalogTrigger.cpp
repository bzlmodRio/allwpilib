
// This file is autogenerated. DO NOT EDIT
#include <robotpy_build.h>




#include <hal/AnalogTrigger.h>
















#include <type_traits>






struct rpybuild_AnalogTrigger_initializer {







  
  py::enum_<::HAL_AnalogTriggerType> enum1;







  py::module &m;

  
  rpybuild_AnalogTrigger_initializer(py::module &m) :

  

  
    enum1
  (m, "AnalogTriggerType"
  ,
    "The type of analog trigger to trigger on."),
  

  

  

    m(m)
  {
    
    
      enum1
  
    .value("kInWindow", ::HAL_AnalogTriggerType::HAL_Trigger_kInWindow)
  
    .value("kState", ::HAL_AnalogTriggerType::HAL_Trigger_kState)
  
    .value("kRisingPulse", ::HAL_AnalogTriggerType::HAL_Trigger_kRisingPulse)
  
    .value("kFallingPulse", ::HAL_AnalogTriggerType::HAL_Trigger_kFallingPulse)
  ;

    

    
  }

void finish() {







m
  .
def
("initializeAnalogTrigger", [](HAL_AnalogInputHandle portHandle) {
                    int32_t status;
          auto __ret =::HAL_InitializeAnalogTrigger(std::move(portHandle), &status);
          return std::make_tuple(__ret,status);
        },
      py::arg("portHandle"), release_gil(), py::doc(
    "Initializes an analog trigger.\n"
"\n"
":param in:  portHandle the analog input to use for triggering\n"
":param out: status     Error status variable. 0 on success.\n"
"\n"
":returns: the created analog trigger handle")
  )
  
  ;
m
  .
def
("initializeAnalogTriggerDutyCycle", [](HAL_DutyCycleHandle dutyCycleHandle) {
                    int32_t status;
          auto __ret =::HAL_InitializeAnalogTriggerDutyCycle(std::move(dutyCycleHandle), &status);
          return std::make_tuple(__ret,status);
        },
      py::arg("dutyCycleHandle"), release_gil(), py::doc(
    "Initializes an analog trigger with a Duty Cycle input\n"
"\n"
":param in:  dutyCycleHandle the analog input to use for duty cycle\n"
":param out: status          Error status variable. 0 on success.\n"
"\n"
":returns: tbe created analog trigger handle")
  )
  
  ;
m
  .
def
("cleanAnalogTrigger", [](HAL_AnalogTriggerHandle analogTriggerHandle) {
                    int32_t status;
          ::HAL_CleanAnalogTrigger(std::move(analogTriggerHandle), &status);
          return status;
        },
      py::arg("analogTriggerHandle"), release_gil(), py::doc(
    "Frees an analog trigger.\n"
"\n"
":param in:  analogTriggerHandle the trigger handle\n"
":param out: status Error status variable. 0 on success.")
  )
  
  ;
m
  .
def
("setAnalogTriggerLimitsRaw", [](HAL_AnalogTriggerHandle analogTriggerHandle, int32_t lower, int32_t upper) {
                    int32_t status;
          ::HAL_SetAnalogTriggerLimitsRaw(std::move(analogTriggerHandle), std::move(lower), std::move(upper), &status);
          return status;
        },
      py::arg("analogTriggerHandle"), py::arg("lower"), py::arg("upper"), release_gil(), py::doc(
    "Sets the raw ADC upper and lower limits of the analog trigger.\n"
"\n"
"HAL_SetAnalogTriggerLimitsVoltage or HAL_SetAnalogTriggerLimitsDutyCycle\n"
"is likely better in most cases.\n"
"\n"
":param in:  analogTriggerHandle the trigger handle\n"
":param in:  lower               the lower ADC value\n"
":param in:  upper               the upper ADC value\n"
":param out: status              Error status variable. 0 on success.")
  )
  
  ;
m
  .
def
("setAnalogTriggerLimitsVoltage", [](HAL_AnalogTriggerHandle analogTriggerHandle, double lower, double upper) {
                    int32_t status;
          ::HAL_SetAnalogTriggerLimitsVoltage(std::move(analogTriggerHandle), std::move(lower), std::move(upper), &status);
          return status;
        },
      py::arg("analogTriggerHandle"), py::arg("lower"), py::arg("upper"), release_gil(), py::doc(
    "Sets the upper and lower limits of the analog trigger.\n"
"\n"
"The limits are given as floating point voltage values.\n"
"\n"
":param in:  analogTriggerHandle the trigger handle\n"
":param in:  lower               the lower voltage value\n"
":param in:  upper               the upper voltage value\n"
":param out: status              Error status variable. 0 on success.")
  )
  
  ;
m
  .
def
("setAnalogTriggerLimitsDutyCycle", [](HAL_AnalogTriggerHandle analogTriggerHandle, double lower, double upper) {
                    int32_t status;
          ::HAL_SetAnalogTriggerLimitsDutyCycle(std::move(analogTriggerHandle), std::move(lower), std::move(upper), &status);
          return status;
        },
      py::arg("analogTriggerHandle"), py::arg("lower"), py::arg("upper"), release_gil(), py::doc(
    "Sets the upper and lower limits of the analog trigger.\n"
"\n"
"The limits are given as floating point duty cycle values.\n"
"\n"
":param in:  analogTriggerHandle the trigger handle\n"
":param in:  lower               the lower duty cycle value\n"
":param in:  upper               the upper duty cycle value\n"
":param out: status              Error status variable. 0 on success.")
  )
  
  ;
m
  .
def
("setAnalogTriggerAveraged", [](HAL_AnalogTriggerHandle analogTriggerHandle, HAL_Bool useAveragedValue) {
                    int32_t status;
          ::HAL_SetAnalogTriggerAveraged(std::move(analogTriggerHandle), std::move(useAveragedValue), &status);
          return status;
        },
      py::arg("analogTriggerHandle"), py::arg("useAveragedValue"), release_gil(), py::doc(
    "Configures the analog trigger to use the averaged vs. raw values.\n"
"\n"
"If the value is true, then the averaged value is selected for the analog\n"
"trigger, otherwise the immediate value is used.\n"
"\n"
"This is not allowed to be used if filtered mode is set.\n"
"This is not allowed to be used with Duty Cycle based inputs.\n"
"\n"
":param in:  analogTriggerHandle the trigger handle\n"
":param in:  useAveragedValue    true to use averaged values, false for raw\n"
":param out: status              Error status variable. 0 on success.")
  )
  
  ;
m
  .
def
("setAnalogTriggerFiltered", [](HAL_AnalogTriggerHandle analogTriggerHandle, HAL_Bool useFilteredValue) {
                    int32_t status;
          ::HAL_SetAnalogTriggerFiltered(std::move(analogTriggerHandle), std::move(useFilteredValue), &status);
          return status;
        },
      py::arg("analogTriggerHandle"), py::arg("useFilteredValue"), release_gil(), py::doc(
    "Configures the analog trigger to use a filtered value.\n"
"\n"
"The analog trigger will operate with a 3 point average rejection filter. This\n"
"is designed to help with 360 degree pot applications for the period where the\n"
"pot crosses through zero.\n"
"\n"
"This is not allowed to be used if averaged mode is set.\n"
"\n"
":param in:  analogTriggerHandle the trigger handle\n"
":param in:  useFilteredValue    true to use filtered values, false for average\n"
"            or raw\n"
":param out: status             Error status variable. 0 on success.")
  )
  
  ;
m
  .
def
("getAnalogTriggerInWindow", [](HAL_AnalogTriggerHandle analogTriggerHandle) {
                    int32_t status;
          auto __ret =::HAL_GetAnalogTriggerInWindow(std::move(analogTriggerHandle), &status);
          return std::make_tuple(__ret,status);
        },
      py::arg("analogTriggerHandle"), release_gil(), py::doc(
    "Returns the InWindow output of the analog trigger.\n"
"\n"
"True if the analog input is between the upper and lower limits.\n"
"\n"
":param in:  analogTriggerHandle the trigger handle\n"
":param out: status Error status variable. 0 on success.\n"
"\n"
":returns: the InWindow output of the analog trigger")
  )
  
  ;
m
  .
def
("getAnalogTriggerTriggerState", [](HAL_AnalogTriggerHandle analogTriggerHandle) {
                    int32_t status;
          auto __ret =::HAL_GetAnalogTriggerTriggerState(std::move(analogTriggerHandle), &status);
          return std::make_tuple(__ret,status);
        },
      py::arg("analogTriggerHandle"), release_gil(), py::doc(
    "Returns the TriggerState output of the analog trigger.\n"
"\n"
"True if above upper limit.\n"
"False if below lower limit.\n"
"If in Hysteresis, maintain previous state.\n"
"\n"
":param in:  analogTriggerHandle the trigger handle\n"
":param out: status              Error status variable. 0 on success.\n"
"\n"
":returns: the TriggerState output of the analog trigger")
  )
  
  ;
m
  .
def
("getAnalogTriggerOutput", [](HAL_AnalogTriggerHandle analogTriggerHandle, HAL_AnalogTriggerType type) {
                    int32_t status;
          auto __ret =::HAL_GetAnalogTriggerOutput(std::move(analogTriggerHandle), std::move(type), &status);
          return std::make_tuple(__ret,status);
        },
      py::arg("analogTriggerHandle"), py::arg("type"), release_gil(), py::doc(
    "Gets the state of the analog trigger output.\n"
"\n"
":param in:  analogTriggerHandle the trigger handle\n"
":param in:  type                the type of trigger to trigger on\n"
":param out: status              Error status variable. 0 on success.\n"
"\n"
":returns: the state of the analog trigger output")
  )
  
  ;
m
  .
def
("getAnalogTriggerFPGAIndex", [](HAL_AnalogTriggerHandle analogTriggerHandle) {
                    int32_t status;
          auto __ret =::HAL_GetAnalogTriggerFPGAIndex(std::move(analogTriggerHandle), &status);
          return std::make_tuple(__ret,status);
        },
      py::arg("analogTriggerHandle"), release_gil(), py::doc(
    "Get the FPGA index for the AnlogTrigger.\n"
"\n"
":param in:  analogTriggerHandle the trigger handle\n"
":param out: status              Error status variable. 0 on success.\n"
"\n"
":returns: the FPGA index")
  )
  
  ;



}

}; // struct rpybuild_AnalogTrigger_initializer

static std::unique_ptr<rpybuild_AnalogTrigger_initializer> cls;

void begin_init_AnalogTrigger(py::module &m) {
  cls = std::make_unique<rpybuild_AnalogTrigger_initializer>(m);
}

void finish_init_AnalogTrigger() {
  cls->finish();
  cls.reset();
}