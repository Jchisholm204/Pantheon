import cocotb
import random
from cocotb.triggers import Timer
import util.testbench as testbench


def to_signed32(n):
    """Convert unsigned 32-bit int to signed 32-bit."""
    n = n & 0xFFFFFFFF
    return n if n < 0x80000000 else n - 0x100000000


async def verify_sra(initial, shift, result):
    assert (result == ((initial >> shift))), \
        f"Failed SRA \
        {bin((initial >> shift))} =/= {bin((result))}, i={shift}"


async def verify_srl(initial, shift, result):
    assert result == (initial >> shift), \
        f"Failed SRL \
        {bin(result)} =/= {bin(initial >> shift)}"


async def verify_sll(initial, shift, result):
    expected = (initial << shift) & 0xFFFFFFFF
    assert result == expected, \
        f"Failed SLL \
        {bin(result)} =/= {bin(expected)}"


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
        verify_sra(initial, i, res)


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
            verify_srl(initial, i, res)


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
            verify_sll(initial, i, res)


def test_shift_runner():
    tb = testbench.TB("test_alu_shift", "SHIFT")
    tb.add_source("processor/ALU/SHIFT.sv")
    tb.run_tests()


if __name__ == "__main__":
    test_shift_runner()
