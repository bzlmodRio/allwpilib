// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include "frc/controller/serde/DifferentialDriveWheelVoltagesSerde.h"

#include "controller.pb.h"

namespace {
constexpr size_t kLeftOff = 0;
constexpr size_t kRightOff = kLeftOff + 8;
}  // namespace

using StructType = wpi::Struct<frc::DifferentialDriveWheelVoltages>;

frc::DifferentialDriveWheelVoltages StructType::Unpack(
    std::span<const uint8_t, kSize> data) {
  return frc::DifferentialDriveWheelVoltages{
      units::volt_t{wpi::UnpackStruct<double, kLeftOff>(data)},
      units::volt_t{wpi::UnpackStruct<double, kRightOff>(data)},
  };
}

void StructType::Pack(std::span<uint8_t, kSize> data,
                      const frc::DifferentialDriveWheelVoltages& value) {
  wpi::PackStruct<kLeftOff>(data, value.left.value());
  wpi::PackStruct<kRightOff>(data, value.right.value());
}

google::protobuf::Message* wpi::Protobuf<
    frc::DifferentialDriveWheelVoltages>::New(google::protobuf::Arena* arena) {
  return google::protobuf::Arena::CreateMessage<
      wpi::proto::ProtobufDifferentialDriveWheelVoltages>(arena);
}

frc::DifferentialDriveWheelVoltages
wpi::Protobuf<frc::DifferentialDriveWheelVoltages>::Unpack(
    const google::protobuf::Message& msg) {
  auto m =
      static_cast<const wpi::proto::ProtobufDifferentialDriveWheelVoltages*>(
          &msg);
  return frc::DifferentialDriveWheelVoltages{
      units::volt_t{m->left_volts()},
      units::volt_t{m->right_volts()},
  };
}

void wpi::Protobuf<frc::DifferentialDriveWheelVoltages>::Pack(
    google::protobuf::Message* msg,
    const frc::DifferentialDriveWheelVoltages& value) {
  auto m =
      static_cast<wpi::proto::ProtobufDifferentialDriveWheelVoltages*>(msg);
  m->set_left_volts(value.left.value());
  m->set_right_volts(value.right.value());
}
