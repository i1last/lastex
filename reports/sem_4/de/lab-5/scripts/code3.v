module counter (clk, load, data, up, out, p_out);
    input clk, load, up;
    input [2:0] data;
    
    output [2:0] out;
    output p_out;
    
    assign p_out = up & (&out) | ~up & ~(|out);
    
    reg [2:0] out;
    always @(posedge clk)
    begin
        if (load)
            out <= data;
        else
            if (up)
                out <= out + 3'b1;
            else
                out <= out - 3'b1;
    end
endmodule
