// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package edu.wpi.first.math.kinematics.serde;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;

import edu.wpi.first.math.kinematics.DifferentialDriveWheelSpeeds;
import edu.wpi.first.math.proto.Kinematics.ProtobufDifferentialDriveWheelSpeeds;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import org.junit.jupiter.api.Test;

public class DifferentialDriveWheelSpeedsSerdeTest {
  private static final DifferentialDriveWheelSpeeds DATA =
      new DifferentialDriveWheelSpeeds(1.91, 2.29);
  private static final byte[] STRUCT_BUFFER =
      new byte[] {-113, -62, -11, 40, 92, -113, -2, 63, 82, -72, 30, -123, -21, 81, 2, 64};

  @Test
  void testStructPack() {
    ByteBuffer buffer = ByteBuffer.allocate(DifferentialDriveWheelSpeeds.struct.getSize());
    buffer.order(ByteOrder.LITTLE_ENDIAN);
    DifferentialDriveWheelSpeeds.struct.pack(buffer, DATA);

    byte[] actual = buffer.array();
    assertArrayEquals(actual, STRUCT_BUFFER);
  }

  @Test
  void testStructUnpack() {
    ByteBuffer buffer = ByteBuffer.wrap(STRUCT_BUFFER);
    buffer.order(ByteOrder.LITTLE_ENDIAN);

    DifferentialDriveWheelSpeeds data = DifferentialDriveWheelSpeeds.struct.unpack(buffer);
    assertEquals(DATA.leftMetersPerSecond, data.leftMetersPerSecond);
    assertEquals(DATA.rightMetersPerSecond, data.rightMetersPerSecond);
  }

  @Test
  void testProtoPack() {
    ProtobufDifferentialDriveWheelSpeeds proto = DifferentialDriveWheelSpeeds.proto.createMessage();
    DifferentialDriveWheelSpeeds.proto.pack(proto, DATA);

    assertEquals(DATA.leftMetersPerSecond, proto.getLeftMps());
    assertEquals(DATA.rightMetersPerSecond, proto.getRightMps());
  }

  @Test
  void testProtoUnpack() {
    ProtobufDifferentialDriveWheelSpeeds proto = DifferentialDriveWheelSpeeds.proto.createMessage();
    proto.setLeftMps(DATA.leftMetersPerSecond);
    proto.setRightMps(DATA.rightMetersPerSecond);

    DifferentialDriveWheelSpeeds data = DifferentialDriveWheelSpeeds.proto.unpack(proto);
    assertEquals(DATA.leftMetersPerSecond, data.leftMetersPerSecond);
    assertEquals(DATA.rightMetersPerSecond, data.rightMetersPerSecond);
  }
}
