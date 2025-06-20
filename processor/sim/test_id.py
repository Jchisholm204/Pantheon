import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.clock import Clock
import testbench
from hex_creator import HexCreator
from pipeline_types import if_id_t, id_ex_t
from sample_mem import mem_sample_add


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


@cocotb.test()
async def test_id_add(dut):
    rom = mem_sample_add()
    await setup_id(dut)
    iIF = if_id_t(dut.iIF)
    for ins in rom.get_ins():
        iIF.instruction = ins
        await RisingEdge(dut.iClk)
