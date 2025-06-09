/**
 * @file ID.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief Instruction Decode Stage
 * @version 0.1
 * @date Created: 2025-05-25
 * @modified Last Modified: 2025-05-25
 *
 * @copyright Copyright (c) 2025
 */
`timescale 1ns/100ps
import rv32_isa::*;

module ID (
    // Pipeline Signals
    input wire iClk, iEn, nRst, iStall,
    input logic iWriteEn,
    // IF Signals
    input logic [31:0] iPC, iPC4, iINS,
    // Write Back Signals
    input logic [RegAddrWidth-1:0] iAddrRd,
    input logic [RegWidth-1:0] iRd,
    output logic [RegAddrWidth-1:0] oAddrRd, oAddrRs1, oAddrRs2,
    // Pipeline Output Signals
    output logic [RegWidth-1:0] oRs1, oRs2,
    output logic [6:0] oFunc7,
    output logic [2:0] oFunc3,
    // Control Signals
    output logic oPCS_EXT,
    output logic [31:0] oPC_EXT,
    output logic oMemEn, oWriteEn
);

logic [6:0] OpCode;
logic [RegAddrWidth-1:0] AddrRs1, AddrRs2, AddrRd;
logic [RegWidth-1:0] ImmI, ImmU, ImmJ, ImmB, ImmS;

register_file rf(
    .iClk(iClk),
    .nRst(nRst),
    .iWriteEn(iWriteEn),
    .iAddr_Rd(iAddrRd),
    .iAddr_Rs1(AddrRs1),
    .iAddr_Rs2(AddrRs2),
    .iRd(iRd),
    .oRs1(oRs1),
    .oRs2(oRs2)
);


decoder dec(
    .iINS(iINS),
    .oOpCode(OpCode),
    .oRS1(AddrRs1),
    .oRS2(AddrRs2),
    .oRD(AddrRd),
    .oFunc3(oFunc3),
    .oFunc7(oFunc7),
    .oImmI(ImmI),
    .oImmU(ImmU),
    .oImmJ(ImmJ),
    .oImmB(ImmB),
    .oImmS(ImmS)
);

endmodule

