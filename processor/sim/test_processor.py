import cocotb
from cocotb.handle import ModifiableObject, NonHierarchyIndexableObject
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.clock import Clock
from reg_transport_t import reg_transport_t
import testbench
from sources import ISA_SOURCES, TYPES_SOURCES, ALU_SOURCES
from sources import MEM_SOURCES, WISHBONE_SOURCES, PIPE_SOURCES
from sources import CTRL_SOURCES
from test_if import setup_mem
from hex_creator import HexCreator
from test_bitwise import to_signed32
from rv32_isa import *


class Processor():
    def __init__(self, dut):
        self.dut = dut
        self.iClk: ModifiableObject = self.dut.iClk
        self.nRst: ModifiableObject = self.dut.nRst
        self.dbg_nRst: ModifiableObject = self.dut.DBG_nRst
        self.dbg_halt: ModifiableObject = self.dut.DBG_halt
        self.dbg_exec: ModifiableObject = self.dut.DBG_exec
        self.dbg_req_init: ModifiableObject = self.dut.DBG_req_init
        self.dbg_regWrite: ModifiableObject = self.dut.DBG_regWrite
        self.dbg_ins: ModifiableObject = self.dut.DBG_ins
        self.dbg_rd = reg_transport_t(self.dut.DBG_rd)
        self.dbg_rs = reg_transport_t(self.dut.DBG_rs)
        self.rf: NonHierarchyIndexableObject = self.dut.rf.reg_outs
        self._setup = False

    async def setup(self):
        self.clock = Clock(self.iClk, 10, units='ns')
        self.nRst.value = 0
        cocotb.start_soon(self.clock.start())
        await RisingEdge(self.iClk)
        await RisingEdge(self.iClk)
        self.nRst.value = 1
        self._setup = True

    async def wait(self, time=0, units='ns'):
        if time == 0:
            await RisingEdge(self.iClk)
        else:
            await Timer(time, units=units)

    async def enter_dbg(self):
        if self._setup is False:
            await self.setup()
        self.dbg_req_init.value = 1
        await RisingEdge(self.iClk)
        self.dbg_halt.value = 1
        self.dbg_nRst.value = 0
        await RisingEdge(self.iClk)
        self.dbg_nRst.value = 1

    async def run_test(self, rom: HexCreator):
        if self._setup is False:
            await self.setup()
        await RisingEdge(self.iClk)
        await self.enter_dbg()
        self.dbg_exec.value = 1
        self.dbg_halt.value = 0
        for ins in rom.get_ins():
            self.dbg_ins.value = ins
            await RisingEdge(self.iClk)
        for _ in range(0, 4):
            await RisingEdge(self.iClk)


# @cocotb.test
# async def proc_basic(dut):
#     proc = Processor(dut)
#     await proc.setup()
#     await proc.wait(100, units='ns')


@cocotb.test
async def proc_dbg(dut):
    proc = Processor(dut)
    hc = HexCreator()
    hc.add_Iins(OpAluI, 1, OpF3ADD, 0, 15)
    hc.add_Iins(OpAluI, 2, OpF3ADD, 1, 10)
    # hc.add_Iins(OpAluI, 0, OpF3ADD, 0, 0)
    # hc.add_Iins(OpAluI, 0, OpF3ADD, 0, 0)
    # hc.add_Iins(OpAluI, 0, OpF3ADD, 0, 0)
    hc.add_Rins(OpAluR, 3, OpF3SUB, 1, 2, OpF7SUB)
    # hc.add_Iins(OpAluI, 0, OpF3ADD, 0, 0)
    await proc.run_test(hc)
    print("dut.rf")
    print(type(dut.rf.reg_outs))
    print(dut.rf.reg_outs[1].value.integer)
    assert proc.rf[1].value == 15, "Fail Load R1"
    assert proc.rf[2].value == 25, "Fail Addi R2"
    assert to_signed32(proc.rf[3].value) == -10, "Fail Sub R3=R1-R2"
    pass


@cocotb.test
async def proc_addi_sub(dut):
    proc = Processor(dut)
    hc = HexCreator()
    hc.add_Iins(OpAluI, 1, OpF3ADD, 0, 15)
    hc.add_Iins(OpAluI, 2, OpF3ADD, 1, 10)
    hc.add_Rins(OpAluR, 3, OpF3SUB, 1, 2, OpF7SUB)
    await proc.run_test(hc)
    print("dut.rf")
    print(type(dut.rf.reg_outs))
    print(dut.rf.reg_outs[1].value.integer)
    assert proc.rf[1].value == 15, "Fail Load R1"
    assert proc.rf[2].value == 25, "Fail Addi R2"
    assert to_signed32(proc.rf[3].value) == -10, "Fail Sub R3=R1-R2"
    pass


def test_processor_runner():
    tb = testbench.TB("test_processor", "Processor")
    fname = "testROM.hex"
    setup_mem(fname).export()
    tb.add_define("ROMFile", f'"../{fname}"')
    tb.add_sources(ISA_SOURCES)
    tb.add_sources(TYPES_SOURCES)
    tb.add_sources(ALU_SOURCES)
    tb.add_sources(MEM_SOURCES)
    tb.add_sources(WISHBONE_SOURCES)
    tb.add_sources(CTRL_SOURCES)
    tb.add_sources(PIPE_SOURCES)
    tb.add_source("control/HazardUnit.sv")
    tb.add_source("Processor.sv")
    tb.run_tests()


if __name__ == "__main__":
    test_processor_runner()
