#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib


class MyRobot(wpilib.TimedRobot):
    """
    This is a demo program showing the use of GenericHID's rumble feature.
    """

    def robotInit(self):
        """Robot initialization function"""

        self.hid = wpilib.XboxController(0)

    def autonomousInit(self):
        # Turn on rumble at the start of auto
        self.hid.setRumble(wpilib.XboxController.RumbleType.kLeftRumble, 1.0)
        self.hid.setRumble(wpilib.XboxController.RumbleType.kRightRumble, 1.0)

    def disabledInit(self):
        # Stop the rumble when entering disabled
        self.hid.setRumble(wpilib.XboxController.RumbleType.kLeftRumble, 0.0)
        self.hid.setRumble(wpilib.XboxController.RumbleType.kRightRumble, 0.0)
