
// This file is autogenerated. DO NOT EDIT
#include <robotpy_build.h>




#include <frc/simulation/DIOSim.h>


#include <pybind11/functional.h>













#include <frc/DigitalInput.h>

#include <frc/DigitalOutput.h>



#include <type_traits>


  using namespace frc;

  using namespace frc::sim;





struct rpybuild_DIOSim_initializer {


  

  












  py::class_<typename frc::sim::DIOSim> cls_DIOSim;

    

    
    

  py::module &m;

  
  rpybuild_DIOSim_initializer(py::module &m) :

  

  

  

  
    cls_DIOSim(m, "DIOSim"),

  

  
  
  

    m(m)
  {
    
    

    
    
  

    
    
  }

void finish() {





  {
  
  
  


  

  cls_DIOSim.doc() =
    "Class to control a simulated digital input or output.";

  cls_DIOSim
  
    
  .def(py::init<const DigitalInput&>(),
      py::arg("input"), release_gil()
    , py::keep_alive<1, 2>(), py::doc(
    "Constructs from a DigitalInput object.\n"
"\n"
":param input: DigitalInput to simulate")
  )
  
  
  
    
  .def(py::init<const DigitalOutput&>(),
      py::arg("output"), release_gil()
    , py::keep_alive<1, 2>(), py::doc(
    "Constructs from a DigitalOutput object.\n"
"\n"
":param output: DigitalOutput to simulate")
  )
  
  
  
    
  .def(py::init<int>(),
      py::arg("channel"), release_gil(), py::doc(
    "Constructs from an digital I/O channel number.\n"
"\n"
":param channel: Channel number")
  )
  
  
  
    
  .
def
("registerInitializedCallback", &frc::sim::DIOSim::RegisterInitializedCallback,
      py::arg("callback"), py::arg("initialNotify"), release_gil(), py::doc(
    "Register a callback to be run when this DIO is initialized.\n"
"\n"
":param callback:      the callback\n"
":param initialNotify: whether to run the callback with the initial state\n"
"\n"
":returns: the CallbackStore object associated with this callback")
  )
  
  
  
    
  .
def
("getInitialized", &frc::sim::DIOSim::GetInitialized, release_gil(), py::doc(
    "Check whether this DIO has been initialized.\n"
"\n"
":returns: true if initialized")
  )
  
  
  
    
  .
def
("setInitialized", &frc::sim::DIOSim::SetInitialized,
      py::arg("initialized"), release_gil(), py::doc(
    "Define whether this DIO has been initialized.\n"
"\n"
":param initialized: whether this object is initialized")
  )
  
  
  
    
  .
def
("registerValueCallback", &frc::sim::DIOSim::RegisterValueCallback,
      py::arg("callback"), py::arg("initialNotify"), release_gil(), py::doc(
    "Register a callback to be run whenever the DIO value changes.\n"
"\n"
":param callback:      the callback\n"
":param initialNotify: whether the callback should be called with the\n"
"                      initial value\n"
"\n"
":returns: the CallbackStore object associated with this callback")
  )
  
  
  
    
  .
def
("getValue", &frc::sim::DIOSim::GetValue, release_gil(), py::doc(
    "Read the value of the DIO port.\n"
"\n"
":returns: the DIO value")
  )
  
  
  
    
  .
def
("setValue", &frc::sim::DIOSim::SetValue,
      py::arg("value"), release_gil(), py::doc(
    "Change the DIO value.\n"
"\n"
":param value: the new value")
  )
  
  
  
    
  .
def
("registerPulseLengthCallback", &frc::sim::DIOSim::RegisterPulseLengthCallback,
      py::arg("callback"), py::arg("initialNotify"), release_gil(), py::doc(
    "Register a callback to be run whenever the pulse length changes.\n"
"\n"
":param callback:      the callback\n"
":param initialNotify: whether to call the callback with the initial state\n"
"\n"
":returns: the CallbackStore object associated with this callback")
  )
  
  
  
    
  .
def
("getPulseLength", &frc::sim::DIOSim::GetPulseLength, release_gil(), py::doc(
    "Read the pulse length.\n"
"\n"
":returns: the pulse length of this DIO port")
  )
  
  
  
    
  .
def
("setPulseLength", &frc::sim::DIOSim::SetPulseLength,
      py::arg("pulseLength"), release_gil(), py::doc(
    "Change the pulse length of this DIO port.\n"
"\n"
":param pulseLength: the new pulse length")
  )
  
  
  
    
  .
def
("registerIsInputCallback", &frc::sim::DIOSim::RegisterIsInputCallback,
      py::arg("callback"), py::arg("initialNotify"), release_gil(), py::doc(
    "Register a callback to be run whenever this DIO changes to be an input.\n"
"\n"
":param callback:      the callback\n"
":param initialNotify: whether the callback should be called with the\n"
"                      initial state\n"
"\n"
":returns: the CallbackStore object associated with this callback")
  )
  
  
  
    
  .
def
("getIsInput", &frc::sim::DIOSim::GetIsInput, release_gil(), py::doc(
    "Check whether this DIO port is currently an Input.\n"
"\n"
":returns: true if Input")
  )
  
  
  
    
  .
def
("setIsInput", &frc::sim::DIOSim::SetIsInput,
      py::arg("isInput"), release_gil(), py::doc(
    "Define whether this DIO port is an Input.\n"
"\n"
":param isInput: whether this DIO should be an Input")
  )
  
  
  
    
  .
def
("registerFilterIndexCallback", &frc::sim::DIOSim::RegisterFilterIndexCallback,
      py::arg("callback"), py::arg("initialNotify"), release_gil(), py::doc(
    "Register a callback to be run whenever the filter index changes.\n"
"\n"
":param callback:      the callback\n"
":param initialNotify: whether the callback should be called with the\n"
"                      initial value\n"
"\n"
":returns: the CallbackStore object associated with this callback")
  )
  
  
  
    
  .
def
("getFilterIndex", &frc::sim::DIOSim::GetFilterIndex, release_gil(), py::doc(
    "Read the filter index.\n"
"\n"
":returns: the filter index of this DIO port")
  )
  
  
  
    
  .
def
("setFilterIndex", &frc::sim::DIOSim::SetFilterIndex,
      py::arg("filterIndex"), release_gil(), py::doc(
    "Change the filter index of this DIO port.\n"
"\n"
":param filterIndex: the new filter index")
  )
  
  
  
    
  .
def
("resetData", &frc::sim::DIOSim::ResetData, release_gil(), py::doc(
    "Reset all simulation data of this object.")
  )
  
  
  ;

  


  }






}

}; // struct rpybuild_DIOSim_initializer

static std::unique_ptr<rpybuild_DIOSim_initializer> cls;

void begin_init_DIOSim(py::module &m) {
  cls = std::make_unique<rpybuild_DIOSim_initializer>(m);
}

void finish_init_DIOSim() {
  cls->finish();
  cls.reset();
}