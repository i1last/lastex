module dc2x4 (in, out);
    input [1:0] in;
    output [3:0] out;
    
    assign out = 1 <<in;
endmodule