import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.clock import Clock
import testbench


async def setup_pc(dut):
    clock = Clock(dut.iClk, 10, units='ns')
    dut.nRst.value = 0
    dut.iStall.value = 0
    dut.iPC.value = 0
    dut.iEXT_S.value = 0
    cocotb.start_soon(clock.start())
    await RisingEdge(dut.iClk)
    await RisingEdge(dut.iClk)
    dut.nRst.value = 1
    await RisingEdge(dut.iClk)


@cocotb.test()
async def pc_reset(dut):
    await setup_pc(dut)
    for i in range(10):
        await RisingEdge(dut.iClk)
    assert dut.oPC.value.integer != 0, "PC Still Zero"
    dut.nRst.value = 0
    await RisingEdge(dut.iClk)
    assert dut.oPC.value.integer == 0, "PC Reset Fail"


@cocotb.test()
async def pc_increment(dut):
    await setup_pc(dut)
    assert dut.oPC.value.integer == 0, "Failed Zero"
    pc = 4
    for i in range(0, 10):
        await RisingEdge(dut.iClk)
        assert dut.oPC.value.integer == pc, "Failed Increment"
        pc += 4


@cocotb.test()
async def pc_ext_load(dut):
    await setup_pc(dut)
    assert dut.oPC.value.integer == 0, "PC Reset Failed"
    dut.iPC.value = 64
    dut.iEXT_S.value = 1
    await RisingEdge(dut.iClk)
    assert dut.oPC.value.integer == 4, "PC Increment Fail"
    await RisingEdge(dut.iClk)
    assert dut.oPC.value.integer == 64, "PC EXT Load Fail"


async def pc_adder_out(dut):
    await setup_pc(dut)
    # The PC4 should always be 4 ahead of the program counter
    assert dut.oPC4.value.integer == 4, "Failed Zero"
    pc = 4
    for i in range(0, 10):
        await RisingEdge(dut.iClk)
        assert dut.oPC4.value.integer == pc+4, "Failed Increment"
        pc += 4


def test_pc_runner():
    tb = testbench.TB("test_pc", "PC")
    tb.add_source("rv32_isa.sv")
    tb.add_source("control/PC.sv")
    tb.add_source("ALU/CLA.sv")
    tb.add_param("START_ADDR", 0)
    tb.run_tests()


if __name__ == "main":
    test_pc_runner()
