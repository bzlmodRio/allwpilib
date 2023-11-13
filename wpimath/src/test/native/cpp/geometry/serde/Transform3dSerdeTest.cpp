// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include <gtest/gtest.h>

#include "frc/geometry/Transform3d.h"
#include "geometry3d.pb.h"

using namespace frc;

namespace {

using StructType = wpi::Struct<frc::Transform3d>;
using ProtoType = wpi::Protobuf<frc::Transform3d>;

constexpr std::array<uint8_t, StructType::kSize> create_test_buffer() {
  std::array<uint8_t, StructType::kSize> output;
  int buffer[] = {
      -113, -62, -11, 40,   92,  -113, -2,  63,  82, -72, 30,  -123, -21, 81,
      2,    64,  -41, -93,  112, 61,   10,  -41, -5, 63,  103, -6,   -36, 49,
      -45,  -62, -37, 63,   41,  -88,  -17, -82, 62, -42, -24, -65,  110, 94,
      -118, -72, -64, -114, -58, 63,   36,  52,  84, -57, -74, 7,    -37, 63};
  for (size_t idx = 0; idx < StructType::kSize; ++idx) {
    output[idx] = static_cast<uint8_t>(buffer[idx]);
  }
  return output;
}

std::array<uint8_t, StructType::kSize> kExpectedStructBuffer =
    create_test_buffer();

const Transform3d kExpectedData{Translation3d(1.91_m, 2.29_m, 1.74_m),
                                Rotation3d(1.1_rad, 2.2_rad, 3.3_rad)};
}  // namespace

TEST(Transform3dSerdeTest, StructPack) {
  uint8_t buffer[StructType::kSize];
  StructType::Pack(buffer, kExpectedData);

  for (size_t i = 0; i < StructType::kSize; ++i) {
    EXPECT_EQ(kExpectedStructBuffer[i], buffer[i]) << " on byte " << i;
  }
}

TEST(Transform3dSerdeTest, StructUnpack) {
  Transform3d unpacked_data = StructType::Unpack(kExpectedStructBuffer);

  EXPECT_EQ(kExpectedData.Translation(), unpacked_data.Translation());
  EXPECT_EQ(kExpectedData.Rotation(), unpacked_data.Rotation());
}

TEST(Transform3dSerdeTest, ProtobufPack) {
  wpi::proto::ProtobufTransform3d proto;
  ProtoType::Pack(&proto, kExpectedData);

  EXPECT_EQ(kExpectedData.Translation().X().value(),
            proto.translation().x_meters());
  EXPECT_EQ(kExpectedData.Translation().Y().value(),
            proto.translation().y_meters());
  EXPECT_EQ(kExpectedData.Translation().Z().value(),
            proto.translation().z_meters());
  EXPECT_EQ(kExpectedData.Rotation().GetQuaternion().W(),
            proto.rotation().quaternion().w());
  EXPECT_EQ(kExpectedData.Rotation().GetQuaternion().X(),
            proto.rotation().quaternion().x());
  EXPECT_EQ(kExpectedData.Rotation().GetQuaternion().Y(),
            proto.rotation().quaternion().y());
  EXPECT_EQ(kExpectedData.Rotation().GetQuaternion().Z(),
            proto.rotation().quaternion().z());
}

TEST(Transform3dSerdeTest, ProtobufUnpack) {
  wpi::proto::ProtobufTransform3d proto;
  proto.mutable_translation()->set_x_meters(
      kExpectedData.Translation().X().value());
  proto.mutable_translation()->set_y_meters(
      kExpectedData.Translation().Y().value());
  proto.mutable_translation()->set_z_meters(
      kExpectedData.Translation().Z().value());
  proto.mutable_rotation()->mutable_quaternion()->set_w(
      kExpectedData.Rotation().GetQuaternion().W());
  proto.mutable_rotation()->mutable_quaternion()->set_x(
      kExpectedData.Rotation().GetQuaternion().X());
  proto.mutable_rotation()->mutable_quaternion()->set_y(
      kExpectedData.Rotation().GetQuaternion().Y());
  proto.mutable_rotation()->mutable_quaternion()->set_z(
      kExpectedData.Rotation().GetQuaternion().Z());

  Transform3d unpacked_data = ProtoType::Unpack(proto);
  EXPECT_EQ(kExpectedData.Translation(), unpacked_data.Translation());
  EXPECT_EQ(kExpectedData.Rotation(), unpacked_data.Rotation());
}
