import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.clock import Clock
from cocotb.handle import ModifiableObject
import testbench
from hex_creator import HexCreator
from rv32_isa import *
from pipeline_types import if_id_t, id_ex_t, ex_mem_t, mem_wb_t
from sources import TYPES_SOURCES, ISA_SOURCES


class HazardUnit():
    def __init__(self, dut):
        self.dut = dut
        self.iClk: ModifiableObject = self.dut.iClk
        self.nRst: ModifiableObject = self.dut.nRst
        self.iBrTrue: ModifiableObject = self.dut.iBrTrue
        self.iIF_ID = if_id_t(dut.iIF_ID)
        self.iID_EX = if_id_t(dut.iID_EX)
        self.iEX_ME = if_id_t(dut.iEX_ME)
        self.iME_WB = if_id_t(dut.iME_WB)
        self.iStall_dbg: ModifiableObject = self.dut.iStall_dbg
        self.iStall_IF: ModifiableObject = self.dut.iStall_IF
        self.iStall_ID: ModifiableObject = self.dut.iStall_ID
        self.iStall_EX: ModifiableObject = self.dut.iStall_EX
        self.iStall_ME: ModifiableObject = self.dut.iStall_ME
        self.oStall_IF: ModifiableObject = self.oStall_IF
        self.oStall_ID: ModifiableObject = self.oStall_ID
        self.oStall_EX: ModifiableObject = self.oStall_EX
        self.oStall_ME: ModifiableObject = self.oStall_ME
        self.oFwExS1_en: ModifiableObject = self.oFwExS1_en
        self.oFwExS2_en: ModifiableObject = self.oFwExS2_en
        self.oFwMeS1_en: ModifiableObject = self.oFwMeS1_en
        self.oFwMeS2_en: ModifiableObject = self.oFwMeS2_en
        self.oRst_IF: ModifiableObject = self.oRst_IF
        self.oRst_ID: ModifiableObject = self.oRst_ID
        self.oRst_EX: ModifiableObject = self.oRst_EX
        self.oRst_ME: ModifiableObject = self.oRst_ME

    async def setup(self):
        self.clock = Clock(self.iClk, 10, units='ns')
        self.nRst.value = 0
        cocotb.start_soon(self.clock.start())
        await RisingEdge(self.iClk)
        await RisingEdge(self.iClk)
        self.nRst.value = 1

    async def check_stall_dbg(self):
        pass

    async def check_stall_IF(self):
        pass

    async def check_stall_ME(self):
        pass

    async def check_stall_load_use(self):
        pass

    async def check_branch(self):
        pass

    async def check_forward(self):
        pass


@cocotb.test
async def check_stall_dbg(dut):
    hu = HazardUnit(dut)
    hu.check_stall_dbg()
    pass


@cocotb.test
async def check_stall_IF(dut):
    hu = HazardUnit(dut)
    hu.check_stall_IF()
    pass


@cocotb.test
async def check_stall_ME(dut):
    hu = HazardUnit(dut)
    hu.check_stall_ME()
    pass


@cocotb.test
async def check_stall_load_use(dut):
    hu = HazardUnit(dut)
    hu.check_stall_load_use()
    pass


@cocotb.test
async def check_branch(dut):
    hu = HazardUnit(dut)
    hu.check_branch()
    pass


@cocotb.test
async def check_forward(dut):
    hu = HazardUnit(dut)
    hu.check_forward()
    pass


def test_hazard_unit_runner():
    tb = testbench.TB("test_hazard_unit", "HazardUnit")
    tb.add_sources(ISA_SOURCES)
    tb.add_sources(TYPES_SOURCES)
    tb.add_source("control/HazardUnit.sv")
    tb.run_tests()


if __name__ == "__main__":
    test_hazard_unit_runner()
