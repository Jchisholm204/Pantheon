/**
 * @file Register.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief 
 * @version 0.1
 * @date Created: 2025-06-14
 * @modified Last Modified: 2025-06-14
 *
 * @copyright Copyright (c) 2025
 */

`timescale 1ns/100ps
module Register #(
    parameter int width = 32
    )(
    input logic iClk, nRst, iWrite,
    input logic [width-1:0] iD,
    output logic [width-1:0] oQ
);

always_ff @(posedge iClk, negedge nRst) begin
    if(!nRst)
        oQ <= {width{1'b0}};
    else if(iWrite)
        oQ <= iD;
end

endmodule

