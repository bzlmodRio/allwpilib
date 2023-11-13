// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include <gtest/gtest.h>

#include "frc/geometry/Twist2d.h"
#include "geometry2d.pb.h"

using namespace frc;

namespace {

using StructType = wpi::Struct<frc::Twist2d>;
using ProtoType = wpi::Protobuf<frc::Twist2d>;

constexpr std::array<uint8_t, StructType::kSize> create_test_buffer() {
  std::array<uint8_t, StructType::kSize> output;
  int buffer[] = {-113, -62, -11, 40, 92,   -113, -2, 63,  82, -72,  30, -123,
                  -21,  81,  2,   64, -123, -21,  81, -72, 30, -123, 65, 64};
  for (size_t idx = 0; idx < StructType::kSize; ++idx) {
    output[idx] = static_cast<uint8_t>(buffer[idx]);
  }
  return output;
}

std::array<uint8_t, StructType::kSize> kExpectedStructBuffer =
    create_test_buffer();

constexpr Twist2d kExpectedData{1.91_m, 2.29_m, 35.04_rad};
}  // namespace

TEST(Twist2dSerdeTest, StructPack) {
  uint8_t buffer[StructType::kSize];
  StructType::Pack(buffer, kExpectedData);

  for (size_t i = 0; i < StructType::kSize; ++i) {
    EXPECT_EQ(kExpectedStructBuffer[i], buffer[i]) << " on byte " << i;
  }
}

TEST(Twist2dSerdeTest, StructUnpack) {
  Twist2d unpacked_data = StructType::Unpack(kExpectedStructBuffer);

  EXPECT_EQ(kExpectedData.dx.value(), unpacked_data.dx.value());
  EXPECT_EQ(kExpectedData.dy.value(), unpacked_data.dy.value());
  EXPECT_EQ(kExpectedData.dtheta.value(), unpacked_data.dtheta.value());
}

TEST(Twist2dSerdeTest, ProtobufPack) {
  wpi::proto::ProtobufTwist2d proto;
  ProtoType::Pack(&proto, kExpectedData);

  EXPECT_EQ(kExpectedData.dx.value(), proto.dx_meters());
  EXPECT_EQ(kExpectedData.dy.value(), proto.dy_meters());
  EXPECT_EQ(kExpectedData.dtheta.value(), proto.dtheta_radians());
}

TEST(Twist2dSerdeTest, ProtobufUnpack) {
  wpi::proto::ProtobufTwist2d proto;
  proto.set_dx_meters(kExpectedData.dx.value());
  proto.set_dy_meters(kExpectedData.dy.value());
  proto.set_dtheta_radians(kExpectedData.dtheta.value());

  Twist2d unpacked_data = ProtoType::Unpack(proto);
  EXPECT_EQ(kExpectedData.dx.value(), unpacked_data.dx.value());
  EXPECT_EQ(kExpectedData.dy.value(), unpacked_data.dy.value());
  EXPECT_EQ(kExpectedData.dtheta.value(), unpacked_data.dtheta.value());
}
