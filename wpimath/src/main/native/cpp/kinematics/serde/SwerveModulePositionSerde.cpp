// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include "frc/kinematics/serde/SwerveModulePositionSerde.h"

#include "kinematics.pb.h"

namespace {
constexpr size_t kDistanceOff = 0;
constexpr size_t kAngleOff = kDistanceOff + 8;
}  // namespace

using StructType = wpi::Struct<frc::SwerveModulePosition>;

frc::SwerveModulePosition StructType::Unpack(
    std::span<const uint8_t, kSize> data) {
  return frc::SwerveModulePosition{
      units::meter_t{wpi::UnpackStruct<double, kDistanceOff>(data)},
      wpi::UnpackStruct<frc::Rotation2d, kAngleOff>(data),
  };
}

void StructType::Pack(std::span<uint8_t, kSize> data,
                      const frc::SwerveModulePosition& value) {
  wpi::PackStruct<kDistanceOff>(data, value.distance.value());
  wpi::PackStruct<kAngleOff>(data, value.angle);
}

void StructType::ForEachNested(
    std::invocable<std::string_view, std::string_view> auto fn) {
  wpi::ForEachStructSchema<frc::Rotation2d>(fn);
}

google::protobuf::Message* wpi::Protobuf<frc::SwerveModulePosition>::New(
    google::protobuf::Arena* arena) {
  return google::protobuf::Arena::CreateMessage<
      wpi::proto::ProtobufSwerveModulePosition>(arena);
}

frc::SwerveModulePosition wpi::Protobuf<frc::SwerveModulePosition>::Unpack(
    const google::protobuf::Message& msg) {
  auto m = static_cast<const wpi::proto::ProtobufSwerveModulePosition*>(&msg);
  return frc::SwerveModulePosition{
      units::meter_t{m->distance_meters()},
      wpi::UnpackProtobuf<frc::Rotation2d>(m->angle()),
  };
}

void wpi::Protobuf<frc::SwerveModulePosition>::Pack(
    google::protobuf::Message* msg, const frc::SwerveModulePosition& value) {
  auto m = static_cast<wpi::proto::ProtobufSwerveModulePosition*>(msg);
  m->set_distance_meters(value.distance.value());
  wpi::PackProtobuf(m->mutable_angle(), value.angle);
}
