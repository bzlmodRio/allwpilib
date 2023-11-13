// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package edu.wpi.first.math.kinematics.serde;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;

import edu.wpi.first.math.kinematics.ChassisSpeeds;
import edu.wpi.first.math.proto.Kinematics.ProtobufChassisSpeeds;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import org.junit.jupiter.api.Test;

public class ChassisSpeedsSerdeTest {
  private static final ChassisSpeeds DATA = new ChassisSpeeds(1.91, 2.29, 3.504);
  private static final byte[] STRUCT_BUFFER =
      new byte[] {
        -113, -62, -11, 40, 92, -113, -2, 63, 82, -72, 30, -123, -21, 81, 2, 64, -43, 120, -23, 38,
        49, 8, 12, 64
      };

  @Test
  void testStructPack() {
    ByteBuffer buffer = ByteBuffer.allocate(ChassisSpeeds.struct.getSize());
    buffer.order(ByteOrder.LITTLE_ENDIAN);
    ChassisSpeeds.struct.pack(buffer, DATA);

    byte[] actual = buffer.array();
    assertArrayEquals(actual, STRUCT_BUFFER);
  }

  @Test
  void testStructUnpack() {
    ByteBuffer buffer = ByteBuffer.wrap(STRUCT_BUFFER);
    buffer.order(ByteOrder.LITTLE_ENDIAN);

    ChassisSpeeds data = ChassisSpeeds.struct.unpack(buffer);
    assertEquals(DATA.vxMetersPerSecond, data.vxMetersPerSecond);
    assertEquals(DATA.vyMetersPerSecond, data.vyMetersPerSecond);
    assertEquals(DATA.omegaRadiansPerSecond, data.omegaRadiansPerSecond);
  }

  @Test
  void testProtoPack() {
    ProtobufChassisSpeeds proto = ChassisSpeeds.proto.createMessage();
    ChassisSpeeds.proto.pack(proto, DATA);

    assertEquals(DATA.vxMetersPerSecond, proto.getVxMps());
    assertEquals(DATA.vyMetersPerSecond, proto.getVyMps());
    assertEquals(DATA.omegaRadiansPerSecond, proto.getOmegaRps());
  }

  @Test
  void testProtoUnpack() {
    ProtobufChassisSpeeds proto = ChassisSpeeds.proto.createMessage();
    proto.setVxMps(DATA.vxMetersPerSecond);
    proto.setVyMps(DATA.vyMetersPerSecond);
    proto.setOmegaRps(DATA.omegaRadiansPerSecond);

    ChassisSpeeds data = ChassisSpeeds.proto.unpack(proto);
    assertEquals(DATA.vxMetersPerSecond, data.vxMetersPerSecond);
    assertEquals(DATA.vyMetersPerSecond, data.vyMetersPerSecond);
    assertEquals(DATA.omegaRadiansPerSecond, data.omegaRadiansPerSecond);
  }
}
