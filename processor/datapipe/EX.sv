/**
 * @file EX.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief 
 * @version 0.2
 * @date Created: 2025-06-21
 * @modified Last Modified: 2025-06-22
 *
 * @copyright Copyright (c) 2025
 */

`timescale 1ns/100ps

import rv32_isa::*;
import pipeline_types::id_ex_t;
import pipeline_types::ex_mem_t;

module EX(
    input logic iClk, nRst,
    input logic iStall, iFlush,
    input id_ex_t iID,
    output ex_mem_t oMEM,
    input logic iFwExS1_en,
    input logic iFwExS2_en,
    input logic iFwMeS1_en,
    input logic iFwMeS2_en,
    input logic [RegWidth-1:0] iFwMe
);

logic [RegWidth-1:0] ALU_A, ALU_B, ALU_Z;
logic [RegWidth-1:0] EX_A, EX_B;

logic [6:0] ALU_F7;
logic [2:0] ALU_F3;

ALU alu(
    .iA(ALU_A),
    .iB(ALU_B),
    .iFunc3(ALU_F3),
    .iFunc7(ALU_F7),
    .oZ(ALU_Z)
);

always_comb begin
    if(iFwMeS1_en)
        EX_A = iFwMe;
    else if(iFwExS1_en)
        EX_A = oMEM.rd.value;
    else
        EX_A = iID.rs1.value;

    if(iFwMeS2_en)
        EX_B = iFwMe;
    else if(iFwExS2_en)
        EX_B = oMEM.rd.value;
    else
        EX_B = iID.rs2.value;

    ALU_A = EX_A;
    if(iID.ctrl.imm_en)
        ALU_B = iID.immediate;
    else
        ALU_B = EX_B;

    if(iID.ctrl.ex_en && iID.ctrl.valid) begin
        ALU_F7 = iID.ctrl.func7;
        ALU_F3 = iID.ctrl.func3;
    end else begin
        ALU_F7 = 7'd0;
        ALU_F3 = 3'd0;
    end

end

always_ff @(posedge iClk, negedge nRst) begin
    if(!nRst | iFlush)
        oMEM = '0;
    else if(!iStall) begin
        oMEM.ctrl = iID.ctrl;
        oMEM.rs.addr = iID.rs2.addr;
        oMEM.rs.value = EX_B;
        oMEM.rd.addr = iID.rd_addr;
        oMEM.rd.value = ALU_Z;
    end
end

endmodule

