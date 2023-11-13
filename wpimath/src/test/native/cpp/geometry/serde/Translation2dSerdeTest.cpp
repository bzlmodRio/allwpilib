// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include <gtest/gtest.h>

#include "frc/geometry/Translation2d.h"
#include "geometry2d.pb.h"

using namespace frc;

namespace {

using StructType = wpi::Struct<frc::Translation2d>;
using ProtoType = wpi::Protobuf<frc::Translation2d>;

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

constexpr Translation2d kExpectedData{1.91_m, 2.29_m};
}  // namespace

TEST(Translation2dSerdeTest, StructPack) {
  uint8_t buffer[StructType::kSize];
  StructType::Pack(buffer, kExpectedData);

  for (size_t i = 0; i < StructType::kSize; ++i) {
    EXPECT_EQ(kExpectedStructBuffer[i], buffer[i]) << " on byte " << i;
  }
}

TEST(Translation2dSerdeTest, StructUnpack) {
  Translation2d unpacked_data = StructType::Unpack(kExpectedStructBuffer);

  EXPECT_EQ(kExpectedData.X().value(), unpacked_data.X().value());
  EXPECT_EQ(kExpectedData.Y().value(), unpacked_data.Y().value());
}

TEST(Translation2dSerdeTest, ProtobufPack) {
  wpi::proto::ProtobufTranslation2d proto;
  ProtoType::Pack(&proto, kExpectedData);

  EXPECT_EQ(kExpectedData.X().value(), proto.x_meters());
  EXPECT_EQ(kExpectedData.Y().value(), proto.y_meters());
}

TEST(Translation2dSerdeTest, ProtobufUnpack) {
  wpi::proto::ProtobufTranslation2d proto;
  proto.set_x_meters(kExpectedData.X().value());
  proto.set_y_meters(kExpectedData.Y().value());

  Translation2d unpacked_data = ProtoType::Unpack(proto);
  EXPECT_EQ(kExpectedData.X().value(), unpacked_data.X().value());
  EXPECT_EQ(kExpectedData.Y().value(), unpacked_data.Y().value());
}
