// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#pragma once

#include <wpi/SymbolExports.h>
#include <wpi/protobuf/Protobuf.h>
#include <wpi/struct/Struct.h>

#include "frc/kinematics/SwerveModuleState.h"

template <>
struct wpi::Struct<frc::SwerveModuleState> {
  static constexpr std::string_view kTypeString = "struct:SwerveModuleState";
  static constexpr size_t kSize = 8 + wpi::Struct<frc::Rotation2d>::kSize;
  static constexpr std::string_view kSchema =
      "double speed_mps;Rotation2d angle";

  static frc::SwerveModuleState Unpack(std::span<const uint8_t, kSize> data);
  static void Pack(std::span<uint8_t, kSize> data,
                   const frc::SwerveModuleState& value);
  static void ForEachNested(
      std::invocable<std::string_view, std::string_view> auto fn);
};

static_assert(wpi::HasNestedStruct<frc::SwerveModuleState>);

template <>
struct WPILIB_DLLEXPORT wpi::Protobuf<frc::SwerveModuleState> {
  static google::protobuf::Message* New(google::protobuf::Arena* arena);
  static frc::SwerveModuleState Unpack(const google::protobuf::Message& msg);
  static void Pack(google::protobuf::Message* msg,
                   const frc::SwerveModuleState& value);
};
