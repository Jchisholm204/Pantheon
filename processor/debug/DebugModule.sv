/**
 * @file DebugModule.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief
 * @version 0.1
 * @date Created: 2025-07-15
 * @modified Last Modified: 2025-07-15
 *
 * @copyright Copyright (c) 2025
 */

`timescale 1ns/100ps
// `include "debug_types.svh"
// `include "reg_transport.svh"
import reg_transport::reg_transport_t;
import debug_types::*;

module DebugModule(
    input  logic iClk, iRst_n,
    input  logic iRunning,
    output logic oSysRst_n,
    output logic oPipeRst_n,
    output logic oHaltReq,
    output logic oDbgReq,
    output logic oResume,
    // Debug Access to Processor Memory
    BBUS_IF.master dbac_rf,
    BBUS_IF.master dbac_csr,
    // Debugger Module Interface
    DBG_IF.processor dmi
);

logic [31:0] data0_d;
logic [31:0] data0_q;
logic [31:0] data1_d;
logic [31:0] data1_q;

dmcontrol_t dmcontrol_d;
dmcontrol_t dmcontrol_q;
dmstatus_t dmstatus_d;
dmstatus_t dmstatus_q;
abstractcs_t abstractcs_d;
abstractcs_t abstractcs_q;
command_t command_d;
command_t command_q;

// System Bus access
sbcs_t sbcs_d;
sbcs_t sbcs_q;
logic [31:0] sbaddress0_d;
logic [31:0] sbaddress0_q;
logic [31:0] sbdata0_d;
logic [31:0] sbdata0_q;

// Split the dmi_wdata type into w_* fields
debug_type_t dmi_wdata;
dmcontrol_t w_dmcontrol;
dmstatus_t w_dmstatus;
abstractcs_t w_abstractcs;
sbcs_t w_sbcs;
assign dmi_wdata = dmi.dm_wdata;
assign w_dmcontrol = dmi_wdata.dmcontrol;
assign w_dmstatus = dmi_wdata.dmstatus;
assign w_abstractcs = dmi_wdata.abstractcs;
assign w_sbcs = dmi_wdata.sbcs;

always_comb begin : dmstatus
    dmstatus_d.zero7 = '0;
    dmstatus_d.resetpending = dmcontrol_q.reset;
    dmstatus_d.stickyunavail = '0;
    dmstatus_d.impebreak = 1'b1;
    dmstatus_d.zero2 = '0;
    // 1 when reset until acked
    dmstatus_d.anyhavereset = ~dmcontrol_q.ackhavereset
        & (dmcontrol_q.reset | dmstatus_q.anyhavereset);
    dmstatus_d.allhavereset = ~dmcontrol_q.ackhavereset
        & (dmcontrol_q.reset | dmstatus_q.allhavereset);
    // Set resume ack when halt request is gone, resume request
    //  is issued, and the processor is running.
    dmstatus_d.anyresumeack = ~dmcontrol_q.haltreq
        & dmcontrol_q.resumereq & iRunning;
    dmstatus_d.allresumeack = ~dmcontrol_q.haltreq
        & dmcontrol_q.resumereq & iRunning;
    // Heart selection invalid feedback to DM
    dmstatus_d.anynonexistent = dmcontrol_q.heartselhi != '0 & dmcontrol_q.heartsello != 10'd1;
    dmstatus_d.allnonexistent = dmcontrol_q.heartselhi != '0 & dmcontrol_q.heartsello != 10'd1;
    // Processor Running
    dmstatus_d.anyrunning = iRunning;
    dmstatus_d.allrunning = iRunning;
    // Processor Halted = not running
    dmstatus_d.anyhalted = ~iRunning;
    dmstatus_d.allhalted = ~iRunning;
    // Authentication module not present
    dmstatus_d.authenticated = 1'b1;
    dmstatus_d.authbusy = 1'b0;
    // The DM preserves and issues halt after heart reset
    dmstatus_d.hasresethaltreq = 1'b1;
    // not used..
    dmstatus_d.confstrptrvalid = 1'b0;
    // Version 1.00 of the RV Specification
    dmstatus_d.version = debug::dmv_1_00;
end

always_comb begin : dmcontrol
    // Handle Writes
    if(dmi.dm_write && dmi.dm_access_valid && dmi.dm_addr == debug::control) begin
        
    end
end

always_ff @(posedge iClk, negedge iRst_n) begin:ff
    if(!iRst_n) begin : ereset
        data0_q <= '0;
        data1_q <= '0;
        dmcontrol_q <= '0;
        dmstatus_q <= '0;
        abstractcs_q <= '0;
        command_q <= '0;
        sbcs_q <= '0;
        sbaddress0_q <= '0;
        sbdata0_q <= '0;
    end : ereset else begin : active
        if(!dmcontrol_q.active) begin : self_rst
            data0_q <= '0;
            data1_q <= '0;
            dmcontrol_q <= '{
                default: '0,
                active: dmcontrol_d.active
            };
            dmstatus_q <= '0;
            abstractcs_q <= '{
                default: '0,
                cmderr: debug::cerr_none
            };
            command_q <= '0;
            sbcs_q <= '0;
            sbaddress0_q <= '0;
            sbdata0_q <= '0;
        end : self_rst else begin : norm_op
            data0_q <= data0_d;
            data1_q <= data1_d;
            dmcontrol_q <= dmcontrol_d;
            dmstatus_q <= dmstatus_d;
            abstractcs_q <= abstractcs_d;
            command_q <= command_d;
            sbcs_q <= sbcs_d;
            sbaddress0_q <= sbaddress0_d;
            sbdata0_q <= sbdata0_d;
        end : norm_op
    end : active
end : ff

endmodule : DebugModule


