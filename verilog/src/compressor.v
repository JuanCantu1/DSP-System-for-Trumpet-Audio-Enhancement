// compressor.v
// ----------------------------------
// Simple single-band compressor: 2:1 ratio above threshold
// Maintains sign, bypass when disabled
// ----------------------------------

module compressor (
    input  wire         clk,
    input  wire         enable,
    input  signed [15:0] in_sample,
    output reg   signed [15:0] out_sample
);
    // === Parameters ===
    parameter signed [15:0] THRESHOLD = 16'sd8000;  // compressor threshold
    parameter        [7:0] RATIO     = 8'd2;       // compression ratio (2:1)

    // === Internals ===
    reg signed [15:0] abs_in;
    reg signed [15:0] comp_val;

    always @(posedge clk) begin
        if (enable) begin
            // compute absolute input
            abs_in = in_sample[15] ? -in_sample : in_sample;
            if (abs_in > THRESHOLD) begin
                // compress above threshold
                if (in_sample >= 0)
                    comp_val = THRESHOLD + ((in_sample - THRESHOLD) / RATIO);
                else
                    comp_val = -THRESHOLD + ((in_sample + THRESHOLD) / RATIO);
                out_sample <= comp_val;
            end else begin
                // below threshold, pass through
                out_sample <= in_sample;
            end
        end else begin
            // bypass
            out_sample <= in_sample;
        end
    end
endmodule
