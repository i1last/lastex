module dff_my(clock,Data,q);
    input clock, Data;
    output q;

    reg q;

    always @(posedge clock)
        q<=Data;
endmodule
