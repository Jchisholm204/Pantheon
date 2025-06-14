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

module IF (
    input wire iClk, iEn, nRst,
    input wire iPCS_EXT, iStall,
    input wire [31:0] iPC_EXT,
    output logic oStall,
    // Pipeline Register
    output if_id_t oID
);

wire [31:0] PC, PC4, ins_data;

WISHBONE_IF wb_imem(
    .iClk(iClk),
    .iRst(~nRst)
);

PC pc(
    .iClk(iClk),
    .nRst(nRst),
    .iStall(iStall),
    .iPC(iPC_EXT),
    .iEXT_S(iPCS_EXT),
    .oPC(PC),
    .oPC4(PC4)
);

IMEM wbi(
    .iEn(iEn & ~iStall),
    .iAddr(PC),
    .oData(ins_data),
    .oStall(oStall),
    .mem_wb(wb_imem)
);

ROMBlock insmem(
    .mem_wb(wb_imem)
);

always_ff @(posedge iClk, negedge nRst) begin
    if(!nRst) begin
        oID.pc <= 32'd0;
        oID.pc4 <= 32'd0;
        oID.instruction <= 32'd0;
    end else if(~iStall) begin
        oID.pc <= PC;
        oID.pc4 <= PC4;
        oID.instruction <= ins_data;
    end
end

endmodule

