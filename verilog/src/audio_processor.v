module audio_processor (
    input  wire         clk,
    input  wire         global_enable,
    input  wire         enable_reverb,
    input  wire         enable_tone_filter,
    input  wire         enable_resonator,
    input  wire         enable_autotune,
    input  wire         enable_noise_gate,
    input  wire         enable_warmer,
    input  wire         enable_envelope,
    input  wire         enable_compressor,
    input  wire         enable_exciter,
    input  signed [15:0] in_sample,
    output signed [15:0] out_sample,
    output       [15:0] est_freq,
    output       [15:0] target_freq
);
    // Internal nets
    wire signed [15:0] ng_out, at_out, env_out;
    wire signed [15:0] res_out, warm_out, comp_out, exc_out, tf_out, rv_out;

    noise_gate          ng  (.clk(clk), .enable(enable_noise_gate), .in_sample(in_sample), .out_sample(ng_out));
    autotune            at  (.clk(clk), .enable(enable_autotune),    .in_sample(ng_out),    .out_sample(at_out),    .est_freq(est_freq), .target_freq(target_freq));
    envelope_shaper     es  (.clk(clk), .enable(enable_envelope),   .in_sample(at_out),     .out_sample(env_out));
    polymoog_resonator  pmr (.clk(clk), .enable(enable_resonator),   .in_sample(env_out),    .out_sample(res_out));
    trumpet_warmer      tw  (.clk(clk), .enable(enable_warmer),      .in_sample(res_out),    .out_sample(warm_out));
    compressor          comp(.clk(clk), .enable(enable_compressor),  .in_sample(warm_out),   .out_sample(comp_out));
    harmonic_exciter    he  (.clk(clk), .enable(enable_exciter),     .in_sample(comp_out),   .out_sample(exc_out));
    tone_filter         tf  (.clk(clk), .enable(enable_tone_filter), .in_sample(exc_out),    .out_sample(tf_out));
    reverb              rv  (.clk(clk), .enable(enable_reverb),      .in_sample(tf_out),     .out_sample(rv_out));

    assign out_sample = global_enable ? rv_out : 16'sd0;
endmodule