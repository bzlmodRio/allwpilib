
// This file is autogenerated. DO NOT EDIT
#include <robotpy_build.h>




#include <frc/simulation/CTREPCMSim.h>


#include <pybind11/functional.h>







#define RPYGEN_ENABLE_frc__sim__CTREPCMSim_PROTECTED_CONSTRUCTORS
#include <rpygen/frc__sim__CTREPCMSim.hpp>







#include <frc/Compressor.h>



#include <type_traits>


  using namespace frc::sim;





struct rpybuild_CTREPCMSim_initializer {


  
    using PneumaticsBase = frc::PneumaticsBase;
  

  












  
  using CTREPCMSim_Trampoline = rpygen::PyTrampoline_frc__sim__CTREPCMSim<typename frc::sim::CTREPCMSim, typename rpygen::PyTrampolineCfg_frc__sim__CTREPCMSim<>>;
    static_assert(std::is_abstract<CTREPCMSim_Trampoline>::value == false, "frc::sim::CTREPCMSim " RPYBUILD_BAD_TRAMPOLINE);
  py::class_<typename frc::sim::CTREPCMSim, CTREPCMSim_Trampoline, frc::sim::PneumaticsBaseSim> cls_CTREPCMSim;

    

    
    

  py::module &m;

  
  rpybuild_CTREPCMSim_initializer(py::module &m) :

  

  

  

  
    cls_CTREPCMSim(m, "CTREPCMSim"),

  

  
  
  

