// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include <gtest/gtest.h>

#include "frc/kinematics/DifferentialDriveWheelSpeeds.h"
#include "kinematics.pb.h"

using namespace frc;

namespace {

using StructType = wpi::Struct<frc::DifferentialDriveWheelSpeeds>;
using ProtoType = wpi::Protobuf<frc::DifferentialDriveWheelSpeeds>;

constexpr std::array<uint8_t, StructType::kSize> create_test_buffer() {
  std::array<uint8_t, StructType::kSize> output;
  int buffer[] = {-113, -62, -11, 40,   92,  -113, -2, 63,
                  82,   -72, 30,  -123, -21, 81,   2,  64};
  for (size_t idx = 0; idx < StructType::kSize; ++idx) {
    output[idx] = static_cast<uint8_t>(buffer[idx]);
  }
  return output;
}

std::array<uint8_t, StructType::kSize> kExpectedStructBuffer =
    create_test_buffer();

constexpr DifferentialDriveWheelSpeeds kExpectedData{1.91_mps, 2.29_mps};
}  // namespace

TEST(DifferentialDriveWheelSpeedsSerdeTest, StructPack) {
  uint8_t buffer[StructType::kSize];
  StructType::Pack(buffer, kExpectedData);

  for (size_t i = 0; i < StructType::kSize; ++i) {
    EXPECT_EQ(kExpectedStructBuffer[i], buffer[i]) << " on byte " << i;
  }
}

TEST(DifferentialDriveWheelSpeedsSerdeTest, StructUnpack) {
  DifferentialDriveWheelSpeeds unpacked_data =
      StructType::Unpack(kExpectedStructBuffer);

  EXPECT_EQ(kExpectedData.left.value(), unpacked_data.left.value());
  EXPECT_EQ(kExpectedData.right.value(), unpacked_data.right.value());
}

TEST(DifferentialDriveWheelSpeedsSerdeTest, ProtobufPack) {
  wpi::proto::ProtobufDifferentialDriveWheelSpeeds proto;
  ProtoType::Pack(&proto, kExpectedData);

  EXPECT_EQ(kExpectedData.left.value(), proto.left_mps());
  EXPECT_EQ(kExpectedData.right.value(), proto.right_mps());
}

TEST(DifferentialDriveWheelSpeedsSerdeTest, ProtobufUnpack) {
  wpi::proto::ProtobufDifferentialDriveWheelSpeeds proto;
  proto.set_left_mps(kExpectedData.left.value());
  proto.set_right_mps(kExpectedData.right.value());

  DifferentialDriveWheelSpeeds unpacked_data = ProtoType::Unpack(proto);
  EXPECT_EQ(kExpectedData.left.value(), unpacked_data.left.value());
  EXPECT_EQ(kExpectedData.right.value(), unpacked_data.right.value());
}
