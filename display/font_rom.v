module font_rom(
    iChar,
    iRow,
    oLine
);

input wire [7:0] iChar;
input wire [3:0] iRow;
output wire [7:0] oLine;

reg [7:0] font_mem [0:4095];

initial begin
    $readmemh("font8x16.hex", font_mem);
end

assign oLine = font_mem[{iChar, iRow}];

endmodule
