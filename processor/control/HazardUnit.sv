/**
 * @file HazardUnit.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief 
 * @version 0.1
 * @date Created: 2025-07-06
 * @modified Last Modified: 2025-07-06
 *
 * @copyright Copyright (c) 2025
 */

`timescale 1ns/100ps
import pipeline_types::*;

module HazardUnit(
    input logic iClk, nRst,
    input logic iBrTrue,
    input if_id_t iIF_ID,
    input id_ex_t iID_EX,
    input ex_mem_t iEX_ME,
    input mem_wb_t iME_WB,
    output logic oStall_IF,
    output logic oStall_ID,
    output logic oStall_EX,
    output logic oStall_ME,
    output logic oFwExS1_en,
    output logic oFwExS2_en,
    output logic oFwMeS1_en,
    output logic oFwMeS2_en,
    output logic oRst_IF,
    output logic oRst_ID,
    output logic oRst_EX,
    output logic oRst_ME
);


endmodule

