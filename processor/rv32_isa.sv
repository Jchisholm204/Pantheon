/**
 * @file rv32_isa.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief Definitions for working with the RV32 ISA
 * @version 0.1
 * @date Created: 2025-05-16
 * @modified Last Modified: 2025-05-16
 *
 * @copyright Copyright (c) 2025
 */

package rv32_isa;

localparam logic [6:0] OpAluR    = 7'b0110011;
localparam logic [6:0] OpAluI    = 7'b0010011;
localparam logic [6:0] OpStore   = 7'b0100011;
localparam logic [6:0] OpLoad    = 7'b0000011;
localparam logic [6:0] OpMscMem  = 7'b0001111;
localparam logic [6:0] OpJal     = 7'b1101111;
localparam logic [6:0] OpJalR    = 7'b1100111;
localparam logic [6:0] OpBranch  = 7'b1100011;
localparam logic [6:0] OpSysCall = 7'b1110011;
localparam logic [6:0] OpLUI     = 7'b0110111;
localparam logic [6:0] OpAUIPC   = 7'b0110111;

// Function 7 - ALU Instructions
localparam logic [6:0] OpF7ADD = 7'b0000000;
localparam logic [6:0] OpF7SUB = 7'b0100000;
localparam logic [6:0] OpF7SLL = 7'b0000000;
localparam logic [6:0] OpF7SLT = 7'b0000000;
localparam logic [6:0] OpF7SLTU= 7'b0000000;
localparam logic [6:0] OpF7XOR = 7'b0000000;
localparam logic [6:0] OpF7SRL = 7'b0000000;
localparam logic [6:0] OpF7SRA = 7'b0100000;
localparam logic [6:0] OpF7OR  = 7'b0000000;
localparam logic [6:0] OpF7AND = 7'b0000000;
// Function 7 - M Extention
localparam logic [6:0] OpF7MUL = 7'b0000001;

// Immediate [11:5] - For Shifts
localparam logic [6:0] OpImSLLI = 7'b0000000;
localparam logic [6:0] OpImSRLI = 7'b0000000;
localparam logic [6:0] OpImSRAI = 7'b0100000;
// Immediate [11:0] - For ECALL/EBREAK
localparam logic [11:0] OpImCall = 12'b000000000000;
localparam logic [11:0] OpImBrk  = 12'b000000000001;

// Function 3 - ALU Instructions
localparam logic [2:0] OpF3ADD  = 3'b000;
localparam logic [2:0] OpF3SUB  = 3'b000;
localparam logic [2:0] OpF3SLL  = 3'b001;
localparam logic [2:0] OpF3SLT  = 3'b010;
localparam logic [2:0] OpF3SLTU = 3'b011;
localparam logic [2:0] OpF3XOR  = 3'b100;
localparam logic [2:0] OpF3SRL  = 3'b101;
localparam logic [2:0] OpF3SRA  = 3'b101;
localparam logic [2:0] OpF3OR   = 3'b110;
localparam logic [2:0] OpF3AND  = 3'b111;

// Function 3 - Store Instructions
localparam logic [2:0] OpF3SB   = 3'b000;
localparam logic [2:0] OpF3SH   = 3'b001;
localparam logic [2:0] OpF3SW   = 3'b010;
// Function 3 - Load Instructions
localparam logic [2:0] OpF3LB   = 3'b000;
localparam logic [2:0] OpF3LH   = 3'b001;
localparam logic [2:0] OpF3LW   = 3'b010;
localparam logic [2:0] OpF3LBU  = 3'b100;
localparam logic [2:0] OpF3LHU  = 3'b101;
// Function 3 - Misc Mem Instructions
localparam logic [2:0] OpF3FENCE = 3'b000;
localparam logic [2:0] OpF3FencI = 3'b001;
// Function 3 - Branch Instructions
localparam logic [2:0] OpF3BEQ  = 3'b000;
localparam logic [2:0] OpF3BNE  = 3'b001;
localparam logic [2:0] OpF3BLT  = 3'b100;
localparam logic [2:0] OpF3BGE  = 3'b101;
localparam logic [2:0] OpF3BLTU = 3'b110;
localparam logic [2:0] OpF3BGEU = 3'b111;
// Function 3 - SysCall Instructions
localparam logic [2:0] OpF3ECALL  = 3'b000;
localparam logic [2:0] OpF3EBREAK = 3'b000;
localparam logic [2:0] OpF3CSRRW  = 3'b001;
localparam logic [2:0] OpF3CSRRS  = 3'b010;
localparam logic [2:0] OpF3CSRRC  = 3'b011;
localparam logic [2:0] OpF3CSRRWI = 3'b101;
localparam logic [2:0] OpF3CSRRCI = 3'b110;
localparam logic [2:0] OpF3CSRRSI = 3'b111;
// Function 3 - M Extention
localparam logic [2:0] OpF3MUL    = 3'b000;
localparam logic [2:0] OpF3MULH   = 3'b001;
localparam logic [2:0] OpF3MULHSU = 3'b010;
localparam logic [2:0] OpF3MULHU  = 3'b011;
localparam logic [2:0] OpF3DIV    = 3'b100;
localparam logic [2:0] OpF3DIVU   = 3'b101;
localparam logic [2:0] OpF3REM    = 3'b110;
localparam logic [2:0] OpF3REMU   = 3'b111;

localparam int RegAddrWidth = 5;
localparam int RegWidth = 32;

endpackage
