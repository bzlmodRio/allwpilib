
// This file is autogenerated. DO NOT EDIT
#include <robotpy_build.h>




#include <frc/simulation/PowerDistributionSim.h>


#include <pybind11/functional.h>













#include <frc/PowerDistribution.h>



#include <type_traits>


  using namespace frc;

  using namespace frc::sim;





struct rpybuild_PowerDistributionSim_initializer {


  

  












  py::class_<typename frc::sim::PowerDistributionSim> cls_PowerDistributionSim;

    

    
    

  py::module &m;

  
  rpybuild_PowerDistributionSim_initializer(py::module &m) :

  

  

  

  
    cls_PowerDistributionSim(m, "PowerDistributionSim"),

  

  
  
  

    m(m)
  {
    
    

    
    
  

    
    
  }

void finish() {





  {
  
  
  


  

  cls_PowerDistributionSim.doc() =
    "Class to control a simulated Power Distribution Panel (PowerDistribution).";

  cls_PowerDistributionSim
  
    
  .def(py::init<int>(),
      py::arg("module") = 0, release_gil(), py::doc(
    "Constructs from a PowerDistribution module number (CAN ID).\n"
"\n"
":param module: module number")
  )
  
  
  
    
  .def(py::init<const PowerDistribution&>(),
      py::arg("pdp"), release_gil()
    , py::keep_alive<1, 2>(), py::doc(
    "Constructs from a PowerDistribution object.\n"
"\n"
":param pdp: PowerDistribution to simulate")
  )
  
  
  
    
  .
def
("registerInitializedCallback", &frc::sim::PowerDistributionSim::RegisterInitializedCallback,
      py::arg("callback"), py::arg("initialNotify"), release_gil(), py::doc(
    "Register a callback to be run when the PowerDistribution is initialized.\n"
"\n"
":param callback:      the callback\n"
":param initialNotify: whether to run the callback with the initial state\n"
"\n"
":returns: the CallbackStore object associated with this callback")
  )
  
  
  
    
  .
def
("getInitialized", &frc::sim::PowerDistributionSim::GetInitialized, release_gil(), py::doc(
    "Check whether the PowerDistribution has been initialized.\n"
"\n"
":returns: true if initialized")
  )
  
  
  
    
  .
def
("setInitialized", &frc::sim::PowerDistributionSim::SetInitialized,
      py::arg("initialized"), release_gil(), py::doc(
    "Define whether the PowerDistribution has been initialized.\n"
"\n"
":param initialized: whether this object is initialized")
  )
  
  
  
    
  .
def
("registerTemperatureCallback", &frc::sim::PowerDistributionSim::RegisterTemperatureCallback,
      py::arg("callback"), py::arg("initialNotify"), release_gil(), py::doc(
    "Register a callback to be run whenever the PowerDistribution temperature\n"
"changes.\n"
"\n"
":param callback:      the callback\n"
":param initialNotify: whether to call the callback with the initial state\n"
"\n"
":returns: the CallbackStore object associated with this callback")
  )
  
  
  
    
  .
def
("getTemperature", &frc::sim::PowerDistributionSim::GetTemperature, release_gil(), py::doc(
    "Check the temperature of the PowerDistribution.\n"
"\n"
":returns: the PowerDistribution temperature")
  )
  
  
  
    
  .
def
("setTemperature", &frc::sim::PowerDistributionSim::SetTemperature,
      py::arg("temperature"), release_gil(), py::doc(
    "Define the PowerDistribution temperature.\n"
"\n"
":param temperature: the new PowerDistribution temperature")
  )
  
  
  
    
  .
def
("registerVoltageCallback", &frc::sim::PowerDistributionSim::RegisterVoltageCallback,
      py::arg("callback"), py::arg("initialNotify"), release_gil(), py::doc(
    "Register a callback to be run whenever the PowerDistribution voltage\n"
"changes.\n"
"\n"
":param callback:      the callback\n"
":param initialNotify: whether to call the callback with the initial state\n"
"\n"
":returns: the CallbackStore object associated with this callback")
  )
  
  
  
    
  .
def
("getVoltage", &frc::sim::PowerDistributionSim::GetVoltage, release_gil(), py::doc(
    "Check the PowerDistribution voltage.\n"
"\n"
":returns: the PowerDistribution voltage.")
  )
  
  
  
    
  .
def
("setVoltage", &frc::sim::PowerDistributionSim::SetVoltage,
      py::arg("voltage"), release_gil(), py::doc(
    "Set the PowerDistribution voltage.\n"
"\n"
":param voltage: the new PowerDistribution voltage")
  )
  
  
  
    
  .
def
("registerCurrentCallback", &frc::sim::PowerDistributionSim::RegisterCurrentCallback,
      py::arg("channel"), py::arg("callback"), py::arg("initialNotify"), release_gil(), py::doc(
    "Register a callback to be run whenever the current of a specific channel\n"
"changes.\n"
"\n"
":param channel:       the channel\n"
":param callback:      the callback\n"
":param initialNotify: whether to call the callback with the initial state\n"
"\n"
":returns: the CallbackStore object associated with this callback")
  )
  
  
  
    
  .
def
("getCurrent", &frc::sim::PowerDistributionSim::GetCurrent,
      py::arg("channel"), release_gil(), py::doc(
    "Read the current in one of the PowerDistribution channels.\n"
"\n"
":param channel: the channel to check\n"
"\n"
":returns: the current in the given channel")
  )
  
  
  
    
  .
def
("setCurrent", &frc::sim::PowerDistributionSim::SetCurrent,
      py::arg("channel"), py::arg("current"), release_gil(), py::doc(
    "Change the current in the given channel.\n"
"\n"
":param channel: the channel to edit\n"
":param current: the new current for the channel")
  )
  
  
  
    
  .
def
("getAllCurrents", [](frc::sim::PowerDistributionSim * __that,int length) {
                    double currents;
          __that->GetAllCurrents(&currents, std::move(length));
          return currents;
        },
      py::arg("length"), release_gil(), py::doc(
    "Read the current of all of the PowerDistribution channels.\n"
"\n"
":param currents: output array; set to the current in each channel. The\n"
"                 array must be big enough to hold all the PowerDistribution\n"
"                 channels\n"
":param length:   length of output array")
  )
  
  
  
    
  .
def
("setAllCurrents", &frc::sim::PowerDistributionSim::SetAllCurrents,
      py::arg("currents"), py::arg("length"), release_gil(), py::doc(
    "Change the current in all of the PowerDistribution channels.\n"
"\n"
":param currents: array containing the current values for each channel. The\n"
"                 array must be big enough to hold all the PowerDistribution\n"
"                 channels\n"
":param length:   length of array")
  )
  
  
  
    
  .
def
("resetData", &frc::sim::PowerDistributionSim::ResetData, release_gil(), py::doc(
    "Reset all PowerDistribution simulation data.")
  )
  
  
  ;

  


  }






}

}; // struct rpybuild_PowerDistributionSim_initializer

static std::unique_ptr<rpybuild_PowerDistributionSim_initializer> cls;

void begin_init_PowerDistributionSim(py::module &m) {
  cls = std::make_unique<rpybuild_PowerDistributionSim_initializer>(m);
}

void finish_init_PowerDistributionSim() {
  cls->finish();
  cls.reset();
}