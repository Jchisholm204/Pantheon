/**
 * @file control.v
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
* @brief 
 * @version 0.1
 * @date Created: 2025-05-11
* @modified Last Modified: 2025-05-11
 *
 * @copyright Copyright (c) 2025
 */

`include "ISA.vh"

module Control (
    // Clock, reset and ready signals
    // Ready is an active high that allows the next step to continue
    iClk, nRst, iRdy,
    // Data Memory Control
    oMemDRead, oMemDWrite,
    // Instruction Memory Control
    oMemIRead, iMemIns,
    // Pipe Control
    oPipe_nRst,
    // Program Counter Control
    oPC_nRst, oPC_en, oPC_tmpEn, oPC_load, oPC_offset,
    // Register File Control
    oRF_Write,
    oRF_AddrA, oRF_AddrB, oRF_AddrC,
    // Write Back Register Control
    oRWB_en,
    // Function Outputs
    oFunc3, oFunc7,
    // ALU Control
    oRA_en, oRB_en,
    oRZH_en, oRZL_en, oRAS_en,
    // Branch Conditional Evaluations (from pipeline)
    iBR_BEQ, iBR_BNE, iBR_BLT, iBR_BGE, iBR_BLTU, iBR_BGEU,
    // Port Register enable
    oREP_en,
    // Multiplexers
    oMUX_BIS, oMUX_RZHS, oMUX_WBM, oMUX_MAP, oMUX_ASS, oMUX_WBP, oMUX_WBE,
    // Imm32 Output
    oImm32
);

// Clock, reset and ready signals
// Ready is an active high that allows the next step to continue
input wire iClk, nRst, iRdy;
// Data Memory Control
output wire oMemDRead, oMemDWrite;
// Instruction Memory Control
output wire oMemIRead;
input wire [31:0] iMemIns;
// Pipe Control
output wire oPipe_nRst;
// Program Counter Control
output wire oPC_nRst, oPC_en, oPC_tmpEn, oPC_load, oPC_offset;
// Register File Control
output wire oRF_Write;
output wire [3:0] oRF_AddrA, oRF_AddrB, oRF_AddrC;
// Write Back Register Control
output wire oRWB_en;
// Function Outputs
output wire [2:0] oFunc3;
output wire [6:0] oFunc7;
// ALU Control
output wire [3:0] oALU_Ctrl;
output wire oRA_en, oRB_en;
output wire oRZH_en, oRZL_en, oRAS_en;
// Branch Conditional Evaluations (from pipeline)
input wire iBR_BEQ, iBR_BNE, iBR_BLT, iBR_BGE, iBR_BLTU, iBR_BGEU;
// External Port Enable
output wire oREP_en;
// Multiplexers
output wire oMUX_BIS, oMUX_RZHS, oMUX_WBM, oMUX_MAP, oMUX_ASS, oMUX_WBP, oMUX_WBE;
// Imm32 Output
output wire [31:0] oImm32;

// Step Counter
reg [5:1] Cycle;

// IR
wire IR_en;
wire [31:0] IR_out;

// Decoder IO
wire [3:0] ID_RA, ID_RB, ID_RC;
wire [4:0] ID_OpCode;
wire [31:0] ID_ImmI, ID_ImmU, ID_ImmJ, ID_ImmB, ID_ImmS;
wire [2:0] ID_Func3;
wire [6:0] ID_Func7;

// OpCode Decoded Wires
wire OP_ALUI, OP_ALUR, OP_STORE, OP_LOAD, 
     OP_FENCE, OP_JAL, OP_JALR, OP_BRANCH,
     OP_SYSCALL, OP_LUI, OP_AUIPC;
// Branch Conditional Wires
wire BR_BEQ, BR_BNE, BR_BLT, BR_BGE, BR_BLTU, BR_BGEU;
wire BR_TRUE;

// Assign Cycle
always @(posedge iClk or negedge nRst)
begin
    if(!nRst)
        Cycle = 5'b00001;
    else begin
        if(iRdy) Cycle = {Cycle[4:1], Cycle[5]};
    end
end

// Instruction Register
assign IR_en = Cycle[1];
REG32 IR(.iClk(iClk), .nRst(nRst), .iEn(IR_en), .iD(iMemIns), .oQ(IR_out));

// Decoder
isa_decoder decoder(
    .iINS(IR_out),
    .oOpCode(ID_OpCode),
    .oRS1(ID_RA),
    .oRS2(ID_RB),
    .oRD(ID_RC),
    .oFunc3(ID_Func3),
    .oFunc7(ID_Func7),
    .oImmI(ID_ImmI),
    .oImmU(ID_ImmU),
    .oImmJ(ID_ImmJ),
    .oImmB(ID_ImmB),
    .oImmS(ID_ImmS)
);

// Assign Function Outputs
assign oFunc3 = ID_Func3;
assign oFunc7 = ID_Func7;

// Assign OpCode Wires
assign OP_ALUI    = (ID_OpCode == `ISA_OP_ALUI);
assign OP_ALUR    = (ID_OpCode == `ISA_OP_ALUR);
assign OP_STORE   = (ID_OpCode == `ISA_OP_STORE);
assign OP_LOAD    = (ID_OpCode == `ISA_OP_LOAD);
assign OP_FENCE   = (ID_OpCode == `ISA_OP_FENCE);
assign OP_JAL     = (ID_OpCode == `ISA_OP_JAL);
assign OP_JALR    = (ID_OpCode == `ISA_OP_JALR);
assign OP_BRANCH  = (ID_OpCode == `ISA_OP_BRANCH);
assign OP_SYSCALL = (ID_OpCode == `ISA_OP_SYSCALL);
assign OP_LUI     = (ID_OpCode == `ISA_OP_LUI);
assign OP_AUIPC   = (ID_OpCode == `ISA_OP_AUIPC);

