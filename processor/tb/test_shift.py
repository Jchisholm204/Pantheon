import cocotb
import os
import random
from cocotb.triggers import Timer
from cocotb.runner import get_runner
from pathlib import Path


def to_signed32(n):
    """Convert unsigned 32-bit int to signed 32-bit."""
    n = n & 0xFFFFFFFF
    return n if n < 0x80000000 else n - 0x100000000


@cocotb.test()
async def right_arith_test_maxval(dut):
    # Test a case where the output value should not change
    initial = 0xFFFFFFFF
    dut.iD.value = initial
    dut.iRightnLeft.value = 1
    dut.iArithnLogic.value = 1
    for i in range(0, 32):
        dut.iShamt.value = i
        await Timer(1, "ns")
        res = dut.oD.value.integer
        assert res == initial, "Failed Right Arithmetic Shift (maxval)"


@cocotb.test
async def right_arith_test_minval(dut):
    """
    Test a case where the output will change
    to 0xFFFFFFFF
    """
    initial = 0x80000000
    dut.iD.value = initial
    initial = to_signed32(initial)
    dut.iRightnLeft.value = 1
    dut.iArithnLogic.value = 1
    for i in range(0, 32):
        dut.iShamt.value = i
        await Timer(1, "ns")
        res = dut.oD.value.integer
        res = to_signed32(res)
        assert ((res)) == ((initial >> i)), \
            f"Failed Right Arithmetic Shift (minval): \
            {bin((initial >> i))} =/= {bin((res))}, i={i}"


@cocotb.test
async def right_logic_test(dut):
    dut.iRightnLeft.value = 1
    # Set to logical shift
    dut.iArithnLogic.value = 0
    for _ in range(16):
        initial = random.getrandbits(32)
        dut.iD.value = initial
        for i in range(0, 32):
            dut.iShamt.value = i
            await Timer(1, "ns")
            res = dut.oD.value.integer
            assert res == (initial >> i), \
                f"Failed Right Logical Shift \
                {bin(res)} =/= {bin(initial >> i)}"


@cocotb.test
async def left_logic_test(dut):
    # Set to left shift
    dut.iRightnLeft.value = 0
    # Set to logical shift
    dut.iArithnLogic.value = 0
    for _ in range(16):
        initial = random.getrandbits(32)
        dut.iD.value = initial
        for i in range(0, 32):
            dut.iShamt.value = i
            await Timer(1, "ns")
            res = dut.oD.value.integer
            expected = (initial << i) & 0xFFFFFFFF
            assert res == expected, \
                f"Failed Right Logical Shift \
                {bin(res)} =/= {bin(expected)}"


def test_shift_runner():
    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent.parent

    sources = [proj_path / "ALU/SHIFT.sv"]

    if sim == "icarus":
        build_args = ["-DICARUS_TRACE_ARRAYS", "-DICARUS_FST"]
    else:
        build_args = ["--trace", "-Wno-fatal"]

    runner = get_runner(sim)
    runner.build(
        verilog_sources=sources,
        hdl_toplevel="SHIFT",
        clean=False,
        waves=True,
        # build_args=["-DICARUS_TRACE_ARRAYS", "-DICARUS_FST"],
        build_args=build_args,
        always=True,
    )
    runner.test(
        hdl_toplevel="SHIFT",
        test_module="test_shift",
        plusargs=["-fst"],
        waves=True
    )


if __name__ == "__main__":
    test_shift_runner()
