/**
 * @file IMEM.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief Instruction Memory Interface
 * @version 0.1
 * @date Created: 2025-05-31
 * @modified Last Modified: 2025-05-31
 *
 * TODO: Add Caching
 *
 * @copyright Copyright (c) 2025
 */

module IMEM (
    // Clock and reset must be driven externally
    iEn, iWrite,
    iAddr, iData,
    oData,
    oStall,
    mem_wb
);
input logic iEn, iWrite;
input logic [31:0] iAddr, iData;
output logic [31:0] oData;
output logic oStall;
WISHBONE_IF.master mem_wb;

// Wishbone Inteface Control Assignments
assign mem_wb.addr = iAddr;
assign mem_wb.we = iWrite;
assign mem_wb.stb = iEn;
assign mem_wb.cyc = iEn;
assign mem_wb.width = eDW_W;
// Wishbone Interface Data Assignments
assign mem_wb.data_write = iData;
assign oData = mem_wb.data_read;
// Processor Memory Stall Output
assign oStall = iEn & ~mem_wb.ack;


endmodule

