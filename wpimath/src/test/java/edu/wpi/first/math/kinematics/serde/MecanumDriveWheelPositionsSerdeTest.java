// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package edu.wpi.first.math.kinematics.serde;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;

import edu.wpi.first.math.kinematics.MecanumDriveWheelPositions;
import edu.wpi.first.math.proto.Kinematics.ProtobufMecanumDriveWheelPositions;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import org.junit.jupiter.api.Test;

public class MecanumDriveWheelPositionsSerdeTest {
  private static final MecanumDriveWheelPositions DATA =
      new MecanumDriveWheelPositions(1.91, 2.29, 35.04, 17.4);
  private static final byte[] STRUCT_BUFFER =
      new byte[] {
        -113, -62, -11, 40, 92, -113, -2, 63, 82, -72, 30, -123, -21, 81, 2, 64, -123, -21, 81, -72,
        30, -123, 65, 64, 102, 102, 102, 102, 102, 102, 49, 64
      };

  @Test
  void testStructPack() {
    ByteBuffer buffer = ByteBuffer.allocate(MecanumDriveWheelPositions.struct.getSize());
    buffer.order(ByteOrder.LITTLE_ENDIAN);
    MecanumDriveWheelPositions.struct.pack(buffer, DATA);

    byte[] actual = buffer.array();
    assertArrayEquals(actual, STRUCT_BUFFER);
  }

  @Test
  void testStructUnpack() {
    ByteBuffer buffer = ByteBuffer.wrap(STRUCT_BUFFER);
    buffer.order(ByteOrder.LITTLE_ENDIAN);

    MecanumDriveWheelPositions data = MecanumDriveWheelPositions.struct.unpack(buffer);
    assertEquals(DATA.frontLeftMeters, data.frontLeftMeters);
    assertEquals(DATA.frontRightMeters, data.frontRightMeters);
    assertEquals(DATA.rearLeftMeters, data.rearLeftMeters);
    assertEquals(DATA.rearRightMeters, data.rearRightMeters);
  }

  @Test
  void testProtoPack() {
    ProtobufMecanumDriveWheelPositions proto = MecanumDriveWheelPositions.proto.createMessage();
    MecanumDriveWheelPositions.proto.pack(proto, DATA);

    assertEquals(DATA.frontLeftMeters, proto.getFrontLeftMeters());
    assertEquals(DATA.frontRightMeters, proto.getFrontRightMeters());
    assertEquals(DATA.rearLeftMeters, proto.getRearLeftMeters());
    assertEquals(DATA.rearRightMeters, proto.getRearRightMeters());
  }

  @Test
  void testProtoUnpack() {
    ProtobufMecanumDriveWheelPositions proto = MecanumDriveWheelPositions.proto.createMessage();
    proto.setFrontLeftMeters(DATA.frontLeftMeters);
    proto.setFrontRightMeters(DATA.frontRightMeters);
    proto.setRearLeftMeters(DATA.rearLeftMeters);
    proto.setRearRightMeters(DATA.rearRightMeters);

    MecanumDriveWheelPositions data = MecanumDriveWheelPositions.proto.unpack(proto);
    assertEquals(DATA.frontLeftMeters, data.frontLeftMeters);
    assertEquals(DATA.frontRightMeters, data.frontRightMeters);
    assertEquals(DATA.rearLeftMeters, data.rearLeftMeters);
    assertEquals(DATA.rearRightMeters, data.rearRightMeters);
  }
}
