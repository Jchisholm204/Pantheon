import cocotb
import os
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.runner import get_runner
from pathlib import Path


async def setup_test(dut):
    # Start clock: 10ns period
    clock = Clock(dut.iClk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset the DUT
    dut.nRst.value = 0
    dut.iWriteEn.value = 0
    await RisingEdge(dut.iClk)
    await RisingEdge(dut.iClk)
    dut.nRst.value = 1
    await RisingEdge(dut.iClk)


@cocotb.test()
async def regfile_write_read_test(dut):
    """Test writing and reading the register file"""
    await setup_test(dut)

    # Write unique values to each register
    for addr in range(1, 31):
        dut.iWriteEn.value = 1
        dut.iAddr_Rd.value = addr
        dut.iRd.value = addr + 0x2A0  # example data pattern
        await RisingEdge(dut.iClk)

    # Disable write enable to test read-only
    dut.iWriteEn.value = 0

    # Read back and check (Reg 1)
    for addr in range(1, 31):
        dut.iAddr_Rs1.value = addr
        dut.iAddr_Rs2.value = 0
        await RisingEdge(dut.iClk)

        data1 = dut.oRs1.value.integer
        data2 = dut.oRs2.value.integer

        assert data1 == addr + 0x2A0, \
            f"Read port 1 mismatch at addr {addr}: \
            expected {addr+0x2A0}, got {data1}"

        assert data2 == 0x000, \
            f"Read port 1 mismatch at addr {addr}: \
            expected {0}, got {data2}"

    # Read back and check (Reg 2)
    for addr in range(1, 31):
        dut.iAddr_Rs1.value = 0
        dut.iAddr_Rs2.value = addr
        await RisingEdge(dut.iClk)

        data1 = dut.oRs1.value.integer
        data2 = dut.oRs2.value.integer

        assert data1 == 0, \
            f"Read port 1 mismatch at addr {addr}: \
            expected {0}, got {data1}"

        assert data2 == 0x2A0 + addr, \
            f"Read port 1 mismatch at addr {addr}: \
            expected {0x2A0 + addr}, got {data2}"

    dut._log.info("Register file write/read test passed!")


@cocotb.test()
async def regfile_test_r0(dut):
    await setup_test(dut)
    # Read from r0
    dut.iAddr_Rs1.value = 0
    dut.iAddr_Rs2.value = 0
    await RisingEdge(dut.iClk)
    data = dut.oRs1.value.integer
    assert data == 0, "Failed to read 0 from R0"
    # Attempt to write to R0 (Should Fail)
    dut.iWriteEn.value = 1
    dut.iAddr_Rd.value = 0
    dut.iRd.value = 0xF0F0F0F0
    await RisingEdge(dut.iClk)
    await RisingEdge(dut.iClk)
    data = dut.oRs1.value.integer
    assert data == 0, "R0 was not 0 after write"
    data = dut.oRs2.value.integer
    assert data == 0, "R0 was not 0 after write"
    dut._log.info("R0 Passed Tests")


@cocotb.test()
async def regfile_test_forwarding(dut):
    await setup_test(dut)

    await FallingEdge(dut.iClk)
    for reg in range(1, 31):
        testVal = reg * 0x1111  # unique value per reg
        dut.iWriteEn.value = 1
        dut.iAddr_Rd.value = reg
        dut.iAddr_Rs1.value = reg
        dut.iRd.value = testVal

        await RisingEdge(dut.iClk)  # write happens on posedge
        dut.iWriteEn.value = 0     # disable write after posedge

        # wait for output to update on negedge
        await FallingEdge(dut.iClk)

        regVal = dut.oRs1.value.integer
        assert regVal == testVal, \
            f"Failed Forward Write on Reg {reg}, expected {testVal:#x}, got {regVal:#x}"


def test_register_file_runner():
    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent.parent

    # sources = [proj_path / "register_file.sv",
    #            proj_path / "rv32_isa.sv"]
    sources = list((proj_path).glob("*.sv"))

    runner = get_runner(sim)
    runner.build(
            verilog_sources=sources,
            hdl_toplevel="register_file",
            clean=False,
            waves=True,
            always=True,
            build_args=["-DICARUS_TRACE_ARRAYS", "-DICARUS_FST"]
            )
    runner.test(
            hdl_toplevel="register_file",
            test_module="test_register_file",
            plusargs=["-fst"],
            waves=True
            )


if __name__ == "__main__":
    test_register_file_runner()
