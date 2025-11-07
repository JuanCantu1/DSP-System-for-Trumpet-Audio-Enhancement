module polymoog_resonator (
    input wire clk,
    input wire enable,
    input signed [15:0] in_sample,
    output reg signed [15:0] out_sample
);

    parameter signed [15:0] LOW_GAIN  = 16'sd20;
    parameter signed [15:0] MID_GAIN  = -16'sd8;
    parameter signed [15:0] HIGH_GAIN = 16'sd0;

    reg signed [15:0] low_d1 = 0, low_d2 = 0;
    reg signed [15:0] mid_d1 = 0, mid_d2 = 0;
    reg signed [15:0] high_d1 = 0, high_d2 = 0;

    reg signed [15:0] low_out, mid_out, high_out;
    reg signed [31:0] mixed_out;
    reg signed [31:0] boosted;
    reg signed [31:0] mellowed;
    reg signed [15:0] prev_out = 0;

    function signed [15:0] saturate16_soft;
        input signed [31:0] val;
        begin
            if (val > 32767)
                saturate16_soft = 32767 - ((val - 32767) >>> 3);
            else if (val < -32768)
                saturate16_soft = -32768 + ((-32768 - val) >>> 3);
            else
                saturate16_soft = val[15:0];
        end
    endfunction

    always @(posedge clk) begin
        if (enable) begin
            // === Filtering ===
            low_out  <= (in_sample >>> 2) - (low_d1 >>> 2) + (low_d2 >>> 3);
            mid_out  <= (in_sample >>> 1) - (mid_d1 >>> 1) + (mid_d2 >>> 2);
            high_out <= (in_sample)      - (high_d1)      + (high_d2 >>> 1);

            low_d2 <= low_d1;
            low_d1 <= in_sample;
            mid_d2 <= mid_d1;
            mid_d1 <= in_sample;
            high_d2 <= high_d1;
            high_d1 <= in_sample;

            // === Mix with warmth gain ===
            mixed_out <= ((LOW_GAIN * low_out) + (MID_GAIN * mid_out) + (HIGH_GAIN * high_out)) >>> 2;

            // === Boost bass artificially ===
            boosted <= mixed_out + (mixed_out >>> 1) + (mixed_out >>> 2);  // +75%

            // === Smooth output ===
            mellowed <= (boosted >>> 1) + (prev_out >>> 1);
            prev_out <= boosted[15:0];  // important: use BOOSTED, not output

            // === Final out ===
            out_sample <= saturate16_soft(mellowed);
        end else begin
            out_sample <= in_sample;
            prev_out <= in_sample;
        end
    end

endmodule
