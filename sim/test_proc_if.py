import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.clock import Clock
import util.testbench as testbench
from util.hex_creator import HexCreator
from rv32_isa import *
from cocotb.handle import ModifiableObject
from incl.pipeline_types import if_id_t
from util.sources import Sources


class IF():
    def __init__(self, dut):
        self.dut = dut
        self.iClk: ModifiableObject = self.dut.iClk
        self.nRst: ModifiableObject = self.dut.nRst
        self.iFlush: ModifiableObject = self.dut.iFlush
        self.iStall: ModifiableObject = self.dut.iStall
        self.iPCS_EXT: ModifiableObject = self.dut.iPCS_EXT
        self.iPC_EXT: ModifiableObject = self.dut.iPC_EXT
        self.iIM_data: ModifiableObject = self.dut.iIM_data
        self.iIM_rdy: ModifiableObject = self.dut.iIM_rdy
        self.oIM_addr: ModifiableObject = self.dut.oIM_addr
        self.oIM_rd: ModifiableObject = self.dut.oIM_rd
        self.oID = if_id_t(self.dut.oID)
        self.rom: HexCreator = None

    async def ins_mem(self, stall_cycles=0):
        while True:
            if self.rom is None:
                await RisingEdge(self.iClk)
                continue

            await RisingEdge(self.iClk)
            self.iIM_rdy.value = 0
            for _ in range(0, stall_cycles):
                await RisingEdge(self.iClk)
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

    async def setup(self, rom: HexCreator, mem_stall_cycles=0):
        self.clock = Clock(self.iClk, 10, units='ns')
        self.nRst.value = 0
        self.rom = rom
        cocotb.start_soon(self.clock.start())
        cocotb.start_soon(self.ins_mem(mem_stall_cycles))
        await RisingEdge(self.iClk)
        self.nRst.value = 1
        self.iFlush.value = 0
        self.iStall.value = 0
        self.iPCS_EXT.value = 0
        self.iIM_rdy.value = 0


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


@cocotb.test()
async def if_memread(dut):
    mem = HexCreator()
    # Clear R1
    mem.add_Iins(OpAluI, 1, OpF3ADD, 0, 0)
    # Calculate summation of all values between 0 and 5
    for i in range(1, 6):
        mem.add_Iins(OpAluI, 1, OpF3ADD, 1, i)
    dut = IF(dut)
    await dut.setup(mem)
    # Attempt to loop through the sample instructions
    for i, ins in enumerate(mem.instructions):
        await RisingEdge(dut.iClk)
        oins = int(if_id_t(dut.oID).instruction)
        # If a NOP (0x13) is present, and is not the current instruction,
        # it is a pipeline stall inserted by the memory read not being ready
        while oins == 0x13 and oins != ins:
            await RisingEdge(dut.iClk)
            oins = int(if_id_t(dut.oID).instruction)
        assert oins == ins, f"INS Assert Failed {i}"
        assert dut.oID.pc == i*4, "Incorrect INS Returned"
        assert dut.oID.pc4 == (i+1)*4, "Incorrect INS Returned"
    pass


@cocotb.test()
async def if_branch(dut):
    mem = HexCreator()
    # Clear R1
    mem.add_Iins(OpAluI, 1, OpF3ADD, 0, 0)
    # Calculate summation of all values between 0 and 5
    for i in range(1, 6):
        mem.add_Iins(OpAluI, 1, OpF3ADD, 1, i)
    dut = IF(dut)
    await dut.setup(mem)
    oins = int(dut.oID.instruction)
    # If a NOP (0x13) is present, and is not the current instruction,
    # it is a pipeline stall inserted by the memory read not being ready
    while oins == 0x13:
        await RisingEdge(dut.iClk)
        oins = int(dut.oID.instruction)

    # Run test
    assert dut.oID.pc == 0, "PC 0 Failed"
    assert dut.oID.pc4 == 4, "PC4 0 Failed"
    await RisingEdge(dut.iClk)
    assert dut.oID.pc == 4, "PC 4 Failed"
    assert dut.oID.pc4 == 8, "PC4 4 Failed"
    # Assert the jump/pc external load signal
    dut.iPCS_EXT.value = 1
    dut.iPC_EXT.value = 0xC4
    await RisingEdge(dut.iClk)
    # PCS appears to the processor in this cycle
    # assert dut.oID.pc == 4, "PC Inc Failed"
    # Reset the external load signals
    dut.iPCS_EXT.value = 0
    dut.iPC_EXT.value = 0x00
    await RisingEdge(dut.iClk)
    # External load signals are disabled
    # PCS is loaded into the PC
    # Pipeline contains penalty ins
    # assert dut.oID.pc == 8, "PC Inc Failed"
    # Insert a nop to avoid a flush
    # assert dut.oID.instruction == 0x13, "Penalty INS Not Loaded"
    await RisingEdge(dut.iClk)
    # Ensure the external load appears in the pipeline
    # assert dut.oID.pc == 0xC4, "PC Jmp Failed"
    await RisingEdge(dut.iClk)
    # assert dut.oID.pc == 0xC8, "PC Jmp Inc Fail"
    await RisingEdge(dut.iClk)
    # assert dut.oID.pc == 0xCC, "PC Jmp Inc Fail"
    pass


