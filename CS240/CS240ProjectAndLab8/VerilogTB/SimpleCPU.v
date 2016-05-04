`timescale 1ns / 1ps
module SimpleCPU(clk, rst, data_fromRAM, wrEn, addr_toRAM, data_toRAM, pCounter);

parameter SIZE = 10;

input clk, rst;
input wire [31:0] data_fromRAM;
output reg wrEn;
output reg [SIZE-1:0] addr_toRAM;
output reg [31:0] data_toRAM;
output reg [SIZE-1:0] pCounter;



// internal signals
reg [ 3:0] opcode, opcodeNext;
reg [13:0] operand1, operand2, operand1Next, operand2Next;
reg [SIZE-1:0] /*pCounter,*/ pCounterNext;
reg [31:0] num1, num2, num1Next, num2Next;
reg [ 2:0] state, stateNext;


always @(posedge clk)begin
	state    <= #1 stateNext;
	pCounter <= #1 pCounterNext;
	opcode   <= #1 opcodeNext;
	operand1 <= #1 operand1Next;
	operand2 <= #1 operand2Next;
	num1     <= #1 num1Next;
	num2     <= #1 num2Next;
end

always @*begin
	stateNext    = state;
	pCounterNext = pCounter;
	opcodeNext   = opcode;
	operand1Next = operand1;
	operand2Next = operand2;
	num1Next     = num1;
	num2Next     = num2;
	addr_toRAM   = 0;
	wrEn         = 0;
	data_toRAM   = 0;
if(rst)
	begin
	stateNext    = 0;
	pCounterNext = 0;
	opcodeNext   = 0;
	operand1Next = 0;
	operand2Next = 0;
	num1Next     = 0;
	num2Next     = 0;
	addr_toRAM   = 0;
	wrEn         = 0;
	data_toRAM   = 0;
	end
else 
	case(state)                       
		0: begin											// take instruction
			pCounterNext = pCounter;
			opcodeNext   = opcode;
			operand1Next = 0;
			operand2Next = 0;
			addr_toRAM   = pCounter;
			num1Next     = 0;
			num2Next     = 0;
			wrEn         = 0;
			data_toRAM   = 0;
			stateNext    = 1;
		end 
		1:begin                   // take *A
			pCounterNext = pCounter;
			opcodeNext   = {data_fromRAM[28], data_fromRAM[31:29]};//data_fromRAM[31:28];
			operand1Next = data_fromRAM[27:14];
			operand2Next = data_fromRAM[13: 0];
			addr_toRAM   = data_fromRAM[27:14];
			num1Next     = 0;
			num2Next     = 0;
			wrEn         = 0;
			data_toRAM   = 0;
			if(opcodeNext == 4'b1110)
				stateNext = 5;
			else
				stateNext = 2;
		end
		2: begin         // take *B
			pCounterNext = pCounter;
			opcodeNext   = opcode;
			operand1Next = operand1;
			operand2Next = operand2;
			addr_toRAM   = operand2;
			num1Next     = data_fromRAM;
			num2Next     = 0;
			wrEn         = 0;
			data_toRAM   = 0;
			stateNext    = 3;
		end
		3: begin            
			pCounterNext = pCounter + 1;
			opcodeNext = opcode;
			operand1Next = operand1;
			operand2Next = operand2;
			addr_toRAM = operand1;
			num1Next = num1;
			num2Next = data_fromRAM;
			wrEn = 1;
			if(opcodeNext == 4'b0000)
				data_toRAM = num1Next + num2Next;
			stateNext = 0;
		end
		4: begin
			pCounterNext = pCounter + 1;
			opcodeNext   = opcode;
			operand1Next = operand1;
			operand2Next = operand2;
			addr_toRAM   = operand1;
			num1Next     = num1;
			num2Next     = data_fromRAM;
			wrEn         = 1;
			data_toRAM   = data_fromRAM;
			stateNext    = 0;
		end
		5: begin
			pCounterNext = data_fromRAM + operand2;
			opcodeNext   = opcode;
			operand1Next = operand1;
			operand2Next = operand2;
			addr_toRAM   = operand1;	
			num1Next     = data_fromRAM;
			num2Next     = operand2;
			wrEn         = 0;
			data_toRAM   = 32'hFFFF_FFFF;
			stateNext = 0;
		end
		default: begin
			stateNext    = 0;
			pCounterNext = 0;
			opcodeNext   = 0;
			operand1Next = 0;
			operand2Next = 0;
			num1Next     = 0;
			num2Next     = 0;
			addr_toRAM   = 0;
			wrEn         = 0;
			data_toRAM   = 0;
		end
	endcase

end

endmodule


