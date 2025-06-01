/**
 * @file IF.sv
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief Instruction Fetch
 * @version 0.1
 * @date Created: 2025-05-25
 * @modified Last Modified: 2025-05-25
 *
 * @copyright Copyright (c) 2025
 */

module IF(
    iClk, iEn, nRst,
    iPC_ext,
    iPC, iMemIns,
    oPC, oIR
);
input wire iClk, iEn, nRst;
input wire iPC_ext;
input wire [31:0] iPC, iMemIns;
output wire [31:0] oPC, oIR;

reg [31:0] IR, PC;

// Next PC calculation
wire [31:0] PCn, PC4;
assign PC4 = PC + 32'd4;
assign PCn = iPC_ext ? iPC : PC4;

always_ff @(posedge iClk, negedge nRst) begin
    if(!nRst) begin
        IR <= 32'd0;
        PC <= 32'd0;
    end else begin
        if(iEn) begin
            IR <= iMemIns;
            PC <= PCn;
        end
    end
end

// Assign module outputs
assign oPC = PC4;
assign oIR = IR;

endmodule

