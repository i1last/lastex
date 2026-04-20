module counter (clk, reset, enable, out);
    input clk, reset, enable;
    
    output [3:0] out;
    
    reg [3:0] out;
    
    always @(posedge clk)
    begin
        if (reset)
            out <= 4'b0; 
        else if (enable)
            out <= out + 4'b1;
    end
endmodule
