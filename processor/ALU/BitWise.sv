/**
 * @file BitWise.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief 
 * @version 0.1
 * @date Created: 2025-05-19
 * @modified Last Modified: 2025-05-19
 *
 * @copyright Copyright (c) 2025
 */
`timescale 1ns/100ps
module BitWise(
    iA, iB,
    iORnXOR, iAND,
    oD
);

input wire [31:0] iA, iB;
input wire iORnXOR, iAND;
output wire [31:0] oD;

wire [31:0] w_and, w_or, w_xor, w_orxor;

assign w_and = iA & iB;
assign w_or  = iA | iB;
assign w_xor = iA ^ iB;

assign w_orxor = iORnXOR ? w_or : w_xor;
assign oD = iAND ? w_and : w_orxor;

endmodule
