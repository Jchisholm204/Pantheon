/**
 * @file frame_buffer.v
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief 
 * @version 0.1
 * @date Created: 2025-05-08
 * @modified Last Modified: 2025-05-08
 *
 * @copyright Copyright (c) 2025
 */

module frame_buffer(
    iClk, nRst, iWriteEn,
    iWAddr, iRAddr,
    iData, oData
);

input wire iClk, nRst, iWriteEn;
input wire [31:0] iWAddr, iRAddr;
input wire [31:0] iData;
output wire [31:0] oData;

localparam N = 2399;


reg [31:0] buffer [0:N];

initial begin
    buffer[1] = 32'hFFFFFF48; // H
    buffer[2] = 32'hFFFFFF69; // i

    buffer[4] = 32'hFFFFFF46; // F
    buffer[5] = 32'hFFFFFF72; // r
    buffer[6] = 32'hFFFFFF6F; // o
    buffer[7] = 32'hFFFFFF6D; // m

    buffer[9]  = 32'hFFFFFF46; // F
    buffer[10] = 32'hFFFFFF50; // P
    buffer[11] = 32'hFFFFFF47; // G
    buffer[12] = 32'hFFFFFF41; // A
end

assign oData = buffer[iRAddr];

always @(posedge iClk or negedge nRst) begin
    if(!nRst) begin
    end else begin
        if(iWriteEn) begin
            buffer[iWAddr] = iData;
        end
    end
end

endmodule
