// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include <gtest/gtest.h>

#include "frc/kinematics/SwerveModulePosition.h"
#include "kinematics.pb.h"

using namespace frc;

namespace {

using StructType = wpi::Struct<frc::SwerveModulePosition>;
using ProtoType = wpi::Protobuf<frc::SwerveModulePosition>;

constexpr std::array<uint8_t, StructType::kSize> create_test_buffer() {
  std::array<uint8_t, StructType::kSize> output;
  int buffer[] = {-113, -62, -11, 40,  92,  -113, -2,  63,
                  -26,  110, 66,  -32, -80, 118,  -92, 63};
  for (size_t idx = 0; idx < StructType::kSize; ++idx) {
    output[idx] = static_cast<uint8_t>(buffer[idx]);
  }
  return output;
}

std::array<uint8_t, StructType::kSize> kExpectedStructBuffer =
    create_test_buffer();

constexpr SwerveModulePosition kExpectedData{1.91_m, Rotation2d{2.29_deg}};
}  // namespace

TEST(SwerveModulePositionSerdeTest, StructPack) {
  uint8_t buffer[StructType::kSize];
  StructType::Pack(buffer, kExpectedData);

  for (size_t i = 0; i < StructType::kSize; ++i) {
    EXPECT_EQ(kExpectedStructBuffer[i], buffer[i]) << " on byte " << i;
  }
}

TEST(SwerveModulePositionSerdeTest, StructUnpack) {
  SwerveModulePosition unpacked_data =
      StructType::Unpack(kExpectedStructBuffer);

  EXPECT_EQ(kExpectedData.distance.value(), unpacked_data.distance.value());
  EXPECT_EQ(kExpectedData.angle, unpacked_data.angle);
}

TEST(SwerveModulePositionSerdeTest, ProtobufPack) {
  wpi::proto::ProtobufSwerveModulePosition proto;
  ProtoType::Pack(&proto, kExpectedData);

  EXPECT_EQ(kExpectedData.distance.value(), proto.distance_meters());
  EXPECT_EQ(kExpectedData.angle.Radians().value(), proto.angle().radians());
}

TEST(SwerveModulePositionSerdeTest, ProtobufUnpack) {
  wpi::proto::ProtobufSwerveModulePosition proto;
  proto.set_distance_meters(kExpectedData.distance.value());
  proto.mutable_angle()->set_radians(kExpectedData.angle.Radians().value());

  SwerveModulePosition unpacked_data = ProtoType::Unpack(proto);
  EXPECT_EQ(kExpectedData.distance.value(), unpacked_data.distance.value());
  EXPECT_EQ(kExpectedData.angle, unpacked_data.angle);
}
