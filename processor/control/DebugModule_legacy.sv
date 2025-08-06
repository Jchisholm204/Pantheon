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

module DebugModule_legacy(
    input logic iClk, nRst,
    output logic onRst,
    output logic oHalt,
    output logic oDbgReq,
    output logic oResume,
    // Debug Access to Processor Memory
    BBUS_IF.master dbac_rf,
    BBUS_IF.master dbac_csr,
    // Debugger Module Interface
    DBG_IF.processor dmi
);
// DBG_IF dmi();

localparam logic [6:0] dmAddr_data0 = 7'h04;
localparam logic [6:0] dmAddr_data1 = 7'h05;
localparam logic [6:0] dmAddr_control = 7'h10;
localparam logic [6:0] dmAddr_status = 7'h11;
localparam logic [6:0] dmAddr_abstractics = 7'h16;
localparam logic [6:0] dmAddr_command = 7'h17;
localparam logic [6:0] dmAddr_progbuf0 = 7'h20;
localparam logic [6:0] dmAddr_progbuf1 = 7'h21;
localparam logic [6:0] dmAddr_sbcs = 7'h38;
localparam logic [6:0] dmAddr_sbaddress0 = 7'h39;
localparam logic [6:0] dmAddr_sbdata0 = 7'h3c;

// Access Register Command
localparam logic [7:0] dmCmd_ARC = 8'd0;
// Quick Access Command
localparam logic [7:0] dmCmd_QA = 8'd1;
// Access Memory Command
localparam logic [7:0] dmCmd_AMC = 8'd2;

localparam logic [2:0] cmderr_none = 3'd0;
localparam logic [2:0] cmderr_busy = 3'd1;
localparam logic [2:0] cmderr_nosupport = 3'd2;
localparam logic [2:0] cmderr_exception = 3'd3;
localparam logic [2:0] cmderr_exefail = 3'd4;
localparam logic [2:0] cmderr_buserr = 3'd5;
localparam logic [2:0] cmderr_other = 3'd7;

logic [31:0] data0;
logic [31:0] data1;

dmcontrol_t dmcontrol;
logic dmcontrol_active;
logic dmcontrol_reset;
logic dmcontrol_clrkeepalive;
logic dmcontrol_setkeepalive;
logic dmcontrol_ackunavail;
logic dmcontrol_ackhavereset;
logic dmcontrol_resumereq;
logic dmcontrol_haltreq;

dmstatus_t dmstatus;
logic dmstatus_allhavereset;
logic dmstatus_anyhavereset;
logic dmstatus_allresumeack;
logic dmstatus_anyresumeack;
logic dmstatus_allnonexistent;
logic dmstatus_anynonexistent;
logic dmstatus_allunavail;
logic dmstatus_anyunavail;
logic dmstatus_allrunning;
logic dmstatus_anyrunning;
logic dmstatus_allhalted;
logic dmstatus_anyhalted;

abstractcs_t abstractcs;
logic abstractcs_busy;
logic abstractcs_relaxedpriv;
logic [2:0] abstractcs_cmderr;

command_t command;
logic [31:0] progbuf0;
logic [31:0] progbuf1;

sbcs_t sbcs;
logic sbcs_busyerror;
logic sbcs_busy;
logic sbcs_readonaddr;
logic [2:0] sbcs_access;
logic sbcs_autoincrement;
logic sbcs_readondata;
logic [2:0] sbcs_error;

logic [31:0] sbaddress0;
logic [31:0] sbdata0;

debug_type_t dmi_wdata;
assign dmi_wdata = dmi.dm_wdata;


