project(glass)

include(CompileWarnings)
include(GenResources)
include(LinkMacOSGUI)

configure_file(src/main/generate/WPILibVersion.cpp.in WPILibVersion.cpp)
generate_resources(src/main/native/resources generated/main/cpp GLASS wpi::glass glass_resources_src)

file(GLOB glass_src src/main/native/cpp/*.cpp ${CMAKE_CURRENT_BINARY_DIR}/WPILibVersion.cpp)

if(WIN32)
    set(glass_rc src/main/native/win/glass.rc)
elseif(APPLE)
    set(MACOSX_BUNDLE_ICON_FILE glass.icns)
    set(APP_ICON_MACOSX src/main/native/mac/glass.icns)
    set_source_files_properties(${APP_ICON_MACOSX} PROPERTIES MACOSX_PACKAGE_LOCATION "Resources")
endif()

add_executable(glass ${glass_src} ${glass_resources_src} ${glass_rc} ${APP_ICON_MACOSX})
wpilib_link_macos_gui(glass)
wpilib_target_warnings(glass)
target_link_libraries(glass libglassnt libglass)

if(WIN32)
    set_target_properties(glass PROPERTIES WIN32_EXECUTABLE YES)
elseif(APPLE)
    set_target_properties(glass PROPERTIES MACOSX_BUNDLE YES OUTPUT_NAME "Glass")
endif()
