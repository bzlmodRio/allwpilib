// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include <gtest/gtest.h>

#include "frc/kinematics/ChassisSpeeds.h"
#include "kinematics.pb.h"

using namespace frc;

namespace {

using StructType = wpi::Struct<frc::ChassisSpeeds>;
using ProtoType = wpi::Protobuf<frc::ChassisSpeeds>;

constexpr std::array<uint8_t, StructType::kSize> create_test_buffer() {
  std::array<uint8_t, StructType::kSize> output;
  int buffer[] = {-113, -62, -11, 40, 92,  -113, -2,  63, 82, -72, 30, -123,
                  -21,  81,  2,   64, -43, 120,  -23, 38, 49, 8,   12, 64};
  for (size_t idx = 0; idx < StructType::kSize; ++idx) {
    output[idx] = static_cast<uint8_t>(buffer[idx]);
  }
  return output;
}

std::array<uint8_t, StructType::kSize> kExpectedStructBuffer =
    create_test_buffer();

constexpr ChassisSpeeds kExpectedData{1.91_mps, 2.29_mps, 3.504_rad_per_s};
}  // namespace

TEST(ChassisSpeedsSerdeTest, StructPack) {
  uint8_t buffer[StructType::kSize];
  StructType::Pack(buffer, kExpectedData);

  for (size_t i = 0; i < StructType::kSize; ++i) {
    EXPECT_EQ(kExpectedStructBuffer[i], buffer[i]) << " on byte " << i;
  }
}

TEST(ChassisSpeedsSerdeTest, StructUnpack) {
  ChassisSpeeds unpacked_data = StructType::Unpack(kExpectedStructBuffer);

  EXPECT_EQ(kExpectedData.vx.value(), unpacked_data.vx.value());
  EXPECT_EQ(kExpectedData.vy.value(), unpacked_data.vy.value());
  EXPECT_EQ(kExpectedData.omega.value(), unpacked_data.omega.value());
}

TEST(ChassisSpeedsSerdeTest, ProtobufPack) {
  wpi::proto::ProtobufChassisSpeeds proto;
  ProtoType::Pack(&proto, kExpectedData);

  EXPECT_EQ(kExpectedData.vx.value(), proto.vx_mps());
  EXPECT_EQ(kExpectedData.vy.value(), proto.vy_mps());
  EXPECT_EQ(kExpectedData.omega.value(), proto.omega_rps());
}

TEST(ChassisSpeedsSerdeTest, ProtobufUnpack) {
  wpi::proto::ProtobufChassisSpeeds proto;
  proto.set_vx_mps(kExpectedData.vx.value());
  proto.set_vy_mps(kExpectedData.vy.value());
  proto.set_omega_rps(kExpectedData.omega.value());

  ChassisSpeeds unpacked_data = ProtoType::Unpack(proto);
  EXPECT_EQ(kExpectedData.vx.value(), unpacked_data.vx.value());
  EXPECT_EQ(kExpectedData.vy.value(), unpacked_data.vy.value());
  EXPECT_EQ(kExpectedData.omega.value(), unpacked_data.omega.value());
}
