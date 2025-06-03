import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.clock import Clock
import testbench


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


@cocotb.test()
async def if_memread(dut):
    await setup_if(dut)


def test_pc_runner():
    tb = testbench.TB("test_if", "IF")
    tb.add_source("rv32_isa.sv")
    tb.add_source("control/PC.sv")
    tb.add_source("ALU/CLA.sv")
    tb.add_source("../wishbone/WISHBONE_IF.sv")
    tb.add_source("memory/ROMBlock.sv")
    tb.add_source("memory/IMEM.sv")
    tb.add_source("datapipe/IF.sv")
    tb.run_tests()


if __name__ == "main":
    test_pc_runner()
