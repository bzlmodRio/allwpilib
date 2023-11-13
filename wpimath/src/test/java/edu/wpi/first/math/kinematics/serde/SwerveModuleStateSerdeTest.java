// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package edu.wpi.first.math.kinematics.serde;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;

import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.math.kinematics.SwerveModuleState;
import edu.wpi.first.math.proto.Kinematics.ProtobufSwerveModuleState;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import org.junit.jupiter.api.Test;

public class SwerveModuleStateSerdeTest {
  private static final SwerveModuleState DATA =
      new SwerveModuleState(1.91, Rotation2d.fromDegrees(17.4));
  private static final byte[] STRUCT_BUFFER =
      new byte[] {-113, -62, -11, 40, 92, -113, -2, 63, -108, -92, -122, -48, -100, 111, -45, 63};

  @Test
  void testStructPack() {
    ByteBuffer buffer = ByteBuffer.allocate(SwerveModuleState.struct.getSize());
    buffer.order(ByteOrder.LITTLE_ENDIAN);
    SwerveModuleState.struct.pack(buffer, DATA);

    byte[] actual = buffer.array();
    assertArrayEquals(actual, STRUCT_BUFFER);
  }

  @Test
  void testStructUnpack() {
    ByteBuffer buffer = ByteBuffer.wrap(STRUCT_BUFFER);
    buffer.order(ByteOrder.LITTLE_ENDIAN);

    SwerveModuleState data = SwerveModuleState.struct.unpack(buffer);
    assertEquals(DATA.speedMetersPerSecond, data.speedMetersPerSecond);
    assertEquals(DATA.angle, data.angle);
  }

  @Test
  void testProtoPack() {
    ProtobufSwerveModuleState proto = SwerveModuleState.proto.createMessage();
    SwerveModuleState.proto.pack(proto, DATA);

    assertEquals(DATA.speedMetersPerSecond, proto.getSpeedMps());
    assertEquals(DATA.angle.getRadians(), proto.getAngle().getRadians());
  }

  @Test
  void testProtoUnpack() {
    ProtobufSwerveModuleState proto = SwerveModuleState.proto.createMessage();
    proto.setSpeedMps(DATA.speedMetersPerSecond);
    proto.getMutableAngle().setRadians(DATA.angle.getRadians());

    SwerveModuleState data = SwerveModuleState.proto.unpack(proto);
    assertEquals(DATA.speedMetersPerSecond, data.speedMetersPerSecond);
    assertEquals(DATA.angle, data.angle);
  }
}
