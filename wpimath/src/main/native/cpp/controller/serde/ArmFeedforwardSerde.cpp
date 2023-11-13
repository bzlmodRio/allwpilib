// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include "frc/controller/serde/ArmFeedforwardSerde.h"

#include "controller.pb.h"

namespace {
constexpr size_t kKsOff = 0;
constexpr size_t kKgOff = kKsOff + 8;
constexpr size_t kKvOff = kKgOff + 8;
constexpr size_t kKaOff = kKvOff + 8;
}  // namespace

using StructType = wpi::Struct<frc::ArmFeedforward>;

frc::ArmFeedforward StructType::Unpack(std::span<const uint8_t, kSize> data) {
  return {
      units::volt_t{wpi::UnpackStruct<double, kKsOff>(data)},
      units::volt_t{wpi::UnpackStruct<double, kKgOff>(data)},
      units::unit_t<frc::ArmFeedforward::kv_unit>{
          wpi::UnpackStruct<double, kKvOff>(data)},
      units::unit_t<frc::ArmFeedforward::ka_unit>{
          wpi::UnpackStruct<double, kKaOff>(data)},
  };
}

void StructType::Pack(std::span<uint8_t, kSize> data,
                      const frc::ArmFeedforward& value) {
  wpi::PackStruct<kKsOff>(data, value.kS());
  wpi::PackStruct<kKgOff>(data, value.kG());
  wpi::PackStruct<kKvOff>(data, value.kV());
  wpi::PackStruct<kKaOff>(data, value.kA());
}

google::protobuf::Message* wpi::Protobuf<frc::ArmFeedforward>::New(
    google::protobuf::Arena* arena) {
  return google::protobuf::Arena::CreateMessage<
      wpi::proto::ProtobufArmFeedforward>(arena);
}

frc::ArmFeedforward wpi::Protobuf<frc::ArmFeedforward>::Unpack(
    const google::protobuf::Message& msg) {
  auto m = static_cast<const wpi::proto::ProtobufArmFeedforward*>(&msg);
  return frc::ArmFeedforward{
      units::volt_t{m->ks()},
      units::volt_t{m->kg()},
      units::unit_t<frc::ArmFeedforward::kv_unit>{m->kv()},
      units::unit_t<frc::ArmFeedforward::ka_unit>{m->ka()},
  };
}

void wpi::Protobuf<frc::ArmFeedforward>::Pack(
    google::protobuf::Message* msg, const frc::ArmFeedforward& value) {
  auto m = static_cast<wpi::proto::ProtobufArmFeedforward*>(msg);
  m->set_ks(value.kS.value());
  m->set_kg(value.kG.value());
  m->set_kv(value.kV.value());
  m->set_ka(value.kA.value());
}
