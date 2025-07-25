import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.clock import Clock
import testbench
from pipeline_types import ex_mem_t, mem_wb_t
from pipeline_types import pipe_control_t
from sample_mem import mem_sample_add, mem_sample_alu, mem_sample_mem
from rv32_isa import *
from sources import ISA_SOURCES, TYPES_SOURCES, WISHBONE_SOURCES, MEM_SOURCES
import random
from test_bitwise import to_signed32

N_TEST = 10

async def setup_me(dut):
    clock = Clock(dut.iClk, 10, units='ns')
    dut.nRst.value = 0
    cocotb.start_soon(clock.start())
    await RisingEdge(dut.iClk)
    await RisingEdge(dut.iClk)
    dut.nRst.value = 1
    dut.iStall.value = 0
    await RisingEdge(dut.iClk)


def test_me_runner():
    tb = testbench.TB("test_me", "ME")
    tb.add_sources(ISA_SOURCES)
    tb.add_sources(TYPES_SOURCES)
    tb.add_sources(WISHBONE_SOURCES)
    tb.add_sources(MEM_SOURCES)
    tb.add_source("datapipe/ME.sv")
    tb.run_tests()


if __name__ == "__main__":
    test_me_runner()


@cocotb.test
async def mem_wr_byte_unsigned(dut):
    await setup_me(dut)
    # Setup a sample instruction (sub)
    await RisingEdge(dut.iClk)
    iEX = ex_mem_t(dut.iEX)
    iEX.ctrl.func3 = OpF3SB
    iEX.ctrl.mem_en = 1
    iEX.ctrl.ex_en = 0
    iEX.ctrl.wb_en = 0
    iEX.ctrl.valid = 1
    for i in range(0, N_TEST):
        iEX.rd.value = i << 2
        iEX.rs.value = 23*(i+1)
        await RisingEdge(dut.iClk)
        await RisingEdge(dut.iClk)
    oWB = mem_wb_t(dut.oWB)
    iEX.ctrl.func3 = OpF3LBU
    iEX.ctrl.mem_en = 1
    iEX.ctrl.ex_en = 0
    iEX.ctrl.wb_en = 1
    iEX.ctrl.valid = 1
    for i in range(0, N_TEST):
        iEX.rd.value = i << 2
        await RisingEdge(dut.iClk)
        await RisingEdge(dut.iClk)
        assert oWB.rd.value == (23*(i+1)) & 0xFF, "Fail"
    pass


@cocotb.test
async def mem_wr_bu_inc(dut):
    await setup_me(dut)
    # Setup a sample instruction (sub)
    await RisingEdge(dut.iClk)
    iEX = ex_mem_t(dut.iEX)
    iEX.ctrl.func3 = OpF3SB
    iEX.ctrl.mem_en = 1
    iEX.ctrl.ex_en = 0
    iEX.ctrl.wb_en = 0
    iEX.ctrl.valid = 1
    for i in range(0, N_TEST):
        iEX.rd.value = i
        iEX.rs.value = 23*(i+1)
        await RisingEdge(dut.iClk)
        await RisingEdge(dut.iClk)
    oWB = mem_wb_t(dut.oWB)
    iEX.ctrl.func3 = OpF3LBU
    iEX.ctrl.mem_en = 1
    iEX.ctrl.ex_en = 0
    iEX.ctrl.wb_en = 1
    iEX.ctrl.valid = 1
    for i in range(0, N_TEST):
        iEX.rd.value = i
        await RisingEdge(dut.iClk)
        await RisingEdge(dut.iClk)
        assert oWB.rd.value == (23*(i+1)) & 0xFF, "Fail"
    pass


@cocotb.test
async def mem_wr_byte_signed(dut):
    await setup_me(dut)
    # Setup a sample instruction (sub)
    await RisingEdge(dut.iClk)
    iEX = ex_mem_t(dut.iEX)
    iEX.ctrl.func3 = OpF3SB
    iEX.ctrl.mem_en = 1
    iEX.ctrl.ex_en = 0
    iEX.ctrl.wb_en = 0
    iEX.ctrl.valid = 1
    for i in range(0, N_TEST):
        iEX.rd.value = i << 2
        iEX.rs.value = (i+1) * -3
        await RisingEdge(dut.iClk)
        await RisingEdge(dut.iClk)
    oWB = mem_wb_t(dut.oWB)
    iEX.ctrl.func3 = OpF3LB
    iEX.ctrl.mem_en = 1
    iEX.ctrl.ex_en = 0
    iEX.ctrl.wb_en = 1
    iEX.ctrl.valid = 1
    for i in range(0, N_TEST):
        iEX.rd.value = i << 2
        await RisingEdge(dut.iClk)
        await RisingEdge(dut.iClk)
        assert to_signed32(oWB.rd.value) == to_signed32(-((3 * (i+1)) & 0xFF)), "Fail"
    pass


