/**
 * @file CLA.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief Carry Lookahead Adder
 * @version 0.1
 * @date Created: 2025-05-17
 * @modified Last Modified: 2025-05-17
 *
 * @copyright Copyright (c) 2025
 */
`timescale 1ns/100ps

module CLA(
    iX,
    iY,
    iCarry,
    oS,
    oCarry,
    oOverflow,
    oZero,
    oNegative
);

input wire iCarry;
input wire [31:0] iX, iY;
output wire [31:0] oS;
output wire oCarry, oOverflow, oZero, oNegative;

wire [3:0] C, O;

assign C[0] = iCarry;

CLA8 add1(
    .iX(iX[7:0]),
    .iY(iY[7:0]),
    .iCarry(C[0]),
    .oCarry(C[1]),
    .oS(oS[7:0]),
    .oOverflow()
);

CLA8 add2(
    .iX(iX[15:8]),
    .iY(iY[15:8]),
    .iCarry(C[1]),
    .oCarry(C[2]),
    .oS(oS[15:8]),
    .oOverflow()
);

CLA8 add3(
    .iX(iX[23:16]),
    .iY(iY[23:16]),
    .iCarry(C[2]),
    .oCarry(C[3]),
    .oS(oS[23:16]),
    .oOverflow()
);

CLA8 add4(
    .iX(iX[31:24]),
    .iY(iY[31:24]),
    .iCarry(C[3]),
    .oCarry(oCarry),
    .oS(oS[31:24]),
    .oOverflow(oOverflow)
);

assign oZero = ~|oS;
assign oNegative = oS[31];

endmodule

module CLA8(iX, iY, iCarry, oCarry, oS, oOverflow);
input wire [7:0] iX, iY;
input wire iCarry;
output wire oCarry, oOverflow;
output wire [7:0] oS;

wire [7:0] G, P;
wire [8:0] C;

// Generate the Generate and Propagate Signals
assign G = iX & iY;
assign P = iX | iY;

// Assign the Carry Signals
assign C[0] = iCarry;
assign C[1] = G[0] | (P[0] & C[0]);
assign C[2] = G[1] | (P[1] & G[0]) | (&P[1:0] & C[0]);
assign C[3] = G[2] | (P[2] & G[1]) | (&P[2:1] & G[0]) | (&P[2:0] & C[0]);
assign C[4] = G[3] | (P[3] & G[2]) | (&P[3:2] & G[1]) | (&P[3:1] & G[0]) | (&P[3:0] & C[0]);
assign C[5] = G[4] | (P[4] & G[3]) | (&P[4:3] & G[2]) | (&P[4:2] & G[1]) | (&P[4:1] & G[0]) | (&P[4:0] & C[0]);
assign C[6] = G[5] | (P[5] & G[4]) | (&P[5:4] & G[3]) | (&P[5:3] & G[2]) | (&P[5:2] & G[1]) | (&P[5:1] & G[0]) | (&P[5:0] & C[0]);
assign C[7] = G[6] | (P[6] & G[5]) | (&P[6:5] & G[4]) | (&P[6:4] & G[3]) | (&P[6:3] & G[2]) | (&P[6:2] & G[1]) | (&P[6:1] & G[0]) | (&P[6:0] & C[0]);
assign C[8] = G[7] | (P[7] & G[6]) | (&P[7:6] & G[5]) | (&P[7:5] & G[4]) | (&P[7:4] & G[3]) | (&P[7:3] & G[2]) | (&P[7:2] & G[1]) | (&P[7:1] & G[0]) | (&P[7:0] & C[0]);
assign oCarry = C[8];


// Assign the Sum
assign oS = iX ^ iY ^ C[7:0];

// Assign the Overflow
assign oOverflow = C[7] ^ C[6];

endmodule
