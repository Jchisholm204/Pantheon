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
import reg_transport::reg_transport_t;
module DebugModule(
    input logic iClk, nRst,
    output logic onRst,
    output logic oHalt,
    output logic oDbgReq,
    output logic oResume,
    inout reg_transport_t rd,
    inout reg_transport_t rs,
    input logic [31:0] iPC,
    output logic [31:0] oPC,
    dmi
);
DBG_IF.processor dmi;

logic [31:0] dpc;
logic [31:0] data0;
logic [31:0] data1;
logic [31:0] dmcontrol;
logic [31:0] dmstatus;
logic [31:0] abstractcs;
logic [31:0] command;
logic [31:0] progbuf0;
logic [31:0] progbuf1;
logic [31:0] sbcs;
logic [31:0] sbaddress0;
logic [31:0] sbdata0;


// DM Status Signals
logic dmstatus_reset, dmstatus_resumeack;
logic dmstatus_allnonexistent, dmstatus_anynonexistent;
logic dmstatus_allunavail, dmstatus_anyunavail;
logic dmstatus_running, dmstatus_halted;
assign dmstatus[31:25] = 7'd0;
// NDM Reset Pending (0 = Unimplimented)
assign dmstatus[24] = 1'b0;
// Sticky Unavail (Unavail bits are sticky when 1)
assign dmstatus[23] = 1'b0;
// Implicit Break at end of program buffer
assign dmstatus[22] = 1'b1;
// Zero
assign dmstatus[21:20] = 2'b0;
// All hearts have been reset
assign dmstatus[19] = dmstatus_reset;
// Any heart has been reset
assign dmstatus[18] = dmstatus_reset;
// All hearts have resumed
assign dmstatus[17] = dmstatus_resumeack;
// Any heart has resumed
assign dmstatus[16] = dmstatus_resumeack;
// All hearts selected do not exist
assign dmstatus[15] = dmstatus_anynonexistent;
// one of the hearts selected does not exist
assign dmstatus[14] = dmstatus_anynonexistent;
// All hearts selected are Unavail
assign dmstatus[13] = dmstatus_allunavail;
// Any hearts selected are Unavail
assign dmstatus[12] = dmstatus_anyunavail;
// All Hearts are running
assign dmstatus[11] = dmstatus_running;
// Any heart is running
assign dmstatus[10] = dmstatus_running;
// All hearts are halted
assign dmstatus[9] = dmstatus_halted;
// Any heart is halted
assign dmstatus[8] = dmstatus_halted;
// Debugger is authenticated
assign dmstatus[7] = 1'b1;
// Debugger Authenticator busy
assign dmstatus[6] = 1'b0;
// Halt on reset supported
assign dmstatus[5] = 1'b0;
// confstrptrvalid is valid
assign dmstatus[4] = 1'b0;
// Specification Version
assign dmstatus[3:0] = 4'd3;

// Debug Module Control Signals (dmcontrol)
logic dmcontrol_haltreq, dmcontrol_resumereq;

// DPC Logic 
always_ff @(posedge iClk, negedge nRst) begin
    if(!nRst) begin
        dpc <= 32'd0;
        data0 <= 32'd0;
        data1 <= 32'd0;
        dmcontrol <= 32'd0;
    end
end

endmodule

