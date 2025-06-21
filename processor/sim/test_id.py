import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.clock import Clock
import testbench
from hex_creator import HexCreator
from pipeline_types import if_id_t, id_ex_t, pipe_control_t
from sample_mem import mem_sample_add, mem_sample_alu, mem_sample_mem
from rv32_isa import *


async def setup_id(dut):
    clock = Clock(dut.iClk, 10, units='ns')
    dut.iEn.value = 1
    dut.nRst.value = 0
    cocotb.start_soon(clock.start())
    await RisingEdge(dut.iClk)
    await RisingEdge(dut.iClk)
    dut.nRst.value = 1
    await RisingEdge(dut.iClk)


def test_id_runner():
    tb = testbench.TB("test_id", "ID")
    tb.add_source("rv32_isa.sv")
    tb.add_source("types/reg_transport.sv")
    tb.add_source("types/pipeline_types.sv")
    tb.add_source("control/decoder.sv")
    tb.add_source("control/BranchOutcome.sv")
    tb.add_source("datapipe/ID.sv")
    tb.run_tests()


if __name__ == "__main__":
    test_id_runner()


@cocotb.test
async def id_sample_add(dut):
    rom = mem_sample_add()
    await setup_id(dut)
    iIF = if_id_t(dut.iIF)
    # Load the first instruction
    ins = rom.get_ins()[0]
    iIF.instruction = ins
    await RisingEdge(dut.iClk)
    await RisingEdge(dut.iClk)
    # Test that the instruction was decoded correctly
    oEX = id_ex_t(dut.oEX)
    ctrl = oEX.ctrl
    assert int(oEX.immediate) == 5, "Imm Decode Fail"
    assert oEX.rs1.addr == 0, "RS1 Decode Fail"
    assert int(ctrl.opcode) == OpAluI, "opcode Decode Fail"
    assert oEX.ctrl.func3 == 0, "F3 Decode Fail"
    assert oEX.ctrl.func7 == 0, "F7 Decode Fail"
    assert oEX.ctrl.wb_en == 1, "WB Enable Fail"
    assert oEX.ctrl.imm_en == 1, "IMM Enable Fail"
    assert oEX.ctrl.ex_en == 1, "EX Enable Fail"
    assert oEX.ctrl.mem_en == 0, "MEM Enable Fail"

    # Load the second instruction
    iIF.instruction = rom.get_ins()[1]
    await RisingEdge(dut.iClk)
    await RisingEdge(dut.iClk)
    # Test that it was decoded correctly
    assert int(oEX.rs1.addr) == 1, "RS1 Decode Fail"
    assert int(oEX.rs2.addr) == 1, "RS2 Decode Fail"
    opcode = oEX.ctrl.opcode
    assert int(opcode) == OpAluR, "opcode Decode Fail"
    assert oEX.ctrl.func3 == 0, "F3 Decode Fail"
    assert oEX.ctrl.func7 == 0, "F7 Decode Fail"
    assert oEX.ctrl.wb_en == 1, "WB Enable Fail"
    assert oEX.ctrl.imm_en == 0, "IMM Enable Fail"
    assert oEX.ctrl.ex_en == 1, "EX Enable Fail"
    assert oEX.ctrl.mem_en == 0, "MEM Enable Fail"


