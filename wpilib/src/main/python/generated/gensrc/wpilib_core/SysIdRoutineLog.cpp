
// This file is autogenerated. DO NOT EDIT
#include <robotpy_build.h>




#include <frc/sysid/SysIdRoutineLog.h>


#include <units_acceleration_type_caster.h>

#include <units_angle_type_caster.h>

#include <units_angular_acceleration_type_caster.h>

#include <units_angular_velocity_type_caster.h>

#include <units_current_type_caster.h>

#include <units_length_type_caster.h>

#include <units_velocity_type_caster.h>

#include <units_voltage_type_caster.h>

#include <wpi_string_map_caster.h>















#include <type_traits>


  using namespace frc::sysid;





struct rpybuild_SysIdRoutineLog_initializer {


  

  




  py::module pkg_sysid;




  
  py::enum_<frc::sysid::State> enum1;






  py::class_<typename frc::sysid::SysIdRoutineLog> cls_SysIdRoutineLog;

    

    
    
    py::class_<typename frc::sysid::SysIdRoutineLog::MotorLog> cls_MotorLog;

    

    
    
    

  py::module &m;

  
  rpybuild_SysIdRoutineLog_initializer(py::module &m) :

  
    pkg_sysid(m.def_submodule("sysid")),
  

  
    enum1
  (pkg_sysid, "State"
  ,
    "Possible state of a SysId routine."),
  

  

  
    cls_SysIdRoutineLog(pkg_sysid, "SysIdRoutineLog"),

  

  
  
    cls_MotorLog(cls_SysIdRoutineLog, "MotorLog"),

  

  
  
  
  

