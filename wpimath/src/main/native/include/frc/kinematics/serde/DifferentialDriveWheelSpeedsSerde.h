// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#pragma once

#include <wpi/SymbolExports.h>
#include <wpi/protobuf/Protobuf.h>
#include <wpi/struct/Struct.h>

#include "frc/kinematics/DifferentialDriveWheelSpeeds.h"

template <>
struct wpi::Struct<frc::DifferentialDriveWheelSpeeds> {
  static constexpr std::string_view kTypeString =
      "struct:DifferentialDriveWheelSpeeds";
  static constexpr size_t kSize = 16;
  static constexpr std::string_view kSchema =
      "double left_mps;double right_mps";

  static frc::DifferentialDriveWheelSpeeds Unpack(
      std::span<const uint8_t, kSize> data);
  static void Pack(std::span<uint8_t, kSize> data,
                   const frc::DifferentialDriveWheelSpeeds& value);
};

template <>
struct WPILIB_DLLEXPORT wpi::Protobuf<frc::DifferentialDriveWheelSpeeds> {
  static google::protobuf::Message* New(google::protobuf::Arena* arena);
  static frc::DifferentialDriveWheelSpeeds Unpack(
      const google::protobuf::Message& msg);
  static void Pack(google::protobuf::Message* msg,
                   const frc::DifferentialDriveWheelSpeeds& value);
};