@cocotb.test
async def id_sample_alu(dut):
    rom = mem_sample_alu()
    await setup_id(dut)
    iIF = if_id_t(dut.iIF)
    oEX = id_ex_t(dut.oEX)
    # Load the first instruction 
    iIF.instruction = rom.get_ins()[0]
    await RisingEdge(dut.iClk)
    # Test that the instruction was decoded correctly
    assert oEX.rs1.addr == 2, "RS1 Decode Fail"
    assert oEX.rs2.addr == 3, "RS2 Decode Fail"
    assert oEX.ctrl.opcode == OpAluR, "opcode Fail"
    assert oEX.ctrl.func3 == OpF3OR, "F3 Decode Fail"
    assert oEX.ctrl.func7 == OpF7OR, "F7 Decode Fail"
    assert oEX.ctrl.wb_en == 1, "WB Enable Fail"
    assert oEX.ctrl.imm_en == 0, "IMM Enable Fail"
    assert oEX.ctrl.ex_en == 1, "EX Enable Fail"
    assert oEX.ctrl.mem_en == 0, "MEM Enable Fail"

    # Load the instruction 
    iIF.instruction = rom.get_ins()[1]
    await RisingEdge(dut.iClk)
    # Test that the instruction was decoded correctly
    assert oEX.rs1.addr == 12, "RS1 Decode Fail"
    assert oEX.rs2.addr == 13, "RS2 Decode Fail"
    assert oEX.ctrl.opcode == OpAluR, "opcode Fail"
    assert oEX.ctrl.func3 == OpF3AND, "F3 Decode Fail"
    assert oEX.ctrl.func7 == OpF7AND, "F7 Decode Fail"
    assert oEX.ctrl.wb_en == 1, "WB Enable Fail"
    assert oEX.ctrl.imm_en == 0, "IMM Enable Fail"
    assert oEX.ctrl.ex_en == 1, "EX Enable Fail"
    assert oEX.ctrl.mem_en == 0, "MEM Enable Fail"

    # Load the instruction 
    iIF.instruction = rom.get_ins()[2]
    await RisingEdge(dut.iClk)
    # Test that the instruction was decoded correctly
    assert oEX.rs1.addr == 30, "RS1 Decode Fail"
    assert oEX.rs2.addr == 17, "RS2 Decode Fail"
    assert oEX.ctrl.opcode == OpAluR, "opcode Fail"
    assert oEX.ctrl.func3 == OpF3SLL, "F3 Decode Fail"
    assert oEX.ctrl.func7 == OpF7SLL, "F7 Decode Fail"
    assert oEX.ctrl.wb_en == 1, "WB Enable Fail"
    assert oEX.ctrl.imm_en == 0, "IMM Enable Fail"
    assert oEX.ctrl.ex_en == 1, "EX Enable Fail"
    assert oEX.ctrl.mem_en == 0, "MEM Enable Fail"


@cocotb.test
async def id_sample_mem(dut):
    rom = mem_sample_mem()
    await setup_id(dut)
    iIF = if_id_t(dut.iIF)
    oEX = id_ex_t(dut.oEX)
    # Load the first instruction 
    iIF.instruction = rom.get_ins()[0]
    await RisingEdge(dut.iClk)
    # Test that the instruction was decoded correctly
    assert oEX.rs1.addr == 2, "RS1 Decode Fail"
    assert oEX.rs2.addr == 3, "RS2 Decode Fail"
    assert oEX.immediate == 20, "Imm Fail"
    assert oEX.ctrl.opcode == OpStore, "opcode Fail"
    assert oEX.ctrl.func3 == OpF3SW, "F3 Decode Fail"
    assert oEX.ctrl.wb_en == 0, "WB Enable Fail"
    assert oEX.ctrl.imm_en == 1, "IMM Enable Fail"
    assert oEX.ctrl.ex_en == 0, "EX Enable Fail"
    assert oEX.ctrl.mem_en == 1, "MEM Enable Fail"
    # Load the first instruction 
    iIF.instruction = rom.get_ins()[1]
    await RisingEdge(dut.iClk)
    # Test that the instruction was decoded correctly
    assert oEX.rs1.addr == 5, "RS1 Decode Fail"
    assert oEX.rd_addr == 4, "RD Dec Fail"
    # assert oEX.rs2.addr == 5, "RS2 Decode Fail"
    assert oEX.immediate == 0x64, "Imm Fail"
    assert oEX.ctrl.opcode == OpLoad, "opcode Fail"
    assert oEX.ctrl.func3 == OpF3LW, "F3 Decode Fail"
    assert oEX.ctrl.wb_en == 1, "WB Enable Fail"
    assert oEX.ctrl.imm_en == 1, "IMM Enable Fail"
    assert oEX.ctrl.ex_en == 0, "EX Enable Fail"
    assert oEX.ctrl.mem_en == 1, "MEM Enable Fail"
