module counter (clk, q);
    input clk;
    
    output [31:0] q;
    
    reg [31:0] q;
    
    always @(posedge clk) 
        q <= q + 32'b1;
endmodule
