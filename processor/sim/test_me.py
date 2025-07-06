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


async def setup_me(dut):
    clock = Clock(dut.iClk, 10, units='ns')
    dut.iEn.value = 0
    dut.nRst.value = 0
    cocotb.start_soon(clock.start())
    await RisingEdge(dut.iClk)
    await RisingEdge(dut.iClk)
    dut.nRst.value = 1
    dut.iEn.value = 1
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
async def mem_wr_byte(dut):
    await setup_me(dut)
    # Setup a sample instruction (sub)
    await RisingEdge(dut.iClk)
    iEX = ex_mem_t(dut.iEX)
    iEX.ctrl.func3 = OpF3SB
    iEX.ctrl.mem_en = 1
    iEX.ctrl.ex_en = 0
    iEX.ctrl.wb_en = 0
    iEX.ctrl.valid = 1
    for i in range(0, 10):
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
    for i in range(0, 10):
        iEX.rd.value = i << 2
        await RisingEdge(dut.iClk)
        await RisingEdge(dut.iClk)
        assert oWB.rd.value == (23*(i+1)) & 0xFF, "Fail"
    pass
