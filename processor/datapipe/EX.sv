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
import pipeline_types::ex_fw_t;

module EX(
    input logic iClk, iEn, nRst, iStall,
    input id_ex_t iID,
    input ex_fw_t iFW,
    output ex_mem_t oMEM,
    input logic iFwExS1_en,
    input logic iFwExS2_en,
    input logic iFwMeS1_en,
    input logic iFwMeS2_en,
    input logic [RegWidth-1:0] iFwMe
);

logic [RegWidth-1:0] ALU_A, ALU_B, ALU_Z;

ALU alu(
    .iA(ALU_A),
    .iB(ALU_B),
    .iFunc3(iID.ctrl.func3),
    .iFunc7(iID.ctrl.func7),
    .oZ(ALU_Z)
);

always_comb begin
    if(iFwMeS1_en)
        ALU_A = iFwMe;
    else if(iFwExS1_en)
        ALU_A = oMEM.rd.value;
    else
        ALU_A = iID.rs1.value;

    if(iFwMeS2_en)
        ALU_B = iFwMe;
    else if(iFwExS2_en)
        ALU_B = oMEM.rd.value;
    else if(iID.ctrl.imm_en)
        ALU_B = iID.immediate;
    else
        ALU_B = iID.rs2.value;
end

always_ff @(posedge iClk, negedge nRst) begin
    if(!nRst)
        oMEM = '0;
    else if(!iStall) begin
        oMEM.ctrl = iID.ctrl;
        oMEM.rs = iD.rs2;
        oMEM.rd.addr = iID.rd_addr;
        oMEM.rd.value = ALU_Z;
    end
end

endmodule

