
// This file is autogenerated. DO NOT EDIT
#include <robotpy_build.h>




#include <hal/simulation/NotifierData.h>
















#include <type_traits>






struct rpybuild_NotifierData_initializer {


  

  












  py::class_<typename ::HALSIM_NotifierInfo> cls_HALSIM_NotifierInfo;

    

    
    

  py::module &m;

  
  rpybuild_NotifierData_initializer(py::module &m) :

  

  

  

  
    cls_HALSIM_NotifierInfo(m, "NotifierInfo"),

  

  
  
  

    m(m)
  {
    
    

    
    
  

    
    
  }

void finish() {





  {
  
  
  


  

  

  cls_HALSIM_NotifierInfo
  
    .def(py::init<>(), release_gil())
  
    .def_readwrite("handle", &::HALSIM_NotifierInfo::handle)
  
    .def_property_readonly("name", [](::HALSIM_NotifierInfo& inst) {
        return py::memoryview::from_buffer(
          &inst.name, sizeof(char),
          py::format_descriptor<char>::value,
          {64}, {sizeof(char)},
          false
        );
    })
  
    .def_readwrite("timeout", &::HALSIM_NotifierInfo::timeout)
  
    .def_readwrite("waitTimeValid", &::HALSIM_NotifierInfo::waitTimeValid)
  ;

  


  }



m
  .
def
("getNextNotifierTimeout", &::HALSIM_GetNextNotifierTimeout, release_gil()
  )
  
  ;
m
  .
def
("getNumNotifiers", &::HALSIM_GetNumNotifiers, release_gil()
  )
  
  ;
m
  .
def
("getNotifierInfo", &::HALSIM_GetNotifierInfo,
      py::arg("arr"), py::arg("size"), release_gil(), py::doc(
    "Gets detailed information about each notifier.\n"
"\n"
":param arr:  array of information to be filled\n"
":param size: size of arr\n"
"\n"
":returns: Number of notifiers; note: may be larger than passed-in size")
  )
  
  ;



}

}; // struct rpybuild_NotifierData_initializer

static std::unique_ptr<rpybuild_NotifierData_initializer> cls;

void begin_init_NotifierData(py::module &m) {
  cls = std::make_unique<rpybuild_NotifierData_initializer>(m);
}

void finish_init_NotifierData() {
  cls->finish();
  cls.reset();
}