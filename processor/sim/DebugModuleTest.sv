/**
 * @file DebugModuleTest.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief SV file for testing the Debug Module
 * @version 0.1
 * @date Created: 2025-07-18
 * @modified Last Modified: 2025-07-18
 *
 * @copyright Copyright (c) 2025
 */

`timescale 1ns/100ps
import reg_transport::reg_transport_t;
module DebugModuleTest(
    input logic iClk, nRst,
    output logic halted,
    output logic running,
    output logic stalled,
    input logic enter_debug,
    input logic req_halt,
    input logic req_resume,
    input logic step,
    output logic [31:0] dm_rdata,
    output logic dm_access_valid,
    input logic dm_write,
    input logic [6:0] dm_addr,
    input logic [31:0] dm_wdata
);

DBG_IF dmi();

assign halted = dmi.halted;
assign running = dmi.running;
assign stalled = dmi.stalled;
assign dmi.enter_debug = enter_debug;
assign dmi.req_halt = req_halt;
assign dmi.req_resume = req_resume;
assign dmi.step = step;
assign dm_rdata = dmi.dm_rdata;
assign dm_access_valid = dmi.dm_access_valid;
assign dmi.dm_write = dm_write;
assign dmi.dm_addr = dm_addr;
assign dmi.dm_wdata = dm_wdata;

reg_transport_t rd, rs;

DebugModule dm(
    .iClk(iClk),
    .nRst(nRst),
    .onRst(),
    .oHalt(),
    .oDbgReq(),
    .oResume(),
    .rd(rd),
    .oRegWrite(),
    .rs(rs),
    .dmi(dmi)
);

RegisterFile rf(
    .iClk(iClk),
    .nRst(nRst),
    .iWriteEn(1'b0),
    .iRd(),
    .iWriteEn_dbg(dm.oRegWrite),
    .iRd_dbg(rd),
    .iAddrRs3(rs.addr),
    .oRs3(rs.value)
);

endmodule

