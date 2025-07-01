import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.clock import Clock
import testbench
from pipeline_types import id_ex_t, ex_mem_t
from pipeline_types import pipe_control_t
from sample_mem import mem_sample_add, mem_sample_alu, mem_sample_mem
from rv32_isa import *
from sources import ISA_SOURCES, TYPES_SOURCES, ALU_SOURCES
import random


async def setup_ex(dut):
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


def test_ex_runner():
    tb = testbench.TB("test_ex", "EX")
    tb.add_sources(ISA_SOURCES)
    tb.add_sources(TYPES_SOURCES)
    tb.add_sources(ALU_SOURCES)
    tb.add_source("datapipe/EX.sv")
    tb.run_tests()


if __name__ == "__main__":
    test_ex_runner()


@cocotb.test
async def ex_std_op(dut):
    await setup_ex(dut)
    # Setup a sample instruction (sub)
    await RisingEdge(dut.iClk)
    iID = id_ex_t(dut.iID)
    # iID.ctrl = pipe_control_t(iID)
    A = 0x22
    B = 0x11
    # iID.rs1.value = A
    iID.rs2.value = B
    # iID.ctrl.func3 = OpF3AND
    # iID.ctrl.func7 = OpF7AND
    # iID.ctrl.valid = 1
    # iID.ctrl.wb_en = 1
    # iID.ctrl.ex_en = 1
    # iID.ctrl.imm_en = 0
    iID.immediate = 0x123
    print("ID VALUE 1")
    print(iID._recent.integer)
    print(dut.iID._type)
    print(dut.oMEM._type)
    # dut.iID.value = iID._recent.integer
    await RisingEdge(dut.iClk)
    ctrl = pipe_control_t(iID)
    ctrl.func3 = 0x1
    ctrl.imm_en = 1
    dut.iID.value = ctrl._recent.integer
    await RisingEdge(dut.iClk)
    print("ID VALUE")
    print(iID._recent.integer)
    dut.iID.value = iID._recent.integer
    await RisingEdge(dut.iClk)
    # Assert that the instruction was performed correctly
    oMEM = ex_mem_t(dut.oMEM)
    # assert oMEM.rd.value == A-B, "Failed SUB"
    pass
