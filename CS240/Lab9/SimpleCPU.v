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
reg [ 3:0] state, stateNext;


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
			num2Next     = 0;
			wrEn         = 0;
			data_toRAM   = 0;
			stateNext    = 1;
			
		end 
		1:begin                   // take *A
			pCounterNext = pCounter;
			opcodeNext   = {data_fromRAM[28], data_fromRAM[31:29]};
			operand1Next = data_fromRAM[27:14];
			operand2Next = data_fromRAM[13:0];
			addr_toRAM   = operand1Next;
			num1Next     = data_fromRAM;
			wrEn         = 0;
			data_toRAM   = 0;
			if( {data_fromRAM[28], data_fromRAM[31:29]} == 4'b0101 ) 	begin
				stateNext = 5;
				addr_toRAM = data_fromRAM[13:0];
				num1Next = operand1;
			end
			else if( {data_fromRAM[28], data_fromRAM[31:29]} == 4'b1101 ) 	begin
				stateNext = 6;
				addr_toRAM = data_fromRAM[27:14];
				num1Next = operand1;
			end
			else if(data_fromRAM[28] == 0 ) // immediate check
				stateNext = 2;  
			else 
				stateNext = 3;
		end
		2: begin         // take *B
			pCounterNext = pCounter;
			opcodeNext   = opcode;
			operand1Next = operand1;
			operand2Next = operand2;
			addr_toRAM   = operand2;
			num1Next     = data_fromRAM;
			wrEn         = 0;
			data_toRAM   = operand2;
			stateNext = 3;
			
		end
		3: begin            
			pCounterNext = pCounter + 1;
			opcodeNext = opcode;
			operand1Next = operand1;
			operand2Next = operand2;
			addr_toRAM = operand1;
			num1Next = num1;
			wrEn = 1;
			stateNext = 0;
			case(opcode)                       
				4'b0000: data_toRAM = num1Next + data_fromRAM; // ADD
				4'b1000: data_toRAM = data_fromRAM + operand2; // ADDi
				4'b0001: data_toRAM = ~(num1Next & data_fromRAM); // NAND 
				4'b1001: data_toRAM = ~(data_fromRAM & operand2); // NANDi
				4'b0010: begin// SRL
					if(data_fromRAM < 32)
						data_toRAM = num1 >> data_fromRAM; 
					else
						data_toRAM = num1 << (data_fromRAM - 32); 
				end
				4'b1010: begin// SRLi
					if(operand2 < 32)
						data_toRAM = data_fromRAM >> operand2; 
					else
						data_toRAM = data_fromRAM << (operand2 - 32); 
				end
				4'b0011: data_toRAM = num1Next < data_fromRAM; // LT
				4'b1011: data_toRAM = data_fromRAM < operand2; // LTi
				4'b0100: data_toRAM = data_fromRAM; // CP
				4'b1100: data_toRAM = operand2; // CPi
				4'b0101: begin// CPI
					data_toRAM = data_fromRAM;
					addr_toRAM = operand1;
					wrEn = 1;
				end
				4'b1101: begin // CPIi
					num2Next = data_fromRAM;
					addr_toRAM = num2;
					data_toRAM = data_fromRAM;
					wrEn = 1;
				end
				4'b0110: begin // BZJ
					if(data_fromRAM == 0)
						pCounterNext = num1;
					else
						pCounterNext = pCounter + 1;
					wrEn = 0;
				end
				4'b1110: begin
					pCounterNext = data_fromRAM + operand2; // BZJi
					wrEn = 0;
				end
				4'b0111: data_toRAM = num1Next * data_fromRAM; // MUL
				4'b1111: data_toRAM = data_fromRAM * operand2; // MULi
			endcase 
		end
		4:begin                   // take **
			pCounterNext = pCounter + 1;
			opcodeNext   = 4'b0100;
			operand1Next = operand1;
			operand2Next = operand2;
			data_toRAM	 = num2;
			wrEn         = 1; 
			stateNext 	 = 0; 
			if(opcode == 4'b0101)
				addr_toRAM   = operand1;
			else if (opcode == 4'b1101)
				addr_toRAM   = num1 ;
		end
		5: begin      
			pCounterNext = pCounter;
			opcodeNext   = opcode;
			operand1Next = operand1;
			operand2Next = operand2;
			addr_toRAM   = data_fromRAM;
			num1Next     = data_fromRAM;
			wrEn         = 0;
			data_toRAM   = operand2;
			stateNext = 3;
		end
		6: begin      
			pCounterNext = pCounter;
			opcodeNext   = opcode;
			operand1Next = operand1;
			operand2Next = operand2;
			addr_toRAM   = data_fromRAM;
			num1Next     = data_fromRAM;
			num2Next     = data_fromRAM;
			wrEn         = 0;
			data_toRAM   = operand2;
			stateNext = 2;
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


