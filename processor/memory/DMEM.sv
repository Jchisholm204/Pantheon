/**
 * @file DMEM.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief Data Memory Interface
 * @version 0.1
 * @date Created: 2025-05-31
 * @modified Last Modified: 2025-05-31
 *
 * TODO: Add Caching
 *
 * @copyright Copyright (c) 2025
 */
`timescale 1ns/100ps
module DMEM (
    input logic iClk, nRst, iEn, iWrite,
    input logic [2:0] iFunc3,
    input logic [31:0] iAddr, iData,
    output logic [31:0] oData,
    output logic oStall,
    WISHBONE_IF.master mem_wb
);

// Signed reads,, data in shorthand
logic [31:0] signed_byte, signed_half, dIn;

// Wishbone Inteface Control Assignments
assign mem_wb.addr = iAddr;
assign mem_wb.we = iWrite;
assign mem_wb.stb = iEn;
assign mem_wb.cyc = iEn;
assign mem_wb.iClk = iClk;
assign mem_wb.iRst = ~nRst;

// Combinational assignment for data width
always_comb begin
    case (iFunc3[1:0])
        2'b00: mem_wb.width = eDW_B;
        2'b01: mem_wb.width = eDW_H;
        default: mem_wb.width = eDW_W;
    endcase
end
// Processor Memory Stall Output
assign oStall = iEn & ~mem_wb.ack;

// Wishbone Interface Data Assignments
assign mem_wb.data_write = iData;
assign dIn = mem_wb.data_read;

always_comb begin
    signed_byte = {{24{dIn[7]}}, dIn[7:0]};
    signed_half = {{16{dIn[15]}}, dIn[15:0]};
    if(iFunc3[2] | iFunc3[1]) begin 
        oData = dIn;
    end else begin
        if(iFunc3[0]) oData = signed_half;
        else oData = signed_byte;
    end
end

endmodule


