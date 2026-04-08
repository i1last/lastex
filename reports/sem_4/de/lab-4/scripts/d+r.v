module dff_r(clock, Data, reset, q);
    input clock, Data, reset;
    output q;

    reg q;

    always @(posedge clock)
        begin
            if (reset)
                q <= 1'b0;
            else
                q <= Data;
        end
endmodule
