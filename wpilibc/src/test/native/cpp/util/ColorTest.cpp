// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include <gtest/gtest.h>

#include "frc/util/Color.h"

TEST(ColorTest, ConstructDefault) {
  constexpr frc::Color color;

  EXPECT_DOUBLE_EQ(0.0, color.red);
  EXPECT_DOUBLE_EQ(0.0, color.green);
  EXPECT_DOUBLE_EQ(0.0, color.blue);
}

TEST(ColorTest, ConstructFromDoubles) {
  constexpr frc::Color color{1.0, 0.5, 0.25};

  EXPECT_NEAR(1.0, color.red, 1e-2);
  EXPECT_NEAR(0.5, color.green, 1e-2);
  EXPECT_NEAR(0.25, color.blue, 1e-2);
}

TEST(ColorTest, ConstructFromInts) {
  constexpr frc::Color color{255, 128, 64};

  EXPECT_NEAR(1.0, color.red, 1e-2);
  EXPECT_NEAR(0.5, color.green, 1e-2);
  EXPECT_NEAR(0.25, color.blue, 1e-2);
}

TEST(ColorTest, ConstructFromHexString) {
  constexpr frc::Color color{"#FF8040"};

  EXPECT_NEAR(1.0, color.red, 1e-2);
  EXPECT_NEAR(0.5, color.green, 1e-2);
  EXPECT_NEAR(0.25, color.blue, 1e-2);

  // No leading #
  EXPECT_THROW(frc::Color{"112233"}, std::invalid_argument);

  // Too long
  EXPECT_THROW(frc::Color{"#11223344"}, std::invalid_argument);

  // Invalid hex characters
  EXPECT_THROW(frc::Color{"#$$$$$$"}, std::invalid_argument);
}

TEST(ColorTest, FromHSV) {
  constexpr frc::Color color = frc::Color::FromHSV(90, 128, 64);

  EXPECT_DOUBLE_EQ(0.1256103515625, color.red);
  EXPECT_DOUBLE_EQ(0.2510986328125, color.green);
  EXPECT_DOUBLE_EQ(0.2510986328125, color.blue);
}

TEST(ColorTest, ToHexString) {
  constexpr frc::Color color{255, 128, 64};

  EXPECT_EQ("#FF8040", color.HexString());
}
