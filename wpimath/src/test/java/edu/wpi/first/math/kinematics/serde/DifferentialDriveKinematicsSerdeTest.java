// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package edu.wpi.first.math.kinematics.serde;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;

import edu.wpi.first.math.kinematics.DifferentialDriveKinematics;
import edu.wpi.first.math.proto.Kinematics.ProtobufDifferentialDriveKinematics;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import org.junit.jupiter.api.Test;

public class DifferentialDriveKinematicsSerdeTest {
  private static final DifferentialDriveKinematics DATA = new DifferentialDriveKinematics(1.91);
  private static final byte[] STRUCT_BUFFER = new byte[] {-113, -62, -11, 40, 92, -113, -2, 63};

  @Test
  void testStructPack() {
    ByteBuffer buffer = ByteBuffer.allocate(DifferentialDriveKinematics.struct.getSize());
    buffer.order(ByteOrder.LITTLE_ENDIAN);
    DifferentialDriveKinematics.struct.pack(buffer, DATA);

    byte[] actual = buffer.array();
    assertArrayEquals(actual, STRUCT_BUFFER);
  }

  @Test
  void testStructUnpack() {
    ByteBuffer buffer = ByteBuffer.wrap(STRUCT_BUFFER);
    buffer.order(ByteOrder.LITTLE_ENDIAN);

    DifferentialDriveKinematics data = DifferentialDriveKinematics.struct.unpack(buffer);
    assertEquals(DATA.trackWidthMeters, data.trackWidthMeters);
  }

  @Test
  void testProtoPack() {
    ProtobufDifferentialDriveKinematics proto = DifferentialDriveKinematics.proto.createMessage();
    DifferentialDriveKinematics.proto.pack(proto, DATA);

    assertEquals(DATA.trackWidthMeters, proto.getTrackWidthMeters());
  }

  @Test
  void testProtoUnpack() {
    ProtobufDifferentialDriveKinematics proto = DifferentialDriveKinematics.proto.createMessage();
    proto.setTrackWidthMeters(DATA.trackWidthMeters);

    DifferentialDriveKinematics data = DifferentialDriveKinematics.proto.unpack(proto);
    assertEquals(DATA.trackWidthMeters, data.trackWidthMeters);
  }
}
