`timescale 1ns / 1ps
module calc(clk, rst, validIn, dataIn, dataOut);
input clk, rst, validIn;
input  [7:0] dataIn;
output reg [7:0] dataOut;

reg [1:0] state, stateNext;
reg [7:0] num1, num1Next, dataOutNext;
reg [2:0] operator, operatorNext;
reg validInDly;
wire valid;

always @(posedge clk) begin
	state         <= #1 stateNext;
	num1          <= #1 num1Next;
	operator      <= #1 operatorNext;
	validInDly    <= #1 validIn;
	dataOut       <= #1 dataOutNext;
end

assign valid = validIn && ~validInDly;

always @(*) begin
	stateNext    = state;
	num1Next     = num1;
	operatorNext = operator;
	dataOutNext  = dataOut;
	if(rst) begin
		stateNext    = 0;
		num1Next     = 0;
		operatorNext = 0;
		dataOutNext  = 0;
	end else begin
		case(state)
			0: begin
				if(valid) begin
					stateNext   = 1;
					num1Next    = dataIn;
					dataOutNext = dataIn;
				end
			end
			1: begin
				if(valid)begin
					case(dataIn)
						3: dataOutNext = num1 * num1;
						4: dataOutNext = num1 + 1;
						5: dataOutNext = num1 - 1;
						default: begin
							dataOutNext = dataIn;
							if(dataIn < 3) begin
								stateNext  = 2;
								operatorNext = dataIn;
							end else
								stateNext  = 1;
						end
					endcase
				end
			end
			2: begin
				if(valid) begin
					stateNext = 0;
					case(operator)
						0: dataOutNext = num1 * dataIn;
						1: dataOutNext = num1 + dataIn;
						2: dataOutNext = num1 - dataIn;
					endcase
				end
			end	
		endcase
	end
end
endmodule
