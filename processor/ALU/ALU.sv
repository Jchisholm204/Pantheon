/**
 * @file ALU.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief 
 * @version 0.1
 * @date Created: 2025-05-19
 * @modified Last Modified: 2025-05-19
 *
 * @copyright Copyright (c) 2025
 */
`timescale 1ns/100ps

module ALU(
    iA, iB,
    iFunc3, iFunc7,
    oHi, oLo,
);
input wire [31:0] iA, iB;
input wire [2:0] iFunc3;
input wire [6:0] iFunc7;
output wire [31:0] oHi, oLo;

endmodule
