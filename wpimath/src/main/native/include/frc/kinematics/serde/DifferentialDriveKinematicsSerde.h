// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#pragma once

#include <wpi/SymbolExports.h>
#include <wpi/protobuf/Protobuf.h>
#include <wpi/struct/Struct.h>

#include "frc/kinematics/DifferentialDriveKinematics.h"

template <>
struct wpi::Struct<frc::DifferentialDriveKinematics> {
  static constexpr std::string_view kTypeString =
      "struct:DifferentialDriveKinematics";
  static constexpr size_t kSize = 8;
  static constexpr std::string_view kSchema = "double track_width_meters";

  static frc::DifferentialDriveKinematics Unpack(
      std::span<const uint8_t, kSize> data);
  static void Pack(std::span<uint8_t, kSize> data,
                   const frc::DifferentialDriveKinematics& value);
};

template <>
struct WPILIB_DLLEXPORT wpi::Protobuf<frc::DifferentialDriveKinematics> {
  static google::protobuf::Message* New(google::protobuf::Arena* arena);
  static frc::DifferentialDriveKinematics Unpack(
      const google::protobuf::Message& msg);
  static void Pack(google::protobuf::Message* msg,
                   const frc::DifferentialDriveKinematics& value);
};
