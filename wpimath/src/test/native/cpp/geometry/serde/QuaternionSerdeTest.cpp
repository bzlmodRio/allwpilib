// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include <gtest/gtest.h>

#include "frc/geometry/Quaternion.h"
#include "geometry3d.pb.h"

using namespace frc;

namespace {

using StructType = wpi::Struct<frc::Quaternion>;
using ProtoType = wpi::Protobuf<frc::Quaternion>;

constexpr std::array<uint8_t, StructType::kSize> create_test_buffer() {
  std::array<uint8_t, StructType::kSize> output;
  int buffer[] = {-102, -103, -103, -103, -103, -103, -15, 63,
                  -102, -103, -103, -103, -103, -103, 1,   64,
                  102,  102,  102,  102,  102,  102,  10,  64,
                  -102, -103, -103, -103, -103, -103, 17,  64};
  for (size_t idx = 0; idx < StructType::kSize; ++idx) {
    output[idx] = static_cast<uint8_t>(buffer[idx]);
  }
  return output;
}

std::array<uint8_t, StructType::kSize> kExpectedStructBuffer =
    create_test_buffer();

const Quaternion kExpectedData{1.1, 2.2, 3.3, 4.4};
}  // namespace

TEST(QuaternionSerdeTest, StructPack) {
  uint8_t buffer[StructType::kSize];
  StructType::Pack(buffer, kExpectedData);

  for (size_t i = 0; i < StructType::kSize; ++i) {
    EXPECT_EQ(kExpectedStructBuffer[i], buffer[i]) << " on byte " << i;
  }
}

TEST(QuaternionSerdeTest, StructUnpack) {
  Quaternion unpacked_data = StructType::Unpack(kExpectedStructBuffer);

  EXPECT_EQ(kExpectedData.W(), unpacked_data.W());
  EXPECT_EQ(kExpectedData.X(), unpacked_data.X());
  EXPECT_EQ(kExpectedData.Y(), unpacked_data.Y());
  EXPECT_EQ(kExpectedData.Z(), unpacked_data.Z());
}

TEST(QuaternionSerdeTest, ProtobufPack) {
  wpi::proto::ProtobufQuaternion proto;
  ProtoType::Pack(&proto, kExpectedData);

  EXPECT_EQ(kExpectedData.W(), proto.w());
  EXPECT_EQ(kExpectedData.X(), proto.x());
  EXPECT_EQ(kExpectedData.Y(), proto.y());
  EXPECT_EQ(kExpectedData.Z(), proto.z());
}

TEST(QuaternionSerdeTest, ProtobufUnpack) {
  wpi::proto::ProtobufQuaternion proto;
  proto.set_w(kExpectedData.W());
  proto.set_x(kExpectedData.X());
  proto.set_y(kExpectedData.Y());
  proto.set_z(kExpectedData.Z());

  Quaternion unpacked_data = ProtoType::Unpack(proto);
  EXPECT_EQ(kExpectedData.W(), unpacked_data.W());
  EXPECT_EQ(kExpectedData.X(), unpacked_data.X());
  EXPECT_EQ(kExpectedData.Y(), unpacked_data.Y());
  EXPECT_EQ(kExpectedData.Z(), unpacked_data.Z());
}
