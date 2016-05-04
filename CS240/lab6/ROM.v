`timescale 1ns / 1ps

module ROM(addrRd, dataRd);
input [7:0] addrRd;
output reg [15:0] dataRd;
always @(*) 
    begin
        case(addrRd)
            8'h00   : dataRd = 16'b11111000_00001000;
            8'h01   : dataRd = 16'b01111100_00011000;
            8'h02   : dataRd = 16'b00111110_00001000;
            8'h03   : dataRd = 16'b00011110_00011000;
            8'h04   : dataRd = 16'b00001110_00001000;
            8'h05   : dataRd = 16'b00000110_00011000;
            8'h06   : dataRd = 16'b00001011_00000000;
            8'h07   : dataRd = 16'b00000001_00100000;
            8'h08   : dataRd = 16'b00000010_00001000;
            8'h09   : dataRd = 16'b00000100_00001000;
            8'h0A   : dataRd = 16'b00001000_00001000;
            8'h0B   : dataRd = 16'b00011000_00000100;
            8'h0C   : dataRd = 16'b00111100_00000100;
            8'h0D   : dataRd = 16'b01111110_00000100;
            8'h0E   : dataRd = 16'b11111111_00000100;
            8'h0F   : dataRd = 16'b00000111_00000000;
            default : dataRd = 16'b00000000_00000000;
        endcase
    end
endmodule
		  