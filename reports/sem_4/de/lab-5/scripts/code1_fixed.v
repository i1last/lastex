module counter (clk, out, p_out);
    input clk;

    output [3:0] out;
    output [0:0] p_out;
    
    reg [3:0] out;
    
    always @(posedge clk)
    begin
        out <= out + 4'b1;
    end

    assign p_out = &out;
endmodule
