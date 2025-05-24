import cocotb
import os
import random
from cocotb.triggers import Timer
from cocotb.runner import get_runner
from pathlib import Path
import rv32_isa


@cocotb.test()
async def alu_add_test(dut):
    dut.iFunc3.value = rv32_isa.OpF3ADD
    dut.iFunc7.value = rv32_isa.OpF7ADD
    for i in range(8):
        random.seed(9876348765*i)
        testX = random.getrandbits(31)
        testY = random.getrandbits(31)
        dut.iA.value = testX
        dut.iB.value = testY
        await Timer(1, units="ns")
        oS = dut.oZ.value.integer
        assert (testX+testY) == oS or \
            f'Random Add Failure: {testX+testY} =/= {oS}'


@cocotb.test()
async def alu_sub_test(dut):
    dut.iFunc3.value = rv32_isa.OpF3SUB
    dut.iFunc7.value = rv32_isa.OpF7SUB
    for i in range(8):
        random.seed(9876348765*i)
        testX = random.getrandbits(31)
        testY = random.getrandbits(31)
        dut.iA.value = testX
        dut.iB.value = testY
        await Timer(1, units="ns")
        oS = dut.oZ.value.integer
        assert (testX-testY) == oS or \
            f'Random Add Failure: {testX-testY} =/= {oS}'


@cocotb.test()
async def alu_sll_test(dut):
    dut.iFunc3.value = rv32_isa.OpF3SLL
    dut.iFunc7.value = rv32_isa.OpF7SLL
    for _ in range(16):
        initial = random.getrandbits(32)
        dut.iA.value = initial
        for i in range(0, 32):
            dut.iB.value = i
            await Timer(1, "ns")
            res = dut.oZ.value.integer
            expected = (initial << i) & 0xFFFFFFFF
            assert res == expected, \
                f"Failed SLL \
                {bin(res)} =/= {bin(expected)}, {i}"


@cocotb.test()
async def alu_xor_test(dut):
    dut.iFunc3.value = rv32_isa.OpF3XOR
    dut.iFunc7.value = rv32_isa.OpF7XOR
    for i in range(8):
        random.seed(9876348765*i)
        testX = random.getrandbits(31)
        testY = random.getrandbits(31)
        dut.iA.value = testX
        dut.iB.value = testY
        await Timer(1, units="ns")
        oS = dut.oZ.value.integer
        assert (testX ^ testY) == oS or \
            f'XOR Fail: {testX ^ testY} =/= {oS}'


@cocotb.test()
async def alu_mul_test(dut):
    dut.iFunc3.value = rv32_isa.OpF3MUL
    dut.iFunc7.value = rv32_isa.OpF7MUL
    for i in range(8):
        random.seed(9876348765*i)
        testX = random.getrandbits(31)
        testY = random.getrandbits(31)
        dut.iA.value = testX
        dut.iB.value = testY
        await Timer(1, units="ns")
        oS = dut.oZ.value.integer
        assert (testX * testY) == oS or \
            f'MUL Fail: {testX * testY} =/= {oS}'


@cocotb.test()
async def alu_div_test(dut):
    dut.iFunc3.value = rv32_isa.OpF3DIV
    dut.iFunc7.value = rv32_isa.OpF7MUL
    for i in range(8):
        random.seed(9876348765*i)
        testX = random.getrandbits(31)
        testY = random.getrandbits(31)
        dut.iA.value = testX
        dut.iB.value = testY
        await Timer(1, units="ns")
        oS = dut.oZ.value.integer
        assert int(testX / testY) == oS or \
            f'DIV Fail: {int(testX / testY)} =/= {oS}'


@cocotb.test()
async def alu_rem_test(dut):
    dut.iFunc3.value = rv32_isa.OpF3REM
    dut.iFunc7.value = rv32_isa.OpF7MUL
    for i in range(8):
        random.seed(9876348765*i)
        testX = random.getrandbits(31)
        testY = random.getrandbits(31)
        dut.iA.value = testX
        dut.iB.value = testY
        await Timer(1, units="ns")
        oS = dut.oZ.value.integer
        assert int(testX % testY) == oS or \
            f'XOR Fail: {int(testX % testY)} =/= {oS}'


def test_alu_runner():
    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent.parent

    sources = [
            proj_path / "rv32_isa.sv",
            proj_path / "ALU/ALU.sv",
            proj_path / "ALU/CLA.sv",
            proj_path / "ALU/BitWise.sv",
            proj_path / "ALU/DIV32.sv",
            proj_path / "ALU/MUL32.sv",
            proj_path / "ALU/SHIFT.sv"
            ]

    if sim == "icarus":
        build_args = ["-DICARUS_TRACE_ARRAYS", "-DICARUS_FST"]
    else:
        build_args = ["--trace", "-Wno-fatal"]

    runner = get_runner(sim)
    runner.build(
        verilog_sources=sources,
        hdl_toplevel="ALU",
        clean=False,
        waves=True,
        # build_args=["-DICARUS_TRACE_ARRAYS", "-DICARUS_FST"],
        build_args=build_args,
        always=True,
    )
    runner.test(
        hdl_toplevel="ALU",
        test_module="test_alu",
        plusargs=["-fst"],
        waves=True
    )


if __name__ == "__main__":
    test_alu_runner()
