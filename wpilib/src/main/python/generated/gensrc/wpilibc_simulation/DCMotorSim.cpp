
// This file is autogenerated. DO NOT EDIT
#include <robotpy_build.h>




#include <frc/simulation/DCMotorSim.h>


#include <pybind11/stl.h>

#include <units_angle_type_caster.h>

#include <units_angular_velocity_type_caster.h>

#include <units_current_type_caster.h>

#include <units_moment_of_inertia_type_caster.h>

#include <units_voltage_type_caster.h>







#define RPYGEN_ENABLE_frc__sim__DCMotorSim_PROTECTED_CONSTRUCTORS
#include <rpygen/frc__sim__DCMotorSim.hpp>









#include <type_traits>


  using namespace frc::sim;





struct rpybuild_DCMotorSim_initializer {


  
    using DCMotor = frc::DCMotor;
  

  












  
  using DCMotorSim_Trampoline = rpygen::PyTrampoline_frc__sim__DCMotorSim<typename frc::sim::DCMotorSim, typename rpygen::PyTrampolineCfg_frc__sim__DCMotorSim<>>;
    static_assert(std::is_abstract<DCMotorSim_Trampoline>::value == false, "frc::sim::DCMotorSim " RPYBUILD_BAD_TRAMPOLINE);
  py::class_<typename frc::sim::DCMotorSim, DCMotorSim_Trampoline, frc::sim::LinearSystemSim<2, 1, 2>> cls_DCMotorSim;

    

    
    

  py::module &m;

  
  rpybuild_DCMotorSim_initializer(py::module &m) :

  

  

  

  
    cls_DCMotorSim(m, "DCMotorSim"),

  

  
  
  

    m(m)
  {
    
    

    
    
  

    
    
  }

void finish() {





  {
  
  
  


  

  cls_DCMotorSim.doc() =
    "Represents a simulated DC motor mechanism.";

  cls_DCMotorSim
  
    
  .def(py::init<const frc::LinearSystem<2,1,2>&, const DCMotor&, double, const std::array<double, 2>&>(),
      py::arg("plant"), py::arg("gearbox"), py::arg("gearing"), py::arg("measurementStdDevs") = std::array<double, 2>{0.0, 0.0}, release_gil()
    , py::keep_alive<1, 2>()
    , py::keep_alive<1, 3>()
    , py::keep_alive<1, 5>(), py::doc(
    "Creates a simulated DC motor mechanism.\n"
"\n"
":param plant:              The linear system representing the DC motor. This\n"
"                           system can be created with\n"
"                           LinearSystemId::DCMotorSystem().\n"
":param gearbox:            The type of and number of motors in the DC motor\n"
"                           gearbox.\n"
":param gearing:            The gearing of the DC motor (numbers greater than\n"
"                           1 represent reductions).\n"
":param measurementStdDevs: The standard deviation of the measurement noise.")
  )
  
  
  
    
  .def(py::init<const DCMotor&, double, units::kilogram_square_meter_t, const std::array<double, 2>&>(),
      py::arg("gearbox"), py::arg("gearing"), py::arg("moi"), py::arg("measurementStdDevs") = std::array<double, 2>{0.0, 0.0}, release_gil()
    , py::keep_alive<1, 2>()
    , py::keep_alive<1, 5>(), py::doc(
    "Creates a simulated DC motor mechanism.\n"
"\n"
":param gearbox:            The type of and number of motors in the DC motor\n"
"                           gearbox.\n"
":param gearing:            The gearing of the DC motor (numbers greater than\n"
"                           1 represent reductions).\n"
":param moi:                The moment of inertia of the DC motor.\n"
":param measurementStdDevs: The standard deviation of the measurement noise.")
  )
  
  
  
    
  .
def
("setState", static_cast<void(frc::sim::DCMotorSim::*)(units::radian_t, units::radians_per_second_t)>(
        &frc::sim::DCMotorSim::SetState),
      py::arg("angularPosition"), py::arg("angularVelocity"), release_gil(), py::doc(
    "Sets the state of the DC motor.\n"
"\n"
":param angularPosition: The new position\n"
":param angularVelocity: The new velocity")
  )
  
  
  
    
  .
def
("getAngularPosition", &frc::sim::DCMotorSim::GetAngularPosition, release_gil(), py::doc(
    "Returns the DC motor position.\n"
"\n"
":returns: The DC motor position.")
  )
  
  
  
    
  .
def
("getAngularVelocity", &frc::sim::DCMotorSim::GetAngularVelocity, release_gil(), py::doc(
    "Returns the DC motor velocity.\n"
"\n"
":returns: The DC motor velocity.")
  )
  
  
  
    
  .
def
("getCurrentDraw", &frc::sim::DCMotorSim::GetCurrentDraw, release_gil(), py::doc(
    "Returns the DC motor current draw.\n"
"\n"
":returns: The DC motor current draw.")
  )
  
  
  
    
  .
def
("setInputVoltage", &frc::sim::DCMotorSim::SetInputVoltage,
      py::arg("voltage"), release_gil(), py::doc(
    "Sets the input voltage for the DC motor.\n"
"\n"
":param voltage: The input voltage.")
  )
  
  
  ;

  


  }






}

}; // struct rpybuild_DCMotorSim_initializer

static std::unique_ptr<rpybuild_DCMotorSim_initializer> cls;

void begin_init_DCMotorSim(py::module &m) {
  cls = std::make_unique<rpybuild_DCMotorSim_initializer>(m);
}

void finish_init_DCMotorSim() {
  cls->finish();
  cls.reset();
}