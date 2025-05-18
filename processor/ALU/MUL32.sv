// TODO: Implement the ability to do this with unsigned numbers also. 
// TODO: Combine all the carry-save adder generate blocks into one generate block.
// EXTRA: index the carry-save adder structure so this multiplier works for N being any power of 2.

// This assumes that the inputs are 32-bit 2's-complement signed integers.
// Multiply (multiplicand) A by (multiplier) B to get (product) P.
module MUL32 (input signed [31:0] iA, input signed [31:0] iB, output signed [63:0] oP);

localparam N = 32;

// The number of booth encoded values.
localparam BTH = (N+1)/2; // = 16
// For an ideal cascade of 4-to-2 reducers to align with the number of inputs, we need N to be a power of 2.
// Number of levels of Carry-Save Addition (CSA) using 4-to-2 reducers.
// localparam CSA_levels = $clog2(BTH); // = 4
// # of 4-to-2 reducers in each level of CSA.
// localparam reducers_in_CSA_level1 = BTH/4; // = 4
// localparam reducers_in_CSA_level2 = CSA_level1*2/4; // = 2
// localparam reducers_in_CSA_level3 = CSA_level2*2/4; // = 1
// Final Carry-Propagate Addition (CPA) is done using the final 2 outputs from the last level of CSA.

// Extend by 1 bit to handle negation
wire signed [N+1:0] A, negA;
wire signed [N+1:0] A2, negA2;
wire [N+1:0] notA;
wire [BTH-1:0] booth_sign;
wire [1:0] booth_magnitude [BTH-1:0];
wire [2*BTH-1:0] flat_booth_magnitude;

