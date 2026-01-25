import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.clock import Clock
import util.testbench as testbench
from util.hex_creator import HexCreator
from rv32_isa import *
from incl.pipeline_types import if_id_t
from util.sources import Sources


async def setup_if(dut):
    clock = Clock(dut.iClk, 10, units='ns')
    dut.iEn.value = 1
    dut.nRst.value = 0
    dut.iFlush.value = 0
    dut.iStall.value = 0
    dut.iPCS_EXT.value = 0
    dut.iPC_EXT.value = 0
    cocotb.start_soon(clock.start())
    await RisingEdge(dut.iClk)
    await RisingEdge(dut.iClk)
    dut.nRst.value = 1
    await RisingEdge(dut.iClk)


def test_if_runner():
    tb = testbench.TB("test_proc_if", "IF")
    tb.add_sources(Sources.ISA())
    tb.add_sources(Sources.TYPES())
    tb.add_source("processor/control/PC.sv")
    tb.add_source("processor/ALU/CLA.sv")
    tb.add_sources(Sources.INTERFACES())
    tb.add_sources(Sources.MEM())
    tb.add_source("processor/datapipe/IF.sv")
    tb.run_tests()


if __name__ == "__main__":
    test_if_runner()


async def ins_memory(dut, mem: HexCreator):
    while True:
        await RisingEdge(dut.iClk)
        addr = dut.oIM_addr.value.integer
        if addr % 4 != 0:
            assert False, f"Addr {addr} not divisible by 4"
        addr = addr / 4
        if addr < 0:
            assert False, f"Addr {addr} was negative!"
        if addr >= len(mem.instructions):
            dut.iIM_data.value = 0
        else:
            dut.iIM_data.value = mem.instructions[int(addr)]


@cocotb.test()
async def if_pcinc(dut):
    await setup_if(dut)
    assert dut.oIM_addr == 0x0, f"PC Init {dut.oIM_addr} != 0 Failed"
    await RisingEdge(dut.iClk)
    for i in range(1, 20):
        addr = i*4
        assert int(dut.oIM_addr) == addr, f"PC Init Inc Failed {
            int(dut.oIM_addr)} != {addr}"
        await RisingEdge(dut.iClk)
    pass


@cocotb.test()
async def if_memread(dut):
    mem = HexCreator()
    # Clear R1
    mem.add_Iins(OpAluI, 1, OpF3ADD, 0, 0)
    # Calculate summation of all values between 0 and 5
    for i in range(0, 5):
        mem.add_Iins(OpAluI, 1, OpF3ADD, 1, i)
    cocotb.start_soon(ins_memory(dut, mem))
    await setup_if(dut)
    await RisingEdge(dut.iClk)
    for i, ins in enumerate(mem.instructions):
        await RisingEdge(dut.iClk)
        oins = int(if_id_t(dut.oID).instruction)
        assert oins == ins, f"INS Assert Failed {i}"

    pass
