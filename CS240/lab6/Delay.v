`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    16:57:46 04/15/2015 
// Design Name: 
// Module Name:    Delay 
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
module Delay(rst, mclk, out);
input mclk;
input rst;
output out;

parameter FREQ_DELAY = 50_000_000/16;
parameter CNT_WDTH = 30; // 2^CNT_WDTH cycles is the maximum delay

reg [CNT_WDTH-1:0] timer,timerNext;
always@(posedge mclk) begin
	timer <= timerNext;
end
always@(*) begin
	if(rst) begin
		timerNext = 0;
	end else if(timer == FREQ_DELAY)begin
		timerNext = 0;
	end else begin
		timerNext = timer + 1;
	end
end
assign out = (timer==0);
endmodule
