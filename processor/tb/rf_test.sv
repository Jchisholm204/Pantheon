/**
 * @file rf_test.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief 
 * @version 0.1
 * @date Created: 2025-05-17
 * @modified Last Modified: 2025-05-17
 *
 * @copyright Copyright (c) 2025
 */
`timescale 1ps/1ns

module rf_test();
wire Clk, nRst;

testClock clock(
    .nRst(nRst),
    .oClk(Clk)
);

logic w_en;
logic [4:0] addr_rd, addr_rs1, addr_rs2;

logic [31:0] Rd, Rs, Rt;

register_file rf(
    .iClk(Clk),
    .nRst(nRst),
    .iWriteEn(w_en),
    .iAddr_Rd(addr_rd),
    .iAddr_Rs1(addr_rs1),
    .iAddr_Rs2(addr_rs2),
    .iRd(Rd),
    .oRs1(Rs),
    .oRs2(Rt)
);

initial begin
    nRst = 1'b0;
    #10;
    nRst = 1'b1;
    #10;
    w_en = 1'b1;
    for(int i = 1; i < 31; i++) begin
        addr_rd = i;
    end
end

endmodule
