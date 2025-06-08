/**
 * @file ROMBlock.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief Block of ROM within the FPGA
 * @version 0.1
 * @date Created: 2025-06-01
 * @modified Last Modified: 2025-06-01
 *
 * @copyright Copyright (c) 2025
 */
`timescale 1ns/100ps
module ROMBlock #(
    parameter SIZE=4096
)(
    WISHBONE_IF.slave mem_wb
);
// input WISHBONE_IF.slave mem_wb;

`ifndef ROMFile
    `define ROMFile "../asm/test.hex"
`endif

// Memory (4kB)
logic [7:0] ROM[SIZE-1:0];

initial begin
    $readmemh(`ROMFile, ROM, 0, SIZE);
end

always_comb begin
    if(mem_wb.stb & mem_wb.cyc & ~mem_wb.we) begin
        mem_wb.data_read[7:0] = ROM[mem_wb.addr];
        if(|mem_wb.width)
            mem_wb.data_read[15:8] = ROM[mem_wb.addr+1];
        else
            mem_wb.data_read[15:8] = 8'd0;
        if(mem_wb.width[1]) begin
            mem_wb.data_read[23:16] = ROM[mem_wb.addr+2];
            mem_wb.data_read[31:24] = ROM[mem_wb.addr+3];
        end
        else begin
            mem_wb.data_read[23:16] = 8'd0;
            mem_wb.data_read[31:24] = 8'd0;
        end
        mem_wb.ack = 1'b1;
    end
    else begin
        mem_wb.data_read = 32'd0;
        mem_wb.ack = 1'b0;
    end
end

endmodule


