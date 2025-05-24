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

import rv32_isa::RegWidth;

module ALU(
    iA, iB,
    iFunc3, iFunc7,
    oZ
);
input wire [31:0] iA, iB;
input wire [2:0] iFunc3;
input wire [6:0] iFunc7;
output logic [31:0] oZ;

wire [31:0] z_bitwize, z_cla, z_div_r, z_div_q, z_mul_hi, z_mul_lo, z_shift;

BitWise bitwise(
    .iA(iA),
    .iB(iB),
    .iORnXOR(iFunc3[1]),
    .iAND(iFunc3[0]),
    .oD(z_bitwize)
);

wire [31:0] cla_iB;
assign cla_iB = iB ^ {RegWidth{iFunc7[5]}};

CLA adder(
    .iX(iA),
    .iY(cla_iB),
    .iCarry(iFunc7[5]),
    .oS(z_cla),
    .oCarry(),
    .oOverflow(),
    .oZero(),
    .oNegative()
);

SHIFT shifter(
    .iD(iA),
    .iShamt(iB[4:0]),
    .iRightnLeft(~iFunc3[0]),
    .iArithnLogic(iFunc7[5]),
    .oD(z_shift)
);

DIV32 div(
    .iSigned(~iFunc3[0]),
    .iDivisor(iB),
    .iDividend(iA),
    .oQ(z_div_q),
    .oR(z_div_r)
);
MUL32 mul(
    .iA(iA),
    .iB(iB),
    .oP({z_mul_hi, z_mul_lo})
);

always_comb begin
    // Select between I and M
    if(iFunc7[0]) begin
        // Div vs Mul
        if(iFunc3[2]) begin
            // Div Hi/Lo
            if(iFunc3[1])
                oZ = z_div_r;
            else
                oZ = z_div_q;
        end else begin
            // Mul Hi/Lo
            if(iFunc3[1:0] == 2'b00)
                oZ = z_mul_hi;
            else
                oZ = z_mul_lo;
        end
    end else begin
        if(iFunc3[1:0] == 2'b01) begin
            oZ = z_shift;
        end else begin
            if(iFunc3[2])
                oZ = z_bitwize;
            else
                oZ = z_cla;
        end
    end
end

endmodule
