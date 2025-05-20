/**
 * @file SHIFT.v
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief Bit Shift Arithmetic Operations
 * @version 0.1
 * @date Created: 2025-05-19
 * @modified Last Modified: 2025-05-19
 *
 * @copyright Copyright (c) 2025
 */
`timescale 1ns/100ps
module SHIFT(
    iD, iShamt,
    iRightnLeft, iArithnLogic,
    oD
);

input wire [31:0] iD;
input wire [4:0] iShamt;
input wire iRightnLeft, iArithnLogic;
output wire [31:0] oD;

wire [31:0] shift_ll, shift_ra, shift_rl, shift_r;

SHIFT_LEFT sll(
    .iD(iD),
    .iShamt(iShamt),
    .oD(shift_ll)
);

SHIFT_RIGHT_LOGIC srl(
    .iD(iD),
    .iShamt(iShamt),
    .oD(shift_rl)
);

SHIFT_RIGHT_ARITH sra(
    .iD(iD),
    .iShamt(iShamt),
    .oD(shift_ra)
);

assign shift_r = iArithnLogic ? shift_ra : shift_rl;
assign oD = iRightnLeft ? shift_r : shift_ll;

endmodule

module SHIFT_LEFT(
    iD, iShamt,
    oD
);

input wire [31:0] iD;
input wire [4:0]  iShamt;
output wire [31:0] oD;

wire [31:0] S1, S2, S3, S4, S5;

assign S1 = iShamt[0] ? {iD[30:0],  1'd0} : iD;
assign S2 = iShamt[1] ? {S1[29:0],  2'd0} : S1;
assign S3 = iShamt[2] ? {S2[27:0],  4'd0} : S2;
assign S4 = iShamt[3] ? {S3[23:0],  8'd0} : S3;
assign S5 = iShamt[4] ? {S4[15:0], 16'd0} : S4;

assign oD = S5;

endmodule

module SHIFT_RIGHT_ARITH(
    iD, iShamt,
    oD
);

input wire [31:0] iD;
input wire [4:0]  iShamt;
output wire [31:0] oD;

wire [31:0] S1, S2, S3, S4, S5;

assign S1 = iShamt[0] ? {{1{iD[31]}}, iD[31:1]}   : iD;
assign S2 = iShamt[1] ? {{2{S1[31]}}, S1[31:2]}   : S1;
assign S3 = iShamt[2] ? {{4{S2[31]}}, S2[31:4]}   : S2;
assign S4 = iShamt[3] ? {{8{S3[31]}}, S3[31:8]}   : S3;
assign S5 = iShamt[4] ? {{16{S4[31]}}, S4[31:16]} : S4;

assign oD = S5;

endmodule

module SHIFT_RIGHT_LOGIC(
    iD, iShamt,
    oD
);

input wire [31:0] iD;
input wire [4:0]  iShamt;
output wire [31:0] oD;

wire [31:0] S1, S2, S3, S4, S5;

assign S1 = iShamt[0] ? {1'd0,  iD[31:1]}  : iD;
assign S2 = iShamt[1] ? {2'd0,  S1[31:2]}  : S1;
assign S3 = iShamt[2] ? {4'd0,  S2[31:4]}  : S2;
assign S4 = iShamt[3] ? {8'd0,  S3[31:8]}  : S3;
assign S5 = iShamt[4] ? {16'd0, S4[31:16]}  : S4;

assign oD = S5;

endmodule
