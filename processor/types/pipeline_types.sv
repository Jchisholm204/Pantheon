/**
 * @file pipeline_types.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief 
 * @version 0.1
 * @date Created: 2025-06-14
 * @modified Last Modified: 2025-06-14
 *
 * @copyright Copyright (c) 2025
 */


`timescale 1ns/100ps
import rv32_isa::RegWidth;
import rv32_isa::RegAddrWidth;
import reg_transport::reg_transport_t;

package pipeline_types;

typedef struct packed {
    logic valid;
    logic imm_en, wb_en, ex_en, mem_en;
    logic [6:0] func7;
    logic [2:0] func3;
    logic [6:0] opcode;
} pipe_control_t;

typedef struct packed {
    logic [31:0] pc;
    logic [31:0] pc4;
    logic [31:0] instruction;
} if_id_t;

typedef struct packed {
    logic [RegAddrWidth-1:0] rd_addr;
    logic [RegWidth-1:0] immediate;
    reg_transport_t rs1, rs2;
    pipe_control_t ctrl;
} id_ex_t;

typedef struct packed {
    pipe_control_t ctrl;
    reg_transport_t rs1, rs2;
    reg_transport_t rd;
} ex_mem_t;

typedef struct packed {
    pipe_control_t ctrl;
    reg_transport_t rd;
} mem_wb_t;

endpackage
