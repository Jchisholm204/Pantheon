module DIV32(
    iSigned,
    iDivisor, iDividend,
    oQ, oR
);

input wire iSigned;
input wire [31:0] iDivisor, iDividend;
output logic [31:0] oQ, oR;

// Internal Signals for DIVisoR and DIVidenD
logic [31:0] divr, divd;

// Temporary Quotient
wire [31:0] Q;
// Accumulator
wire [31:0] A[31:0];

// Initialize the first partial remainder as 0
assign A[0] = 32'd0;

// Create 31 divisor levels
generate
    genvar i;
    for(i = 0; i < 31; i = i + 1) begin : gen_div_lvl
        DIV_LEVEL divlvl (
            .iA(A[i]),
            .iDivR(divr[31-i]),
            .iDivD(divd),
            .oA(A[i+1]),
            .oQ(Q[31-i])
        );
    end
endgenerate

// Final divisor Level
wire [31:0] shift, X, R;

assign shift = {A[31][30:0], divr[0]};
assign X = shift[31] ? shift + divd : shift - divd;
assign Q[0] = ~X[31];
// Remainder assignment
assign R = X[31] ? X + divd : X;

always_comb begin
    // Flip signs for signed division
    divr = iSigned && iDividend[31] ? (~iDividend + 1) : iDividend;
    divd = iSigned && iDivisor[31]  ? (~iDivisor + 1)  : iDivisor;

    // Compute remainder
    oR = iSigned && iDividend[31] ? (~R + 1) : R;

    // Compute quotient sign
    if (iSigned && (iDividend[31] ^ iDivisor[31]))
        oQ = (~Q + 1);  // negate result
    else
        oQ = Q;
end


endmodule

module DIV_LEVEL(
    iA, iDivD, iDivR,
    oA, oQ
);

input wire [31:0] iA, iDivD;
input wire iDivR;
// Output Accumulator
output wire [31:0] oA;
// Output Quotient
output wire oQ;

wire [31:0] shift;

// Shift in the next bit of the quotient
assign shift = {iA[30:0], iDivR};
// Add or subtract the divisor
assign oA = shift[31] ? shift + iDivD : shift - iDivD;
// Output 1 to result if the add/sub result was positive
assign oQ = ~oA[31];

endmodule
