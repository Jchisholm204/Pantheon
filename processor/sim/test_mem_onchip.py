import cocotb
import os
import random
from cocotb.triggers import Timer, FallingEdge, RisingEdge
from cocotb.clock import Clock
from cocotb.runner import get_runner
from pathlib import Path
import rv32_isa
from testbench import TB


async def onchipMem_setup(dut, iReadnWrite=None, iEn=1):
    clock = Clock(dut.iClk, 10, units="ns")
    cocotb.start_soon(clock.start())
    await RisingEdge(dut.iClk)
    if iReadnWrite is not None:
        dut.iReadnWrite.value = iReadnWrite
    if iEn is not None:
        dut.iEn.value = iEn


# @cocotb.test
# async def onchipMem_rw(dut):
#     # Setup chip and attempt to write to an address
#     await onchipMem_setup(dut, 0, 1)
#     dut.iAddr.value = 1
#     randval = random.getrandbits(32)
#     dut.iData.value = randval
#     # Wait for the data to latch, Check it
#     await RisingEdge(dut.iClk)
#     read = dut.oData.value.integer
#     assert read == randval, \
#         f'Failed RW test, {read} =/= {randval}'
#
#
# async def onchipMem_rwmulti(dut):
#     # Setup chip and attempt to write to an address
#     await onchipMem_setup(dut, 0, 1)
#     for i in range(0, 4096):
#         dut.iAddr.value = i
#         random.seed(231485261*i)
#         randval = random.getrandbits(32)
#         dut.iData.value = randval
#         # Wait for the data to latch, Check it
#         await RisingEdge(dut.iClk)
#         read = dut.oData.value.integer
#         assert read == randval, \
#             f'Failed RW test, {read} =/= {randval}'


# def test_onchipMem_runner():
#     tb = TB("test_mem_onchip", "MEM")
#     tb.add_source("rv32_isa.sv")
#     tb.add_source("MEM.sv")
#     tb.run_tests()
#
#
# if __name__ == "main":
#     test_onchipMem_runner()
