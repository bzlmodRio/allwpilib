// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#pragma once

#include <wpi/SymbolExports.h>
#include <wpi/protobuf/Protobuf.h>
#include <wpi/struct/Struct.h>

#include "frc/controller/ArmFeedforward.h"

template <>
struct wpi::Struct<frc::ArmFeedforward> {
  static constexpr std::string_view kTypeString = "struct:ArmFeedforward";
  static constexpr size_t kSize = 32;
  static constexpr std::string_view kSchema =
      "double ks;double kg;double kv;double ka";

  static frc::ArmFeedforward Unpack(std::span<const uint8_t, kSize> data);
  static void Pack(std::span<uint8_t, kSize> data,
                   const frc::ArmFeedforward& value);
};

template <>
struct WPILIB_DLLEXPORT wpi::Protobuf<frc::ArmFeedforward> {
  static google::protobuf::Message* New(google::protobuf::Arena* arena);
  static frc::ArmFeedforward Unpack(const google::protobuf::Message& msg);
  static void Pack(google::protobuf::Message* msg,
                   const frc::ArmFeedforward& value);
};
