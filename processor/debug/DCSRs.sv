/**
 * @file DCSRs.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief Debug CSRs
 * @version 0.1
 * @date Created: 2025-08-03
 * @modified Last Modified: 2025-08-03
 *
 * @copyright Copyright (c) 2025
 */

`timescale 1ns/100ps
`include "reg_transport.svh"
`include "debug.svh"
import reg_transport::reg_transport_t;

module DCSRs(
    input logic iClk, iRst_n,
    input logic iRunning,
    output logic oHalt,
    output logic oHeartRst_n,
    // Command Connections
    input logic cmd_iBusy,
    input debug::cmderr_e cmd_iCerr,
    output debug::command_t cmd_oCmd,
    // System Bus Access
    input logic sb_iBusy,
    input debug::sberr_e sb_iErr,
    input logic [31:0] sb_iData,
    output logic [31:0] sb_oData,
    output logic [31:0] sb_oAddr,
    output logic sb_oRead,
    output logic sb_oWrite,
    output debug::sbaccess_e sb_oWidth,
    DBG_IF.processor dmi
);

endmodule

