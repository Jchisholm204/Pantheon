/**
 * @file RegisterFile.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief 
 * @version 0.1
 * @date Created: 2025-06-14
 * @modified Last Modified: 2025-06-14
 *
 * @copyright Copyright (c) 2025
 */

`timescale 1ns/100ps
import reg_transport::reg_transport_t;
import rv32_isa::RegWidth;
import rv32_isa::RegAddrWidth;

module RegisterFile #(
    parameter int n_regs = 32,
    parameter reg_width = RegWidth,
    parameter addr_width = RegAddrWidth
    )(
    input logic iClk, nRst,
    input logic iWriteEn,
    input reg_transport_t  iRd,
    input logic iWriteEn_dbg,
    input reg_transport_t  iRd_dbg,
    input logic [addr_width-1:0] iAddrRs1,
    input logic [addr_width-1:0] iAddrRs2,
    input logic [addr_width-1:0] iAddrRs3,
    output logic [reg_width-1:0] oRs1,
    output logic [reg_width-1:0] oRs2,
    output logic [reg_width-1:0] oRs3
);

logic [reg_width-1:0] reg_outs[n_regs];

assign oRs1 = reg_outs[iAddrRs1];
assign oRs2 = reg_outs[iAddrRs2];
assign oRs3 = reg_outs[iAddrRs3];

reg_transport_t rd;
assign rd = iWriteEn_dbg ? iRd_dbg : iRd;

logic wen;
assign wen = iWriteEn | iWriteEn_dbg;

genvar i;
generate 
for(i=1; i < n_regs; i++) begin : gen_regs
    Register #(reg_width) Rx(
        .iClk(iClk),
        .nRst(nRst),
        .iWrite((rd.addr == i) & wen),
        .iD(rd.value),
        .oQ(reg_outs[i])
        );
end
endgenerate

endmodule
