// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include "frc/controller/serde/ElevatorFeedforwardSerde.h"

#include "controller.pb.h"

namespace {
constexpr size_t kKsOff = 0;
constexpr size_t kKgOff = kKsOff + 8;
constexpr size_t kKvOff = kKgOff + 8;
constexpr size_t kKaOff = kKvOff + 8;
}  // namespace

using StructType = wpi::Struct<frc::ElevatorFeedforward>;

frc::ElevatorFeedforward StructType::Unpack(
    std::span<const uint8_t, kSize> data) {
  return frc::ElevatorFeedforward{
      units::volt_t{wpi::UnpackStruct<double, kKsOff>(data)},
      units::volt_t{wpi::UnpackStruct<double, kKgOff>(data)},
      units::unit_t<frc::ElevatorFeedforward::kv_unit>{
          wpi::UnpackStruct<double, kKvOff>(data)},
      units::unit_t<frc::ElevatorFeedforward::ka_unit>{
          wpi::UnpackStruct<double, kKaOff>(data)},
  };
}

void StructType::Pack(std::span<uint8_t, kSize> data,
                      const frc::ElevatorFeedforward& value) {
  wpi::PackStruct<kKsOff>(data, value.kS());
  wpi::PackStruct<kKgOff>(data, value.kG());
  wpi::PackStruct<kKvOff>(data, value.kV());
  wpi::PackStruct<kKaOff>(data, value.kA());
}

google::protobuf::Message* wpi::Protobuf<frc::ElevatorFeedforward>::New(
    google::protobuf::Arena* arena) {
  return google::protobuf::Arena::CreateMessage<
      wpi::proto::ProtobufElevatorFeedforward>(arena);
}

frc::ElevatorFeedforward wpi::Protobuf<frc::ElevatorFeedforward>::Unpack(
    const google::protobuf::Message& msg) {
  auto m = static_cast<const wpi::proto::ProtobufElevatorFeedforward*>(&msg);
  return frc::ElevatorFeedforward{
      units::volt_t{m->ks()},
      units::volt_t{m->kg()},
      units::unit_t<frc::ElevatorFeedforward::kv_unit>{m->kv()},
      units::unit_t<frc::ElevatorFeedforward::ka_unit>{m->ka()},
  };
}

void wpi::Protobuf<frc::ElevatorFeedforward>::Pack(
    google::protobuf::Message* msg, const frc::ElevatorFeedforward& value) {
  auto m = static_cast<wpi::proto::ProtobufElevatorFeedforward*>(msg);
  m->set_ks(value.kS());
  m->set_kg(value.kG());
  m->set_kv(value.kV());
  m->set_ka(value.kA());
}
