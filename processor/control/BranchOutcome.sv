/**
 * @file BranchOutcome.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief 
 * @version 0.1
 * @date Created: 2025-06-08
 * @modified Last Modified: 2025-06-08
 *
 * @copyright Copyright (c) 2025
 */
`timescale 1ns/100ps
import rv32_isa::RegWidth;
module BranchOutcome(
    iRs1, iRs2,
    oBEQ, oBNE, oBLT, oBGE,
    oBLTU, oBGEU
);
input logic signed [RegWidth-1:0] iRs1, iRs2;
output logic oBEQ, oBNE, oBLT, oBGE;
output logic oBLTU, oBGEU;

// Unsigned Logic for unsigned branch conditionals
logic unsigned [RegWidth-1:0] Rs1U, Rs2U;

// Signed Branch Conditions
assign oBEQ = iRs1 == iRs2;
assign oBNE = ~oBEQ;
assign oBLT = iRs1 < iRs2;
assign oBGE = ~oBLT;

// Unsigned branch Conditions
assign oBLTU = Rs1U < Rs2U;
assign oBGEU = ~oBLTU;

endmodule
