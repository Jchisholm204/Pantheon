import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.clock import Clock
from cocotb.handle import ModifiableObject
import util.testbench as testbench
from util.hex_creator import HexCreator
from rv32_isa import *
from incl.pipeline_types import if_id_t, id_ex_t, ex_mem_t, mem_wb_t
from util.sources import Sources


class DebugModule():
    def __init__(self, dut):
        self.dut = dut
        self.iClk: ModifiableObject = self.dut.iClk
        self.nRst: ModifiableObject = self.dut.nRst
        self.halted: ModifiableObject = self.dut.halted
        self.running: ModifiableObject = self.dut.running
        self.enter_debug: ModifiableObject = self.dut.enter_debug
        self.req_halt: ModifiableObject = self.dut.req_halt
        self.req_resume: ModifiableObject = self.dut.req_resume
        self.step: ModifiableObject = self.dut.step
        self.dm_rdata: ModifiableObject = self.dut.dm_rdata
        self.dm_wdata: ModifiableObject = self.dut.dm_wdata
        self.dm_access_valid: ModifiableObject = self.dut.dm_access_valid
        self.dm_write: ModifiableObject = self.dut.dm_write
        self.dm_addr: ModifiableObject = self.dut.dm_addr

    async def setup(self):
        self.clock = Clock(self.iClk, 10, units='ns')
        self.nRst.value = 0
        cocotb.start_soon(self.clock.start())
        await RisingEdge(self.iClk)
        await RisingEdge(self.iClk)
        self.nRst.value = 1

    async def write_reg(self, reg, value):
        self.dm_addr.value = reg
        self.dm_write.value = 1
        self.dm_access_valid.value = 1
        self.dm_wdata.value = value
        await RisingEdge(self.iClk)

    async def read_reg(self, reg, value):
        self.dm_addr.value = reg
        self.dm_write.value = 0
        self.dm_access_valid.value = 1
        await RisingEdge(self.iClk)
        return self.dm_rdata.value



@cocotb.test
async def dbg_mod_scratch(dut):
    pass


def test_debugmodule_runner():
    tb = testbench.TB("test_debugmodule", "DebugModuleTest")
    tb.add_sources(Sources.ISA())
    tb.add_sources(Sources.TYPES())
    tb.add_sources(Sources.INTERFACES())
    tb.add_sources(Sources.MEM())
    tb.add_source("processor/control/DebugModule.sv")
    tb.add_source("sim/DebugModuleTest.sv")
    tb.run_tests()


if __name__ == "__main__":
    test_debugmodule_runner()
