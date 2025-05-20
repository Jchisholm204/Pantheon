import cocotb
import os
import random
from cocotb.triggers import Timer
from cocotb.runner import get_runner
from pathlib import Path


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
    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent.parent

    sources = [proj_path / "ALU/CLA.sv"]

    if sim == "icarus":
        build_args = ["-DICARUS_TRACE_ARRAYS", "-DICARUS_FST"]
    else:
        build_args = ["--trace", "-Wno-fatal"]

    runner = get_runner(sim)
    runner.build(
        verilog_sources=sources,
        hdl_toplevel="CLA",
        clean=False,
        waves=True,
        # build_args=["-DICARUS_TRACE_ARRAYS", "-DICARUS_FST"],
        build_args=build_args,
        always=True,
    )
    runner.test(
        hdl_toplevel="CLA",
        test_module="test_cla",
        plusargs=["-fst"],
        waves=True
    )


if __name__ == "__main__":
    test_cla_runner()
