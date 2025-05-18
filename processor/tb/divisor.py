import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure
from cocotb.binary import BinaryValue
import random

@cocotb.test()
async def test_div32_basic(dut):
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
async def test_div32_large(dut):
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
async def test_div32_small(dut):
    """Basic test for DIV32 module"""
    random.seed(9876348765)
    for signed in [0, 1]:
        for i in range(200):
            # dividend = random.randint(0, 2**31 - 1)
            # divisor = random.randint(1, 2**31 - 1)
            random.seed(i*23040274)
            divisor = int(random.random()*894923202)
            random.seed(i*2873462)
            dividend = int(random.random()*28376)

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
