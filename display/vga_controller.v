/**
 * @file vga_controller.v
 * @author Jacob Chisholm (https://Jchisholm204.github.io)
 * @brief Simple VGA Controller
 * @version 0.1
 * @date Created: 2025-05-07
 * @modified Last Modified: 2025-05-07 
 *
 * 640x480 Resolution
 * outputs the row and column of the pixel
 *
 * @copyright Copyright (c) 2025
 */


module vga_controller(
    iClk_50, nRst,
    // Interfaces to VGA interface
    iRed, iBlue, iGreen,
    oRow, oCol,
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
// Interfaces to VGA interface
input wire  [9:0] iRed, iBlue, iGreen;
output wire [9:0] oRow, oCol;
// Outputs to the VGA hardware
output wire [9:0] oVGA_R, oVGA_G, oVGA_B;
output wire oVGA_Clk, oVGA_Blank, oVGA_HSync, oVGA_VSync, oVGA_Sync;

// Visible Area
parameter COL_VA = 10'd640;
// Front Porch
parameter COL_FP = 10'd16;
// Sync Pulse
parameter COL_SP = 10'd96;
// Back Porch
parameter COL_BP = 10'd48;
// Line Length
parameter COL_LN = (COL_VA + COL_FP + COL_SP + COL_BP);

parameter ROW_VA = 10'd480;
parameter ROW_FP = 10'd10;
parameter ROW_SP = 10'd2;
parameter ROW_BP = 10'd33;
parameter ROW_LN = (ROW_VA + ROW_FP + ROW_SP + ROW_BP);

// Signal Clock Counters
reg [9:0] row, col;

// Assign row and col outputs
assign oCol = col;
assign oRow = row;

// Clock Divider
reg Clk_25;
always @(posedge iClk_50, negedge nRst) begin
    if(~nRst) Clk_25 = 1'b0;
    else Clk_25 = ~Clk_25;
end

// Vertical and horizontal sync outputs
wire hSync, vSync;
assign hSync = col < (COL_VA + COL_FP) || col >= (COL_VA + COL_FP + COL_SP);
assign vSync = row < (ROW_VA + ROW_FP) || row >= (ROW_VA + ROW_FP + ROW_SP);
assign oVGA_HSync = hSync;
assign oVGA_VSync = vSync;
// VGA sync, blank and clock outputs
assign oVGA_Sync  = 1'b1;
assign oVGA_Blank = hSync & vSync;
assign oVGA_Clk = iClk_50;

// Visible Area
wire visible;
assign visible = (col < COL_VA) && (row < ROW_VA);

// Output Color
assign oVGA_R = visible ? iRed   : 10'd0;
assign oVGA_G = visible ? iGreen : 10'd0;
assign oVGA_B = visible ? iBlue  : 10'd0;

always @(posedge Clk_25 or negedge nRst) begin
    if(!nRst) begin
        row = 10'd0;
        col = 10'd0;
    end else begin
        if(col < (COL_LN-10'd1)) begin
            col = col + 10'd1;
        end else begin
            col = 10'd0;
            if(row < (ROW_LN-10'd1)) begin
                row = row + 10'd1;
            end else begin 
                row = 10'd0;
            end
        end
    end
end

endmodule

