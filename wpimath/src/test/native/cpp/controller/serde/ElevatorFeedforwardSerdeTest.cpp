// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include <gtest/gtest.h>

#include "controller.pb.h"
#include "frc/controller/ElevatorFeedforward.h"

using namespace frc;

namespace {

using StructType = wpi::Struct<frc::ElevatorFeedforward>;
using ProtoType = wpi::Protobuf<frc::ElevatorFeedforward>;

constexpr std::array<uint8_t, StructType::kSize> create_test_buffer() {
  std::array<uint8_t, StructType::kSize> output;
  int buffer[] = {-113, -62, -11, 40,  92,  -113, -2,  63,  82,  -72, 30,
                  -123, -21, 81,  2,   64,  -123, -21, 81,  -72, 30,  -123,
                  65,   64,  -41, -93, 112, 61,   10,  -41, -5,  63};
  for (size_t idx = 0; idx < StructType::kSize; ++idx) {
    output[idx] = static_cast<uint8_t>(buffer[idx]);
  }
  return output;
}

std::array<uint8_t, StructType::kSize> kExpectedStructBuffer =
    create_test_buffer();

static constexpr auto Ks = 1.91_V;
static constexpr auto Kg = 2.29_V;
static constexpr auto Kv = 35.04_V * 1_s / 1_m;
static constexpr auto Ka = 1.74_V * 1_s * 1_s / 1_m;

constexpr ElevatorFeedforward kExpectedData{Ks, Kg, Kv, Ka};
}  // namespace

TEST(ElevatorFeedforwardSerdeTest, StructPack) {
  uint8_t buffer[StructType::kSize];
  StructType::Pack(buffer, kExpectedData);

  for (size_t i = 0; i < StructType::kSize; ++i) {
    EXPECT_EQ(kExpectedStructBuffer[i], buffer[i]) << " on byte " << i;
  }
}

TEST(ElevatorFeedforwardSerdeTest, StructUnpack) {
  ElevatorFeedforward unpacked_data = StructType::Unpack(kExpectedStructBuffer);

  EXPECT_EQ(kExpectedData.kS.value(), unpacked_data.kS.value());
  EXPECT_EQ(kExpectedData.kG.value(), unpacked_data.kG.value());
  EXPECT_EQ(kExpectedData.kV.value(), unpacked_data.kV.value());
  EXPECT_EQ(kExpectedData.kA.value(), unpacked_data.kA.value());
}

TEST(ElevatorFeedforwardSerdeTest, ProtobufPack) {
  wpi::proto::ProtobufElevatorFeedforward proto;
  ProtoType::Pack(&proto, kExpectedData);

  EXPECT_EQ(kExpectedData.kS.value(), proto.ks());
  EXPECT_EQ(kExpectedData.kG.value(), proto.kg());
  EXPECT_EQ(kExpectedData.kV.value(), proto.kv());
  EXPECT_EQ(kExpectedData.kA.value(), proto.ka());
}

TEST(ElevatorFeedforwardSerdeTest, ProtobufUnpack) {
  wpi::proto::ProtobufElevatorFeedforward proto;
  proto.set_ks(kExpectedData.kS.value());
  proto.set_kg(kExpectedData.kG.value());
  proto.set_kv(kExpectedData.kV.value());
  proto.set_ka(kExpectedData.kA.value());

  ElevatorFeedforward unpacked_data = ProtoType::Unpack(proto);
  EXPECT_EQ(kExpectedData.kS.value(), unpacked_data.kS.value());
  EXPECT_EQ(kExpectedData.kG.value(), unpacked_data.kG.value());
  EXPECT_EQ(kExpectedData.kV.value(), unpacked_data.kV.value());
  EXPECT_EQ(kExpectedData.kA.value(), unpacked_data.kA.value());
}
