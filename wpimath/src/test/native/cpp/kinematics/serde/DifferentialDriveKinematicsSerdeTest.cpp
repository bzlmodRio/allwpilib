// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include <gtest/gtest.h>

#include "frc/kinematics/DifferentialDriveKinematics.h"
#include "kinematics.pb.h"

using namespace frc;

namespace {

using StructType = wpi::Struct<frc::DifferentialDriveKinematics>;
using ProtoType = wpi::Protobuf<frc::DifferentialDriveKinematics>;

constexpr std::array<uint8_t, StructType::kSize> create_test_buffer() {
  std::array<uint8_t, StructType::kSize> output;
  int buffer[] = {-113, -62, -11, 40, 92, -113, -2, 63};
  for (size_t idx = 0; idx < StructType::kSize; ++idx) {
    output[idx] = static_cast<uint8_t>(buffer[idx]);
  }
  return output;
}

std::array<uint8_t, StructType::kSize> kExpectedStructBuffer =
    create_test_buffer();

const DifferentialDriveKinematics kExpectedData{1.91_m};
}  // namespace

TEST(DifferentialDriveKinematicsSerdeTest, StructPack) {
  uint8_t buffer[StructType::kSize];
  StructType::Pack(buffer, kExpectedData);

  for (size_t i = 0; i < StructType::kSize; ++i) {
    EXPECT_EQ(kExpectedStructBuffer[i], buffer[i]) << " on byte " << i;
  }
}

TEST(DifferentialDriveKinematicsSerdeTest, StructUnpack) {
  DifferentialDriveKinematics unpacked_data =
      StructType::Unpack(kExpectedStructBuffer);

  EXPECT_EQ(kExpectedData.trackWidth.value(), unpacked_data.trackWidth.value());
}

TEST(DifferentialDriveKinematicsSerdeTest, ProtobufPack) {
  wpi::proto::ProtobufDifferentialDriveKinematics proto;
  ProtoType::Pack(&proto, kExpectedData);

  EXPECT_EQ(kExpectedData.trackWidth.value(), proto.track_width_meters());
}

TEST(DifferentialDriveKinematicsSerdeTest, ProtobufUnpack) {
  wpi::proto::ProtobufDifferentialDriveKinematics proto;
  proto.set_track_width_meters(kExpectedData.trackWidth.value());

  DifferentialDriveKinematics unpacked_data = ProtoType::Unpack(proto);
  EXPECT_EQ(kExpectedData.trackWidth.value(), unpacked_data.trackWidth.value());
}