    m(m)
  {
    
    

    
    
  

    
    
  }

void finish() {





  {
  
  
  


  

  cls_CTREPCMSim.doc() =
    "Class to control a simulated Pneumatic Control Module (PCM).";

  cls_CTREPCMSim
  
    
  .def(py::init<>(), release_gil(), py::doc(
    "Constructs with the default PCM module number (CAN ID).")
  )
  
  
  
    
  .def(py::init<int>(),
      py::arg("module"), release_gil(), py::doc(
    "Constructs from a PCM module number (CAN ID).\n"
"\n"
":param module: module number")
  )
  
  
  
    
  .def(py::init<const PneumaticsBase&>(),
      py::arg("pneumatics"), release_gil()
    , py::keep_alive<1, 2>()
  )
  
  
  
    
  .
def
("registerInitializedCallback", &frc::sim::CTREPCMSim::RegisterInitializedCallback,
      py::arg("callback"), py::arg("initialNotify"), release_gil()
  )
  
  
  
    
  .
def
("getInitialized", &frc::sim::CTREPCMSim::GetInitialized, release_gil()
  )
  
  
  
    
  .
def
("setInitialized", &frc::sim::CTREPCMSim::SetInitialized,
      py::arg("initialized"), release_gil()
  )
  
  
  
    
  .
def
("registerSolenoidOutputCallback", &frc::sim::CTREPCMSim::RegisterSolenoidOutputCallback,
      py::arg("channel"), py::arg("callback"), py::arg("initialNotify"), release_gil()
  )
  
  
  
    
  .
def
("getSolenoidOutput", &frc::sim::CTREPCMSim::GetSolenoidOutput,
      py::arg("channel"), release_gil()
  )
  
  
  
    
  .
def
("setSolenoidOutput", &frc::sim::CTREPCMSim::SetSolenoidOutput,
      py::arg("channel"), py::arg("solenoidOutput"), release_gil()
  )
  
  
  
    
  .
def
("registerCompressorOnCallback", &frc::sim::CTREPCMSim::RegisterCompressorOnCallback,
      py::arg("callback"), py::arg("initialNotify"), release_gil()
  )
  
  
  
    
  .
def
("getCompressorOn", &frc::sim::CTREPCMSim::GetCompressorOn, release_gil()
  )
  
  
  
    
  .
def
("setCompressorOn", &frc::sim::CTREPCMSim::SetCompressorOn,
      py::arg("compressorOn"), release_gil()
  )
  
  
  
    
  .
def
("registerClosedLoopEnabledCallback", &frc::sim::CTREPCMSim::RegisterClosedLoopEnabledCallback,
      py::arg("callback"), py::arg("initialNotify"), release_gil(), py::doc(
    "Register a callback to be run whenever the closed loop state changes.\n"
"\n"
":param callback:      the callback\n"
":param initialNotify: whether the callback should be called with the\n"
"                      initial value\n"
"\n"
":returns: the CallbackStore object associated with this callback")
  )
  
  
  
    
  .
def
("getClosedLoopEnabled", &frc::sim::CTREPCMSim::GetClosedLoopEnabled, release_gil(), py::doc(
    "Check whether the closed loop compressor control is active.\n"
"\n"
":returns: true if active")
  )
  
  
  
    
  .
def
("setClosedLoopEnabled", &frc::sim::CTREPCMSim::SetClosedLoopEnabled,
      py::arg("closedLoopEnabled"), release_gil(), py::doc(
    "Turn on/off the closed loop control of the compressor.\n"
"\n"
":param closedLoopEnabled: whether the control loop is active")
  )
  
  
  
    
  .
def
("registerPressureSwitchCallback", &frc::sim::CTREPCMSim::RegisterPressureSwitchCallback,
      py::arg("callback"), py::arg("initialNotify"), release_gil(), py::doc(
    "Register a callback to be run whenever the pressure switch value changes.\n"
"\n"
":param callback:      the callback\n"
":param initialNotify: whether the callback should be called with the\n"
"                      initial value\n"
"\n"
":returns: the CallbackStore object associated with this callback")
  )
  
  
  
    
  .
def
("getPressureSwitch", &frc::sim::CTREPCMSim::GetPressureSwitch, release_gil(), py::doc(
    "Check the value of the pressure switch.\n"
"\n"
":returns: the pressure switch value")
  )
  
  
  
    
  .
def
("setPressureSwitch", &frc::sim::CTREPCMSim::SetPressureSwitch,
      py::arg("pressureSwitch"), release_gil(), py::doc(
    "Set the value of the pressure switch.\n"
"\n"
":param pressureSwitch: the new value")
  )
  
  
  
    
  .
def
("registerCompressorCurrentCallback", &frc::sim::CTREPCMSim::RegisterCompressorCurrentCallback,
      py::arg("callback"), py::arg("initialNotify"), release_gil(), py::doc(
    "Register a callback to be run whenever the compressor current changes.\n"
"\n"
":param callback:      the callback\n"
":param initialNotify: whether to call the callback with the initial state\n"
"\n"
":returns: the CallbackStore object associated with this callback")
  )
  
  
  
    
  .
def
("getCompressorCurrent", &frc::sim::CTREPCMSim::GetCompressorCurrent, release_gil(), py::doc(
    "Read the compressor current.\n"
"\n"
":returns: the current of the compressor connected to this module")
  )
  
  
  
    
  .
def
("setCompressorCurrent", &frc::sim::CTREPCMSim::SetCompressorCurrent,
      py::arg("compressorCurrent"), release_gil(), py::doc(
    "Set the compressor current.\n"
"\n"
":param compressorCurrent: the new compressor current")
  )
  
  
  
    
  .
def
("getAllSolenoidOutputs", &frc::sim::CTREPCMSim::GetAllSolenoidOutputs, release_gil()
  )
  
  
  
    
  .
def
("setAllSolenoidOutputs", &frc::sim::CTREPCMSim::SetAllSolenoidOutputs,
      py::arg("outputs"), release_gil()
  )
  
  
  
    
  .
def
("resetData", &frc::sim::CTREPCMSim::ResetData, release_gil()
  )
  
  
  ;

  


  }






}

}; // struct rpybuild_CTREPCMSim_initializer

static std::unique_ptr<rpybuild_CTREPCMSim_initializer> cls;

void begin_init_CTREPCMSim(py::module &m) {
  cls = std::make_unique<rpybuild_CTREPCMSim_initializer>(m);
}

void finish_init_CTREPCMSim() {
  cls->finish();
  cls.reset();
}