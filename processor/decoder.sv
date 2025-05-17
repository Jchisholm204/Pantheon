/**
 * @file decoder.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief Instruction Mapping Decoder
 * @version 0.1
 * @date Created: 2025-05-14
 * @modified Last Modified: 2025-05-14
 *
 * @copyright Copyright (c) 2025
 */
import rv32_isa::*;

module decoder (
    iINS,
    oOpCode,
    oRS1, oRS2, oRD,
    oFunc3, oFunc7,
    oImmI, oImmU, oImmJ, oImmB, oImmS
);

input  wire [RegWidth-1:0] iINS;
output wire [31:0] oOpCode;
output wire [RegAddrWidth-1:0] oRS1, oRS2, oRD;
output wire [2:0] oFunc3;
output wire [6:0] oFunc7;
output wire [31:0] oImmI;
output wire [31:0] oImmU;
output wire [31:0] oImmJ;
output wire [31:0] oImmB;
output wire [31:0] oImmS;

wire [11:0] ImmI;
wire [19:0] ImmU;
wire [20:0] ImmJ;
wire [11:0] ImmB;
wire [11:0] ImmS;

assign oOpCode = iINS[6:0];
assign oRS1 = iINS[19:15];
assign oRS2 = iINS[24:20];
assign oRD  = iINS[11:7];
assign oFunc3 = iINS[14:12];
assign oFunc7 = iINS[31:25];

assign ImmI = iINS[31:20];
assign ImmU = iINS[31:12];
assign ImmJ = {iINS[31], iINS[19:12], iINS[20], iINS[30:21], 1'b0};
assign ImmB = {iINS[31], iINS[7], iINS[30:25], iINS[11:6]};
assign ImmS = {iINS[31:25], iINS[11:7]};

assign oImmI = {{20{ImmI[11]}}, ImmI};
assign oImmU = {ImmU, 12'd0};
assign oImmJ = {{11{ImmJ[20]}}, ImmJ};
assign oImmB = {{19{ImmB[11]}}, ImmB};
assign oImmS = {{19{ImmS[11]}}, ImmS};

endmodule

