/**
 * @file HazardUnit.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief
 * @version 0.1
 * @date Created: 2025-07-06
 * @modified Last Modified: 2025-07-06
 *
 * @copyright Copyright (c) 2025
 */

`timescale 1ns/100ps
import pipeline_types::*;
import rv32_isa::*;

module HazardUnit(
    input logic iClk, nRst,
    input logic nRst_dbg,
    input logic iBrTrue,
    input if_id_t iIF_ID,
    input id_ex_t iID_EX,
    input ex_mem_t iEX_ME,
    input mem_wb_t iME_WB,
    input logic iStall_dbg,
    input logic iStall_IF,
    input logic iStall_ME,
    output logic oStall_IF,
    output logic oStall_ID,
    output logic oStall_EX,
    output logic oStall_ME,
    output logic oFwExS1_en,
    output logic oFwExS2_en,
    output logic oFwMeS1_en,
    output logic oFwMeS2_en,
    output logic oRst_IF,
    output logic oRst_ID,
    output logic oRst_EX,
    output logic oRst_ME,
    output logic oFlush_IF,
    output logic oFlush_ID,
    output logic oFlush_EX,
    output logic oFlush_ME
);

// Forwarding Signals
assign oFwExS1_en = iID_EX.rs1.addr == iEX_ME.rd.addr
                    & iID_EX.rs1.addr != '0
                    & iEX_ME.ctrl.ex_en;

assign oFwExS2_en = iID_EX.rs2.addr == iEX_ME.rd.addr
                    & iID_EX.rs2.addr != '0
                    & iEX_ME.ctrl.ex_en;

assign oFwMeS1_en = iID_EX.rs1.addr == iME_WB.rd.addr
                    & iID_EX.rs1.addr != '0;
                    // & iME_WB.ctrl.mem_en;

assign oFwMeS2_en = iID_EX.rs2.addr == iME_WB.rd.addr
                    & iID_EX.rs2.addr != '0;
                    // & iME_WB.ctrl.mem_en;

// Stall for ME (WAR Hazard)
logic stallMeS1, stallMeS2, stallMe, stallMu;
assign stallMeS1 = iID_EX.rs1.addr == iEX_ME.rd.addr & iID_EX.rs1.addr != '0;
assign stallMeS2 = iID_EX.rs2.addr == iEX_ME.rd.addr & iID_EX.rs2.addr != '0;
// assign stallMeS2 = iID_EX.rs2.addr == iEX_ME.rd.addr;
// Stall on load use hazard
assign stallMe = (stallMeS1 | stallMeS2) & iEX_ME.ctrl.mem_en;
// Stall pipe on Memory Unit busy
assign stallMu = iStall_IF | iStall_ME;

// Stall Signals
assign oStall_IF = stallMe | stallMu | iStall_dbg;
assign oStall_ID = stallMe | stallMu | iStall_dbg;
assign oStall_EX = stallMe | stallMu | iStall_dbg;
assign oStall_ME = stallMu | iStall_dbg;

// Reset Signals
// System Reset ONLY (not for pipeline flushing)
assign oRst_IF = nRst & nRst_dbg;
assign oRst_ID = nRst & nRst_dbg;
assign oRst_EX = nRst & nRst_dbg;
assign oRst_ME = nRst & nRst_dbg;

// Flush Outputs - For Pipeline Flushing
assign oFlush_IF = ~oRst_IF | iBrTrue;
assign oFlush_ID = ~oRst_ID;
assign oFlush_EX = ~oRst_EX;
assign oFlush_ME = ~oRst_ME;


endmodule

