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

font_rom fonts(
    .iChar(char),
    .iRow(row[3:0]),
    .oLine(line)
);

always @(posedge iClk_50) begin
    if(col[3]) begin
        char = 8'h69;
    end else begin
        char = 8'h0;
    end
    // if(row > 16 && row < 32 && col < 16 && col > 8) begin
    //     R = 10'd0;
    //     G = 10'd0;
    //     B = 10'd0;
    // end else if(row < vga_controller.ROW_VA/2) begin
    //     R = 10'd400;
    //     G = 10'd0;
    //     B = 10'd800;
    // end else begin
    //     R = 10'd200;
    //     G = 10'd0;
    //     B = 10'd400;
    // end
    R = line[col[2:0]] ? 10'd1000 : 10'd0;
    G = line[col[2:0]] ? 10'd1000 : 10'd0;
    B = line[col[2:0]] ? 10'd1000 : 10'd0;
end

endmodule
