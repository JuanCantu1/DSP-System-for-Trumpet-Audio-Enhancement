module trumpet_warmer (
    input wire clk,
    input wire enable,
    input signed [15:0] in_sample,
    output reg signed [15:0] out_sample
);

    reg signed [15:0] prev_sample = 0;
    reg signed [15:0] filtered_sample;
    reg signed [31:0] tone_shaped;

    // === Gentle tone softener ===
    // Smoother saturation with minimal fold
    function signed [15:0] saturate_soft;
        input signed [31:0] val;
        begin
            if (val > 32767)
                saturate_soft = 32767 - ((val - 32767) >>> 4);  // very gentle fold
            else if (val < -32768)
                saturate_soft = -32768 + ((-32768 - val) >>> 4);
            else
                saturate_soft = val[15:0];
        end
    endfunction

    always @(posedge clk) begin
        if (enable) begin
            // === Gentle dynamic EQ: blend current + previous ===
            // Slight lowpass smooths the edge
            filtered_sample <= (in_sample >>> 1) + (prev_sample >>> 1);

            // === Shaping tone slightly darker ===
            tone_shaped = filtered_sample
                        - (filtered_sample >>> 4);  // drop tiny bit of highs (~6%)

            out_sample <= saturate_soft(tone_shaped);
            prev_sample <= in_sample;
        end else begin
            out_sample <= in_sample;
            prev_sample <= in_sample;
        end
    end
endmodule
