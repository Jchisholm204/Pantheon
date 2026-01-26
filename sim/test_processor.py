import cocotb
import util.testbench as testbench
from util.sources import Sources
from cocotb.handle import ModifiableObject, NonHierarchyIndexableObject
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.clock import Clock
from incl.reg_transport_t import reg_transport_t
from util.hex_creator import HexCreator
from util.representation import to_signed32
from rv32_isa import *


class Processor():
    def __init__(self, dut):
        self.dut = dut
        self.iClk: ModifiableObject = self.dut.iClk
        self.nRst: ModifiableObject = self.dut.nRst
        self.iIM_data: ModifiableObject = self.dut.iIM_data
        self.iIM_rdy: ModifiableObject = self.dut.iIM_rdy
        self.oIM_addr: ModifiableObject = self.dut.oIM_addr
        self.oIM_rd: ModifiableObject = self.dut.oIM_rd
        self.rf: NonHierarchyIndexableObject = self.dut.rf.reg_outs
        self._setup = False
        self.rom: HexCreator = None

    async def _ins_mem(self, stall_cycles=0):
        while True:
            if self.rom is None:
                await RisingEdge(self.iClk)
                continue
            self.iIM_rdy.value = 0
            addr = self.oIM_addr.value.integer
            if addr % 4 != 0:
                assert False, f"Addr {addr} not divisible by 4"
            addr = addr / 4
            if addr < 0:
                assert False, f"Addr {addr} was negative!"
            if addr >= len(self.rom.get_ins()):
                self.iIM_data.value = 0
                self.iIM_rdy.value = 1
            else:
                self.iIM_data.value = self.rom.get_ins()[int(addr)]
                self.iIM_rdy.value = 1
            await RisingEdge(self.iClk)
            self.iIM_rdy.value = 0
            for _ in range(0, stall_cycles):
                await RisingEdge(self.iClk)

    async def setup(self, mem: HexCreator = None):
        self.clock = Clock(self.iClk, 10, units='ns')
        self.nRst.value = 0
        self.rom = mem
        cocotb.start_soon(self.clock.start())
        cocotb.start_soon(self._ins_mem())
        await RisingEdge(self.iClk)
        await RisingEdge(self.iClk)
        self.nRst.value = 1
        self._setup = True

    async def wait(self, time=0, units='ns'):
        if time == 0:
            await RisingEdge(self.iClk)
        else:
            await Timer(time, units=units)

    async def run_test(self, rom: HexCreator = None):
        if self._setup is False:
            await self.setup()
        if self.rom is None:
            self.rom = rom
        if self.rom is None:
            return
        await RisingEdge(self.iClk)
        for ins in self.rom.get_ins():
            await RisingEdge(self.iClk)

# For debugging purposes only.. not actual testing


# @cocotb.test
# async def proc_dbg(dut):
#     return
#     proc = Processor(dut)
#     hc = HexCreator()
#     hc.add_Iins(OpAluI, 1, OpF3ADD, 0, 15)
#     hc.add_Iins(OpAluI, 2, OpF3ADD, 1, 10)
#     # hc.add_Iins(OpAluI, 0, OpF3ADD, 0, 0)
#     # hc.add_Iins(OpAluI, 0, OpF3ADD, 0, 0)
#     # hc.add_Iins(OpAluI, 0, OpF3ADD, 0, 0)
#     hc.add_Rins(OpAluR, 3, OpF3SUB, 1, 2, OpF7SUB)
#     # hc.add_Iins(OpAluI, 0, OpF3ADD, 0, 0)
#     await proc.run_test(hc)
#     print("dut.rf")
#     print(type(dut.rf.reg_outs))
#     print(dut.rf.reg_outs[1].value.integer)
#     assert proc.rf[1].value == 15, "Fail Load R1"
#     assert proc.rf[2].value == 25, "Fail Addi R2"
#     assert to_signed32(proc.rf[3].value) == -10, "Fail Sub R3=R1-R2"
#     pass


