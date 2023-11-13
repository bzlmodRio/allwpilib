// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package edu.wpi.first.math.kinematics.serde;

import edu.wpi.first.math.kinematics.ChassisSpeeds;
import edu.wpi.first.math.proto.Kinematics.ProtobufChassisSpeeds;
import edu.wpi.first.util.protobuf.Protobuf;
import us.hebi.quickbuf.Descriptors.Descriptor;

public class ChassisSpeedsProtoSerde implements Protobuf<ChassisSpeeds, ProtobufChassisSpeeds> {
  @Override
  public Class<ChassisSpeeds> getTypeClass() {
    return ChassisSpeeds.class;
  }

  @Override
  public Descriptor getDescriptor() {
    return ProtobufChassisSpeeds.getDescriptor();
  }

  @Override
  public ProtobufChassisSpeeds createMessage() {
    return ProtobufChassisSpeeds.newInstance();
  }

  @Override
  public ChassisSpeeds unpack(ProtobufChassisSpeeds msg) {
    return new ChassisSpeeds(msg.getVxMps(), msg.getVyMps(), msg.getOmegaRps());
  }

  @Override
  public void pack(ProtobufChassisSpeeds msg, ChassisSpeeds value) {
    msg.setVxMps(value.vxMetersPerSecond);
    msg.setVyMps(value.vyMetersPerSecond);
    msg.setOmegaRps(value.omegaRadiansPerSecond);
  }
}
