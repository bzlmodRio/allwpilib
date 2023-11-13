// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include "frc/kinematics/serde/SwerveModuleStateSerde.h"

#include "kinematics.pb.h"

namespace {
constexpr size_t kSpeedOff = 0;
constexpr size_t kAngleOff = kSpeedOff + 8;
}  // namespace

using StructType = wpi::Struct<frc::SwerveModuleState>;

frc::SwerveModuleState StructType::Unpack(
    std::span<const uint8_t, kSize> data) {
  return frc::SwerveModuleState{
      units::meters_per_second_t{wpi::UnpackStruct<double, kSpeedOff>(data)},
      wpi::UnpackStruct<frc::Rotation2d, kAngleOff>(data),
  };
}

void StructType::Pack(std::span<uint8_t, kSize> data,
                      const frc::SwerveModuleState& value) {
  wpi::PackStruct<kSpeedOff>(data, value.speed.value());
  wpi::PackStruct<kAngleOff>(data, value.angle);
}

void StructType::ForEachNested(
    std::invocable<std::string_view, std::string_view> auto fn) {
  wpi::ForEachStructSchema<frc::Rotation2d>(fn);
}

google::protobuf::Message* wpi::Protobuf<frc::SwerveModuleState>::New(
    google::protobuf::Arena* arena) {
  return google::protobuf::Arena::CreateMessage<
      wpi::proto::ProtobufSwerveModuleState>(arena);
}

frc::SwerveModuleState wpi::Protobuf<frc::SwerveModuleState>::Unpack(
    const google::protobuf::Message& msg) {
  auto m = static_cast<const wpi::proto::ProtobufSwerveModuleState*>(&msg);
  return frc::SwerveModuleState{
      units::meters_per_second_t{m->speed_mps()},
      wpi::UnpackProtobuf<frc::Rotation2d>(m->angle()),
  };
}

void wpi::Protobuf<frc::SwerveModuleState>::Pack(
    google::protobuf::Message* msg, const frc::SwerveModuleState& value) {
  auto m = static_cast<wpi::proto::ProtobufSwerveModuleState*>(msg);
  m->set_speed_mps(value.speed.value());
  wpi::PackProtobuf(m->mutable_angle(), value.angle);
}
