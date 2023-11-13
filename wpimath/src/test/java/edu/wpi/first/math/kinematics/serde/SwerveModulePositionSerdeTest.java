// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package edu.wpi.first.math.kinematics.serde;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;

import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.math.kinematics.SwerveModulePosition;
import edu.wpi.first.math.proto.Kinematics.ProtobufSwerveModulePosition;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import org.junit.jupiter.api.Test;

public class SwerveModulePositionSerdeTest {
  private static final SwerveModulePosition DATA =
      new SwerveModulePosition(1.91, Rotation2d.fromDegrees(2.29));
  private static final byte[] STRUCT_BUFFER =
      new byte[] {-113, -62, -11, 40, 92, -113, -2, 63, -26, 110, 66, -32, -80, 118, -92, 63};

  @Test
  void testStructPack() {
    ByteBuffer buffer = ByteBuffer.allocate(SwerveModulePosition.struct.getSize());
    buffer.order(ByteOrder.LITTLE_ENDIAN);
    SwerveModulePosition.struct.pack(buffer, DATA);

    byte[] actual = buffer.array();
    assertArrayEquals(actual, STRUCT_BUFFER);
  }

  @Test
  void testStructUnpack() {
    ByteBuffer buffer = ByteBuffer.wrap(STRUCT_BUFFER);
    buffer.order(ByteOrder.LITTLE_ENDIAN);

    SwerveModulePosition data = SwerveModulePosition.struct.unpack(buffer);
    assertEquals(DATA.distanceMeters, data.distanceMeters);
    assertEquals(DATA.angle, data.angle);
  }

  @Test
  void testProtoPack() {
    ProtobufSwerveModulePosition proto = SwerveModulePosition.proto.createMessage();
    SwerveModulePosition.proto.pack(proto, DATA);

    assertEquals(DATA.distanceMeters, proto.getDistanceMeters());
    assertEquals(DATA.angle.getRadians(), proto.getAngle().getRadians());
  }

  @Test
  void testProtoUnpack() {
    ProtobufSwerveModulePosition proto = SwerveModulePosition.proto.createMessage();
    proto.setDistanceMeters(DATA.distanceMeters);
    proto.getMutableAngle().setRadians(DATA.angle.getRadians());

    SwerveModulePosition data = SwerveModulePosition.proto.unpack(proto);
    assertEquals(DATA.distanceMeters, data.distanceMeters);
    assertEquals(DATA.angle, data.angle);
  }
}
