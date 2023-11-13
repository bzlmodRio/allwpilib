// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include "frc/kinematics/serde/MecanumDriveWheelSpeedsSerde.h"

#include "kinematics.pb.h"

namespace {
constexpr size_t kFrontLeftOff = 0;
constexpr size_t kFrontRightOff = kFrontLeftOff + 8;
constexpr size_t kRearLeftOff = kFrontRightOff + 8;
constexpr size_t kRearRightOff = kRearLeftOff + 8;
}  // namespace

using StructType = wpi::Struct<frc::MecanumDriveWheelSpeeds>;

frc::MecanumDriveWheelSpeeds StructType::Unpack(
    std::span<const uint8_t, kSize> data) {
  return frc::MecanumDriveWheelSpeeds{
      units::meters_per_second_t{
          wpi::UnpackStruct<double, kFrontLeftOff>(data)},
      units::meters_per_second_t{
          wpi::UnpackStruct<double, kFrontRightOff>(data)},
      units::meters_per_second_t{wpi::UnpackStruct<double, kRearLeftOff>(data)},
      units::meters_per_second_t{
          wpi::UnpackStruct<double, kRearRightOff>(data)},
  };
}

void StructType::Pack(std::span<uint8_t, kSize> data,
                      const frc::MecanumDriveWheelSpeeds& value) {
  wpi::PackStruct<kFrontLeftOff>(data, value.frontLeft.value());
  wpi::PackStruct<kFrontRightOff>(data, value.frontRight.value());
  wpi::PackStruct<kRearLeftOff>(data, value.rearLeft.value());
  wpi::PackStruct<kRearRightOff>(data, value.rearRight.value());
}

google::protobuf::Message* wpi::Protobuf<frc::MecanumDriveWheelSpeeds>::New(
    google::protobuf::Arena* arena) {
  return google::protobuf::Arena::CreateMessage<
      wpi::proto::ProtobufMecanumDriveWheelSpeeds>(arena);
}

frc::MecanumDriveWheelSpeeds
wpi::Protobuf<frc::MecanumDriveWheelSpeeds>::Unpack(
    const google::protobuf::Message& msg) {
  auto m =
      static_cast<const wpi::proto::ProtobufMecanumDriveWheelSpeeds*>(&msg);
  return frc::MecanumDriveWheelSpeeds{
      units::meters_per_second_t{m->front_left_mps()},
      units::meters_per_second_t{m->front_right_mps()},
      units::meters_per_second_t{m->rear_left_mps()},
      units::meters_per_second_t{m->rear_right_mps()},
  };
}

void wpi::Protobuf<frc::MecanumDriveWheelSpeeds>::Pack(
    google::protobuf::Message* msg, const frc::MecanumDriveWheelSpeeds& value) {
  auto m = static_cast<wpi::proto::ProtobufMecanumDriveWheelSpeeds*>(msg);
  m->set_front_left_mps(value.frontLeft.value());
  m->set_front_right_mps(value.frontRight.value());
  m->set_rear_left_mps(value.rearLeft.value());
  m->set_rear_right_mps(value.rearRight.value());
}