always_ff @(posedge iClk, negedge nRst) begin
    // Writes from debugger to internal module
    if(!nRst | !dmcontrol_active) begin
        data0 <= 32'd0;
        data1 <= 32'd0;
        dmcontrol_haltreq <= 1'b0;
        dmcontrol_resumereq <= 1'b0;
        dmcontrol_ackhavereset <= 1'b0;
        dmcontrol_setkeepalive <= 1'b0;
        dmcontrol_clrkeepalive <= 1'b0;
        dmcontrol_reset <= 1'b0;
        // Debugger self reset logic
        if(dmi.dm_write & dmi.dm_addr == dmAddr_control)
            dmcontrol_active <= dmi_wdata.dmcontrol.active;
        else
            dmcontrol_active <= 1'b0;
        abstractcs_relaxedpriv <= 1'b0;
        abstractcs_cmderr <= 3'd0;
        progbuf0 <= 32'd0;
        progbuf1 <= 32'd0;
        sbcs_readonaddr <= 1'b0;
        sbcs_access <= 3'd0;
        sbcs_autoincrement <= 1'b0;
        sbcs_readondata <= 1'b0;
        sbcs_error <= 3'd0;
        sbaddress0 <= 32'd0;
        sbdata0 <= 32'd0;
    end else if(dmi.dm_write) begin
        if(dmi.dm_addr == dmAddr_data0)
            data0 <= dmi.dm_wdata;
        if(dmi.dm_addr == dmAddr_data1)
            data1 <= dmi.dm_wdata;
        if(dmi.dm_addr == dmAddr_control) begin
            dmcontrol_haltreq <= dmi_wdata.dmcontrol.haltreq;
            if(dmi_wdata.dmcontrol.resumereq) begin
                dmcontrol_resumereq <= 1'b1;
                dmstatus_allresumeack <= 1'b0;
                dmstatus_anyresumeack <= 1'b0;
            end
            if(dmi_wdata.dmcontrol.ackhavereset & ~abstractcs_busy) begin
                dmcontrol_ackhavereset <= 1'b1;
            end
            dmcontrol_setkeepalive <= dmi_wdata.dmcontrol.setkeepalive;
            dmcontrol_clrkeepalive <= dmi_wdata.dmcontrol.clrkeepalive;
            dmcontrol_reset <= dmi_wdata.dmcontrol.reset;
            dmcontrol_active <= dmi_wdata.dmcontrol.active;
        end
        if(dmi.dm_addr == dmAddr_abstractics) begin
            abstractcs_relaxedpriv <= dmi_wdata.abstractcs.relaxedpriv;
            abstractcs_cmderr <= abstractcs_cmderr & ~dmi_wdata.abstractcs.cmderr;
        end
        if(dmi.dm_addr == dmAddr_command) begin
            command <= dmi.dm_wdata;
            abstractcs_busy <= 1'b1;
        end
        if(dmi.dm_addr == dmAddr_progbuf0)
            progbuf0 <= dmi.dm_wdata;
        if(dmi.dm_addr == dmAddr_progbuf1)
            progbuf1 <= dmi.dm_wdata;
        if(dmi.dm_addr == dmAddr_sbcs) begin
            sbcs_readonaddr <= dmi_wdata.sbcs.readonaddr;
            sbcs_access <= dmi_wdata.sbcs.access;
            sbcs_autoincrement <= dmi_wdata.sbcs.autoincrement;
            sbcs_readondata <= dmi_wdata.sbcs.readondata;
            if(|dmi_wdata.sbcs.error)
                sbcs_error <= 3'd0;
        end
        if(dmi.dm_addr == dmAddr_sbaddress0)
            sbaddress0 <= dmi.dm_wdata;
        if(dmi.dm_addr == dmAddr_sbdata0)
            sbdata0 <= dmi.dm_wdata;
    end

    // Command Processing
    if(abstractcs_busy) begin
        if(command[7:0] == dmCmd_ARC) begin
            // Size check the access
            if(command.acc_reg.aarsize != 3'd2)
                abstractcs_cmderr <= cmderr_buserr;
            // Process Access Register Command
            else if (command.acc_reg.transfer) begin
                // Access General Purpose Regs
                if(command.acc_reg.regno[15:8] == 8'h10) begin
                    dbac_rf.addr <= command.acc_reg.regno[7:0];
                    if(command.acc_reg.write) begin
                        dbac_rf.write_en <= 1'b1;
                        dbac_rf.read_en <= 1'b0;
                        if(dbac_rf.write_ack)
                            abstractcs_busy <= 1'b0;
                    end else begin
                        dbac_rf.write_en <= 1'b0;
                        dbac_rf.read_en <= 1'b1;
                        if(dbac_rf.read_ack) begin
                            data0 <= dbac_rf.rdata;
                            abstractcs_busy <= 1'b0;
                        end
                    end
                end
            end
        end
    end
end

// Debugger Read from internal registers
always_comb begin
    if(dmi.dm_write)
        dmi.dm_rdata = 32'd0;
    else if(dmi.dm_addr == dmAddr_data0)
        dmi.dm_rdata = data0;
    else if(dmi.dm_addr == dmAddr_data1)
        dmi.dm_rdata = data1;
    else if(dmi.dm_addr == dmAddr_control)
        dmi.dm_rdata = dmcontrol;
    else if(dmi.dm_addr == dmAddr_status)
        dmi.dm_rdata = dmstatus;
    else if(dmi.dm_addr == dmAddr_abstractics)
        dmi.dm_rdata = abstractcs;
    else if(dmi.dm_addr == dmAddr_command)
        dmi.dm_rdata = command;
    else if(dmi.dm_addr == dmAddr_progbuf0)
        dmi.dm_rdata = progbuf0;
    else if(dmi.dm_addr == dmAddr_progbuf1)
        dmi.dm_rdata = progbuf1;
    else if(dmi.dm_addr == dmAddr_sbcs)
        dmi.dm_rdata = sbcs;
    else if(dmi.dm_addr == dmAddr_sbaddress0)
        dmi.dm_rdata = sbaddress0;
    else if(dmi.dm_addr == dmAddr_sbdata0)
        dmi.dm_rdata = sbdata0;
    else
        dmi.dm_rdata = 32'd0;
end

// Assign out values to structs for read out
always_comb begin
    dmcontrol.active = dmcontrol_active;
    dmcontrol.reset = dmcontrol_reset;
    dmcontrol.clrresethaltreq = 1'b0;
    dmcontrol.setresethaltreq = 1'b0;
    dmcontrol.clrkeepalive = dmcontrol_clrkeepalive;
    dmcontrol.setkeepalive = dmcontrol_setkeepalive;
    dmcontrol.heartselhi = 10'd0;
    dmcontrol.heartsello = 10'd0;
    dmcontrol.hasel = 1'b0;
    dmcontrol.ackunavail = dmcontrol_ackunavail;
    dmcontrol.ackhavereset = dmcontrol_ackhavereset;
    dmcontrol.heartreset = 1'b0;
    dmcontrol.resumereq = dmcontrol_resumereq;
    dmcontrol.haltreq = dmcontrol_haltreq;

    dmstatus.zero7 = 7'd0;
    dmstatus.resetpending = dmcontrol_reset;
    dmstatus.stickyunavail = 1'b0;
    dmstatus.impebreak = 1'b1;
    dmstatus.zero2 = 2'd0;
    dmstatus.allhavereset = dmstatus_allhavereset;
    dmstatus.anyhavereset = dmstatus_anyhavereset;
    dmstatus.allresumeack = dmstatus_allresumeack;
    dmstatus.anyresumeack = dmstatus_anyresumeack;
    dmstatus.allnonexistent = dmstatus_allnonexistent;
    dmstatus.anynonexistent = dmstatus_anynonexistent;
    dmstatus.allunavail = dmstatus_allunavail;
    dmstatus.anyunavail = dmstatus_anyunavail;
    dmstatus.allrunning = dmstatus_allrunning;
    dmstatus.anyrunning = dmstatus_anyrunning;
    dmstatus.allhalted = dmstatus_allhalted;
    dmstatus.anyhalted = dmstatus_anyhalted;
    dmstatus.authenticated = 1'b1;
    dmstatus.authbusy = 1'b0;
    dmstatus.hasresethaltreq = 1'b0;
    dmstatus.confstrptrvalid = 1'b0;
    dmstatus.version = 4'd3;

    abstractcs.zero3 = 3'd0;
    abstractcs.progbufsize = 5'd2;
    abstractcs.zero11 = 11'd0;
    abstractcs.busy = abstractcs_busy;
    abstractcs.relaxedpriv = abstractcs_relaxedpriv;
    abstractcs.cmderr = abstractcs_cmderr;
    abstractcs.zero4 = 4'd0;
    abstractcs.datacount = 4'd2;

    sbcs.version = 3'd1;
    sbcs.zero6 = 6'd0;
    sbcs.busyerror = sbcs_busyerror;
    sbcs.busy = sbcs_busy;
    sbcs.readonaddr = sbcs_readonaddr;
    sbcs.access = sbcs_access;
    sbcs.autoincrement = sbcs_autoincrement;
    sbcs.readondata = sbcs_readondata;
    sbcs.error = sbcs_error;
    sbcs.size = 7'd32;
    sbcs.access128 = 1'b0;
    sbcs.access64 = 1'b0;
    sbcs.access32 = 1'b1;
    sbcs.access16 = 1'b1;
    sbcs.access8 = 1'b1;
end

endmodule

