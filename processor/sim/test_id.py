import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.clock import Clock
import testbench
from hex_creator import HexCreator
from pipeline_types import if_id_t, id_ex_t, pipe_control_t
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


@cocotb.test
async def id_sample_add(dut):
    rom = mem_sample_add()
    await setup_id(dut)
    iIF = if_id_t(dut.iIF)
    ins = rom.get_ins()[0]
    iIF.instruction = ins
    await RisingEdge(dut.iClk)
    await RisingEdge(dut.iClk)
    oEX = id_ex_t(dut.oEX)
    # assert int(oEX.immediate) == 5, "Imm Decode Fail"
    assert oEX.rs1.addr == 0, "RS1 Decode Fail"
    iIF.instruction = rom.get_ins()[1]
    await RisingEdge(dut.iClk)
    await RisingEdge(dut.iClk)
    assert int(oEX.rs1.value) == 1, "RS1 Decode Fail"
    # opcode = dut.oEX.value[0:6]
    # opcode = pipe_control_t(dut.oEX).opcode
    opcode = oEX.ctrl.opcode
    assert int(opcode) == 51, "opcode Decode Fail"
    # assert oEX.ctrl.func3 == 0, "F3 Decode Fail"
    # assert oEX.ctrl.func7 == 0, "F7 Decode Fail"
