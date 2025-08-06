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
    input  logic iHaltReq,
    output logic oRst_n,
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

debug_type_t dmi_wdata;
assign dmi_wdata = dmi.dm_wdata;

always_comb begin : status
    dmstatus_d.version = debug::dmv_1_00;
    dmstatus_d.confstrptrvalid = 1'b0;
    dmstatus_d.hasresethaltreq = 1'b1;
    dmstatus_d.authbusy = 1'b0;
    dmstatus_d.authenticated = 1'b1;
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


