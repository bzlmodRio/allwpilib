

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>



#include <frc/XboxController.h>


#include <frc/DriverStation.h>

#include <frc/event/BooleanEvent.h>









#include <rpygen/frc__GenericHID.hpp>



namespace rpygen {


using namespace frc;





template <typename CfgBase = EmptyTrampolineCfg>
struct PyTrampolineCfg_frc__XboxController :


    PyTrampolineCfg_frc__GenericHID<

CfgBase
>

{
    using Base = frc::XboxController;

    
    
};




template <typename PyTrampolineBase, typename PyTrampolineCfg>
using PyTrampolineBase_frc__XboxController =

    PyTrampoline_frc__GenericHID<

        PyTrampolineBase

        
        , PyTrampolineCfg
    >

;

template <typename PyTrampolineBase, typename PyTrampolineCfg>
struct PyTrampoline_frc__XboxController : PyTrampolineBase_frc__XboxController<PyTrampolineBase, PyTrampolineCfg> {
    using PyTrampolineBase_frc__XboxController<PyTrampolineBase, PyTrampolineCfg>::PyTrampolineBase_frc__XboxController;



  using Button [[maybe_unused]] = typename frc::XboxController::Button;

  using Axis [[maybe_unused]] = typename frc::XboxController::Axis;









    
    

    
    

    

    
};

}; // namespace rpygen

