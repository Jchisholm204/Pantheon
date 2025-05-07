# test_vga_sync.py
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Edge, Timer, First
from cocotb.result import TestFailure


@cocotb.test()
async def test_vga_sync_pulses(dut):
    """Test VGA Controller HSync and VSync pulse widths and intervals."""

    # Start 50 MHz clock
    clk_50 = Clock(dut.iClk_50, 20, units="ns")  # 50 MHz -> 20 ns period
    cocotb.start_soon(clk_50.start())

    # Apply reset
    dut.nRst.value = 0
    for _ in range(5):
        await RisingEdge(dut.iClk_50)
    dut.nRst.value = 1
    for _ in range(5):
        await RisingEdge(dut.iClk_50)

    # Monitor HSync pulse widths and periods
    hsync_low_times = []
    hsync_periods = []

    prev_fall = None
    for _ in range(5):  # Capture 5 HSync pulses
        await FallingEdge(dut.oVGA_HSync)
        fall_time = cocotb.utils.get_sim_time(units="ns")
        await RisingEdge(dut.oVGA_HSync)
        rise_time = cocotb.utils.get_sim_time(units="ns")

        pulse_width = rise_time - fall_time
        hsync_low_times.append(pulse_width)

        if prev_fall is not None:
            period = fall_time - prev_fall
            hsync_periods.append(period)
        prev_fall = fall_time

    # Monitor VSync pulse widths and periods
    vsync_low_times = []
    vsync_periods = []

    prev_fall = None
    for _ in range(2):  # VSync happens once per frame, so just capture 2
        await FallingEdge(dut.oVGA_VSync)
        fall_time = cocotb.utils.get_sim_time(units="ns")
        await RisingEdge(dut.oVGA_VSync)
        rise_time = cocotb.utils.get_sim_time(units="ns")

        pulse_width = rise_time - fall_time
        vsync_low_times.append(pulse_width)

        if prev_fall is not None:
            period = fall_time - prev_fall
            vsync_periods.append(period)
        prev_fall = fall_time

    dut._log.info(f"HSync pulse widths (ns): {hsync_low_times}")
    dut._log.info(f"HSync periods (ns): {hsync_periods}")
    dut._log.info(f"VSync pulse widths (ns): {vsync_low_times}")
    dut._log.info(f"VSync periods (ns): {vsync_periods}")

    # Optional: Add assertions based on expected timing
    expected_hsync_pulse_ns = 96 * 40  # 96 Clk_25 cycles * 40 ns (25 MHz)
    expected_vsync_pulse_ns = 2 * 40_000  # 2 lines * 40 us (for 25 MHz)

    assert all(abs(p - expected_hsync_pulse_ns) < 100 for p in hsync_low_times), "HSync pulse width incorrect"
    assert all(p > expected_hsync_pulse_ns for p in hsync_periods), "HSync period too short"

    assert all(p >= expected_vsync_pulse_ns for p in vsync_low_times), "VSync pulse width incorrect"

