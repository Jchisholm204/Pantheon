/**
 * @file ROM.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief Processor Memory Interface
 * @version 0.1
 * @date Created: 2025-05-24
 * @modified Last Modified: 2025-05-24
 *
 * @copyright Copyright (c) 2025
 */

// import rv32_isa::*;
`timescale 1ns/100ps
module MEM(
    iClk, nRst,
    iEn, iReadnWrite,
    iData, iAddr,
    oData
);

input wire iClk, nRst, iEn, iReadnWrite;
input wire [31:0] iData, iAddr;
output logic [31:0] oData;

localparam n_progMem = 4095;

reg [31:0] progMem [n_progMem:0];

initial begin
    // $readmemh("progMem.hex", progMem);
    progMem[0] = 32'd55;
end

always_comb begin
    if(iEn & iReadnWrite) begin
        if(iAddr <= n_progMem)
            oData = progMem[iAddr];
        else
            oData = 32'd0;
    end else begin
        oData = iData;
    end
end

always_ff @(posedge iClk) begin
    if(iEn & ~iReadnWrite) begin
        if(iAddr <= n_progMem)
            progMem[iAddr] <= iData;
    end
end

endmodule
