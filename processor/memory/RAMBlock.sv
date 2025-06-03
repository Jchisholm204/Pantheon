/**
 * @file RAMBlock.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief Block of RAM within the FPGA
 * @version 0.1
 * @date Created: 2025-06-01
 * @modified Last Modified: 2025-06-01
 *
 * @copyright Copyright (c) 2025
 */
`timescale 1ns/100ps
module RAMBlock #(parameter SIZE=4096)
(
    mem_wb
);
WISHBONE_IF.slave mem_wb;


// Memory (4kB)
logic [7:0] RAM[SIZE-1:0];

always_ff @(posedge mem_wb.iClk, negedge mem_wb.iRst) begin
    if(!mem_wb.iRst) begin
        integer i;
        for(i = 0; i < SIZE; i++) begin
            RAM[i] <= 8'd0;
        end
    end else begin
        if(mem_wb.stb & mem_wb.cyc & mem_wb.we) begin
            RAM[mem_wb.addr] <= mem_wb.data_write[7:0];
            if(|mem_wb.width)
                RAM[mem_wb.addr+1] <= mem_wb.data_write[15:8];
            if(mem_wb.width[1]) begin
                RAM[mem_wb.addr+2] <= mem_wb.data_write[23:16];
                RAM[mem_wb.addr+3] <= mem_wb.data_write[31:24];
            end
        end
    end
end 

always_comb begin
    if(mem_wb.stb & mem_wb.cyc & ~mem_wb.we) begin
        mem_wb.data_read[7:0] = RAM[mem_wb.addr];
        if(|mem_wb.width)
            mem_wb.data_read[15:8] = RAM[mem_wb.addr+1];
        else
            mem_wb.data_read[15:8] = 8'd0;
        if(mem_wb.width[1]) begin
            mem_wb.data_read[23:16] = RAM[mem_wb.addr+2];
            mem_wb.data_read[31:24] = RAM[mem_wb.addr+3];
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

