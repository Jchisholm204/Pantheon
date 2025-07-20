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
    input logic [addr_width-1:0] iAddrRs1,
    input logic [addr_width-1:0] iAddrRs2,
    output logic [reg_width-1:0] oRs1,
    output logic [reg_width-1:0] oRs2,
    `ifndef RF_TOP
    BBUS_IF.slave dbg_acc
    `endif
);

logic [reg_width-1:0] reg_outs[n_regs];
logic write_en;
logic [addr_width-1:0] w_addr;
logic [reg_width-1:0] w_data;

assign oRs1 = reg_outs[iAddrRs1];
assign oRs2 = reg_outs[iAddrRs2];

always_comb begin
    `ifndef RF_TOP
    if(dbg_acc.read_en) begin
        dbg_acc.rdata = reg_outs[dbg_acc.addr];
        dbg_acc.read_ack = 1'b1;
    end else begin
        dbg_acc.rdata = 32'd0;
        dbg_acc.read_ack = 1'b0;
    end

    if(dbg_acc.write_en) begin
        w_addr = dbg_acc.addr;
        w_data = dbg_acc.wdata;
    end else begin
        w_addr = iRd.addr;
        w_data = iRd.value;
    end
    `endif
    `ifdef RF_TOP
    w_addr = iRd.addr;
    w_data = iRd.value;
    `endif
end

`ifndef RF_TOP
always_ff @(posedge iClk) begin
    if(dbg_acc.write_en)
        dbg_acc.write_ack <= 1'b1;
    else
        dbg_acc.write_ack <= 1'b0;
end

assign write_en = iWriteEn | dbg_acc.write_en;

`endif
`ifdef RF_TOP
assign write_en = iWriteEn;
`endif

genvar i;
generate
for(i=1; i < n_regs; i++) begin : gen_regs
    Register #(reg_width) Rx(
        .iClk(iClk),
        .nRst(nRst),
        .iWrite((w_addr == i) & write_en),
        .iD(w_data),
        .oQ(reg_outs[i])
        );
end
endgenerate

endmodule
