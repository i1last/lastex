module d_l_ff (data, load, q);
	input data, load;
	output q;
	
	reg q;
	
	always @ (load or data)
	begin
		if (load)
		q <= data;
	end
endmodule