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

module IF (
    // Standard Module Inputs
    input wire iClk, nRst, iFlush, iStall,
    // PC Input (from branch unit)
    input wire iPCS_EXT,
    input wire [31:0] iPC_EXT,
    // Instruction Memory Wires
    input logic [31:0] iIM_data,
    input logic iIM_rdy,
    output logic [31:0] oIM_addr,
    output logic oIM_rd,
    // Pipeline Register
    output if_id_t oID
);

wire [31:0] oPC, oPC4;

assign oIM_addr = oPC;
assign oIM_rd = nRst & ~iStall;

PC pc(
    .iClk(iClk),
    .nRst(nRst),
    .iStall(iStall | ~iIM_rdy),
    .iPC(iPC_EXT),
    .iEXT_S(iPCS_EXT),
    .oPC(oPC),
    .oPC4(oPC4)
);

always_ff @(posedge iClk, negedge nRst) begin
    if(!nRst) begin
        oID.pc <= 32'd0;
        oID.pc4 <= 32'd0;
    end else if(iFlush | ~iIM_rdy | iStall | iPCS_EXT) begin
        oID.pc <= oPC;
        oID.pc4 <= oPC4;
        // Insert a NOP (addi r0, r0, 0) as a pipeline stall
        oID.instruction <= {{12{1'b0}}, {5{1'b0}}, OpF3ADD, {5{1'b0}}, OpAluI};
    end else begin
        oID.pc <= oPC;
        oID.pc4 <= oPC4;
        oID.instruction <= iIM_data;
    end
end

endmodule

