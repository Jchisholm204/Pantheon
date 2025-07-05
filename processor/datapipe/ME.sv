/**
 * @file ME.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief Memory Pipeline Stage
 * @version 0.1
 * @date Created: 2025-07-05
 * @modified Last Modified: 2025-07-05
 *
 * @copyright Copyright (c) 2025
 */

`timescale 1ns/100ps

import pipeline_types::ex_mem_t;
import pipeline_types::mem_wb_t;

module ME(
    input logic iClk, iEn, nRst,
    input logic iStall,
    input ex_mem_t iEX,
    output mem_wb_t oWB,
    output logic oStall
);

logic mem_en;
logic [31:0] mem_out;
WISHBONE_IF dmem_wb;
assign mem_en = iEn & iEX.ctrl.mem_en & iEX.ctrl.valid;

DMEM dmem(
    .iClk(iClk),
    .nRst(nRst),
    .iEn(mem_en),
    .iWrite(mem_en & iEX.ctrl.wb_en),
    .iFunc3(iEX.ctrl.func3),
    .iAddr(iEX.rd.value),
    .iData(iEX.rs.value),
    .oData(mem_out),
    .oStall(oStall),
    .mem_wb(dmem_wb)
);

RAMBlock cram(
    .mem_wb(dmem_wb)
);

always_ff @(posedge iClk, negedge nRst) begin : WB_ASSIGN
    if(!nRst)
        oWB = '0;
    else if(!iStall) begin
        oWB.ctrl = iEX.ctrl;
        oWB.rd.addr = iEX.rd.addr;
        if(iEX.ctrl.mem_en)
            oWB.rd.value = mem_out;
        else
            oWB.rd.value = iEX.rd.value;
    end
end

endmodule

