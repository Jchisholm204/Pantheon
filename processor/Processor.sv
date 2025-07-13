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
logic IF_en, IF_rst, IF_flush, IF_PCS, IF_iStall, IF_oStall;
logic [31:0] IF_iPC;

// ID Signals
logic ID_en, ID_rst, ID_flush, ID_iStall, ID_brTrue;
logic [RegAddrWidth-1:0] ID_addrRs1, ID_addrRs2;
logic [RegWidth-1:0] ID_rs1, ID_rs2;

// EX Signals
logic EX_en, EX_rst, EX_flush, EX_iStall;
logic EX_FwExS1_en, EX_FwExS2_en;
logic EX_FwMeS1_en, EX_FwMeS2_en;

// MEM Signals
logic ME_en, ME_rst, ME_flush, ME_iStall, ME_oStall;

// Debugger Signals
logic DBG_stall;

HazardUnit hu(
    .iClk(iClk),
    .nRst(nRst),
    .iBrTrue(ID_brTrue),
    .iIF_ID(IF_ID),
    .iID_EX(ID_EX),
    .iEX_ME(EX_ME),
    .iME_WB(ME_WB),
    .iStall_dbg(DBG_stall),
    .iStall_IF(IF_oStall),
    .iStall_ME(ME_oStall),
    .oStall_IF(IF_iStall),
    .oStall_ID(ID_iStall),
    .oStall_EX(EX_iStall),
    .oStall_ME(ME_iStall),
    .oFwExS1_en(EX_FwExS1_en),
    .oFwExS2_en(EX_FwExS2_en),
    .oFwMeS1_en(EX_FwMeS1_en),
    .oFwMeS2_en(EX_FwMeS2_en),
    .oRst_IF(IF_rst),
    .oRst_ID(ID_rst),
    .oRst_EX(EX_rst),
    .oRst_ME(ME_rst),
    .oFlush_IF(IF_flush),
    .oFlush_ID(ID_flush),
    .oFlush_EX(EX_flush),
    .oFlush_ME(ME_flush)
);


// --- Pipeline Stages --- //

IF insfet(
    .iClk(iClk),
    .iEn(IF_en),
    .nRst(IF_rst),
    .iFlush(IF_flush),
    .iPCS_EXT(IF_PCS),
    .iPC_EXT(IF_iPC),
    .iStall(IF_iStall),
    .oStall(IF_oStall),
    .oID(IF_ID)
);

ID insdec(
    .iClk(iClk),
    .iEn(ID_en),
    .nRst(ID_rst),
    .iStall(ID_iStall),
    .iFlush(ID_flush),
    .iIF(IF_ID),
    .oEX(ID_EX),
    .iRs1(ID_rs1),
    .iRs2(ID_rs2),
    .oAddrRs1(ID_addrRs1),
    .oAddrRs2(ID_addrRs2),
    .oBrTrue(ID_brTrue),
    .oBrPc(IF_iPC)
);

EX ex(
    .iClk(iClk),
    .iEn(EX_en),
    .nRst(EX_rst),
    .iStall(EX_iStall),
    .iFlush(EX_flush),
    .iID(ID_EX),
    .oMEM(EX_ME),
    .iFwExS1_en(EX_FwExS1_en),
    .iFwExS2_en(EX_FwExS2_en),
    .iFwMeS1_en(EX_FwMeS1_en),
    .iFwMeS2_en(EX_FwMeS2_en),
    .iFwMe(ME_WB.rd.value)
);

ME me(
    .iClk(iClk),
    .iEn(ME_en),
    .nRst(ME_rst),
    .iStall(ME_iStall),
    .iFlush(ME_flush),
    .iEX(EX_ME),
    .oWB(ME_WB),
    .oStall(ME_oStall)
);

endmodule

