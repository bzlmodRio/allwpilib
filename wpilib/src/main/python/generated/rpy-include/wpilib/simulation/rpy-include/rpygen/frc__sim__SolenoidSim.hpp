

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>



#include <frc/simulation/SolenoidSim.h>










namespace rpygen {


using namespace frc::sim;





template <typename CfgBase = EmptyTrampolineCfg>
struct PyTrampolineCfg_frc__sim__SolenoidSim :

    CfgBase

{
    using Base = frc::sim::SolenoidSim;

    
    
    using override_base_RegisterOutputCallback_TNotifyCallback_b = frc::sim::SolenoidSim;
    
};



template <typename PyTrampolineBase, typename PyTrampolineCfg>
struct PyTrampoline_frc__sim__SolenoidSim : PyTrampolineBase, virtual py::trampoline_self_life_support {
    using PyTrampolineBase::PyTrampolineBase;





    using PneumaticsModuleType = frc::PneumaticsModuleType;







    
    
#ifndef RPYGEN_DISABLE_RegisterOutputCallback_TNotifyCallback_b
    std::unique_ptr<CallbackStore> RegisterOutputCallback(NotifyCallback callback, bool initialNotify) override {
    
    
    
    
        using LookupBase = typename PyTrampolineCfg::Base;
    
    
        using CxxCallBase = typename PyTrampolineCfg::override_base_RegisterOutputCallback_TNotifyCallback_b;
        PYBIND11_OVERRIDE_IMPL(PYBIND11_TYPE(std::unique_ptr<CallbackStore>), LookupBase,
            "registerOutputCallback", callback, initialNotify);
        return CxxCallBase::RegisterOutputCallback(std::move(callback), std::move(initialNotify));
    
    
    
    }
#endif

    

    
    

    

    
};

}; // namespace rpygen

