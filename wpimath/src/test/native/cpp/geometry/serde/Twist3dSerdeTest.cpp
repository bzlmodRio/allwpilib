// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include <gtest/gtest.h>

#include "frc/geometry/Twist3d.h"
#include "geometry3d.pb.h"

using namespace frc;

namespace {

using StructType = wpi::Struct<frc::Twist3d>;
using ProtoType = wpi::Protobuf<frc::Twist3d>;

constexpr std::array<uint8_t, StructType::kSize> create_test_buffer() {
  std::array<uint8_t, StructType::kSize> output;
  int buffer[] = {-113, -62,  -11,  40, 92,  -113, -2,  63, 82, -72, 30,   -123,
                  -21,  81,   2,    64, -41, -93,  112, 61, 10, -41, -5,   63,
                  119,  45,   33,   31, -12, 108,  -42, 63, 30, 22,  106,  77,
                  -13,  -114, -109, 63, 23,  72,   80,  -4, 24, 115, -105, 63};
  for (size_t idx = 0; idx < StructType::kSize; ++idx) {
    output[idx] = static_cast<uint8_t>(buffer[idx]);
  }
  return output;
}

std::array<uint8_t, StructType::kSize> kExpectedStructBuffer =
    create_test_buffer();

constexpr Twist3d kExpectedData{1.91_m,    2.29_m,    1.74_m,
                                .3504_rad, .0191_rad, .0229_rad};
}  // namespace

TEST(Twist3dSerdeTest, StructPack) {
  uint8_t buffer[StructType::kSize];
  StructType::Pack(buffer, kExpectedData);

  for (size_t i = 0; i < StructType::kSize; ++i) {
    EXPECT_EQ(kExpectedStructBuffer[i], buffer[i]) << " on byte " << i;
  }
}

TEST(Twist3dSerdeTest, StructUnpack) {
  Twist3d unpacked_data = StructType::Unpack(kExpectedStructBuffer);

  EXPECT_EQ(kExpectedData.dx.value(), unpacked_data.dx.value());
  EXPECT_EQ(kExpectedData.dy.value(), unpacked_data.dy.value());
  EXPECT_EQ(kExpectedData.dz.value(), unpacked_data.dz.value());
  EXPECT_EQ(kExpectedData.rx.value(), unpacked_data.rx.value());
  EXPECT_EQ(kExpectedData.ry.value(), unpacked_data.ry.value());
  EXPECT_EQ(kExpectedData.rz.value(), unpacked_data.rz.value());
}

TEST(Twist3dSerdeTest, ProtobufPack) {
  wpi::proto::ProtobufTwist3d proto;
  ProtoType::Pack(&proto, kExpectedData);

  EXPECT_EQ(kExpectedData.dx.value(), proto.dx_meters());
  EXPECT_EQ(kExpectedData.dy.value(), proto.dy_meters());
  EXPECT_EQ(kExpectedData.dz.value(), proto.dz_meters());
  EXPECT_EQ(kExpectedData.rx.value(), proto.rx_radians());
  EXPECT_EQ(kExpectedData.ry.value(), proto.ry_radians());
  EXPECT_EQ(kExpectedData.rz.value(), proto.rz_radians());
}

TEST(Twist3dSerdeTest, ProtobufUnpack) {
  wpi::proto::ProtobufTwist3d proto;
  proto.set_dx_meters(kExpectedData.dx.value());
  proto.set_dy_meters(kExpectedData.dy.value());
  proto.set_dz_meters(kExpectedData.dz.value());
  proto.set_rx_radians(kExpectedData.rx.value());
  proto.set_ry_radians(kExpectedData.ry.value());
  proto.set_rz_radians(kExpectedData.rz.value());

  Twist3d unpacked_data = ProtoType::Unpack(proto);
  EXPECT_EQ(kExpectedData.dx.value(), unpacked_data.dx.value());
  EXPECT_EQ(kExpectedData.dy.value(), unpacked_data.dy.value());
  EXPECT_EQ(kExpectedData.dz.value(), unpacked_data.dz.value());
  EXPECT_EQ(kExpectedData.rx.value(), unpacked_data.rx.value());
  EXPECT_EQ(kExpectedData.ry.value(), unpacked_data.ry.value());
  EXPECT_EQ(kExpectedData.rz.value(), unpacked_data.rz.value());
}
