`timescale 1ms/1ps

// Default clock speed = 50Mhz (DE2 CCO)
module testClock#(
    parameter int ClockFrequency = 50e6
) (
    nRst,
    oClk
);

// Taken From VHDL Whiz
parameter int ClockPeriod = 1000/ClockFrequency;

// Explicit declaration of inputs as wires (inputs are implictly wires)
input  wire nRst;
output wire oClk;

// Declaration of Clk register
reg  Clk = 1'b0;

// Assign block must be used to assert registers into wires
assign oClk = Clk & nRst; // Ensure output clock is low on reset (active low reset)

// Run Clk on rising edge of reset
always begin
    // while (nRst == 1'b1) begin // While reset is not enabled (active low)
        #(ClockPeriod/2); // Simulation Delay (not synthesizable)
        // assign Clk to oposite of Clk // Ensure Clk is low on reset (active low)
        Clk = ~Clk & nRst;
    // end
end

endmodule
