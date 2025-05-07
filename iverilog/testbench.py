import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


@cocotb.test()
async def basic_count(dut):
    # Generate a clock
    cocotb.start_soon(Clock(dut.clk, 1, units="ns").start())
    # Reset the DUT
    dut.reset.value = 1
    # Wait for two rising edges
    for _ in range(2):
        await RisingEdge(dut.clk)

    dut.reset.value = 0

    for cnt in range(50):
        await RisingEdge(dut.clk)
        v_count = dut.count.value
        mod_count = cnt % 16
        assert v_count.integer == mod_count, "Counter result is incorrect"
