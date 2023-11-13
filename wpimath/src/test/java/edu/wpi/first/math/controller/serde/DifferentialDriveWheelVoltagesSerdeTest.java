// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package edu.wpi.first.math.controller.serde;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;

import edu.wpi.first.math.controller.DifferentialDriveWheelVoltages;
import edu.wpi.first.math.proto.Controller.ProtobufDifferentialDriveWheelVoltages;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import org.junit.jupiter.api.Test;

public class DifferentialDriveWheelVoltagesSerdeTest {
  private static final DifferentialDriveWheelVoltages DATA =
      new DifferentialDriveWheelVoltages(1.91, 2.29);
  private static final byte[] STRUCT_BUFFER =
      new byte[] {-113, -62, -11, 40, 92, -113, -2, 63, 82, -72, 30, -123, -21, 81, 2, 64};

  @Test
  void testStructPack() {
    ByteBuffer buffer = ByteBuffer.allocate(DifferentialDriveWheelVoltages.struct.getSize());
    buffer.order(ByteOrder.LITTLE_ENDIAN);
    DifferentialDriveWheelVoltages.struct.pack(buffer, DATA);

    byte[] actual = buffer.array();
    assertArrayEquals(actual, STRUCT_BUFFER);
  }

  @Test
  void testStructUnpack() {
    ByteBuffer buffer = ByteBuffer.wrap(STRUCT_BUFFER);
    buffer.order(ByteOrder.LITTLE_ENDIAN);

    DifferentialDriveWheelVoltages data = DifferentialDriveWheelVoltages.struct.unpack(buffer);
    assertEquals(DATA.left, data.left);
    assertEquals(DATA.right, data.right);
  }

  @Test
  void testProtoPack() {
    ProtobufDifferentialDriveWheelVoltages proto =
        DifferentialDriveWheelVoltages.proto.createMessage();
    DifferentialDriveWheelVoltages.proto.pack(proto, DATA);

    assertEquals(DATA.left, proto.getLeftVolts());
    assertEquals(DATA.right, proto.getRightVolts());
  }

  @Test
  void testProtoUnpack() {
    ProtobufDifferentialDriveWheelVoltages proto =
        DifferentialDriveWheelVoltages.proto.createMessage();
    proto.setLeftVolts(DATA.left);
    proto.setRightVolts(DATA.right);

    DifferentialDriveWheelVoltages data = DifferentialDriveWheelVoltages.proto.unpack(proto);
    assertEquals(DATA.left, data.left);
    assertEquals(DATA.right, data.right);
  }
}
