/**
 * @file ISA.vh
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief 
 * @version 0.1
 * @date Created: 2025-05-10
 * @modified Last Modified: 2025-05-10
 *
 * @copyright Copyright (c) 2025
 */


/*
* ALU Instructions
*  - Uses different opcodes for Immediate vs Register operands
*  - I and R-Type instruction formats
*  - Function 3 remains unchanged
*/
`define ISA_OP_ALUR 7'b0110011
`define ISA_OP_ALUI 7'b0010011
// Function 7
`define ISA_F7_ADD  7'b0000000
`define ISA_F7_SUB  7'b0100000
`define ISA_F7_SLL  7'b0000000
`define ISA_F7_SLT  7'b0000000
`define ISA_F7_SLTU 7'b0000000
`define ISA_F7_XOR  7'b0000000
`define ISA_F7_SRL  7'b0000000
`define ISA_F7_SRA  7'b0100000
`define ISA_F7_OR   7'b0000000
`define ISA_F7_AND  7'b0000000
// M Extention
`define ISA_F7_MUL  7'b0000001

// Immediate [11:5] - For Shifts
`define ISA_IM_SLLI 7'b0000000
`define ISA_IM_SRLI 7'b0000000
`define ISA_IM_SRAI 7'b0100000

// Function 3
`define ISA_F3_ADD  3'b000
`define ISA_F3_SUB  3'b000
`define ISA_F3_SLL  3'b001
`define ISA_F3_SLT  3'b010
`define ISA_F3_SLTU 3'b011
`define ISA_F3_XOR  3'b100
`define ISA_F3_SRL  3'b101
`define ISA_F3_SRA  3'b101
`define ISA_F3_OR   3'b110
`define ISA_F3_AND  3'b111
// M Extention
`define ISA_F3_MUL   3'b000
`define ISA_F3_MULH  3'b001
`define ISA_F3_MULSU 3'b010
`define ISA_F3_MULU  3'b011
`define ISA_F3_DIV   3'b100
`define ISA_F3_DIVU  3'b101
`define ISA_F3_REM   3'b110
`define ISA_F3_REMU  3'b111

/*
* Store Type Instructions
*  - Uses S-Type Format
*/
`define ISA_OP_STORE  7'b0100011

// Function 3
`define ISA_F3_SB 3'b000
`define ISA_F3_SH 3'b001
`define ISA_F3_SW 3'b010

/*
* Load Type Instructions
*  - Uses I-Type Format
*/
`define ISA_OP_LOAD   7'b0000011

// Load Function 3
`define ISA_F3_LB  3'b000
`define ISA_F3_LH  3'b001
`define ISA_F3_LW  3'b010
`define ISA_F3_LBU 3'b100
`define ISA_F3_LHU 3'b101

/*
* Fence Instructions
*  - Uses I-Type Format
*/
`define ISA_OP_FENCE  7'b0001111

`define ISA_F3_FENCE  3'b000
`define ISA_F3_FENCEI 3'b001

/*
* Control Flow Instructions
*/
// Jal is UI type
`define ISA_OP_JAL  7'b1101111
// Jalr is I type
`define ISA_OP_JALR 7'b1100111

// Branch Instructions (Conditional Jumps) - SB-Type
`define ISA_OP_BRANCH 7'b1100011
`define ISA_F3_BEQ  3'b000
`define ISA_F3_BNE  3'b001
`define ISA_F3_BLT  3'b100
`define ISA_F3_BGE  3'b101
`define ISA_F3_BLTU 3'b110
`define ISA_F3_BGEU 3'b111

/*
* Load Type Instructions
*  - Uses I-Type Format
*/
`define ISA_OP_SYSCALL 7'b1110011

// Immediate [11:0] - For ECALL/EBREAK
`define ISA_IM_ECALL  12'b000000000000
`define ISA_IM_EBREAK 12'b000000000001

// Function 3
`define ISA_F3_ECALL  3'b000
`define ISA_F3_EBREAK 3'b000
`define ISA_F3_CSRRW  3'b001
`define ISA_F3_CSRRS  3'b010
`define ISA_F3_CSRRC  3'b011
`define ISA_F3_CSRRWI 3'b101
`define ISA_F3_CSRRCI 3'b110
`define ISA_F3_CSRRSI 3'b111


// U Type Instructions
`define ISA_OP_LUI   7'b0110111
`define ISA_OP_AUIPC 7'b0110111




