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
async def and_test_specific(dut):
    dut.iORnXOR.value = 1
    dut.iAND.value = 1
    tests = [
            (0x00000000, 0x00000000),
            (0xFFFFFFFF, 0xFFFFFFFF),
            (0xFFFFFFFF, 0x00000000),
            (0x00000000, 0xFFFFFFFF),
            (0x12345678, 0xABCDEF3F),
            ]
    for (A, B) in tests:
        dut.iA.value = A
        dut.iB.value = B
        await Timer(1, "ns")
        res = dut.oD.value.integer
        expected = A & B
        assert res == expected, f"AND Fail {res} =/= {expected}"


@cocotb.test()
async def and_test_random(dut):
    dut.iORnXOR.value = 1
    dut.iAND.value = 1
    for _ in range(16):
        A = random.getrandbits(32)
        B = random.getrandbits(32)
        dut.iA.value = A
        dut.iB.value = B
        await Timer(1, "ns")
        res = dut.oD.value.integer
        expected = A & B
        assert res == expected, f"AND Fail {res} =/= {expected}"


@cocotb.test()
async def or_test_specific(dut):
    dut.iORnXOR.value = 1
    dut.iAND.value = 0
    tests = [
            (0x00000000, 0x00000000),
            (0xFFFFFFFF, 0xFFFFFFFF),
            (0xFFFFFFFF, 0x00000000),
            (0x00000000, 0xFFFFFFFF),
            (0x12345678, 0xABCDEF3F),
            ]
    for (A, B) in tests:
        dut.iA.value = A
        dut.iB.value = B
        await Timer(1, "ns")
        res = dut.oD.value.integer
        expected = A | B
        assert res == expected, f"OR Fail {res} =/= {expected}"


@cocotb.test()
async def or_test_random(dut):
    dut.iORnXOR.value = 1
    dut.iAND.value = 0
    for _ in range(16):
        A = random.getrandbits(32)
        B = random.getrandbits(32)
        dut.iA.value = A
        dut.iB.value = B
        await Timer(1, "ns")
        res = dut.oD.value.integer
        expected = A | B
        assert res == expected, f"OR Fail {res} =/= {expected}"


@cocotb.test()
async def xor_test_specific(dut):
    dut.iORnXOR.value = 0
    dut.iAND.value = 0
    tests = [
            (0x00000000, 0x00000000),
            (0xFFFFFFFF, 0xFFFFFFFF),
            (0xFFFFFFFF, 0x00000000),
            (0x00000000, 0xFFFFFFFF),
            (0x12345678, 0xABCDEF3F),
            ]
    for (A, B) in tests:
        dut.iA.value = A
        dut.iB.value = B
        await Timer(1, "ns")
        res = dut.oD.value.integer
        expected = A ^ B
        assert res == expected, f"OR Fail {res} =/= {expected}"


@cocotb.test()
async def xor_test_random(dut):
    dut.iORnXOR.value = 0
    dut.iAND.value = 0
    for _ in range(16):
        A = random.getrandbits(32)
        B = random.getrandbits(32)
        dut.iA.value = A
        dut.iB.value = B
        await Timer(1, "ns")
        res = dut.oD.value.integer
        expected = A ^ B
        assert res == expected, f"OR Fail {res} =/= {expected}"


def test_bitwise_runner():
    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent.parent

    sources = [proj_path / "ALU/BitWise.sv"]

    if sim == "icarus":
        build_args = ["-DICARUS_TRACE_ARRAYS", "-DICARUS_FST"]
    else:
        build_args = ["--trace", "-Wno-fatal"]

    runner = get_runner(sim)
    runner.build(
        verilog_sources=sources,
        hdl_toplevel="BitWise",
        clean=False,
        waves=True,
        # build_args=["-DICARUS_TRACE_ARRAYS", "-DICARUS_FST"],
        build_args=build_args,
        always=True,
    )
    runner.test(
        hdl_toplevel="BitWise",
        test_module="test_bitwise",
        plusargs=["-fst"],
        waves=True
    )


if __name__ == "__main__":
    test_bitwise_runner()
