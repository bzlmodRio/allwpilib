// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include <gtest/gtest.h>

#include "frc/geometry/Rotation3d.h"
#include "geometry3d.pb.h"

using namespace frc;

namespace {

using StructType = wpi::Struct<frc::Rotation3d>;
using ProtoType = wpi::Protobuf<frc::Rotation3d>;

constexpr std::array<uint8_t, StructType::kSize> create_test_buffer() {
  std::array<uint8_t, StructType::kSize> output;
  int buffer[] = {10,  -88, 124, 104, -38, 70, -27, -65, 95,  75,   113,
                  113, 97,  -20, -30, 63,  11, -40, 66,  111, -115, -46,
                  -55, -65, 44,  -40, 31,  20, -91, 49,  -38, -65};
  for (size_t idx = 0; idx < StructType::kSize; ++idx) {
    output[idx] = static_cast<uint8_t>(buffer[idx]);
  }
  return output;
}

std::array<uint8_t, StructType::kSize> kExpectedStructBuffer =
    create_test_buffer();

const Rotation3d kExpectedData{1.91_rad, 2.29_rad, 35.04_rad};
}  // namespace

TEST(Rotation3dSerdeTest, StructPack) {
  uint8_t buffer[StructType::kSize];
  StructType::Pack(buffer, kExpectedData);

  for (size_t i = 0; i < StructType::kSize; ++i) {
    EXPECT_EQ(kExpectedStructBuffer[i], buffer[i]) << " on byte " << i;
  }
}

TEST(Rotation3dSerdeTest, StructUnpack) {
  Rotation3d unpacked_data = StructType::Unpack(kExpectedStructBuffer);

  EXPECT_EQ(kExpectedData.GetQuaternion(), unpacked_data.GetQuaternion());
}

TEST(Rotation3dSerdeTest, ProtobufPack) {
  wpi::proto::ProtobufRotation3d proto;
  ProtoType::Pack(&proto, kExpectedData);

  EXPECT_EQ(kExpectedData.GetQuaternion().W(), proto.quaternion().w());
  EXPECT_EQ(kExpectedData.GetQuaternion().X(), proto.quaternion().x());
  EXPECT_EQ(kExpectedData.GetQuaternion().Y(), proto.quaternion().y());
  EXPECT_EQ(kExpectedData.GetQuaternion().Z(), proto.quaternion().z());
}

TEST(Rotation3dSerdeTest, ProtobufUnpack) {
  wpi::proto::ProtobufRotation3d proto;
  proto.mutable_quaternion()->set_w(kExpectedData.GetQuaternion().W());
  proto.mutable_quaternion()->set_x(kExpectedData.GetQuaternion().X());
  proto.mutable_quaternion()->set_y(kExpectedData.GetQuaternion().Y());
  proto.mutable_quaternion()->set_z(kExpectedData.GetQuaternion().Z());

  Rotation3d unpacked_data = ProtoType::Unpack(proto);
  EXPECT_EQ(kExpectedData.GetQuaternion(), unpacked_data.GetQuaternion());
}
