/**
 * @file PC.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief Program Counter Module
 * @version 0.1
 * @date Created: 2025-05-31
 * @modified Last Modified: 2025-05-31
 *
 * @copyright Copyright (c) 2025
 */
`timescale 1ns/100ps
module PC(
    iClk, nRst, iStall,
    iPC, iEXT_S,
    oPC, oPC4
);

input wire iClk, nRst, iStall;
input wire [31:0] iPC;
input wire iEXT_S;
output logic [31:0] oPC, oPC4;

// Unused wires for CLA
wire unused_neg, unused_overflow, unused_carry, unused_zero;

CLA pc_adder(
    .iX(32'd4),
    .iY(oPC),
    .iCarry(1'b0),
    .oS(oPC4),
    .oNegative(unused_neg),
    .oOverflow(unused_overflow), 
    .oCarry(unused_carry), 
    .oZero(unused_zero)
);

always_ff @(posedge iClk, negedge nRst) begin
    // Active Low Reset Signal
    if(!nRst) begin
        oPC <= 32'd0;
    end else begin
        // PC External Load Select (Stall is active high)
        if(!iStall) oPC <= iEXT_S ? iPC : oPC4;
    end
end

endmodule
