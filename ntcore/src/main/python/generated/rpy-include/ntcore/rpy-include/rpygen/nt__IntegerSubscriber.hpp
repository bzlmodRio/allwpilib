

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>



#include <networktables/IntegerTopic.h>










#include <rpygen/nt__Subscriber.hpp>



namespace rpygen {


using namespace nt;





template <typename CfgBase = EmptyTrampolineCfg>
struct PyTrampolineCfg_nt__IntegerSubscriber :


    PyTrampolineCfg_nt__Subscriber<

CfgBase
>

{
    using Base = nt::IntegerSubscriber;

    
    
};




template <typename PyTrampolineBase, typename PyTrampolineCfg>
using PyTrampolineBase_nt__IntegerSubscriber =

    PyTrampoline_nt__Subscriber<

        PyTrampolineBase

        
        , PyTrampolineCfg
    >

;

template <typename PyTrampolineBase, typename PyTrampolineCfg>
struct PyTrampoline_nt__IntegerSubscriber : PyTrampolineBase_nt__IntegerSubscriber<PyTrampolineBase, PyTrampolineCfg> {
    using PyTrampolineBase_nt__IntegerSubscriber<PyTrampolineBase, PyTrampolineCfg>::PyTrampolineBase_nt__IntegerSubscriber;






    using TopicType [[maybe_unused]] = typename nt::IntegerSubscriber::TopicType;

    using ValueType [[maybe_unused]] = typename nt::IntegerSubscriber::ValueType;

    using ParamType [[maybe_unused]] = typename nt::IntegerSubscriber::ParamType;

    using TimestampedValueType [[maybe_unused]] = typename nt::IntegerSubscriber::TimestampedValueType;






    
    

    
    

    

    
};

}; // namespace rpygen

