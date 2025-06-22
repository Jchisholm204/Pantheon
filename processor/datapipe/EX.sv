/**
 * @file EX.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief 
 * @version 0.1
 * @date Created: 2025-06-21
 * @modified Last Modified: 2025-06-21
 *
 * @copyright Copyright (c) 2025
 */

`timescale 1ns/100ps

import rv32_isa::*;
import pipeline_types::id_ex_t;
import pipeline_types::ex_mem_t;

module EX(
    input logic iClk, iEn, nRst, iStall,
    input id_ex_t iID,
    output ex_mem_t oMEM
);

endmodule

