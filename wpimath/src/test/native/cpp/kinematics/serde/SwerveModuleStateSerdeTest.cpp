// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include <gtest/gtest.h>

#include "frc/kinematics/SwerveModuleState.h"
#include "kinematics.pb.h"

using namespace frc;

namespace {

using StructType = wpi::Struct<frc::SwerveModuleState>;
using ProtoType = wpi::Protobuf<frc::SwerveModuleState>;

constexpr std::array<uint8_t, StructType::kSize> create_test_buffer() {
  std::array<uint8_t, StructType::kSize> output;
  int buffer[] = {-113, -62, -11,  40,  92,   -113, -2,  63,
                  -108, -92, -122, -48, -100, 111,  -45, 63};
  for (size_t idx = 0; idx < StructType::kSize; ++idx) {
    output[idx] = static_cast<uint8_t>(buffer[idx]);
  }
  return output;
}

std::array<uint8_t, StructType::kSize> kExpectedStructBuffer =
    create_test_buffer();

constexpr SwerveModuleState kExpectedData{1.91_mps, Rotation2d{17.4_deg}};
}  // namespace

TEST(SwerveModuleStateSerdeTest, StructPack) {
  uint8_t buffer[StructType::kSize];
  StructType::Pack(buffer, kExpectedData);

  for (size_t i = 0; i < StructType::kSize; ++i) {
    EXPECT_EQ(kExpectedStructBuffer[i], buffer[i]) << " on byte " << i;
  }
}

TEST(SwerveModuleStateSerdeTest, StructUnpack) {
  SwerveModuleState unpacked_data = StructType::Unpack(kExpectedStructBuffer);

  EXPECT_EQ(kExpectedData.speed.value(), unpacked_data.speed.value());
  EXPECT_EQ(kExpectedData.angle, unpacked_data.angle);
}

TEST(SwerveModuleStateSerdeTest, ProtobufPack) {
  wpi::proto::ProtobufSwerveModuleState proto;
  ProtoType::Pack(&proto, kExpectedData);

  EXPECT_EQ(kExpectedData.speed.value(), proto.speed_mps());
  EXPECT_EQ(kExpectedData.angle.Radians().value(), proto.angle().radians());
}

TEST(SwerveModuleStateSerdeTest, ProtobufUnpack) {
  wpi::proto::ProtobufSwerveModuleState proto;
  proto.set_speed_mps(kExpectedData.speed.value());
  proto.mutable_angle()->set_radians(kExpectedData.angle.Radians().value());

  SwerveModuleState unpacked_data = ProtoType::Unpack(proto);
  EXPECT_EQ(kExpectedData.speed.value(), unpacked_data.speed.value());
  EXPECT_EQ(kExpectedData.angle, unpacked_data.angle);
}
