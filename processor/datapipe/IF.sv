/**
 * @file IF.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief Instruction Fetch
 * @version 0.1
 * @date Created: 2025-05-25
 * @modified Last Modified: 2025-05-25
 *
 * @copyright Copyright (c) 2025
 */

`timescale 1ns/100ps
import pipeline_types::if_id_t;
import rv32_isa::*;

module IF #(
    parameter logic [31:0] START_ADDR = 32'd0
) (
    // Standard Module Inputs
    input wire iClk, nRst, iFlush, iStall,
    // PC Input (from branch unit)
    input wire iPCS_EXT,
    input wire [31:0] iPC_EXT,
    // Instruction Memory Wires
    input wire [31:0] iIM_data,
    input wire iIM_rdy,
    output wire [31:0] oIM_addr,
    output wire oIM_rd,
    // Pipeline Register
    output if_id_t oID
);

// Fetch Address and memory out
assign oIM_addr = iPCS_EXT ? iPC_EXT : pc_fetch;
assign oIM_rd = nRst & ~iStall;

logic [31:0] pc_current, pc_next, pc_fetch, pc_adder_in;
logic IM_stall;
// Unused wires for CLA
wire unused_neg, unused_overflow, unused_carry, unused_zero;

assign pc_adder_in = iPCS_EXT ? iPC_EXT : pc_fetch;

CLA pc_adder (
    .iX(32'd4),
    .iY(pc_adder_in),
    .iCarry(1'b0),
    .oS(pc_next),
    .oNegative(unused_neg),
    .oOverflow(unused_overflow),
    .oCarry(unused_carry),
    .oZero(unused_zero)
);

always_ff @(posedge iClk, negedge nRst) begin
    // Active Low Reset Signal
    if (!nRst) begin
        pc_fetch <= START_ADDR;
        pc_current <= START_ADDR;
    end else begin
        // PC External Load Select (Stall is active high)
        if (!iStall && iIM_rdy) begin
            pc_fetch <= pc_next;
            pc_current <= iPCS_EXT ? pc_adder_in : pc_fetch;
        end
    end
end

always_ff @(posedge iClk, negedge nRst) begin
    if(!nRst) begin
        oID.pc <= 32'd0;
        oID.pc4 <= 32'd0;
        oID.instruction <= {{12{1'b0}}, {5{1'b0}}, OpF3ADD, {5{1'b0}}, OpAluI};
        oID.valid <= 1'b0;
    end else if(iFlush | iPCS_EXT | IM_stall) begin
        oID.pc <= iPC_EXT;
        oID.pc4 <= pc_next;
        // Insert a NOP (addi r0, r0, 0) as a pipeline stall
        oID.instruction <= {{12{1'b0}}, {5{1'b0}}, OpF3ADD, {5{1'b0}}, OpAluI};
        oID.valid <= 1'b0;
    end else if(iStall) begin
        // Change nothing on a stall
    end else begin
        oID.pc <= pc_current;
        oID.pc4 <= pc_fetch;
        oID.instruction <= iIM_data;
        oID.valid <= 1'b1;
    end
    IM_stall <= ~iIM_rdy;
end

endmodule

