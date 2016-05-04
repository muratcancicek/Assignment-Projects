module LedCPUcore(
	clk,
	rst,
	addrRd,
	dataRd,
	outPattern
    );
input clk,rst;
output reg [7:0] addrRd;
input [15:0] dataRd;
output reg [7:0] outPattern; 

parameter FREQ_DELAY = 50_000_000/16;
Delay #(FREQ_DELAY) dly(.rst(rst), .mclk(clk), .out(enable)); 

reg [7:0] addrRdNext;
reg state, stateNext;
reg [7:0] outPatternNext;
reg [7:0] processTime, processTimeNext;

always@(posedge clk) begin
	addrRd <= addrRdNext;
	state <= stateNext;
	outPattern <= outPatternNext;
	processTime <= processTimeNext;
end

always@(*)begin
	outPatternNext = outPattern;
	processTimeNext = processTime;
	stateNext = state;
	addrRdNext = addrRd;
	if(rst)begin
		addrRdNext = 0;
		stateNext = 0;
		outPatternNext = 0;
		processTimeNext = 0;
	end
	else begin
		if(dataRd[7:0] == 0)	begin		
			 addrRdNext = dataRd[15:8];
			end
			else begin
				outPatternNext = dataRd[15:8];
			if(enable) begin
				processTimeNext=processTimeNext+1;  
				if(processTime==dataRd[7:0]) begin
					addrRdNext = addrRd+1;
					processTimeNext = 0;
				end
			end
		end
		// !!!Important notes!!!
		// TO DO: Write Verilog Code Here to implement design
		// Firstly read existing codes and try to understand
		// Registers that I gave you is enough to implement. 
		// However if your design in your mind is need more, you can add (comply to general structure (this is safe))
		// Show your design to your TA to get grade
		// Upload your code (only LedCPUcore.v) into LMS for code correlation (don't cheat)
		// Good Luck
		
	end
end
endmodule
