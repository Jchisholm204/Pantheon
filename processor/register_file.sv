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
output logic [RegWidth-1:0] oRs1, oRs2;

reg [RegWidth-1:0] registers [NRegs-1];

always_ff @(posedge iClk or negedge nRst) begin
    if(!nRst) begin
        for (int i = 1; i < NRegs; i++) begin
            registers[i] <= {RegWidth{1'b0}};
        end
    end else begin
        if(iWriteEn)
            registers[iAddr_Rd] <= iRd;
    end
end

always_ff @(negedge iClk) begin
    if(iAddr_Rs1 == {RegAddrWidth{1'b0}})
        oRs1 <= {RegWidth{1'b0}};
    else
        oRs1 <= registers[iAddr_Rs1];

    if(iAddr_Rs2 == {RegAddrWidth{1'b0}})
        oRs2 <= {RegWidth{1'b0}};
    else
        oRs2 <= registers[iAddr_Rs2];
end

// initial begin
//     $dumpfile("register_file.vcd");
//     $dumpvars(0, register_file);
// end

endmodule
