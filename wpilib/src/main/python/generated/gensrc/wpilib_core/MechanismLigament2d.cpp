
// This file is autogenerated. DO NOT EDIT
#include <robotpy_build.h>




#include <frc/smartdashboard/MechanismLigament2d.h>


#include <units_angle_type_caster.h>







#define RPYGEN_ENABLE_frc__MechanismLigament2d_PROTECTED_CONSTRUCTORS
#include <rpygen/frc__MechanismLigament2d.hpp>









#include <type_traits>


  using namespace frc;





struct rpybuild_MechanismLigament2d_initializer {


  

  












  
  using MechanismLigament2d_Trampoline = rpygen::PyTrampoline_frc__MechanismLigament2d<typename frc::MechanismLigament2d, typename rpygen::PyTrampolineCfg_frc__MechanismLigament2d<>>;
    static_assert(std::is_abstract<MechanismLigament2d_Trampoline>::value == false, "frc::MechanismLigament2d " RPYBUILD_BAD_TRAMPOLINE);
  py::class_<typename frc::MechanismLigament2d, MechanismLigament2d_Trampoline, frc::MechanismObject2d> cls_MechanismLigament2d;

    

    
    

  py::module &m;

  
  rpybuild_MechanismLigament2d_initializer(py::module &m) :

  

  

  

  
    cls_MechanismLigament2d(m, "MechanismLigament2d"),

  

  
  
  

    m(m)
  {
    
    

    
    
  

    
    
  }

void finish() {





  {
  
  
  


  

  cls_MechanismLigament2d.doc() =
    "Ligament node on a Mechanism2d.\n"
"\n"
"A ligament can have its length changed (like an elevator) or angle changed,\n"
"like an arm.\n"
"\n"
"@see Mechanism2d";

  cls_MechanismLigament2d
  
    
  .
def
("setColor", &frc::MechanismLigament2d::SetColor,
      py::arg("color"), release_gil(), py::doc(
    "Set the ligament color.\n"
"\n"
":param color: the color of the line")
  )
  
  
  
    
  .
def
("getColor", &frc::MechanismLigament2d::GetColor, release_gil(), py::doc(
    "Get the ligament color.\n"
"\n"
":returns: the color of the line")
  )
  
  
  
    
  .
def
("setLength", &frc::MechanismLigament2d::SetLength,
      py::arg("length"), release_gil(), py::doc(
    "Set the ligament's length.\n"
"\n"
":param length: the line length")
  )
  
  
  
    
  .
def
("getLength", &frc::MechanismLigament2d::GetLength, release_gil(), py::doc(
    "Get the ligament length.\n"
"\n"
":returns: the line length")
  )
  
  
  
    
  .
def
("setAngle", &frc::MechanismLigament2d::SetAngle,
      py::arg("angle"), release_gil(), py::doc(
    "Set the ligament's angle relative to its parent.\n"
"\n"
":param angle: the angle")
  )
  
  
  
    
  .
def
("getAngle", &frc::MechanismLigament2d::GetAngle, release_gil(), py::doc(
    "Get the ligament's angle relative to its parent.\n"
"\n"
":returns: the angle")
  )
  
  
  
    
  .
def
("setLineWeight", &frc::MechanismLigament2d::SetLineWeight,
      py::arg("lineWidth"), release_gil(), py::doc(
    "Set the line thickness.\n"
"\n"
":param lineWidth: the line thickness")
  )
  
  
  
    
  .
def
("getLineWeight", &frc::MechanismLigament2d::GetLineWeight, release_gil(), py::doc(
    "Get the line thickness.\n"
"\n"
":returns: the line thickness")
  )
  
  
  
    
  .
def
("_updateEntries", static_cast<void(frc::MechanismLigament2d::*)(std::shared_ptr<nt::NetworkTable>)>(&MechanismLigament2d_Trampoline::UpdateEntries),
      py::arg("table"), release_gil()
  )
  
  
  ;

  


  }






}

}; // struct rpybuild_MechanismLigament2d_initializer

static std::unique_ptr<rpybuild_MechanismLigament2d_initializer> cls;

void begin_init_MechanismLigament2d(py::module &m) {
  cls = std::make_unique<rpybuild_MechanismLigament2d_initializer>(m);
}

void finish_init_MechanismLigament2d() {
  cls->finish();
  cls.reset();
}