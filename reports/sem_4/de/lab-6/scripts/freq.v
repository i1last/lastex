module freq (clk, dig, leds);
    input clk;
    reg [31:0] counter;
    output dig;
    output reg [7:1] leds;

    always @ (posedge clk)
        counter <= counter + 32'd1;

    always @ (counter[29:26]) 
    case (counter[29:26])
              0: leds = 7'b1000000;
              1: leds = 7'b1111001;
              2: leds = 7'b0100100;
              3: leds = 7'b0110000;
              4: leds = 7'b0011001;
              5: leds = 7'b0010010;
              6: leds = 7'b0000010;
              7: leds = 7'b1111000;
              8: leds = 7'b0000000;
              9: leds = 7'b0010000;
           4'hA: leds = 7'b0001000;
           4'hB: leds = 7'b0000011;
           4'hC: leds = 7'b1000110;
           4'hD: leds = 7'b0100001;
           4'hE: leds = 7'b0000110;
           4'hF: leds = 7'b0001110;
        default: leds = 7'b0101010;
    endcase
    
    assign dig = 1;
endmodule