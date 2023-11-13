// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include <gtest/gtest.h>

#include "frc/kinematics/MecanumDriveWheelSpeeds.h"
#include "kinematics.pb.h"

using namespace frc;

namespace {

using StructType = wpi::Struct<frc::MecanumDriveWheelSpeeds>;
using ProtoType = wpi::Protobuf<frc::MecanumDriveWheelSpeeds>;

constexpr std::array<uint8_t, StructType::kSize> create_test_buffer() {
  std::array<uint8_t, StructType::kSize> output;
  int buffer[] = {-102, -103, -103, -103, -103, 25,   51,  64, 102,  102, 102,
                  102,  102,  -26,  54,   64,   -104, 110, 18, -125, -64, -54,
                  -43,  63,   18,   -125, -64,  -54,  -95, 69, -58,  63};
  for (size_t idx = 0; idx < StructType::kSize; ++idx) {
    output[idx] = static_cast<uint8_t>(buffer[idx]);
  }
  return output;
}

std::array<uint8_t, StructType::kSize> kExpectedStructBuffer =
    create_test_buffer();

constexpr MecanumDriveWheelSpeeds kExpectedData{19.1_mps, 22.9_mps, 0.3405_mps,
                                                0.174_mps};
}  // namespace

TEST(MecanumDriveWheelSpeedsSerdeTest, StructPack) {
  uint8_t buffer[StructType::kSize];
  StructType::Pack(buffer, kExpectedData);

  for (size_t i = 0; i < StructType::kSize; ++i) {
    EXPECT_EQ(kExpectedStructBuffer[i], buffer[i]) << " on byte " << i;
  }
}

TEST(MecanumDriveWheelSpeedsSerdeTest, StructUnpack) {
  MecanumDriveWheelSpeeds unpacked_data =
      StructType::Unpack(kExpectedStructBuffer);

  EXPECT_EQ(kExpectedData.frontLeft.value(), unpacked_data.frontLeft.value());
  EXPECT_EQ(kExpectedData.frontRight.value(), unpacked_data.frontRight.value());
  EXPECT_EQ(kExpectedData.rearLeft.value(), unpacked_data.rearLeft.value());
  EXPECT_EQ(kExpectedData.rearRight.value(), unpacked_data.rearRight.value());
}

TEST(MecanumDriveWheelSpeedsSerdeTest, ProtobufPack) {
  wpi::proto::ProtobufMecanumDriveWheelSpeeds proto;
  ProtoType::Pack(&proto, kExpectedData);

  EXPECT_EQ(kExpectedData.frontLeft.value(), proto.front_left_mps());
  EXPECT_EQ(kExpectedData.frontRight.value(), proto.front_right_mps());
  EXPECT_EQ(kExpectedData.rearLeft.value(), proto.rear_left_mps());
  EXPECT_EQ(kExpectedData.rearRight.value(), proto.rear_right_mps());
}

TEST(MecanumDriveWheelSpeedsSerdeTest, ProtobufUnpack) {
  wpi::proto::ProtobufMecanumDriveWheelSpeeds proto;
  proto.set_front_left_mps(kExpectedData.frontLeft.value());
  proto.set_front_right_mps(kExpectedData.frontRight.value());
  proto.set_rear_left_mps(kExpectedData.rearLeft.value());
  proto.set_rear_right_mps(kExpectedData.rearRight.value());

  MecanumDriveWheelSpeeds unpacked_data = ProtoType::Unpack(proto);
  EXPECT_EQ(kExpectedData.frontLeft.value(), unpacked_data.frontLeft.value());
  EXPECT_EQ(kExpectedData.frontRight.value(), unpacked_data.frontRight.value());
  EXPECT_EQ(kExpectedData.rearLeft.value(), unpacked_data.rearLeft.value());
  EXPECT_EQ(kExpectedData.rearRight.value(), unpacked_data.rearRight.value());
}
