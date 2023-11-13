// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package edu.wpi.first.math.kinematics.serde;

import edu.wpi.first.math.kinematics.MecanumDriveWheelSpeeds;
import edu.wpi.first.util.struct.Struct;
import java.nio.ByteBuffer;

public class MecanumDriveWheelSpeedsStructSerde implements Struct<MecanumDriveWheelSpeeds> {
  @Override
  public Class<MecanumDriveWheelSpeeds> getTypeClass() {
    return MecanumDriveWheelSpeeds.class;
  }

  @Override
  public String getTypeString() {
    return "struct:MecanumDriveWheelSpeeds";
  }

  @Override
  public int getSize() {
    return kSizeDouble * 4;
  }

  @Override
  public String getSchema() {
    return "double front_left_mps;double front_right_mps;double rear_left_mps;double rear_right_mps";
  }

  @Override
  public MecanumDriveWheelSpeeds unpack(ByteBuffer bb) {
    double frontLeft = bb.getDouble();
    double frontRight = bb.getDouble();
    double rearLeft = bb.getDouble();
    double rearRight = bb.getDouble();
    return new MecanumDriveWheelSpeeds(frontLeft, frontRight, rearLeft, rearRight);
  }

  @Override
  public void pack(ByteBuffer bb, MecanumDriveWheelSpeeds value) {
    bb.putDouble(value.frontLeftMetersPerSecond);
    bb.putDouble(value.frontRightMetersPerSecond);
    bb.putDouble(value.rearLeftMetersPerSecond);
    bb.putDouble(value.rearRightMetersPerSecond);
  }
}
