module sdvig_wrong (clock, ds, qa, qb, qc, qd);
    input clock, ds;
    output reg qa, qb, qc, qd;

    always @(posedge clock)
    begin
        qa=ds;
        qb=qa;
        qc=qb;
        qd=qc;
    end
endmodule