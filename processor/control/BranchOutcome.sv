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
import rv32_isa::OpF3BEQ;
import rv32_isa::OpF3BNE;
import rv32_isa::OpF3BLT;
import rv32_isa::OpF3BGE;
import rv32_isa::OpF3BLTU;
import rv32_isa::OpF3BGEU;

module BranchOutcome(
    input logic signed [RegWidth-1:0] iRs1, iRs2,
    input logic [2:0] iFunc3,
    output logic oBrTrue
);

logic f3_BEQ, f3_BNE, f3_BLT, f3_BGE, f3_BLTU, f3_BGEU;
logic cond_BEQ, cond_BNE, cond_BLT, cond_BGE, cond_BLTU, cond_BGEU;

// Unsigned Logic for unsigned branch conditionals
logic unsigned [RegWidth-1:0] Rs1U, Rs2U;

// Signed Branch Conditions
assign cond_BEQ = iRs1 == iRs2;
assign cond_BNE = ~cond_BEQ;
assign cond_BLT = iRs1 < iRs2;
assign cond_BGE = ~cond_BLT;

// Unsigned branch Conditions
assign cond_BLTU = Rs1U < Rs2U;
assign cond_BGEU = ~cond_BLTU;

assign f3_BEQ  = iFunc3 == OpF3BEQ;
assign f3_BNE  = iFunc3 == OpF3BNE;
assign f3_BLT  = iFunc3 == OpF3BLT;
assign f3_BGE  = iFunc3 == OpF3BGE;
assign f3_BLTU = iFunc3 == OpF3BLTU;
assign f3_BGEU = iFunc3 == OpF3BGEU;

assign oBrTrue = (f3_BEQ  & cond_BEQ)  |
                 (f3_BNE  & cond_BNE)  |
                 (f3_BLT  & cond_BLT)  |
                 (f3_BGE  & cond_BGE)  |
                 (f3_BLTU & cond_BLTU) |
                 (f3_BGEU & cond_BGEU) ;

endmodule
