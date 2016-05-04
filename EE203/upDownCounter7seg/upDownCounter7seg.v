`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    16:24:16 11/28/2014 
// Design Name: 
// Module Name:    upDownCounter7seg 
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
module upDownCounter7seg(upDown,rst,mclk,seg,an);

input upDown;
input rst;
input mclk;
output reg[7:0] seg;
output reg [3:0] an;

wire enable;
delay delay(.rst(rst),.mclk(mclk),.out(enable));
reg [3:0] counter,counterNext;
always@(posedge mclk) begin
	counter <= counterNext;
	end
	always@(*)begin
		counterNext=counter;
			if(enable) begin
				if(rst)begin
					counterNext=0;
				end else begin
		
					if(upDown==1) begin
						counterNext=counter + 1;
				
						if(counter==9) begin
							counterNext=0;		
						end
					end else	if(upDown==0) begin
						counterNext=counter - 1;
				
						if(counter==0)begin
							counterNext=9;
						
						end
					end
				end
			end
	end
	
	always@(*)begin
	an=4'b0000;
	case(counter)
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
	
	endcase
	
end


endmodule
