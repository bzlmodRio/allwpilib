// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package edu.wpi.first.hal;

@SuppressWarnings("MemberName")
public class REVPHFaults {
  public final boolean Channel0Fault;

  public final boolean Channel1Fault;

  public final boolean Channel2Fault;

  public final boolean Channel3Fault;

  public final boolean Channel4Fault;

  public final boolean Channel5Fault;

  public final boolean Channel6Fault;

  public final boolean Channel7Fault;

  public final boolean Channel8Fault;

  public final boolean Channel9Fault;

  public final boolean Channel10Fault;

  public final boolean Channel11Fault;

  public final boolean Channel12Fault;

  public final boolean Channel13Fault;

  public final boolean Channel14Fault;

  public final boolean Channel15Fault;

  public final boolean CompressorOverCurrent;

  public final boolean CompressorOpen;

  public final boolean SolenoidOverCurrent;

  public final boolean Brownout;

  public final boolean CanWarning;

  public final boolean HardwareFault;

  /**
   * Called from HAL to construct.
   *
   * @param faults the fault bitfields
   */
  public REVPHFaults(int faults) {
    Channel0Fault = (faults & (1 << 0)) != 0;
    Channel1Fault = (faults & (1 << 1)) != 0;
    Channel2Fault = (faults & (1 << 2)) != 0;
    Channel3Fault = (faults & (1 << 3)) != 0;
    Channel4Fault = (faults & (1 << 4)) != 0;
    Channel5Fault = (faults & (1 << 5)) != 0;
    Channel6Fault = (faults & (1 << 6)) != 0;
    Channel7Fault = (faults & (1 << 7)) != 0;
    Channel8Fault = (faults & (1 << 8)) != 0;
    Channel9Fault = (faults & (1 << 9)) != 0;
    Channel10Fault = (faults & (1 << 10)) != 0;
    Channel11Fault = (faults & (1 << 11)) != 0;
    Channel12Fault = (faults & (1 << 12)) != 0;
    Channel13Fault = (faults & (1 << 13)) != 0;
    Channel14Fault = (faults & (1 << 14)) != 0;
    Channel15Fault = (faults & (1 << 15)) != 0;
    CompressorOverCurrent = (faults & (1 << 16)) != 0;
    CompressorOpen = (faults & (1 << 17)) != 0;
    SolenoidOverCurrent = (faults & (1 << 18)) != 0;
    Brownout = (faults & (1 << 19)) != 0;
    CanWarning = (faults & (1 << 20)) != 0;
    HardwareFault = (faults & (1 << 21)) != 0;
  }
}
