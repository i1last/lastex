module jkff_my(clock,J,K,q);
    input clock, J,K;
    output q;

    reg q;
    
    always @(posedge clock)
        case({J,K})
            2'b0_0 : q <= q;
            2'b0_1 : q <= 1'b0;
            2'b1_0 : q <= 1'b1;
            2'b1_1 : q <= ~q;
        endcase
endmodule
