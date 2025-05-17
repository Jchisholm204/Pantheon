/**
 * @file register_file.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief Register File
 * @version 0.1
 * @date Created: 2025-05-16
 * @modified Last Modified: 2025-05-16
 *
 * @copyright Copyright (c) 2025
 */

import rv32_isa::RegWidth;
import rv32_isa::RegAddrWidth;

module register #(
    parameter logic [RegAddrWidth-1:0] Rid
)(
    iClk, nRst, iWriteEn,
    iAddrRs, iAddrRt, iAddrRd,
    iRd, oRs, oRt
);

input wire iClk, nRst, iWriteEn;
input wire [RegAddrWidth-1:0] iAddrRs, iAddrRt, iAddrRd;
input wire [RegWidth-1:0] iRd;
output wor [RegWidth-1:0] oRs, oRt;

logic [RegWidth-1:0] register;

always_ff @(posedge iClk, negedge nRst) begin : reg_write
    if(!nRst)
        register <= {RegWidth{1'b0}};
    else begin
        if(iWriteEn & (iAddrRd == Rid))
            register <= iRd;
    end
end

assign oRs = (iAddrRs == Rid) ? register : {RegWidth{1'b0}};
assign oRt = (iAddrRt == Rid) ? register : {RegWidth{1'b0}};

endmodule

module register_file #(
    parameter int NRegs = 32
)(
    iClk, nRst, iWriteEn,
    iAddr_Rd, iAddr_Rs1, iAddr_Rs2,
    iRd, oRs1, oRs2
);

input wire iClk, nRst, iWriteEn;
input wire [RegAddrWidth-1:0] iAddr_Rd, iAddr_Rs1, iAddr_Rs2;
input wire [RegWidth-1:0] iRd;
output wor [RegWidth-1:0] oRs1, oRs2;


genvar i;
generate
for(i=1; i < NRegs-1; i++) begin : gen_registers
    register #(i) R (
        .iClk(iClk),
        .nRst(nRst),
        .iWriteEn(iWriteEn),
        .iAddrRs(iAddr_Rs1),
        .iAddrRt(iAddr_Rs2),
        .iAddrRd(iAddr_Rd),
        .iRd(iRd),
        .oRs(oRs1),
        .oRt(oRs2)
        );
end
endgenerate

endmodule
