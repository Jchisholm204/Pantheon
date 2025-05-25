/**
 * @file control.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief 
 * @version 0.1
 * @date Created: 2025-05-25
 * @modified Last Modified: 2025-05-25
 *
 * @copyright Copyright (c) 2025
 */

import rv32_isa::*;

module control(
    iClk, nRst,
    iMemIns,
    oMEM_en, oALU_en, oRF_en,
    oRs1, oRs2, oRd,
    oFunc3, oFunc7,
    oImm_en,
    oImm32
);
input wire iClk, nRst;
input wire [31:0] iMemIns;
output logic oMEM_en, oALU_en, oRF_en;
output wire [RegAddrWidth-1:0] oRs1, oRs2, oRd;
output wire [2:0] oFunc3; 
output wire [6:0] oFunc7;
output logic oImm_en;
output logic [31:0] oImm32;

// ID Wires
wire [6:0] ID_OpCode, ID_F7;
wire [2:0] ID_F3;
wire [RegAddrWidth-1:0] ID_Rs1, ID_Rs2, ID_Rd;
wire [31:0] ID_ImmI, ID_ImmU, ID_ImmJ, ID_ImmB, ID_ImmS;

decoder ID(
    .iINS(iMemIns),
    .oOpCode(ID_OpCode),
    .oRS1(ID_Rs1),
    .oRS2(ID_Rs2),
    .oRD(ID_Rd),
    .oFunc3(ID_F3),
    .oFunc7(ID_F7),
    .oImmI(ID_ImmI),
    .oImmU(ID_ImmU),
    .oImmJ(ID_ImmJ),
    .oImmB(ID_ImmB),
    .oImmS(ID_ImmS)
);

// OpCode one hot signals
wire OP_ALUR, OP_ALUI, OP_Store, OP_Load, OP_JAL, OP_JALR;
wire OP_Branch, OP_SysCall, OP_LUI, OP_AUIPC;

assign OP_ALUR    = ID_OpCode == OpAluR;
assign OP_ALUI    = ID_OpCode == OpAluI;
assign OP_Store   = ID_OpCode == OpStore;
assign OP_Load    = ID_OpCode == OpLoad;
assign OP_JAL     = ID_OpCode == OpJal;
assign OP_JALR    = ID_OpCode == OpJalR;
assign OP_Branch  = ID_OpCode == OpBranch;
assign OP_SysCall = ID_OpCode == OpSysCall;
assign OP_LUI     = ID_OpCode == OpLUI;
assign OP_AUIPC   = ID_OpCode == OpAUIPC;

// OpCode Formats
wire OPF_I, OPF_U, OPF_R, OPF_B, OPF_J, OPF_S;
assign OPF_I = (OP_ALUI | OP_JALR | OP_Load);
assign OPF_U = (OP_LUI | OP_AUIPC);
assign OPF_R = (OP_ALUR | OP_AUIPC);
assign OPF_B = (OP_Branch);
assign OPF_J = (OP_JAL);
assign OPF_S = (OP_Store);

// Register Address Enables
wire Rs1_en, Rs2_en, Rd_en;
assign Rs1_en = OPF_I | OPF_R | OPF_B | OPF_S;
assign Rs2_en = OPF_R | OPF_B | OPF_S;
assign Rd_en  = OPF_I | OPF_U | OPF_R | OPF_J;

// Register Address Assignments
assign oRs1 = Rs1_en ? ID_Rs1 : {RegAddrWidth{1'b0}};
assign oRs2 = Rs2_en ? ID_Rs2 : {RegAddrWidth{1'b0}};
assign oRd  = Rd_en  ? ID_Rd  : {RegAddrWidth{1'b0}};
assign oRF_en = Rd_en;

// Control Enable Signals
assign oMEM_en = OP_Store | OP_Load;
assign oALU_en = OP_ALUR | OP_ALUI;

// Immediate Value Assignment
assign oImm32 = OPF_I ? ID_ImmI :
                OPF_U ? ID_ImmU :
                OPF_B ? ID_ImmB :
                OPF_J ? ID_ImmJ :
                OPF_S ? ID_ImmS :
                32'd0;
assign oImm_en = OPF_I | OPF_U | OPF_B | OPF_J | OPF_S;

// Function Codes
assign oFunc3 = ID_F3;
assign oFunc7 = ID_F7;

endmodule
