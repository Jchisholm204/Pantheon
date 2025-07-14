import cocotb
from cocotb.handle import ModifiableObject
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.clock import Clock
from reg_transport_t import reg_transport_t
import testbench
from sources import ISA_SOURCES, TYPES_SOURCES, ALU_SOURCES
from sources import MEM_SOURCES, WISHBONE_SOURCES, PIPE_SOURCES
from sources import CTRL_SOURCES


class Processor():
    def __init__(self, dut):
        self.dut = dut
        self.iClk: ModifiableObject = self.dut.iClk
        self.nRst: ModifiableObject = self.dut.nRst
        self.dbg_halt: ModifiableObject = self.dut.DBG_halt
        self.dbg_exec: ModifiableObject = self.dut.DBG_exec
        self.dbg_req_init: ModifiableObject = self.dut.DBG_req_init
        self.dbg_regWrite: ModifiableObject = self.dut.DBG_regWrite
        self.dbg_ins: ModifiableObject = self.dut.DBG_ins
        self.dbg_rd = reg_transport_t(self.dut.DBG_rd)
        self.dbg_rs = reg_transport_t(self.dut.DBG_rs)

    async def setup(self):
        self.clock = Clock(self.iClk, 10, units='ns')
        self.nRst.value = 0
        cocotb.start_soon(self.clock.start())
        await RisingEdge(self.iClk)
        await RisingEdge(self.iClk)
        self.nRst.value = 1

    async def wait(self, time=0, units='ns'):
        if time == 0:
            await RisingEdge(self.iClk)
        else:
            await Timer(time, units=units)


@cocotb.test
async def proc_basic(dut):
    proc = Processor(dut)
    await proc.setup()
    await proc.wait(100, units='ns')


def test_processor_runner():
    tb = testbench.TB("test_processor", "Processor")
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
