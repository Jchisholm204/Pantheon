import cocotb
import os
import random
from cocotb.triggers import Timer
from cocotb.runner import get_runner
from pathlib import Path
import util.testbench as testbench


@cocotb.test()
async def div32_basic(dut):
    """Basic test for DIV32 module"""
    random.seed(9876348765)
    for signed in [0, 1]:
        for i in range(200):
            # dividend = random.randint(0, 2**31 - 1)
            # divisor = random.randint(1, 2**31 - 1)
            random.seed(i*23040274)
            dividend = int(random.random()*50000)
            random.seed(i*2873462)
            divisor = int(random.random()*50000)

            dut.iSigned.value = signed
            dut.iDividend.value = dividend
            dut.iDivisor.value = divisor

            await Timer(1, units="ns")  # Adjust depending on latency

            expected_q = int(dividend // divisor)
            expected_r = int(dividend % divisor)

            q = dut.oQ.value.signed_integer if signed else dut.oQ.value.integer
            r = dut.oR.value.signed_integer if signed else dut.oR.value.integer

            assert q == expected_q, f'{dividend}/{divisor}, Q: {expected_q}, got {q}'
            assert r == expected_r, f"Expected remainder {expected_r}, got {r}"


@cocotb.test()
async def div32_large(dut):
    """Basic test for DIV32 module"""
    random.seed(9876348765)
    for signed in [0, 1]:
        for i in range(200):
            # dividend = random.randint(0, 2**31 - 1)
            # divisor = random.randint(1, 2**31 - 1)
            random.seed(i*23040274)
            dividend = int(random.random()*894923202)
            random.seed(i*2873462)
            divisor = int(random.random()*28376)

            dut.iSigned.value = signed
            dut.iDividend.value = dividend
            dut.iDivisor.value = divisor

            await Timer(1, units="ns")  # Adjust depending on latency

            expected_q = int(dividend // divisor)
            expected_r = int(dividend % divisor)

            q = dut.oQ.value.signed_integer if signed else dut.oQ.value.integer
            r = dut.oR.value.signed_integer if signed else dut.oR.value.integer

            assert q == expected_q, f'{dividend}/{divisor}, Q: {expected_q}, got {q}'
            assert r == expected_r, f"Expected remainder {expected_r}, got {r}"


@cocotb.test()
async def div32_small(dut):
    """Basic test for DIV32 module"""
    random.seed(9876348765)
    for signed in [1, -1]:
        for i in range(200):
            # dividend = random.randint(0, 2**31 - 1)
            # divisor = random.randint(1, 2**31 - 1)
            random.seed(i*23040274)
            divisor = int(random.random()*894923202)*signed
            random.seed(i*2873462)
            dividend = int(random.random()*28376)*signed

            dut.iSigned.value = signed < 0
            dut.iDividend.value = dividend
            dut.iDivisor.value = divisor

            await Timer(1, units="ns")  # Adjust depending on latency

            expected_q = int(dividend // divisor)
            expected_r = int(dividend % divisor)

            q = dut.oQ.value.signed_integer if signed else dut.oQ.value.integer
            r = dut.oR.value.signed_integer if signed else dut.oR.value.integer

            assert q == expected_q, f'{dividend}/{divisor}, Q: {expected_q}, got {q}'
            assert r == expected_r, f"Expected remainder {expected_r}, got {r}"


def test_div32_runner():
    tb = testbench.TB("test_alu_divisor", "DIV32")
    tb.add_source("processor/ALU/DIV32.sv")


if __name__ == "__main__":
    test_div32_runner()
