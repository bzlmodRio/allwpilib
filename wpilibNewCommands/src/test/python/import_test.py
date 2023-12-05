from typing import TYPE_CHECKING

import commands2
from util import *  # type: ignore

if TYPE_CHECKING:
    from .util import *

import pytest


@pytest.fixture(autouse=True)
def scheduler():
    commands2.CommandScheduler.resetInstance()
    DriverStationSim.setEnabled(True)
    DriverStationSim.notifyNewData()
    return commands2.CommandScheduler.getInstance()


@pytest.fixture()
def nt_instance():
    inst = NetworkTableInstance.create()
    inst.startLocal()
    yield inst
    inst.stopLocal()


def test_waitUntil(scheduler: commands2.CommandScheduler):
    raise
    condition = OOBoolean()

    command = commands2.WaitUntilCommand(condition)

    scheduler.schedule(command)
    scheduler.run()
    assert scheduler.isScheduled(command)
    condition.set(True)
    scheduler.run()
    assert not scheduler.isScheduled(command)
    assert False