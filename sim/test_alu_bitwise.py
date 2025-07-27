import cocotb
import os
import random
from cocotb.triggers import Timer
from cocotb.runner import get_runner
from pathlib import Path
from util.representation import to_signed32 as to_signed32
import util.testbench as testbench

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
    tb = testbench.TB("test_alu_bitwise", "BitWise")
    tb.add_source("processor/ALU/BitWise.sv")


if __name__ == "__main__":
    test_bitwise_runner()
