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
`timescale 1ns/100ps
import rv32_isa::RegWidth;
import rv32_isa::RegAddrWidth;

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
for(i=1; i < NRegs; i++) begin : gen_registers
    logic [RegWidth-1:0] R;
    always_ff @(posedge iClk, negedge nRst) begin : reg_write
        if(!nRst)
            R <= {RegWidth{1'b0}};
        else begin
            if(iWriteEn & (iAddr_Rd == i[RegAddrWidth-1:0]))
                R <= iRd;
        end
    end

    assign oRs1 = (iAddr_Rs1 == i[RegAddrWidth-1:0]) ? R : 'z;
    assign oRs2 = (iAddr_Rs2 == i[RegAddrWidth-1:0]) ? R : 'z;
end
endgenerate

// Assign Zero Register
assign oRs1 = (iAddr_Rs1 == {RegAddrWidth{1'b0}}) ? {RegWidth{1'b0}} : 'z;
assign oRs2 = (iAddr_Rs2 == {RegAddrWidth{1'b0}}) ? {RegWidth{1'b0}} : 'z;

endmodule;
