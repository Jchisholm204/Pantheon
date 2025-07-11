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
        self.iID_EX = id_ex_t(dut.iID_EX)
        self.iEX_ME = ex_mem_t(dut.iEX_ME)
        self.iME_WB = mem_wb_t(dut.iME_WB)
        self.iStall_dbg: ModifiableObject = self.dut.iStall_dbg
        self.iStall_IF: ModifiableObject = self.dut.iStall_IF
        self.iStall_ME: ModifiableObject = self.dut.iStall_ME
        self.oStall_IF: ModifiableObject = self.dut.oStall_IF
        self.oStall_ID: ModifiableObject = self.dut.oStall_ID
        self.oStall_EX: ModifiableObject = self.dut.oStall_EX
        self.oStall_ME: ModifiableObject = self.dut.oStall_ME
        self.oFwExS1_en: ModifiableObject = self.dut.oFwExS1_en
        self.oFwExS2_en: ModifiableObject = self.dut.oFwExS2_en
        self.oFwMeS1_en: ModifiableObject = self.dut.oFwMeS1_en
        self.oFwMeS2_en: ModifiableObject = self.dut.oFwMeS2_en
        self.oRst_IF: ModifiableObject = self.dut.oRst_IF
        self.oRst_ID: ModifiableObject = self.dut.oRst_ID
        self.oRst_EX: ModifiableObject = self.dut.oRst_EX
        self.oRst_ME: ModifiableObject = self.dut.oRst_ME

    async def setup(self):
        self.clock = Clock(self.iClk, 10, units='ns')
        self.nRst.value = 0
        cocotb.start_soon(self.clock.start())
        await RisingEdge(self.iClk)
        await RisingEdge(self.iClk)
        self.nRst.value = 1

    async def check_stall_dbg(self):
        if self.iStall_dbg.value == 1:
            assert self.oStall_IF == 1, "HU DBG Stall Fail, oStall_IF"
            assert self.oStall_ID == 1, "HU DBG Stall Fail, oStall_ID"
            assert self.oStall_EX == 1, "HU DBG Stall Fail, oStall_EX"
            assert self.oStall_ME == 1, "HU DBG Stall Fail, oStall_ME"
        pass

    async def check_stall_IF(self):
        if self.iStall_IF.value == 1:
            assert self.oStall_IF == 1, "HU iIF Stall Fail, oStall_IF"
            assert self.oStall_ID == 1, "HU iIF Stall Fail, oStall_ID"
            assert self.oStall_EX == 1, "HU iIF Stall Fail, oStall_EX"
            assert self.oStall_ME == 1, "HU iIF Stall Fail, oStall_ME"
        pass

    async def check_stall_ME(self):
        if self.iStall_ME.value == 1:
            assert self.oStall_IF == 1, "HU iME Stall Fail, oStall_IF"
            assert self.oStall_ID == 1, "HU iME Stall Fail, oStall_ID"
            assert self.oStall_EX == 1, "HU iME Stall Fail, oStall_EX"
            assert self.oStall_ME == 1, "HU iME Stall Fail, oStall_ME"
        pass

    async def check_stall_load_use(self, check_me_stall=False):
        stall_s1 = (self.iID_EX.rs1.addr == self.iEX_ME.rd.addr)
        stall_s2 = (self.iID_EX.rs2.addr == self.iEX_ME.rd.addr)
        if stall_s1 | stall_s2:
            assert self.oStall_IF == 1, "HU LU Stall Fail, oStall_IF"
            assert self.oStall_ID == 1, "HU LU Stall Fail, oStall_ID"
            assert self.oStall_EX == 1, "HU LU Stall Fail, oStall_EX"
            if check_me_stall:
                assert self.oStall_ME == 0, "HU LU Stall Fail, oStall_ME"
        pass

    async def check_branch(self):
        if self.iBrTrue.value == 1:
            assert self.oRst_IF.value == 1, "HU Branch IF Reset Fail"
        pass

    async def check_forward(self):
        if self.iID_EX.rs1.addr == self.iEX_ME.rd.addr:
            if self.iID_EX.rs1 != 0 & self.iEX_ME.ctrl.ex_en:
                assert self.oFwExS1_en.value == 1, "HU FW Fail, oFwExS1_en"
        if self.iID_EX.rs2.addr == self.iEX_ME.rd.addr:
            if self.iID_EX.rs2 != 0 & self.iEX_ME.ctrl.ex_en:
                assert self.oFwExS2_en.value == 1, "HU FW Fail, oFwExS2_en"
        if self.iID_EX.rs1.addr == self.iME_WB.rd.addr:
            if self.iID_EX.rs1 != 0 & self.iME_WB.ctrl.mem_en:
                assert self.oFwMeS1_en.value == 1, "HU FW Fail, oFwMeS1_en"
        if self.iID_EX.rs2.addr == self.iME_WB.rd.addr:
            if self.iID_EX.rs2 != 0 & self.iME_WB.ctrl.mem_en:
                assert self.oFwMeS2_en.value == 1, "HU FW Fail, oFwMeS2_en"
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
