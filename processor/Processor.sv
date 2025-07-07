/**
 * @file Processor.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief 
 * @version 0.1
 * @date Created: 2025-07-05
 * @modified Last Modified: 2025-07-05
 *
 * @copyright Copyright (c) 2025
 */

`timescale 1ns/100ps
import pipeline_types::*;
import rv32_isa::*;

module Processor(
    input logic iClk, nRst
);

// Pipeline Registers
if_id_t  IF_ID;
id_ex_t  ID_EX;
ex_mem_t EX_ME;
mem_wb_t ME_WB;

// IF Signals
logic IF_en, IF_PCS, IF_iStall, IF_oStall;
logic [31:0] IF_iPC;

// ID Signals
logic ID_en, ID_iStall, ID_brTrue;
logic [RegAddrWidth-1:0] ID_addrRs1, ID_addrRs2;
logic [RegWidth-1:0] ID_rs1, ID_rs2;

// EX Signals
logic EX_en, EX_iStall;
logic EX_FwExS1_en, EX_FwExS2_en;
logic EX_FwMeS1_en, EX_FwMeS2_en;
logic [31:0] EX_FwMe;

// MEM Signals
logic ME_en, ME_iStall, ME_oStall;

IF insfet(
    .iClk(iClk),
    .iEn(IF_en),
    .nRst(nRst),
    .iPCS_EXT(IF_PCS),
    .iStall(IF_iStall),
    .iPCS_EXT(IF_PCS),
    .oStall(IF_oStall),
    .oID(IF_ID)
);

ID insdec(
    .iClk(iClk),
    .iEn(ID_en),
    .nRst(nRst),
    .iStall(ID_iStall),
    .iIF(IF_ID),
    .oEX(ID_EX),
    .iRs1(ID_rs1),
    .iRs2(ID_rs2),
    .oAddrRs1(ID_addrRs1),
    .oAddrRs2(ID_addrRs2),
    .oBrTrue(ID_brTrue)
);

EX ex(
    .iClk(iClk),
    .iEn(EX_en),
    .nRst(nRst),
    .iStall(EX_iStall),
    .iID(ID_EX),
    .oMEM(EX_ME),
    .iFwExS1_en(EX_FwExS1_en),
    .iFwExS2_en(EX_FwExS2_en),
    .iFwMeS1_en(EX_FwMeS1_en),
    .iFwMeS2_en(EX_FwMeS2_en),
    .iFwMe(EX_FwMe)
);

ME me(
    .iClk(iClk),
    .iEn(ME_en),
    .nRst(nRst),
    .iStall(ME_iStall),
    .iEX(EX_ME),
    .oWB(ME_WB),
    .oStall(ME_oStall)
);

endmodule

