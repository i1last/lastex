module verilog(a1, a2, a3, a4, f); 
input a1, a2, a3, a4;
output f;
assign f = (~a1 | a2) & (~a1 | ~a3) & (~a3 | ~a4 | a2);
endmodule