
// This file is autogenerated. DO NOT EDIT
#include <robotpy_build.h>




#include <frc/controller/BangBangController.h>








#define RPYGEN_ENABLE_frc__BangBangController_PROTECTED_CONSTRUCTORS
#include <rpygen/frc__BangBangController.hpp>









#include <type_traits>


  using namespace frc;





struct rpybuild_BangBangController_initializer {


  

  




  py::module pkg_controller;









  
  using BangBangController_Trampoline = rpygen::PyTrampoline_frc__BangBangController<typename frc::BangBangController, typename rpygen::PyTrampolineCfg_frc__BangBangController<>>;
    static_assert(std::is_abstract<BangBangController_Trampoline>::value == false, "frc::BangBangController " RPYBUILD_BAD_TRAMPOLINE);
  py::class_<typename frc::BangBangController, BangBangController_Trampoline, wpi::Sendable> cls_BangBangController;

    

    
    

  py::module &m;

  
  rpybuild_BangBangController_initializer(py::module &m) :

  
    pkg_controller(m.def_submodule("controller")),
  

  

  

  
    cls_BangBangController(pkg_controller, "BangBangController"),

  

  
  
  

    m(m)
  {
    
    

    
    
  

    
    
  }

void finish() {





  {
  
  
  


  

  cls_BangBangController.doc() =
    "Implements a bang-bang controller, which outputs either 0 or 1 depending on\n"
"whether the measurement is less than the setpoint. This maximally-aggressive\n"
"control approach works very well for velocity control of high-inertia\n"
"mechanisms, and poorly on most other things.\n"
"\n"
"Note that this is an *asymmetric* bang-bang controller - it will not exert\n"
"any control effort in the reverse direction (e.g. it won't try to slow down\n"
"an over-speeding shooter wheel). This asymmetry is *extremely important.*\n"
"Bang-bang control is extremely simple, but also potentially hazardous. Always\n"
"ensure that your motor controllers are set to \"coast\" before attempting to\n"
"control them with a bang-bang controller.";

  cls_BangBangController
  
    
  .def(py::init<double>(),
      py::arg("tolerance") = std::numeric_limits<double>::infinity (), release_gil(), py::doc(
    "Creates a new bang-bang controller.\n"
"\n"
"Always ensure that your motor controllers are set to \"coast\" before\n"
"attempting to control them with a bang-bang controller.\n"
"\n"
":param tolerance: Tolerance for atSetpoint.")
  )
  
  
  
    
  .
def
("setSetpoint", &frc::BangBangController::SetSetpoint,
      py::arg("setpoint"), release_gil(), py::doc(
    "Sets the setpoint for the bang-bang controller.\n"
"\n"
":param setpoint: The desired setpoint.")
  )
  
  
  
    
  .
def
("getSetpoint", &frc::BangBangController::GetSetpoint, release_gil(), py::doc(
    "Returns the current setpoint of the bang-bang controller.\n"
"\n"
":returns: The current setpoint.")
  )
  
  
  
    
  .
def
("atSetpoint", &frc::BangBangController::AtSetpoint, release_gil(), py::doc(
    "Returns true if the error is within the tolerance of the setpoint.\n"
"\n"
":returns: Whether the error is within the acceptable bounds.")
  )
  
  
  
    
  .
def
("setTolerance", &frc::BangBangController::SetTolerance,
      py::arg("tolerance"), release_gil(), py::doc(
    "Sets the error within which AtSetpoint will return true.\n"
"\n"
":param tolerance: Position error which is tolerable.")
  )
  
  
  
    
  .
def
("getTolerance", &frc::BangBangController::GetTolerance, release_gil(), py::doc(
    "Returns the current tolerance of the controller.\n"
"\n"
":returns: The current tolerance.")
  )
  
  
  
    
  .
def
("getMeasurement", &frc::BangBangController::GetMeasurement, release_gil(), py::doc(
    "Returns the current measurement of the process variable.\n"
"\n"
":returns: The current measurement of the process variable.")
  )
  
  
  
    
  .
def
("getError", &frc::BangBangController::GetError, release_gil(), py::doc(
    "Returns the current error.\n"
"\n"
":returns: The current error.")
  )
  
  
  
    
  .
def
("calculate", static_cast<double(frc::BangBangController::*)(double, double)>(
        &frc::BangBangController::Calculate),
      py::arg("measurement"), py::arg("setpoint"), release_gil(), py::doc(
    "Returns the calculated control output.\n"
"\n"
"Always ensure that your motor controllers are set to \"coast\" before\n"
"attempting to control them with a bang-bang controller.\n"
"\n"
":param measurement: The most recent measurement of the process variable.\n"
":param setpoint:    The setpoint for the process variable.\n"
"\n"
":returns: The calculated motor output (0 or 1).")
  )
  
  
  
    
  .
def
("calculate", static_cast<double(frc::BangBangController::*)(double)>(
        &frc::BangBangController::Calculate),
      py::arg("measurement"), release_gil(), py::doc(
    "Returns the calculated control output.\n"
"\n"
":param measurement: The most recent measurement of the process variable.\n"
"\n"
":returns: The calculated motor output (0 or 1).")
  )
  
  
  
    
  .
def
("initSendable", &frc::BangBangController::InitSendable,
      py::arg("builder"), release_gil()
  )
  
  
  ;

  


  }






}

}; // struct rpybuild_BangBangController_initializer

static std::unique_ptr<rpybuild_BangBangController_initializer> cls;

void begin_init_BangBangController(py::module &m) {
  cls = std::make_unique<rpybuild_BangBangController_initializer>(m);
}

void finish_init_BangBangController() {
  cls->finish();
  cls.reset();
}