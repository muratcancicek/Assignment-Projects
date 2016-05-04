`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    16:03:56 11/21/2014 
// Design Name: 
// Module Name:    sevenSegDriver 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module sevenSegDriver(sw, seg, an);

input[3:0] sw;
output [3:0] an;
output [7:0] seg; // {DP,CG,CF,CE,CD,CC,DB,CA}

reg[3:0] an;
reg[7:0] seg;

always@(*) begin
an=4'b0110;
case(sw)
	0: seg = 8'b01000000; // only g is off
	1: seg = 8'b01111001;
	2: seg = 8'b00100100;
	3: seg = 8'b00110000;
	4: seg = 8'b00011001;
	5: seg = 8'b00010010;
   6: seg = 8'b00000010;
	7: seg = 8'b01111000;
	8: seg = 8'b00000000;
	9: seg = 8'b00010000;
	10: seg = 8'b00001000;
	11: seg = 8'b00000011;
	12: seg = 8'b01000110;
	13: seg = 8'b00100001;
	14: seg = 8'b00000110;
	15: seg =	8'b00001110;
	
	
	endcase
end	


endmodule
