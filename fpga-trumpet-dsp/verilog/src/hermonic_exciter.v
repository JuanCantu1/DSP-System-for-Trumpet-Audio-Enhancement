// harmonic_exciter.v
// ----------------------------------
// Simple waveshaper-based harmonic exciter
// Generates 2nd harmonic and mixes with dry signal (compile-time MIX)
// ----------------------------------

module harmonic_exciter (
    input  wire         clk,
    input  wire         enable,
    input  signed [15:0] in_sample,
    output reg   signed [15:0] out_sample
);
    // Mix ratio (0 = 100% dry, 255 = 100% wet)
    parameter [7:0] MIX = 8'd128;  // default ~50/50 dry/wet

    // === Internal signals ===
    wire signed [15:0] abs_in;
    wire signed [31:0] raw_exc;
    wire signed [15:0] exc16;
    reg  signed [31:0] mix_num;

    // compute absolute value
    assign abs_in  = in_sample[15] ? -in_sample : in_sample;
    // generate 2nd harmonic: sign(x)*|x|*|x|
    assign raw_exc = in_sample * abs_in;
    // scale down to 16-bit (extract Q15 -> Q0)
    assign exc16   = raw_exc[30:15];  

    always @(posedge clk) begin
        if (enable) begin
            // mix dry and wet: (MIX*exc16 + (255-MIX)*dry) >> 8
            mix_num <= MIX * $signed(exc16) + (8'd255 - MIX) * $signed(in_sample);
            out_sample <= mix_num >>> 8;
        end else begin
            out_sample <= in_sample;
        end
    end
endmodule