@cocotb.test
async def proc_addi_sub(dut):
    proc = Processor(dut)
    hc = HexCreator()
    hc.add_Iins(OpAluI, 0, OpF3ADD, 0, 0)
    hc.add_Iins(OpAluI, 1, OpF3ADD, 0, 15)
    hc.add_Iins(OpAluI, 2, OpF3ADD, 1, 10)
    hc.add_Rins(OpAluR, 3, OpF3SUB, 1, 2, OpF7SUB)
    hc.add_Iins(OpAluI, 0, OpF3ADD, 0, 0)
    hc.add_Iins(OpAluI, 0, OpF3ADD, 0, 0)
    hc.add_Iins(OpAluI, 0, OpF3ADD, 0, 0)
    hc.add_Iins(OpAluI, 0, OpF3ADD, 0, 0)
    await proc.run_test(hc)
    print("dut.rf")
    print(type(dut.rf.reg_outs))
    print(dut.rf.reg_outs[1].value.integer)
    assert proc.rf[1].value == 15, "Fail Load R1"
    assert proc.rf[2].value == 25, "Fail Addi R2"
    assert to_signed32(proc.rf[3].value) == -10, "Fail Sub R3=R1-R2"
    pass


# @cocotb.test
# async def proc_load_store_word(dut):
#     proc = Processor(dut)
#     hc = HexCreator()
#     tval: int = 0x3CF
#     shampt: int = 12
#     hc.add_Iins(OpAluI, 1, OpF3ADD, 0, tval)
#     # Shift the test value to be larger than a hw
#     hc.add_Iins(OpAluI, 1, OpF3SLL, 1, shampt)
#     tval = tval << shampt
#     # Store the test value
#     hc.add_Sins(OpStore, OpF3SW, 0, 1, 10)
#
#     hc.add_Iins(OpLoad, 2, OpF3LW, 0, 10)
#     await proc.run_test(hc)
#     assert proc.rf[1].value.integer == tval, "Fail Addi R1"
#     assert proc.rf[2].value.integer == tval, "Fail Load Word R2"
#     pass


# @cocotb.test
# async def proc_load_store_hw(dut):
#     proc = Processor(dut)
#     hc = HexCreator()
#     tval = 0x3CF
#     hc.add_Iins(OpAluI, 1, OpF3ADD, 0, tval)
#     hc.add_Sins(OpStore, OpF3SW, 0, 1, 10)
#     hc.add_Iins(OpLoad, 2, OpF3LW, 0, 10)
#     await proc.run_test(hc)
#     assert proc.rf[1].value == tval, "Fail Addi R1"
#     assert proc.rf[2].value == tval, "Fail Load Word R2"
#     pass


# @cocotb.test
# async def proc_branch(dut):
#     proc = Processor(dut)
#     hc = HexCreator()
#     hc.add_Iins(OpAluI, 1, OpF3ADD, 0, 15)
#     hc.add_Sins(OpStore, OpF3SW, 0, 1, 10)
#     hc.add_Iins(OpLoad, 2, OpF3LW, 0, 10)
#     await proc.run_test(hc)
#     print("dut.rf")
#     print(type(dut.rf.reg_outs))
#     print(dut.rf.reg_outs[1].value.integer)
#     assert proc.rf[1].value == 15, "Fail Addi R1"
#     assert proc.rf[2].value == 15, "Fail Load R2"
#     pass


def test_processor_runner():
    tb = testbench.TB("test_processor", "Processor")
    tb.add_define("RF_TOP", 1)
    # for x in Sources.CTRL:
    #     print(x)
    tb.add_sources(Sources.ISA())
    tb.add_sources(Sources.INTERFACES())
    tb.add_sources(Sources.TYPES())
    tb.add_sources(Sources.PROC())
    for s in tb.sources:
        print(s)
    tb.run_tests()


if __name__ == "__main__":
    test_processor_runner()
