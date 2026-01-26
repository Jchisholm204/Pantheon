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
        self.iIM_rdy.value = 0
        await RisingEdge(self.iClk)
        await RisingEdge(self.iClk)
        while True:
            if self.rom is None:
                await RisingEdge(self.iClk)
                continue

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
            await RisingEdge(self.iClk)

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
    await RisingEdge(dut.iClk)
    # Attempt to loop through the sample instructions
    for i, ins in enumerate(mem.instructions):
        await RisingEdge(dut.iClk)
        while dut.oID.valid == 0:
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
    # Calculate summation of all values
    # This is mostly non-random instruction memory fill
    for i in range(1, 30):
        mem.add_Iins(OpAluI, 1, OpF3ADD, 1, i)
    dut = IF(dut)
    await dut.setup(mem)

    # Wait for IF to issue a valid instruction
    while dut.oID.valid == 0:
        await RisingEdge(dut.iClk)

    # Run through a few instructions
    for i in range(0, 2):
        # Assert the ins issued = instruction mem
        assert dut.oID.pc == i*4, f"PC {i} Failed"
        assert dut.oID.pc4 == (i+1)*4, f"PC4 {i} Failed"
        assert dut.oID.valid == 1, f"Ins {i} Not Valid"
        assert dut.oID.instruction == mem.get_ins()[i], "Ins 0 Incorrect Issue"

        # Wait for IF to issue next valid instruction
        await RisingEdge(dut.iClk)

    # Inject a branch instruction
    dut.iPCS_EXT.value = 1
    dut.iPC_EXT.value = 0x20
    await RisingEdge(dut.iClk)
    # Assert the "branch" instruction is in IF/ID
    assert dut.oID.pc == 0xC, "PC 3 Failed"
    assert dut.oID.pc4 == 0x10, "PC4 3 Failed"
    assert dut.oID.valid == 1, "Ins 3 Not Valid"
    assert dut.oID.instruction == mem.get_ins()[3], "Ins 3 Incorrect Issue"
    # IF now loading the new control path
    assert dut.oIM_addr == 0x20, "Jmp Fetch Fail"
    # Reset the external load signals for next cycle
    dut.iPCS_EXT.value = 0
    dut.iPC_EXT.value = 0x00
    await RisingEdge(dut.iClk)
    # Processor is now stalled
    assert dut.oID.valid == 0, "Jmp Stall Fail"
    assert dut.oID.instruction == 0x13, "Jmp Stall Not NOP"
    await RisingEdge(dut.iClk)
    # Run through a few instructions
    for j in range(0, 2):
        i = j + 8
        # Assert the ins issued = instruction mem
        assert dut.oID.pc == i*4, f"PC {i} Failed"
        assert dut.oID.pc4 == (i+1)*4, f"PC4 {i} Failed"
        assert dut.oID.valid == 1, f"Ins {i} Not Valid"
        assert dut.oID.instruction == mem.get_ins()[i], "Ins 0 Incorrect Issue"

        # Wait for IF to issue next valid instruction
        await RisingEdge(dut.iClk)
    await RisingEdge(dut.iClk)
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
#     # Processor will stall on this instruction
#     assert dut.oID.pc == 4, "PC 4 Failed"
#     await RisingEdge(dut.iClk)
#     # Processor is stalled on the 2nd instruction
#     assert dut.oID.pc == 4, "PC Stall Failed"
#     assert dut.oID.instruction == 0x13, "Ins Stall Failed"
#     assert dut.oID.valid == 0, "Stall INS not invalid"
#     await RisingEdge(dut.iClk)
#     # Processor is stalled on the 2nd instruction
#     assert dut.oID.pc == 4, "PC Stall Failed"
#     assert dut.oID.instruction == 0x13, "Ins Stall Failed"
#     assert dut.oID.valid == 0, "Stall INS not invalid"
#     await RisingEdge(dut.iClk)
#     # Processor is stalled on the 2nd instruction
#     assert dut.oID.pc == 4, "PC Stall Failed"
#     assert dut.oID.instruction == 0x13, "Ins Stall Failed"
#     assert dut.oID.valid == 0, "Stall INS not invalid"
#     # Undo Stall Signal
#     dut.iStall.value = 0
#     await RisingEdge(dut.iClk)
#     # Continue signal appears
#     # Processor sends out the next instruction
#     assert dut.oID.pc == 4, "PC Resume Failed"
#     assert dut.oID.valid == 1, "Valid Resume Fail"
#     assert dut.oID.instruction == mem.get_ins()[1], "INS Fetch Fail"
#     await RisingEdge(dut.iClk)
#     assert dut.oID.pc == 8, "PC Increment Failed"
#     assert dut.oID.instruction == mem.get_ins()[2], "INS Fetch Fail"
#     assert dut.oID.valid == 1, "Valid Resume Fail"
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
