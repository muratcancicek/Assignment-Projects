`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    13:50:23 12/12/2014 
// Design Name: 
// Module Name:    lab6 
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
module lab6(mclk,rst,seg);
input mclk,rst;
output[7:0] seg;

reg [21:0] counter,counterNext;
reg [7:0] seg,segNext;
reg direction,directionNext;

parameter COUNT = 22'h3FFFFF;

always@(posedge mclk) begin
	counter <= counterNext;
	seg <=  segNext;
	direction <= directionNext;
		
end

	


//registers
always@(*) begin
	if(rst)begin
		segNext=8'b1000_0000;
		counterNext = 0;
	end
	else if(counter ==COUNT-1) begin
		if(direction==0) begin
		segNext = seg >> 1;
		//segNext ={seg[0],seg[7:1]};
		counterNext=0;
		end
		else begin
		segNext = seg << 1;
		//segNext ={seg[7:1],seg[0]};
		counterNext=0;
		end
		
		if(seg == 1) begin
	
		directionNext = 1;
		end else if(seg == 128) begin
			directionNext = 0;
			end
		
	end 
	else begin
		segNext = seg;
		counterNext = counter +1;
		end	
end
endmodule
