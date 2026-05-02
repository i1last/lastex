module sdvig (clock, data_in,load,qa, qb, qc, qd);
    input clock, load;
    input [3:0] data_in;
    output reg qa, qb, qc, qd;

    always @(posedge clock)
    begin
        if (load) 
        begin
            qa<=data_in[0];
            qb<=data_in[1];
            qc<=data_in[2];
            qd<=data_in[3];	
        end 
        else 
        begin
            qb<=qa;
            qc<=qb;
            qd<=qc;
            qa<=qd;
        end
    end
endmodule