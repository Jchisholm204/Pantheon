import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.clock import Clock
import util.testbench as testbench
from incl.pipeline_types import id_ex_t, ex_mem_t
from incl.pipeline_types import pipe_control_t
from util.sample_mem import mem_sample_add, mem_sample_alu, mem_sample_mem
from rv32_isa import *
from util.sources import Sources
import random


async def setup_ex(dut):
    clock = Clock(dut.iClk, 10, units='ns')
    dut.nRst.value = 0
    cocotb.start_soon(clock.start())
    await RisingEdge(dut.iClk)
    await RisingEdge(dut.iClk)
    dut.nRst.value = 1
    dut.iStall.value = 0
    await RisingEdge(dut.iClk)


def test_ex_runner():
    tb = testbench.TB("test_ex", "EX")
    tb.add_sources(Sources.ISA())
    tb.add_sources(Sources.TYPES())
    tb.add_sources(Sources.ALU())
    tb.add_source("processor/datapipe/EX.sv")
    tb.run_tests()


if __name__ == "__main__":
    test_ex_runner()


@cocotb.test
async def ex_sub_tes(dut):
    await setup_ex(dut)
    # Setup a sample instruction (sub)
    await RisingEdge(dut.iClk)
    iID = id_ex_t(dut.iID)
    A = 100
    B = 55
    iID.rs1.value = A
    iID.rs2.value = B
    iID.ctrl.func3 = OpF3SUB
    iID.ctrl.opcode = 0x7F
    iID.ctrl.func7 = OpF7SUB
    iID.ctrl.valid = 1
    iID.ctrl.wb_en = 1
    iID.ctrl.ex_en = 1
    iID.ctrl.imm_en = 0
    iID.immediate = 0x124
    # Value will appear on input on rising edge
    await RisingEdge(dut.iClk)
    # Wait for procesing
    # Value latches in output reg on next rising edge
    await RisingEdge(dut.iClk)
    # Assert that the instruction was performed correctly
    oMEM = ex_mem_t(dut.oMEM)
    assert oMEM.rd.value == A-B, "Failed SUB"
    # Add extra sim time for readability
    await RisingEdge(dut.iClk)
    pass


@cocotb.test
async def ex_mem_tes(dut):
    await setup_ex(dut)
    # Setup a sample instruction (sub)
    # await RisingEdge(dut.iClk)
    iID = id_ex_t(dut.iID)
    A = 0x123
    B = 0x456
    C = 0x235
    iID.rs1.value = A
    iID.rs2.value = B
    iID.ctrl.func3 = OpF3SUB
    iID.ctrl.opcode = 0x7F
    iID.ctrl.func7 = OpF7SUB
    iID.ctrl.valid = 1
    iID.ctrl.wb_en = 1
    # Ensure EX is disabled, immediate is enabled
    iID.ctrl.ex_en = 0
    iID.ctrl.mem_en = 1
    iID.ctrl.imm_en = 1
    iID.immediate = C
    # Value will appear on input on rising edge
    await RisingEdge(dut.iClk)
    # Wait for procesing
    # Value latches in output reg on next rising edge
    await RisingEdge(dut.iClk)
    # Assert that the instruction was performed correctly
    oMEM = ex_mem_t(dut.oMEM)
    assert oMEM.rd.value == A+C, "Failed Mem Add"
    assert oMEM.rs.value == B, "Failed Pass RS"
    # Add extra sim time for readability
    await RisingEdge(dut.iClk)
    pass


@cocotb.test
async def ex_stall(dut):
    await setup_ex(dut)
    # Setup a sample instruction (sub)
    # await RisingEdge(dut.iClk)
    iID = id_ex_t(dut.iID)
    A = 0x123
    B = 0x456
    C = 0x235
    iID.rs1.value = A
    iID.rs2.value = B
    iID.ctrl.func3 = OpF3ADD
    iID.ctrl.opcode = 0x7F
    iID.ctrl.func7 = OpF7ADD
    iID.ctrl.valid = 1
    iID.ctrl.wb_en = 1
    # Ensure EX is disabled, immediate is enabled
    iID.ctrl.ex_en = 1
    iID.ctrl.mem_en = 1
    iID.ctrl.imm_en = 1
    iID.immediate = C
    # Value will appear on input on rising edge
    await RisingEdge(dut.iClk)
    # Wait for procesing
    # Value latches in output reg on next rising edge
    await RisingEdge(dut.iClk)
    # Assert that the instruction was performed correctly
    oMEM = ex_mem_t(dut.oMEM)
    assert oMEM.rd.value == A+C, "Failed Mem Add"
    assert oMEM.rs.value == B, "Failed Pass RS"
    # Assert the stall signal
    dut.iStall.value = 1
    # Change inputs
    iID.rs1.value = 0
    iID.rs2.value = 0
    iID.immediate = 0
    await RisingEdge(dut.iClk)
    await RisingEdge(dut.iClk)
    assert oMEM.rd.value == A+C, "Failed Mem Add"
    assert oMEM.rs.value == B, "Failed Pass RS"
    dut.iStall.value = 0
    # iID.rs1.write(0)
    iID.rs1.value = 0x0
    iID.rs2.value = 0x0
    iID.ctrl.imm_en = 0
    await RisingEdge(dut.iClk)
    await RisingEdge(dut.iClk)
    assert oMEM.rd.value == 0, "Failed Mem Add"
    assert oMEM.rs.value == 0, "Failed Pass RS"
    # Add extra sim time for readability
    await RisingEdge(dut.iClk)
    pass
