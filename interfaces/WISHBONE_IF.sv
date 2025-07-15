/**
 * @file WISHBONE_IF.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief 
 * @version 0.1
 * @date Created: 2025-05-31
 * @modified Last Modified: 2025-05-31
 *
 * 
 * All wishbone signals must be active high
 * Port sizes must be 8, 16, 32, or 64 bit
 *  Default port size is 32 bit
 *
 * All interfaces should use little endian format
 *  (Lowest Byte in Lowest Address)
 *
 *
 * @copyright Copyright (c) 2025
 */

typedef enum logic [1:0] {
    // Byte
    eDW_B = 2'b00,
    // Half Word
    eDW_H = 2'b01,
    // Word
    eDW_W = 2'b10
} eDataWidth;

interface WISHBONE_IF 
#(parameter ADDR_WIDTH=32, DATA_WIDTH=32)
(
    iClk, iRst
);
input logic iClk, iRst;

logic [ADDR_WIDTH-1:0] addr;
logic [DATA_WIDTH-1:0] data_read, data_write;
// Write Enable
logic we;
// Chip Select
logic stb;
// Write Cycle Valid
logic cyc;
// Ack
logic ack;
// Transfer Width
eDataWidth width;

modport master (
    input iClk, iRst, ack, data_read,
    output addr, data_write, we, stb, cyc, width
);

modport slave(
    input iClk, iRst, addr, data_write, we, stb, cyc, width,
    output ack, data_read
);

endinterface