@cocotb.test
async def mem_wr_hw_unsigned(dut):
    await setup_me(dut)
    # Setup a sample instruction (sub)
    await RisingEdge(dut.iClk)
    iEX = ex_mem_t(dut.iEX)
    iEX.ctrl.func3 = OpF3SH
    iEX.ctrl.mem_en = 1
    iEX.ctrl.ex_en = 0
    iEX.ctrl.wb_en = 0
    iEX.ctrl.valid = 1
    for i in range(0, N_TEST):
        iEX.rd.value = i << 2
        iEX.rs.value = (i+1) * 23
        await RisingEdge(dut.iClk)
        await RisingEdge(dut.iClk)
    oWB = mem_wb_t(dut.oWB)
    iEX.ctrl.func3 = OpF3LHU
    iEX.ctrl.mem_en = 1
    iEX.ctrl.ex_en = 0
    iEX.ctrl.wb_en = 1
    iEX.ctrl.valid = 1
    for i in range(0, N_TEST):
        iEX.rd.value = i << 2
        await RisingEdge(dut.iClk)
        await RisingEdge(dut.iClk)
        assert int(oWB.rd.value) == (23 * (i+1)), "Fail"
    pass


@cocotb.test
async def mem_wr_hw_signed(dut):
    await setup_me(dut)
    # Setup a sample instruction (sub)
    await RisingEdge(dut.iClk)
    iEX = ex_mem_t(dut.iEX)
    iEX.ctrl.func3 = OpF3SH
    iEX.ctrl.mem_en = 1
    iEX.ctrl.ex_en = 0
    iEX.ctrl.wb_en = 0
    iEX.ctrl.valid = 1
    for i in range(0, N_TEST):
        iEX.rd.value = i << 2
        iEX.rs.value = int(i-N_TEST/2) * 23
        await RisingEdge(dut.iClk)
        await RisingEdge(dut.iClk)
    oWB = mem_wb_t(dut.oWB)
    iEX.ctrl.func3 = OpF3LH
    iEX.ctrl.mem_en = 1
    iEX.ctrl.ex_en = 0
    iEX.ctrl.wb_en = 1
    iEX.ctrl.valid = 1
    for i in range(0, N_TEST):
        iEX.rd.value = i << 2
        await RisingEdge(dut.iClk)
        await RisingEdge(dut.iClk)
        assert to_signed32(oWB.rd.value) == (23 * int(i-N_TEST/2)), "Fail"
    pass


@cocotb.test
async def mem_wr_word(dut):
    await setup_me(dut)
    # Setup a sample instruction (sub)
    await RisingEdge(dut.iClk)
    iEX = ex_mem_t(dut.iEX)
    iEX.ctrl.func3 = OpF3SW
    iEX.ctrl.mem_en = 1
    iEX.ctrl.ex_en = 0
    iEX.ctrl.wb_en = 0
    iEX.ctrl.valid = 1
    for i in range(0, N_TEST):
        iEX.rd.value = i << 2
        iEX.rs.value = (i+1) * 23
        await RisingEdge(dut.iClk)
        await RisingEdge(dut.iClk)
    oWB = mem_wb_t(dut.oWB)
    iEX.ctrl.func3 = OpF3LW
    iEX.ctrl.mem_en = 1
    iEX.ctrl.ex_en = 0
    iEX.ctrl.wb_en = 1
    iEX.ctrl.valid = 1
    for i in range(0, N_TEST):
        iEX.rd.value = i << 2
        await RisingEdge(dut.iClk)
        await RisingEdge(dut.iClk)
        assert to_signed32(oWB.rd.value) == (23 * (i+1)), "Fail"
    pass
