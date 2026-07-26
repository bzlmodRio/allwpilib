// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include "wpi/math/trajectory/struct/TrapezoidProfileStruct.hpp"

#include <cstring>

#include <gtest/gtest.h>

using namespace wpi::math;

TEST(TrapezoidProfileStructTest, NonBaseDistanceConstraintRoundtrip) {
  using Constraints = TrapezoidProfile<wpi::units::feet>::Constraints;
  using StructType = wpi::util::Struct<Constraints>;

  const Constraints expected{Constraints::Velocity_t{3.0},
                             Constraints::Acceleration_t{4.0}};
  uint8_t buffer[StructType::GetSize()];
  std::memset(buffer, 0, StructType::GetSize());

  StructType::Pack(buffer, expected);

  const double packedVelocity = wpi::util::UnpackStruct<double, 0>(buffer);
  const double packedAcceleration = wpi::util::UnpackStruct<double, 8>(buffer);

  EXPECT_NEAR(0.9144, packedVelocity, 1e-12);
  EXPECT_NEAR(1.2192, packedAcceleration, 1e-12);

  Constraints unpackedData = StructType::Unpack(buffer);

  EXPECT_NEAR(expected.maxVelocity.value(), unpackedData.maxVelocity.value(),
              1e-12);
  EXPECT_NEAR(expected.maxAcceleration.value(),
              unpackedData.maxAcceleration.value(), 1e-12);
}