// Assign Branch Conditionals
assign BR_BEQ  = (ID_Func3 == `ISA_F3_BEQ)  & iBR_BEQ;
assign BR_BNE  = (ID_Func3 == `ISA_F3_BNE)  & iBR_BNE;
assign BR_BLT  = (ID_Func3 == `ISA_F3_BLT)  & iBR_BLT;
assign BR_BGE  = (ID_Func3 == `ISA_F3_BGE)  & iBR_BGE;
assign BR_BLTU = (ID_Func3 == `ISA_F3_BLTU) & iBR_BLTU;
assign BR_BGEU = (ID_Func3 == `ISA_F3_BGEU) & iBR_BGEU;
assign BR_TRUE = (BR_BEQ | BR_BNE | BR_BLT | BR_BGE | BR_BLTU | BR_BGEU) & OP_BRANCH;

// Assign Control outputs based on Codes and Cycle

// Pipe Reset Signal
assign oPipe_nRst = nRst;

// Program Counter Control Signals
// PC Reset (Should only be reset on CPU reset)
assign oPC_nRst = nRst;
// PC Load Enable
assign oPC_en = Cycle[1] || (Cycle[3] && (BR_TRUE || OP_JAL || OP_JFR));
assign oPC_tmpEn = Cycle[1];
// PC Jump Enable
assign oPC_offset = Cycle[3] && BR_TRUE;
assign oPC_load = Cycle[3] && (OP_JFR || OP_JAL);

// Register File Control Signals
assign oRF_Write = Cycle[5] && (OPF_R || (OPF_I && ~OP_DIV && ~OP_MUL && ~OP_ST) || OP_MFH || OP_MFL || OP_JAL || OP_IN);
// Note: Most ISA's use RC as the write back address, MiniSRC uses RA 
// RA is dependent on ISA type, use R0 if RA is not specified
// RA is used to load PC on JMP/JAL
assign oRF_AddrA =  (OPF_R | OPF_I) ? ID_RB :
                    (OPF_J) ? ID_RA : 4'h0;
// RB is dependent on ISA type, use R0 if RB is not specified
assign oRF_AddrB =  (OPF_I | OPF_B | OPF_J) ? ID_RA :
                    (OPF_R) ? ID_RC : 4'h0;
// Store is always RA
// ISA Specification states to store PC in r15 on JAL (Jump and Link)
assign oRF_AddrC = (OP_JAL) ? 4'h8 : ID_RA;

// Register File Write Back Register Load Enable
assign oRWB_en = 1'b1;

// ALU Control Signals Also, this should be renamed to "Ctrl" like the key on the keyboard.
assign oALU_Ctrl =  (OP_ADD || OP_ADDI) ? `CTRL_ALU_ADD :
                    (OP_SUB)            ? `CTRL_ALU_SUB :
                    (OP_OR  || OP_ORI)  ? `CTRL_ALU_OR  :
                    (OP_AND || OP_ANDI) ? `CTRL_ALU_AND :
                    (OP_MUL)            ? `CTRL_ALU_MUL :
                    (OP_DIV)            ? `CTRL_ALU_DIV :
                    (OP_SLL)            ? `CTRL_ALU_SLL :
                    (OP_SRL)            ? `CTRL_ALU_SRL :
                    (OP_SRA)            ? `CTRL_ALU_SRA :
                    (OP_ROR)            ? `CTRL_ALU_ROR :
                    (OP_ROL)            ? `CTRL_ALU_ROL :
                    (OP_NOT)            ? `CTRL_ALU_NOT :
                    (OP_NEG)            ? `CTRL_ALU_NEG :
                    // ALU Add is default for most instructions - so why not remove the (OP_ADD || OP_ADDI) ?
                    `CTRL_ALU_ADD;
// ALU Input A Register Load Enable
assign oRA_en = 1'b1; 
// ALU Input B Register Load Enable
assign oRB_en = 1'b1;

// ALU Result High Load EN
assign oRZH_en = 1'b1;
// ALU Result Low Load EN
assign oRZL_en = 1'b1;
// ALU Result Save EN
assign oRAS_en = (OP_DIV || OP_MUL);

// External Port Register Enable
assign oREP_en = OP_OUT && Cycle[4];

// ALU B Input Select (Selects Imm)
assign oMUX_BIS = OPF_I && ~(OP_DIV || OP_MUL);
// ALU Result High Select
assign oMUX_RZHS = (OP_MFH);
// RF Write Back Select
assign oMUX_WBM = (OP_LD);
// Memory Address Output Select
// assign oMUX_MA = Cycle[1];
assign oMUX_MAP = ~((OP_LD || OP_ST) && Cycle[4]);
// ALU Storage Select
assign oMUX_ASS = (OP_MFL || OP_MFH);
// Write Back Program Counter Select
assign oMUX_WBP = OP_JAL;
// Write Back External Port Select
assign oMUX_WBE = OP_IN;

// Immediate value output
// Assign Imm32 branch distance if the branch is true
assign oImm32 = OP_BRx ? ID_BRD : ID_imm32;

// Memory Read/Write Signals
assign oMemRead = Cycle[1] || (Cycle[4] && OP_LD);
assign oMemWrite = Cycle[4] && OP_ST;

endmodule
