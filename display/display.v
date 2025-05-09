/**
 * @file display.v
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief 
 * @version 0.1
 * @date Created: 2025-05-07
 * @modified Last Modified: 2025-05-07
 *
 * @copyright Copyright (c) 2025
 */

module display(
    iClk_50, nRst,
    // Outputs to the VGA hardware
    oVGA_R,
    oVGA_G,
    oVGA_B,
    oVGA_Clk,
    oVGA_Blank,
    oVGA_HSync,
    oVGA_VSync,
    oVGA_Sync
);

input wire iClk_50, nRst;
// Outputs to the VGA hardware
output wire [9:0] oVGA_R, oVGA_G, oVGA_B;
output wire oVGA_Clk, oVGA_Blank, oVGA_HSync, oVGA_VSync, oVGA_Sync;

reg [9:0] R, G, B;
wire [9:0] row, col;


vga_controller vga(
    .iClk_50(iClk_50), 
    .nRst(nRst),
    // Interfaces to VGA interface
    .iRed(R),
    .iGreen(G),
    .iBlue(B),
    .oRow(row),
    .oCol(col),
    // Outputs to the VGA hardware
    .oVGA_R(oVGA_R),
    .oVGA_G(oVGA_G),
    .oVGA_B(oVGA_B),
    .oVGA_Clk(oVGA_Clk),
    .oVGA_Blank(oVGA_Blank),
    .oVGA_HSync(oVGA_HSync),
    .oVGA_VSync(oVGA_VSync),
    .oVGA_Sync(oVGA_Sync)
);

wire [7:0] line;
reg [7:0] char;
wire [31:0] buffer_data;

font_rom fonts(
    .iChar(char),
    .iRow(row[3:0]),
    .oLine(line)
);

frame_buffer buffer(
    .iClk(iClk_50),
    .nRst(nRst),
    .iWriteEn(1'b0),
    .iWAddr(32'd0),
    .iRAddr({19'd0, row[9:4], col[9:3]}),
    .iData(32'd0),
    .oData(buffer_data)
);

always @(posedge iClk_50) begin
    char = buffer_data[7:0];
    R = line[col[3:0]] ? {buffer_data[31:24], 2'b00} : 10'd0;
    G = line[col[3:0]] ? {buffer_data[23:16], 2'b00} : 10'd0;
    B = line[col[3:0]] ? {buffer_data[15:8],  2'b00} : 10'd0;

    // R = line[col[3:0]] ? 10'd500 : 10'd0;
    // G = line[col[3:0]] ? 10'd500 : 10'd0;
    // B = line[col[3:0]] ? 10'd500 : 10'd0;
end

endmodule
