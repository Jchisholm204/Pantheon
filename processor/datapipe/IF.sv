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
module IF(
    iClk, iEn, nRst,
    iPCS_EXT, iStall,
    iPC_EXT,
    oStall,
    // Pipeline Register
    oPC, oPC4, oIR
);
input wire iClk, iEn, nRst;
input wire iPCS_EXT, iStall;
input wire [31:0] iPC_EXT;
output logic oStall;
output logic [31:0] oPC, oPC4, oIR;

wire [31:0] PC, PC4, IR;

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
    .oData(IR),
    .oStall(oStall),
    .mem_wb(wb_imem.master)
);

ROMBlock insmem(
    .mem_wb(wb_imem.slave)
);

always_ff @(posedge iClk) begin
    oPC <= PC;
    oPC4 <= PC4;
    oIR <= IR;
end

endmodule

