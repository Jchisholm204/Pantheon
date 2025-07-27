import cocotb
import os
import random
from cocotb.triggers import Timer
from cocotb.runner import get_runner
from pathlib import Path
import util.testbench as testbench


@cocotb.test()
async def cla_add_random(dut):
    dut.iCarry.value = 0
    for i in range(8):
        random.seed(9876348765*i)
        testX = random.getrandbits(31)
        testY = random.getrandbits(31)
        dut.iX.value = testX
        dut.iY.value = testY
        await Timer(1, units="ns")
        oS = dut.oS.value.integer
        overflow = dut.oOverflow.value.integer
        assert (testX+testY) == oS or overflow == 1, \
            f'Random Add Failure: {testX+testY} =/= {oS}, {overflow}'


@cocotb.test()
async def cla_add_tests(dut):
    dut.iCarry.value = 0
    tests = [
            # iA, iB, iCarry, Expected Overflow/oCarry
            (0xFFFFFFFF, 0xFFFFFFFF, 0, 1),
            (0xFFFFFFF, 0xFFFFFFF, 0, 0),
            (0, 0xFFFFFFF, 0, 0),
            (0xFFFFFFF, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 1, 0),
            (2, 5, 1, 0),
            (23984, 234, 1, 0),
            ]
    for test in tests:
        dut.iX.value = test[0]
        dut.iY.value = test[1]
        dut.iCarry = test[2]
        await Timer(1, units="ns")
        propSum = test[0] + test[1] + test[2]
        oS = dut.oS.value.integer
        overflow = dut.oOverflow.value.integer
        oCarry = dut.oCarry.value.integer
        assert propSum == oS or overflow or oCarry, f'Test Failed: {test}'
        assert overflow == test[3] or oCarry == test[3], f'Overflow Error {test}'


def test_cla_runner():
    tb = testbench.TB("test_alu_cla", "CLA")
    tb.add_source("processor/ALU/CLA.sv")


if __name__ == "__main__":
    test_cla_runner()