    m(m)
  {
    
    
      enum1
  
    .value("kQuasistaticForward", frc::sysid::State::kQuasistaticForward,
      "Quasistatic forward test.")
  
    .value("kQuasistaticReverse", frc::sysid::State::kQuasistaticReverse,
      "Quasistatic reverse test.")
  
    .value("kDynamicForward", frc::sysid::State::kDynamicForward,
      "Dynamic forward test.")
  
    .value("kDynamicReverse", frc::sysid::State::kDynamicReverse,
      "Dynamic reverse test.")
  
    .value("kNone", frc::sysid::State::kNone,
      "No test.")
  .def("__str__", &SysIdRoutineLog::StateEnumToString)
;

    

    
    
  

    
    
  

    
    
  }

void finish() {





  {
  
  using MotorLog [[maybe_unused]] = typename frc::sysid::SysIdRoutineLog::MotorLog;
  
  
  


  

  cls_SysIdRoutineLog.doc() =
    "Utility for logging data from a SysId test routine. Each complete routine\n"
"(quasistatic and dynamic, forward and reverse) should have its own\n"
"SysIdRoutineLog instance, with a unique log name.";

  cls_SysIdRoutineLog
  
    
  .def(py::init<std::string_view>(),
      py::arg("logName"), release_gil(), py::doc(
    "Create a new logging utility for a SysId test routine.\n"
"\n"
":param logName: The name for the test routine in the log. Should be unique\n"
"                between complete test routines (quasistatic and dynamic, forward and\n"
"                reverse). The current state of this test (e.g. \"quasistatic-forward\")\n"
"                will appear in WPILog under the \"sysid-test-state-logName\" entry.")
  )
  
  
  
    
  .
def
("recordState", &frc::sysid::SysIdRoutineLog::RecordState,
      py::arg("state"), release_gil(), py::doc(
    "Records the current state of the SysId test routine. Should be called once\n"
"per iteration during tests with the type of the current test, and once upon\n"
"test end with state `none`.\n"
"\n"
":param state: The current state of the SysId test routine.")
  )
  
  
  
    
  .
def
("motor", &frc::sysid::SysIdRoutineLog::Motor,
      py::arg("motorName"), release_gil(), py::doc(
    "Log data from a motor during a SysId routine.\n"
"\n"
":param motorName: The name of the motor.\n"
"\n"
":returns: Handle with chainable callbacks to log individual data fields.")
  )
  
  
  
    
  .
def_static
("stateEnumToString", &frc::sysid::SysIdRoutineLog::StateEnumToString,
      py::arg("state"), release_gil()
  )
  
  
  ;

  


  

  cls_MotorLog.doc() =
    "Logs data from a single motor during a SysIdRoutine.";

  cls_MotorLog
  
    
  .
def
("value", &frc::sysid::SysIdRoutineLog::MotorLog::value,
      py::arg("name"), py::arg("value"), py::arg("unit"), release_gil(), py::doc(
    "Log a generic data value from the motor.\n"
"\n"
":param name:  The name of the data field being recorded.\n"
":param value: The numeric value of the data field.\n"
":param unit:  The unit string of the data field.\n"
"\n"
":returns: The motor log (for call chaining).")
  )
  
  
  
    
  .
def
("voltage", &frc::sysid::SysIdRoutineLog::MotorLog::voltage,
      py::arg("voltage"), release_gil(), py::doc(
    "Log the voltage applied to the motor.\n"
"\n"
":param voltage: The voltage to record.\n"
"\n"
":returns: The motor log (for call chaining).")
  )
  
  
  
    
  .
def
("position", static_cast<MotorLog&(frc::sysid::SysIdRoutineLog::MotorLog::*)(units::meter_t)>(
        &frc::sysid::SysIdRoutineLog::MotorLog::position),
      py::arg("position"), release_gil(), py::doc(
    "Log the linear position of the motor.\n"
"\n"
":param position: The linear position to record.\n"
"\n"
":returns: The motor log (for call chaining).")
  )
  
  
  
    
  .
def
("angularPosition", static_cast<MotorLog&(frc::sysid::SysIdRoutineLog::MotorLog::*)(units::turn_t)>(
        &frc::sysid::SysIdRoutineLog::MotorLog::position),
      py::arg("position"), release_gil(), py::doc(
    "Log the angular position of the motor.\n"
"\n"
":param position: The angular position to record.\n"
"\n"
":returns: The motor log (for call chaining).")
  )
  
  
  
    
  .
def
("velocity", static_cast<MotorLog&(frc::sysid::SysIdRoutineLog::MotorLog::*)(units::meters_per_second_t)>(
        &frc::sysid::SysIdRoutineLog::MotorLog::velocity),
      py::arg("velocity"), release_gil(), py::doc(
    "Log the linear velocity of the motor.\n"
"\n"
":param velocity: The linear velocity to record.\n"
"\n"
":returns: The motor log (for call chaining).")
  )
  
  
  
    
  .
def
("angularVelocity", static_cast<MotorLog&(frc::sysid::SysIdRoutineLog::MotorLog::*)(units::turns_per_second_t)>(
        &frc::sysid::SysIdRoutineLog::MotorLog::velocity),
      py::arg("velocity"), release_gil(), py::doc(
    "Log the angular velocity of the motor.\n"
"\n"
":param velocity: The angular velocity to record.\n"
"\n"
":returns: The motor log (for call chaining).")
  )
  
  
  
    
  .
def
("acceleration", static_cast<MotorLog&(frc::sysid::SysIdRoutineLog::MotorLog::*)(units::meters_per_second_squared_t)>(
        &frc::sysid::SysIdRoutineLog::MotorLog::acceleration),
      py::arg("acceleration"), release_gil(), py::doc(
    "Log the linear acceleration of the motor.\n"
"\n"
"This is optional; SysId can perform an accurate fit without it.\n"
"\n"
":param acceleration: The linear acceleration to record.\n"
"\n"
":returns: The motor log (for call chaining).")
  )
  
  
  
    
  .
def
("angularAcceleration", static_cast<MotorLog&(frc::sysid::SysIdRoutineLog::MotorLog::*)(units::turns_per_second_squared_t)>(
        &frc::sysid::SysIdRoutineLog::MotorLog::acceleration),
      py::arg("acceleration"), release_gil(), py::doc(
    "Log the angular acceleration of the motor.\n"
"\n"
"This is optional; SysId can perform an accurate fit without it.\n"
"\n"
":param acceleration: The angular acceleration to record.\n"
"\n"
":returns: The motor log (for call chaining).")
  )
  
  
  
    
  .
def
("current", &frc::sysid::SysIdRoutineLog::MotorLog::current,
      py::arg("current"), release_gil(), py::doc(
    "Log the current applied to the motor.\n"
"\n"
"This is optional; SysId can perform an accurate fit without it.\n"
"\n"
":param current: The current to record.\n"
"\n"
":returns: The motor log (for call chaining).")
  )
  
  
  ;

  


  
  }






}

}; // struct rpybuild_SysIdRoutineLog_initializer

static std::unique_ptr<rpybuild_SysIdRoutineLog_initializer> cls;

void begin_init_SysIdRoutineLog(py::module &m) {
  cls = std::make_unique<rpybuild_SysIdRoutineLog_initializer>(m);
}

void finish_init_SysIdRoutineLog() {
  cls->finish();
  cls.reset();
}