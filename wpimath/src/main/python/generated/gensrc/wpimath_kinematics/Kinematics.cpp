
// This file is autogenerated. DO NOT EDIT
#include <robotpy_build.h>




#include <frc/kinematics/Kinematics.h>


#include <wpi_array_type_caster.h>







#define RPYGEN_ENABLE_frc__Kinematics_PROTECTED_CONSTRUCTORS
#include <rpygen/frc__Kinematics.hpp>





#include "Kinematics_tmpl.hpp"



#include <frc/kinematics/DifferentialDriveWheelPositions.h>

#include <frc/kinematics/DifferentialDriveWheelSpeeds.h>

#include <frc/kinematics/MecanumDriveWheelPositions.h>

#include <frc/kinematics/MecanumDriveWheelSpeeds.h>

#include <frc/kinematics/SwerveDriveKinematics.h>

#include <frc/kinematics/SwerveDriveWheelPositions.h>



#include <type_traits>


  using namespace frc;





struct rpybuild_Kinematics_initializer {












  
      rpygen::bind_frc__Kinematics_0 tmplCls0;
    
      rpygen::bind_frc__Kinematics_1 tmplCls1;
    
      rpygen::bind_frc__Kinematics_2 tmplCls2;
    
      rpygen::bind_frc__Kinematics_3 tmplCls3;
    
      rpygen::bind_frc__Kinematics_4 tmplCls4;
    
      rpygen::bind_frc__Kinematics_5 tmplCls5;
    

  py::module &m;

  
  rpybuild_Kinematics_initializer(py::module &m) :

  

  

  

  
    
        tmplCls0(m, "DifferentialDriveKinematicsBase"),
      
        tmplCls1(m, "MecanumDriveKinematicsBase"),
      
        tmplCls2(m, "SwerveDrive2KinematicsBase"),
      
        tmplCls3(m, "SwerveDrive3KinematicsBase"),
      
        tmplCls4(m, "SwerveDrive4KinematicsBase"),
      
        tmplCls5(m, "SwerveDrive6KinematicsBase"),
      
  

    m(m)
  {
    
    

    
    
  

    
    
  }

void finish() {



  tmplCls0.finish(
    NULL,
    NULL
  );

  tmplCls1.finish(
    NULL,
    NULL
  );

  tmplCls2.finish(
    NULL,
    NULL
  );

  tmplCls3.finish(
    NULL,
    NULL
  );

  tmplCls4.finish(
    NULL,
    NULL
  );

  tmplCls5.finish(
    NULL,
    NULL
  );








}

}; // struct rpybuild_Kinematics_initializer

static std::unique_ptr<rpybuild_Kinematics_initializer> cls;

void begin_init_Kinematics(py::module &m) {
  cls = std::make_unique<rpybuild_Kinematics_initializer>(m);
}

void finish_init_Kinematics() {
  cls->finish();
  cls.reset();
}