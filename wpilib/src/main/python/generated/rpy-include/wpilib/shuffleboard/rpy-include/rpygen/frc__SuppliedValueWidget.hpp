

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>



#include <frc/shuffleboard/SuppliedValueWidget.h>










#include <pybind11/stl.h>


namespace rpygen {


using namespace frc;




template <typename T>
struct bind_frc__SuppliedValueWidget {

    

    
  
  

    

    py::class_<typename frc::SuppliedValueWidget<T>, frc::ShuffleboardWidget<SuppliedValueWidget<T>>> cls_SuppliedValueWidget;

    

    
    

    py::module &m;
    std::string clsName;

bind_frc__SuppliedValueWidget(py::module &m, const char * clsName) :
    
    cls_SuppliedValueWidget(m, clsName),

  

  
  
    m(m),
    clsName(clsName)
{
    
  

}

void finish(const char * set_doc = NULL, const char * add_doc = NULL) {

    

  

  cls_SuppliedValueWidget
  
    
  .
def
("buildInto", &frc::SuppliedValueWidget<T>::BuildInto,
      py::arg("parentTable"), py::arg("metaTable"), release_gil()
  )
  
  
  ;

  



    if (set_doc) {
        cls_SuppliedValueWidget.doc() = set_doc;
    }
    if (add_doc) {
        cls_SuppliedValueWidget.doc() = py::cast<std::string>(cls_SuppliedValueWidget.doc()) + add_doc;
    }

    
}

}; // struct bind_frc__SuppliedValueWidget

}; // namespace rpygen