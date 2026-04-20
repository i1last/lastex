module counter (clk, out, p_out);
    input clk;
    
    output [3:0] out;
    output [0:0] p_out;
    
    reg [3:0] out;
    reg [0:0] p_out;
    
    always @(posedge clk)
    begin
        if (out < 4'd9)
            out <= out + 4'b1;
        else
            out <= 4'b0;
        p_out <= !(out ^ 4'd9);
    end
endmodule
