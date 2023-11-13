// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include "frc/kinematics/serde/ChassisSpeedsSerde.h"

#include "kinematics.pb.h"

namespace {
constexpr size_t kVxOff = 0;
constexpr size_t kVyOff = kVxOff + 8;
constexpr size_t kOmegaOff = kVyOff + 8;
}  // namespace

using StructType = wpi::Struct<frc::ChassisSpeeds>;

frc::ChassisSpeeds StructType::Unpack(std::span<const uint8_t, kSize> data) {
  return frc::ChassisSpeeds{
      units::meters_per_second_t{wpi::UnpackStruct<double, kVxOff>(data)},
      units::meters_per_second_t{wpi::UnpackStruct<double, kVyOff>(data)},
      units::radians_per_second_t{wpi::UnpackStruct<double, kOmegaOff>(data)},
  };
}

void StructType::Pack(std::span<uint8_t, kSize> data,
                      const frc::ChassisSpeeds& value) {
  wpi::PackStruct<kVxOff>(data, value.vx.value());
  wpi::PackStruct<kVyOff>(data, value.vy.value());
  wpi::PackStruct<kOmegaOff>(data, value.omega.value());
}

google::protobuf::Message* wpi::Protobuf<frc::ChassisSpeeds>::New(
    google::protobuf::Arena* arena) {
  return google::protobuf::Arena::CreateMessage<
      wpi::proto::ProtobufChassisSpeeds>(arena);
}

frc::ChassisSpeeds wpi::Protobuf<frc::ChassisSpeeds>::Unpack(
    const google::protobuf::Message& msg) {
  auto m = static_cast<const wpi::proto::ProtobufChassisSpeeds*>(&msg);
  return frc::ChassisSpeeds{
      units::meters_per_second_t{m->vx_mps()},
      units::meters_per_second_t{m->vy_mps()},
      units::radians_per_second_t{m->omega_rps()},
  };
}

void wpi::Protobuf<frc::ChassisSpeeds>::Pack(google::protobuf::Message* msg,
                                             const frc::ChassisSpeeds& value) {
  auto m = static_cast<wpi::proto::ProtobufChassisSpeeds*>(msg);
  m->set_vx_mps(value.vx.value());
  m->set_vy_mps(value.vy.value());
  m->set_omega_rps(value.omega.value());
}
