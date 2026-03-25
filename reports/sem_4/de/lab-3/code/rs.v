module s_r_ff (not_set, reset, q, not_q);
	input not_set, reset;
	output q, not_q;
	
	assign not_q = ~q;
	reg q;
	
	always @ (not_set or reset)
	begin
		if (reset)
		q <= 1'b0;
		else if (~not_set)
		q <= 1'b1;
	end
endmodule
