// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#pragma once

#include <wpi/SymbolExports.h>
#include <wpi/protobuf/Protobuf.h>
#include <wpi/struct/Struct.h>

#include "frc/kinematics/MecanumDriveWheelPositions.h"

template <>
struct wpi::Struct<frc::MecanumDriveWheelPositions> {
  static constexpr std::string_view kTypeString =
      "struct:MecanumDriveWheelPositions";
  static constexpr size_t kSize = 32;
  static constexpr std::string_view kSchema =
      "double front_left_meters;double front_right_meters;double "
      "rear_left_meters;double rear_right_meters";

  static frc::MecanumDriveWheelPositions Unpack(
      std::span<const uint8_t, kSize> data);
  static void Pack(std::span<uint8_t, kSize> data,
                   const frc::MecanumDriveWheelPositions& value);
};

template <>
struct WPILIB_DLLEXPORT wpi::Protobuf<frc::MecanumDriveWheelPositions> {
  static google::protobuf::Message* New(google::protobuf::Arena* arena);
  static frc::MecanumDriveWheelPositions Unpack(
      const google::protobuf::Message& msg);
  static void Pack(google::protobuf::Message* msg,
                   const frc::MecanumDriveWheelPositions& value);
};
