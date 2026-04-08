module jkff_my(clock,J,K,q);
    input clock, J,K;
    output q;

    reg q;
    
    always @(posedge clock)
        if (J==1 && K==0)
            q<=1;
        else if (J==0 && K==1)
            q<=0;
        else if (J==1 && K==1)
            q<=~q;
endmodule
