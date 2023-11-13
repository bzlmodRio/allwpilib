// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include "frc/kinematics/serde/DifferentialDriveKinematicsSerde.h"

#include "kinematics.pb.h"

namespace {
constexpr size_t kTrackWidthOff = 0;
}  // namespace

using StructType = wpi::Struct<frc::DifferentialDriveKinematics>;

frc::DifferentialDriveKinematics StructType::Unpack(
    std::span<const uint8_t, kSize> data) {
  return frc::DifferentialDriveKinematics{
      units::meter_t{wpi::UnpackStruct<double, kTrackWidthOff>(data)},
  };
}

void StructType::Pack(std::span<uint8_t, kSize> data,
                      const frc::DifferentialDriveKinematics& value) {
  wpi::PackStruct<kTrackWidthOff>(data, value.trackWidth.value());
}

google::protobuf::Message* wpi::Protobuf<frc::DifferentialDriveKinematics>::New(
    google::protobuf::Arena* arena) {
  return google::protobuf::Arena::CreateMessage<
      wpi::proto::ProtobufDifferentialDriveKinematics>(arena);
}

frc::DifferentialDriveKinematics
wpi::Protobuf<frc::DifferentialDriveKinematics>::Unpack(
    const google::protobuf::Message& msg) {
  auto m =
      static_cast<const wpi::proto::ProtobufDifferentialDriveKinematics*>(&msg);
  return frc::DifferentialDriveKinematics{
      units::meter_t{m->track_width_meters()},
  };
}

void wpi::Protobuf<frc::DifferentialDriveKinematics>::Pack(
    google::protobuf::Message* msg,
    const frc::DifferentialDriveKinematics& value) {
  auto m = static_cast<wpi::proto::ProtobufDifferentialDriveKinematics*>(msg);
  m->set_track_width_meters(value.trackWidth.value());
}
