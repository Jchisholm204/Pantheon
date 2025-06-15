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
import pipeline_types::if_id_t;
import pipeline_types::id_ex_t;
import pipeline_types::pipe_control_t;

module ID (
    // Pipeline Signals
    input wire iClk, iEn, nRst, iStall,
    input if_id_t iIF,
    input logic [RegWidth-1:0] iRs1, iRs2,
    output logic [RegAddrWidth-1:0] oAddrRs1, oAddrRs2,
    output id_ex_t oEX
);

logic [RegWidth-1:0] ImmI, ImmU, ImmJ, ImmB, ImmS;

decoder dec(
    .iINS(iIF.instruction),
    .oOpCode(oEX.ctrl.opcode),
    .oRS1(oEX.rs1.addr),
    .oRS2(oEX.rs2.addr),
    .oRD(oEX.rd_addr),
    .oFunc3(oEX.ctrl.func3),
    .oFunc7(oEX.ctrl.func7),
    .oImmI(ImmI),
    .oImmU(ImmU),
    .oImmJ(ImmJ),
    .oImmB(ImmB),
    .oImmS(ImmS)
);

endmodule

