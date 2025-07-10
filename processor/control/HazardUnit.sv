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
    input logic iBrTrue,
    input if_id_t iIF_ID,
    input id_ex_t iID_EX,
    input ex_mem_t iEX_ME,
    input mem_wb_t iME_WB,
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
    output logic oRst_ME
);

// Forwarding Signals
assign oFwExS1_en = iID_EX.rs1.addr == iEX_ME.rd.addr
                    & iID.rs1.addr != '0
                    & iEX_ME.ctrl.ex_en;

assign oFwExS2_en = iID_EX.rs2.addr == iEX_ME.rd.addr
                    & iID.rs2.addr != '0
                    & iEX_ME.ctrl.ex_en;

assign oFwMeS1_en = iID_EX.rs1.addr == iME_WB.rd.addr
                    & iID.rs1.addr != '0
                    & iME_WB.ctrl.mem_en;

assign oFwMeS2_en = iID_EX.rs1.addr == iME_WB.rd.addr
                    & iID.rs2.addr != '0
                    & iME_WB.ctrl.mem_en;

// Stall for ME
logic stallMeS1, stallMeS2, stallMe;
assign stallMeS1 = iID_EX.rs1.addr == iEX_ME.rd.addr;
assign stallMeS2 = iID_EX.rs2.addr == iEX_ME.rd.addr;
assign stallMe = stallMeS1 | stallMeS2;

// Stall Signals
assign oStall_IF = stallMe;
assign oStall_ID = stallMe;
assign oStall_EX = stallMe;
assign oStall_ME = 1'b0;

// Reset Signals
// Pipeline Flushing or on System Reset
assign oRst_IF = nRst | iBrTrue;
assign oRst_ID = nRst;
assign oRst_EX = nRst;
assign oRst_ME = nRst;


endmodule

