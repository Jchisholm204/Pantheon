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
    output id_ex_t oEX,
    // Register File Signals
    input logic [RegWidth-1:0] iRs1, iRs2,
    output logic [RegAddrWidth-1:0] oAddrRs1, oAddrRs2,
    // External Control Signals
    output logic oBrTrue,
    output logic [RegWidth-1:0] oBrPc
);

// Instruction Decode Signals
logic [RegAddrWidth-1:0] dec_rs1, dec_rs2;
logic [RegAddrWidth-1:0] dec_rd;
logic [6:0] dec_opcode, dec_func7;
logic [2:0] dec_func3;
logic [RegWidth-1:0] dec_immI, dec_immU, dec_immJ,
                     dec_immB, dec_immS;

decoder dec(
    .iINS(iIF.instruction),
    .oOpCode(dec_opcode),
    .oRS1(dec_rs1),
    .oRS2(dec_rs2),
    .oRD(dec_rd),
    .oFunc3(dec_func3),
    .oFunc7(dec_func7),
    .oImmI(dec_immI),
    .oImmU(dec_immU),
    .oImmJ(dec_immJ),
    .oImmB(dec_immB),
    .oImmS(dec_immS)
);


// OpCode one hot signals
logic OP_ALUR, OP_ALUI, OP_Store, OP_Load, OP_JAL, OP_JALR;
logic OP_Branch, OP_SysCall, OP_LUI, OP_AUIPC;
assign OP_ALUR    = dec_opcode == OpAluR;
assign OP_ALUI    = dec_opcode == OpAluI;
assign OP_Store   = dec_opcode == OpStore;
assign OP_Load    = dec_opcode == OpLoad;
assign OP_JAL     = dec_opcode == OpJal;
assign OP_JALR    = dec_opcode == OpJalR;
assign OP_Branch  = dec_opcode == OpBranch;
assign OP_SysCall = dec_opcode == OpSysCall;
assign OP_LUI     = dec_opcode == OpLUI;
assign OP_AUIPC   = dec_opcode == OpAUIPC;

// OpCode Formats
logic OPF_I, OPF_U, OPF_R, OPF_B, OPF_J, OPF_S;
assign OPF_I = (OP_ALUI | OP_JALR | OP_Load);
assign OPF_U = (OP_LUI | OP_AUIPC);
assign OPF_R = (OP_ALUR | OP_AUIPC);
assign OPF_B = (OP_Branch);
assign OPF_J = (OP_JAL);
assign OPF_S = (OP_Store);

// Register Address Enables
logic rs1_en, rs2_en, rd_en, imm_en;
assign rs1_en = OPF_I | OPF_R | OPF_B | OPF_S;
assign rs2_en = OPF_R | OPF_B | OPF_S;
assign rd_en  = OPF_I | OPF_U | OPF_R | OPF_J;
assign imm_en = OPF_I | OPF_U | OPF_J | OPF_B | OPF_S;

// Pipeline Control Outputs
always_ff @(posedge iClk, negedge nRst) begin
    if(!nRst) begin
        oEX <= '0;
    end
    if(!iStall) begin
        oEX.ctrl.mem_en <= OP_Store | OP_Load;
        oEX.ctrl.ex_en <= OP_ALUR | OP_ALUI;
        oEX.ctrl.wb_en  <= rd_en;
        oEX.ctrl.imm_en <= imm_en;
        oEX.ctrl.valid <= ~iStall;
        oEX.ctrl.opcode <= dec_opcode;
        oEX.ctrl.func3  <= dec_func3;
        oEX.ctrl.func7  <= dec_func7;
        oEX.rs1.value <= rs1_en ? iRs1    : {RegWidth{1'b0}};
        oEX.rs1.addr  <= rs1_en ? dec_rs1 : {RegAddrWidth{1'b0}};
        oEX.rs2.value <= rs2_en ? iRs2    : {RegWidth{1'b0}};
        oEX.rs2.addr  <= rs2_en ? dec_rs2 : {RegAddrWidth{1'b0}};
        oEX.rd_addr   <= rd_en  ? dec_rd  : {RegAddrWidth{1'b0}};
        oEX.immediate <= OPF_I ? dec_immI :
            OPF_U ? dec_immU :
            OPF_B ? dec_immB :
            OPF_J ? dec_immJ :
            OPF_S ? dec_immS :
            32'd0;
    end
end

// Branch Outcome Signals
logic brtrue;
BranchOutcome bpred(
    .iRs1(iRs1),
    .iRs2(iRs2),
    .iFunc3(dec_func3),
    .oBrTrue(brtrue)
);

assign oBrTrue = (brtrue & OP_Branch) | OPF_J;
assign oBrPc = OPF_J ? oEX.immediate : iID.pc4 + oEX.immediate;

endmodule

