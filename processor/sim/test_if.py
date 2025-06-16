import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.clock import Clock
import testbench
from hex_creator import HexCreator
from rv32_isa import *
from sv_structs import if_id_t


def setup_mem(fname="testROM.hex"):
    rom = HexCreator(fname)
    rom.add_Iins(OpAluI, 1, OpF3ADD, 0, 0xF)
    rom.add_Rins(OpAluR, 2, OpF3ADD, 1, 1, OpF7ADD)
    return rom


async def setup_if(dut):
    clock = Clock(dut.iClk, 10, units='ns')
    dut.iEn.value = 1
    dut.nRst.value = 0
    dut.iStall.value = 0
    dut.iPCS_EXT.value = 0
    dut.iPC_EXT.value = 0
    cocotb.start_soon(clock.start())
    await RisingEdge(dut.iClk)
    await RisingEdge(dut.iClk)
    dut.nRst.value = 1
    await RisingEdge(dut.iClk)


def test_if_runner():
    fname = "testROM.hex"
    setup_mem(fname).export()
    tb = testbench.TB("test_if", "IF")
    tb.add_define("ROMFile", f'"../{fname}"')
    tb.add_source("rv32_isa.sv")
    tb.add_source("types/reg_transport.sv")
    tb.add_source("types/pipeline_types.sv")
    tb.add_source("control/PC.sv")
    tb.add_source("ALU/CLA.sv")
    tb.add_source("../wishbone/WISHBONE_IF.sv")
    tb.add_source("memory/ROMBlock.sv")
    tb.add_source("memory/IMEM.sv")
    tb.add_source("datapipe/IF.sv")
    tb.run_tests()


if __name__ == "__main__":
    test_if_runner()


@cocotb.test()
async def if_memread(dut):
    rom = setup_mem()
    await setup_if(dut)
    for ins in rom.get_ins():
        await RisingEdge(dut.iClk)
        # oIR = dut.oID.value[64:95].integer
        oIR = if_id_t(dut.oID).instruction
        # oIR = gets(dut.oID, IF_ID, "instruction").integer
        assert oIR == ins, "Failed Memory Read"
