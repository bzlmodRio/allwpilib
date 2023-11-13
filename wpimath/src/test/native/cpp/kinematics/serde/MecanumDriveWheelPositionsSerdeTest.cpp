// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include <gtest/gtest.h>

#include "frc/kinematics/MecanumDriveWheelPositions.h"
#include "kinematics.pb.h"

using namespace frc;

namespace {

using StructType = wpi::Struct<frc::MecanumDriveWheelPositions>;
using ProtoType = wpi::Protobuf<frc::MecanumDriveWheelPositions>;

constexpr std::array<uint8_t, StructType::kSize> create_test_buffer() {
  std::array<uint8_t, StructType::kSize> output;
  int buffer[] = {-113, -62, -11, 40,  92,  -113, -2,  63,  82,  -72, 30,
                  -123, -21, 81,  2,   64,  -123, -21, 81,  -72, 30,  -123,
                  65,   64,  102, 102, 102, 102,  102, 102, 49,  64};
  for (size_t idx = 0; idx < StructType::kSize; ++idx) {
    output[idx] = static_cast<uint8_t>(buffer[idx]);
  }
  return output;
}

std::array<uint8_t, StructType::kSize> kExpectedStructBuffer =
    create_test_buffer();

constexpr MecanumDriveWheelPositions kExpectedData{1.91_m, 2.29_m, 35.04_m,
                                                   17.4_m};
}  // namespace

TEST(MecanumDriveWheelPositionsSerdeTest, StructPack) {
  uint8_t buffer[StructType::kSize];
  StructType::Pack(buffer, kExpectedData);

  for (size_t i = 0; i < StructType::kSize; ++i) {
    EXPECT_EQ(kExpectedStructBuffer[i], buffer[i]) << " on byte " << i;
  }
}

TEST(MecanumDriveWheelPositionsSerdeTest, StructUnpack) {
  MecanumDriveWheelPositions unpacked_data =
      StructType::Unpack(kExpectedStructBuffer);

  EXPECT_EQ(kExpectedData.frontLeft.value(), unpacked_data.frontLeft.value());
  EXPECT_EQ(kExpectedData.frontRight.value(), unpacked_data.frontRight.value());
  EXPECT_EQ(kExpectedData.rearLeft.value(), unpacked_data.rearLeft.value());
  EXPECT_EQ(kExpectedData.rearRight.value(), unpacked_data.rearRight.value());
}

TEST(MecanumDriveWheelPositionsSerdeTest, ProtobufPack) {
  wpi::proto::ProtobufMecanumDriveWheelPositions proto;
  ProtoType::Pack(&proto, kExpectedData);

  EXPECT_EQ(kExpectedData.frontLeft.value(), proto.front_left_meters());
  EXPECT_EQ(kExpectedData.frontRight.value(), proto.front_right_meters());
  EXPECT_EQ(kExpectedData.rearLeft.value(), proto.rear_left_meters());
  EXPECT_EQ(kExpectedData.rearRight.value(), proto.rear_right_meters());
}

TEST(MecanumDriveWheelPositionsSerdeTest, ProtobufUnpack) {
  wpi::proto::ProtobufMecanumDriveWheelPositions proto;
  proto.set_front_left_meters(kExpectedData.frontLeft.value());
  proto.set_front_right_meters(kExpectedData.frontRight.value());
  proto.set_rear_left_meters(kExpectedData.rearLeft.value());
  proto.set_rear_right_meters(kExpectedData.rearRight.value());

  MecanumDriveWheelPositions unpacked_data = ProtoType::Unpack(proto);
  EXPECT_EQ(kExpectedData.frontLeft.value(), unpacked_data.frontLeft.value());
  EXPECT_EQ(kExpectedData.frontRight.value(), unpacked_data.frontRight.value());
  EXPECT_EQ(kExpectedData.rearLeft.value(), unpacked_data.rearLeft.value());
  EXPECT_EQ(kExpectedData.rearRight.value(), unpacked_data.rearRight.value());
}
