import rv32_isa::RegWidth;
import rv32_isa::RegAddrWidth;
module rf_wrapper #(
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

register_file #(
    .NRegs(NRegs)
) rf (
    .iClk(iClk),
    .nRst(nRst),
    .iWriteEn(iWriteEn),
    .iAddr_Rd(iAddr_Rd),
    .iAddr_Rs1(iAddr_Rs1),
    .iAddr_Rs2(iAddr_Rs2),
    .iRd(iRd),
    .oRs1(oRs1),
    .oRs2(oRs2)
);

initial begin
    $dumpfile("dump.vcd");
    $dumpvars(0, rf);
end

endmodule
