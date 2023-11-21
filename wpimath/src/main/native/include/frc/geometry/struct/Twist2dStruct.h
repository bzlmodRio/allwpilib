// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#pragma once

#include <wpi/SymbolExports.h>
#include <wpi/struct/Struct.h>

#include "frc/geometry/Twist2d.h"

template <>
struct WPILIB_DLLEXPORT wpi::Struct<frc::Twist2d> {
  static constexpr std::string_view kTypeString = "struct:Twist2d";
  static constexpr size_t kSize = 24;
  static constexpr std::string_view kSchema =
      "double dx;double dy;double dtheta";

  static frc::Twist2d Unpack(std::span<const uint8_t, kSize> data);
  static void Pack(std::span<uint8_t, kSize> data, const frc::Twist2d& value);
};
