// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include <gtest/gtest.h>

#include "controller.pb.h"
#include "frc/controller/DifferentialDriveWheelVoltages.h"

using namespace frc;

namespace {

using StructType = wpi::Struct<frc::DifferentialDriveWheelVoltages>;
using ProtoType = wpi::Protobuf<frc::DifferentialDriveWheelVoltages>;

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

constexpr DifferentialDriveWheelVoltages kExpectedData{1.91_V, 2.29_V};
}  // namespace

TEST(DifferentialDriveWheelVoltagesSerdeTest, StructPack) {
  uint8_t buffer[StructType::kSize];
  StructType::Pack(buffer, kExpectedData);

  for (size_t i = 0; i < StructType::kSize; ++i) {
    EXPECT_EQ(kExpectedStructBuffer[i], buffer[i]) << " on byte " << i;
  }
}

TEST(DifferentialDriveWheelVoltagesSerdeTest, StructUnpack) {
  DifferentialDriveWheelVoltages unpacked_data =
      StructType::Unpack(kExpectedStructBuffer);

  EXPECT_EQ(kExpectedData.left.value(), unpacked_data.left.value());
  EXPECT_EQ(kExpectedData.right.value(), unpacked_data.right.value());
}

TEST(DifferentialDriveWheelVoltagesSerdeTest, ProtobufPack) {
  wpi::proto::ProtobufDifferentialDriveWheelVoltages proto;
  ProtoType::Pack(&proto, kExpectedData);

  EXPECT_EQ(kExpectedData.left.value(), proto.left_volts());
  EXPECT_EQ(kExpectedData.right.value(), proto.right_volts());
}

TEST(DifferentialDriveWheelVoltagesSerdeTest, ProtobufUnpack) {
  wpi::proto::ProtobufDifferentialDriveWheelVoltages proto;
  proto.set_left_volts(kExpectedData.left.value());
  proto.set_right_volts(kExpectedData.right.value());

  DifferentialDriveWheelVoltages unpacked_data = ProtoType::Unpack(proto);
  EXPECT_EQ(kExpectedData.left.value(), unpacked_data.left.value());
  EXPECT_EQ(kExpectedData.right.value(), unpacked_data.right.value());
}