# @cocotb.test()
# async def if_stall(dut):
#     mem = HexCreator()
#     # Clear R1
#     mem.add_Iins(OpAluI, 1, OpF3ADD, 0, 0)
#     # Calculate summation of all values between 0 and 5
#     for i in range(0, 5):
#         mem.add_Iins(OpAluI, 1, OpF3ADD, 1, i)
#     dut = IF(dut)
#     await dut.setup(mem)
#     await RisingEdge(dut.iClk)
#     await RisingEdge(dut.iClk)
#     assert dut.oID.pc == 0, "PC 0 Failed"
#     # Assert the stall signal
#     dut.iStall.value = 1
#     await RisingEdge(dut.iClk)
#     # stall signal appears in PC
#     assert dut.oID.pc == 4, "PC 4 Failed"
#     await RisingEdge(dut.iClk)
#     # PC + 4 appears in pipe with stall ins
#     assert dut.oID.pc == 8, "PC 8 Failed"
#     assert dut.oID.instruction == 0x13, "Stall Failed"
#     await RisingEdge(dut.iClk)
#     # PC should not advance
#     assert dut.oID.pc == 8, "PC 8 Failed"
#     assert dut.oID.instruction == 0x13, "Stall Failed"
#     # Undo Stall Signal
#     dut.iStall.value = 0
#     await RisingEdge(dut.iClk)
#     # Continue signal appears
#     # PC should still not advance
#     assert dut.oID.pc == 8, "PC 8 Failed"
#     assert dut.oID.instruction == 0x13, "Stall Failed"
#     await RisingEdge(dut.iClk)
#     # Expect that the instruction from 8 will not be loaded into the pipeline
#     assert dut.oID.pc == 8, "PC Reload Failed"
#     assert dut.oID.instruction == mem.get_ins()[2], "INS Fetch Fail"
#     await RisingEdge(dut.iClk)
#     pass
#
#
# @cocotb.test()
# async def if_mem_stall(dut):
#     mem = HexCreator()
#     # Clear R1
#     mem.add_Iins(OpAluI, 1, OpF3ADD, 0, 0)
#     # Calculate summation of all values between 0 and 5
#     for i in range(0, 5):
#         mem.add_Iins(OpAluI, 1, OpF3ADD, 1, i)
#     dut = IF(dut)
#     # Setup memory with two stall cycles
#     await dut.setup(mem, 2)
#     await RisingEdge(dut.iClk)
#     await RisingEdge(dut.iClk)
#     # Start the test
#     assert dut.oID.pc == 0, "PC 0 Failed"
#     # Wait for memory stall to expire
#     while dut.oID.instruction == 0x13:
#         await RisingEdge(dut.iClk)
#     assert dut.oID.instruction == mem.get_ins()[0], "Ins 0 Failed"
#     await RisingEdge(dut.iClk)
#     assert dut.oID.pc == 4, "PC 4 Failed"
#     # Wait for memory stall to expire
#     while dut.oID.instruction == 0x13:
#         await RisingEdge(dut.iClk)
#     assert dut.oID.instruction == mem.get_ins()[1], "Ins 1 Failed"
#     await RisingEdge(dut.iClk)
#     pass
