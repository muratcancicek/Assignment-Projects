`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    16:56:14 11/28/2014 
// Design Name: 
// Module Name:    delay 
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
module delay(rst,mclk,out);
	 input mclk;
	 input rst;
	 output out;
	 
	 parameter CNT_WIDTH=26;
	 reg[CNT_WIDTH-1:0] timer,timerNext;
	 
	 always@(posedge mclk)begin
	 timer <=#1 timerNext;
	 end
	 
	 always@(*)begin
	 if(rst)begin
	 timerNext=0;
	 end else begin
	 timerNext=timer+1;
	 end
	 end
	 assign out = (timer==0);

endmodule
