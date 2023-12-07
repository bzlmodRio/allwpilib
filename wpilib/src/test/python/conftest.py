import logging

import pytest
import ntcore
import wpilib
import _wpilib_core


@pytest.fixture
def cfg_logging(caplog):
    caplog.set_level(logging.INFO)


@pytest.fixture(scope="function")
def nt(cfg_logging):
    instance = ntcore.NetworkTableInstance.getDefault()
    instance.startLocal()

    try:
        yield instance
    finally:
        instance.stopLocal()
        instance._reset()
        _wpilib_core._clearSmartDashboardData()