assign A = {{2{iA[N-1]}}, iA};
assign negA = notA + 1'b1;
assign A2 = {iA[N-1], iA, 1'b0};
assign negA2 = {negA[N:0], 1'b0};

// Compute the Booth Encoding of the multiplier (B).
genvar i;
generate
for (i = 0; i < N+2; i = i + 1) begin : gen_notA
    assign notA[i] = ~A[i];
end
for (i = 0; i < BTH; i = i + 1) begin : map_booth_magnitude
    assign booth_magnitude[i] = {flat_booth_magnitude[i+BTH], flat_booth_magnitude[i]};
end
endgenerate

BoothEncode_2bit_Nbit #(N) be2bit(iB, booth_sign, flat_booth_magnitude[2*BTH-1:BTH], flat_booth_magnitude[BTH-1:0]);

wire signed [N+1:0] initialValue[BTH-1:0];

generate
    for (i = 0; i < BTH; i = i + 1) begin : gen_initialValue
        assign initialValue[i] = booth_magnitude[i][1] ? (booth_sign[i] ? negA2 : A2)
            : (booth_magnitude[i][0] ? (booth_sign[i] ? negA : A) 
            : {(N+1){1'b0}});
    end
endgenerate
/*
the s's in this diagram represent the sign bit of the initial values.
the z's in this diagram represent the padded zero bit of the initial values.
        00000000
ssssss0000000000
ssss0000000000zz
ss0000000000zzzz
0000000000zzzzzz
*/
wire signed [2*N-1:0] shiftedInitialValue[BTH-1:0];
generate
    for (i = 0; i < BTH; i = i + 1) begin : gen_shiftedInitialValue
        assign shiftedInitialValue[i] = {{(N-2*i){initialValue[i][N+1]}}, initialValue[i], {(2*i){1'b0}}};
    end
endgenerate
// CSA Layer 1: 16 numbers (34-bit each+shifts) -> 4*4-to-2 reducers. -> 8 numbers (64-bit each).
// Carry-Save Addition using 4-to-2 reducers.
/* same as this but with 32-bit numbers.
0 0000 0000 0000 0000
------00000000000000000 i = 0, j = 0
----00000000000000000--        j = 1
--00000000000000000----        j = 2
00000000000000000------        j = 3
....................... i = 1, j = 0
*/
// need to make sure that sign extension is done properly.
// The lowest 2 bits are piped directly to the output.
// We can ignore the upper bit from each reducer because it is place value 2*N, and the final result (oP) is only 2*N bits (not 2*N+1).
wire signed [2*N-1:2] iCSA1[3:0][3:0];
wire signed [2*N:2] oCSA1[3:0][1:0];
genvar j;
generate
    // i is the index of each reducer in the first layer.
    for (i = 0; i < 4; i = i + 1) begin : gen_CSA1
        for (j = 0; j < 4; j = j + 1) begin : gen_CSA1_shift
            assign iCSA1[i][j] = shiftedInitialValue[4*i+j][2*N-1:2];
        end
        Reducer4to2_Nbit #(2*N-2) CSA1_i(
            .iW(iCSA1[i][3]), .iX(iCSA1[i][2]), .iY(iCSA1[i][1]), .iZ(iCSA1[i][0]), .iCarry(1'b0), 
            .oSum1(oCSA1[i][1][2*N:3]), .oSum0(oCSA1[i][0][2*N:2]));
        assign oCSA1[i][1][2] = 1'b0;
    end
endgenerate

// CSA Layer 2: 8 numbers -> 2*4-to-2 reducers. -> 4 numbers
wire [2*N-1:2] iCSA2[1:0][3:0];
wire [2*N:2] oCSA2[1:0][1:0];
generate
    for (i = 0; i < 2; i = i + 1) begin : gen_CSA2
        for (j = 0; j < 4; j = j + 1) begin : gen_CSA2_shift
            assign iCSA2[i][j] = oCSA1[2*i+j/2][j%2][2*N-1:2];
        end
        Reducer4to2_Nbit #(2*N-2) CSA2_i(
            .iW(iCSA2[i][3]), .iX(iCSA2[i][2]), .iY(iCSA2[i][1]), .iZ(iCSA2[i][0]), .iCarry(1'b0), 
            .oSum1(oCSA2[i][1][2*N:3]), .oSum0(oCSA2[i][0][2*N:2]));
        assign oCSA2[i][1][2] = 1'b0;
    end
endgenerate

// CSA Layer 3: 4 numbers -> 1*4-to-2 reducer -> 2 numbers
wire [2*N-1:2] iCSA3[3:0];
wire [2*N:2] oCSA3[1:0];
generate
    for (i = 0; i < 4; i = i + 1) begin : gen_CAS3
        assign iCSA3[i] = oCSA2[i/2][i%2][2*N-1:2];
    end
endgenerate
Reducer4to2_Nbit #(2*N-2) CSA3(
    .iW(iCSA3[3]), .iX(iCSA3[2]), .iY(iCSA3[1]), .iZ(iCSA3[0]), .iCarry(1'b0), 
    .oSum1(oCSA3[1][2*N:3]), .oSum0(oCSA3[0][2*N:2]));
assign oCSA3[1][2] = 1'b0;

// Carry-Propagate Addition using final 2 outputs from carry-save adders.
assign oP = {oCSA3[1][2*N-1:2] + oCSA3[0][2*N-1:2], initialValue[0][1:0]};

endmodule

module BoothEncode_2bit_Nbit #(parameter N = 32) (input signed [N-1:0] iA, output [(N+1)/2-1:0] oSign, output [(N+1)/2-1:0] oMagnitude1, output [(N+1)/2-1:0] oMagnitude0);

wire [N+1:0] A2;
assign A2 = {iA[N-1], iA, 1'b0};


genvar i;
generate
    for (i = 1; i+1 <= N+1; i = i + 2) begin : gen
        BoothEncode_2bit be2bit(A2[i+1:i-1], oSign[i/2], {oMagnitude1[i/2], oMagnitude0[i/2]});
    end
endgenerate
endmodule


// 0, 1, 2, -2, -1,
// 1 bit for sign: 0 = positive/zero, 1 = negative
// 2 bits for magnitude: 0 = 00, 1 = 01, 2 = 10
// table
//     // iA  : oSign  oMagnitude
//     3'b000 : 0      2'b00;
//     3'b001 : 0      2'b01;
//     3'b010 : 0      2'b01;
//     3'b011 : 0      2'b10;
//     3'b100 : 1      2'b10;
//     3'b101 : 1      2'b01;
//     3'b110 : 1      2'b01;
//     3'b111 : 0      2'b00; // making sure that there is no sign for zero.
// endtable
module BoothEncode_2bit(input [2:0] iA, output oSign, output [1:0] oMagnitude);

assign oSign = iA[2] & (~iA[1] | ~iA[0]);
assign oMagnitude[0] = iA[1] ^ iA[0];
assign oMagnitude[1] = (iA[2] && !(iA[1] || iA[0])) || (!iA[2] && (iA[1] && iA[0]));

endmodule

module Reducer4to2_Nbit #(parameter N = 32) (input [N-1:0] iW, input [N-1:0] iX, input [N-1:0] iY, input [N-1:0] iZ, input iCarry, output [N-1:0] oSum1, output [N:0] oSum0);

wire carry [N:0];

assign carry[0] = iCarry;

genvar i;
generate
for (i = 0; i < N; i = i + 1) begin : gen
    Reducer4to2 r4to2({iW[i], iX[i], iY[i], iZ[i]}, carry[i], {oSum1[i], oSum0[i]}, carry[i+1]);
end
endgenerate

assign oSum0[N] = carry[N];

endmodule

// oCarry is of the same place value of the most significant bit of the sum. https://www.geoffknagge.com/fyp/carrysave.shtml
module Reducer4to2 (input [3:0] iA, input iCarry, output [1:0] oSum, output oCarry);
wire w, x, y, z;
assign {w, x, y, z} = iA;

// used Karnaugh Maps to simplify the equations (https://www.charlie-coleman.com/experiments/kmap/)

assign oSum[1] = (w & x & y & z) | (iCarry & (w ^ x ^ y ^ z));

assign oSum[0] = iCarry ^ w ^ x ^ y ^ z;

assign oCarry = (w | x | y) & (w | x | z) & (w | y | z) & (x | y | z);

endmodule
